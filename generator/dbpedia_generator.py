from .generator import Generator
import generator.sparql_hardcoded as HC
from SPARQLWrapper import SPARQLWrapper, JSON
import random 


def format_entity(entity):
    if "dbr:" in entity or "dbo:" in entity:
        return entity

    escape_chars = [",", "(", ")", ":", "'", ".", "?", "!", "&"]
    for char in escape_chars:
        entity = entity.replace(char, "\\" + char) if char in entity else entity
    entity = entity.replace("\\\\", "\\") if "\\\\" in entity else entity

    entity = entity.replace(" ", "_") if " " in entity else entity
    entity = "dbr:" + entity
    return entity


class DBPediaGenerator(Generator):
    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(DBPediaGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.description = 'DBPediaGenerator!'
        self.type_label = 'DBPediaGenerator'
        self.gen_type = data_item["gen_type"]
        self.gen_data = data_item

        self.databank = []
        verify = False
        try:
            self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            self.query = ""
            self.colnames = []
            self.generate_gen_type()
        except Exception as e:
            self.verify_gen_type()
            verify = True
            raise e
        finally:
            if len(self.databank) == 0 and not verify:
                self.verify_gen_type()
            # self.databank.append({self.gen_type: "DBPEDIA QUERY NOT VALID"})

    def verify_gen_type(self):
        needed_keys = {"raw_query": ["query", "cols"],
                       "hard_coded": ["query_name"],
                       "fill_in_single": ["input_entity", "col", "predicate"],
                       "fill_in_multi": ["main_type", "col", {"related_entities":
                                                                  ["col", "predicate"]}]}

        if self.gen_type not in needed_keys.keys():
            print("\nERROR: NOT A VALID DBPEDIA gen_type:", self.gen_type)
            return False

        valid = True
        for key in needed_keys[self.gen_type]:
            if type(key) == str and key not in self.gen_data:
                print("\nERROR: DBPEDIA QUERY MISSING KEY:", key)
                valid = False
            if type(key) == dict:
                for key_k, sub_list in key.items():
                    if key_k in self.gen_data:
                        sub_data = self.gen_data[key_k]
                        for data in sub_data:
                            for sub in sub_list:
                                if sub not in data:
                                    print("\nERROR: DBPEDIA QUERY MISSING KEY:", key_k, sub)
                    else:
                        print("\nERROR: DBPEDIA QUERY MISSING KEY:", key_k)
        return valid

    def generate_gen_type(self):
        print("generate gen type")
        if self.gen_type == "raw_query":
            self.query = self.gen_data['query']
            self.colnames = self.gen_data['cols']
            self.databank = self.generate_data_bank()
        elif self.gen_type == "hard_coded":
            self.query_by_name(self.gen_data["query_name"])
            self.databank = self.generate_data_bank()
        elif self.gen_type == "fill_in_single":
            self.databank = self.single_col_madlib()
        elif self.gen_type == "fill_in_multi":
            self.databank = self.multiple_col_madlib()

    def query_by_name(self, name):
        if name == "usa_cities":
            self.query = HC.USA_CITIES_QUERY
            self.colnames = HC.USA_CITIES_COLNAMES
        elif name == "global_cities":
            self.query = HC.GLOBAL_CITIES_QUERY
            self.colnames = HC.GLOBAL_CITIES_COLNAMES
        elif name == "books":
            self.query = HC.BOOKS_QUERY
            self.colnames = HC.BOOKS_COLNAMES
        elif name == "video_games":
            self.query = HC.VIDEO_GAMES_QUERY
            self.colnames = HC.VIDEO_GAMES_COLNAMES
        elif name == "phones":
            self.query = HC.PHONES_QUERY
            self.colnames = HC.PHONES_COLNAMES
        elif name == "airports":
            self.query = HC.AIRPORTS_QUERY
            self.colnames = HC.AIRPORTS_COLNAMES
        elif name == "city_company":
            self.query = HC.CITY_COMPANY_QUERY % format_entity(self.gen_data["input"])
            self.colnames = HC.CITY_COMPANY_COLNAMES
        else:
            print("INVALID HARD_CODED NAME")

    def get_error_outputs(self, query, type_info="predicate"):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)

        try:
            ret = self.sparql.query().convert()
        except Exception as e:
            print("Error running sparql query.")
            raise e

        ret_results = ret["results"]["bindings"]
        if len(ret_results) == 0:
            return []

        values = list()
        c = None
        for x in list(ret_results[0].keys()):
            if x != "count":
                c = x
        if not c:
            return []

        for r in ret_results:
            val = r[c]['value'].split("/")[-1]
            if type_info == "filter":
                _type = r[c]['value'].split("/")[-2]
                if _type == "ontology":
                    if val not in values:
                        values.append(val)
            elif type_info == "multi_predicate":
                _type = r[c]['value'].split("/")[-2]
                if _type == "ontology" or _type == "property":
                    if "wikiPage" not in val:
                        if val not in values:
                            values.append(val)
            else:
                if val not in values:
                    values.append(val)

        return values

    def single_col_madlib(self):
        # Input variable which decides what input entity is that will find other entity based on
        input_entity = self.gen_data["input_entity"]
        # Input predicate to find output entities given input entity
        predicate = self.gen_data["predicate"]
        # Type to filter output entities by, must be type in rdf:type to work. Optional.
        _filter = self.gen_data["filter"] if "filter" in self.gen_data else None
        colname = self.gen_data["col"] if "col" in self.gen_data else "out"

        input_entity = format_entity(input_entity)

        if "dbp:" in predicate or "dbo:" in predicate:
            predicate = predicate.split(":")[1]
        predicate1 = "dbp:" + predicate
        predicate2 = "dbo:" + predicate

        if _filter and not "dbo:" in _filter:
            _filter = "dbo:" + _filter

        filter_bind = ""
        filter_func = ""
        if _filter:
            filter_bind = "BIND(%s as ?filterType)" % _filter
            filter_func = "?outNode rdf:type ?filterType."

        self.colnames = [colname]
        self.query = f"""
        SELECT DISTINCT ?{colname}
        WHERE {{ 
              BIND({input_entity} as ?inNode)
              BIND({predicate1} as ?predicate1)
              BIND({predicate2} as ?predicate2)
              {filter_bind}

             {{{{?inNode ?predicate1 ?outNode.}}
                UNION
             {{?outNode ?predicate1 ?inNode.}}
                UNION
             {{?inNode ?predicate2 ?outNode.}}
                UNION
             {{?outNode ?predicate2 ?inNode.}}

             {filter_func}

             ?outNode rdfs:label ?{colname}.
             FILTER(lang(?{colname}) = 'en').}}

                UNION

             {{{{?inNode ?predicate1 ?{colname}.}}
                UNION
             {{?{colname} ?predicate1 ?inNode.}}
                UNION
             {{?inNode ?predicate2 ?{colname}.}}
                UNION
             {{?{colname} ?predicate2 ?inNode.}}
             FILTER(isLiteral(?{colname})).}}

        }}"""

        databank = self.generate_data_bank()

        if len(databank) == 0:
            databank = [{colname: "SEE ERROR STATEMENT"}]
            filter_error = False
            if _filter:
                filterSearch = f"""
                    SELECT DISTINCT ?filterType
                    WHERE {{ 
                          BIND({input_entity} as ?inNode)
                          BIND({predicate1} as ?predicate1)
                          BIND({predicate2} as ?predicate2)

                         {{?inNode ?predicate1 ?outNode.}}
                            UNION
                         {{?outNode ?predicate1 ?inNode.}}
                            UNION
                         {{?inNode ?predicate2 ?outNode.}}
                            UNION
                         {{?outNode ?predicate2 ?inNode.}}

                         ?outNode rdf:type ?filterType.
                    }}"""

                filter_values = self.get_error_outputs(filterSearch, type_info="filter")
                if len(filter_values) > 0:
                    print("\nFilter Incorrect, try one of the following:")
                    for p in filter_values:
                        print(p)
                    filter_error = True

            if not filter_error:
                predicateSearch = f"""
                SELECT DISTINCT ?predicate
                WHERE {{ 
                      BIND({input_entity} as ?inNode)
                      {filter_bind}

                     {{?inNode ?predicate ?outNode.}}
                        UNION
                     {{?outNode ?predicate ?inNode.}}

                     {filter_func}

                     ?outNode rdfs:label ?out.
                     FILTER(lang(?out) = 'en').
                }}"""

                pred_values = self.get_error_outputs(predicateSearch)
                if len(pred_values) > 0:
                    print("\nPredicate Incorrect, try one of the following:")
                    for p in pred_values:
                        print(p)
                else:
                    predicateSearch = f"""
                    SELECT DISTINCT ?predicate
                    WHERE {{ 
                          BIND({input_entity} as ?inNode)

                         {{?inNode ?predicate ?outNode.}}
                            UNION
                         {{?outNode ?predicate ?inNode.}}

                         ?outNode rdfs:label ?out.
                         FILTER(lang(?out) = 'en').
                    }}"""

                    pred_values = self.get_error_outputs(predicateSearch)
                    if len(pred_values) > 0:
                        print("Predicate Incorrect, try one of the following:")
                        for p in pred_values:
                            print(p)
                    else:
                        print("""Entity Incorrect, confirm name on Wikipedia and try again. 
                              If entity is correct and it still doesn't work, add backslash before all non-alphanumeric 
                              characters""")
        return databank

    def multiple_col_madlib(self):
        # The type of the input the rest of entities center upon (city, then find state, zip, etc. info)
        main_type = self.gen_data["main_type"]
        # The column label for main entity
        col = self.gen_data["col"]
        # related entities to main entity, allows user to get related, linked information
        related_entities = self.gen_data["related_entities"]

        if ":" not in main_type:
            main_type = "dbo:" + main_type

        self.colnames = [col]
        related_cols = []
        related_subquery = []
        for rel in related_entities:
            rel_col = rel["col"]
            self.colnames.append(rel_col)
            related_cols.append("?" + rel_col)

            predicate = rel["predicate"]
            if "dbp:" in predicate or "dbo:" in predicate:
                subquery = f"""
                              {{?{rel_col}Node {predicate} ?{col}Node.}}
                                 UNION
                              {{?{col}Node {predicate} ?{rel_col}Node.}}"""

                subquery_literal = f"""
                                ?{col}Node {predicate} ?{rel_col}.
                                FILTER(isLiteral(?{rel_col})).
                                """
            else:
                predicate1 = "dbp:" + predicate
                predicate2 = "dbo:" + predicate
                subquery = f"""
                              {{?{rel_col}Node {predicate1} ?{col}Node.}}
                                 UNION
                              {{?{col}Node {predicate1} ?{rel_col}Node.}}
                                 UNION
                              {{?{rel_col}Node {predicate2} ?{col}Node.}}
                                 UNION
                              {{?{col}Node {predicate2} ?{rel_col}Node.}}"""

                subquery_literal = f"""
                              {{?{col}Node {predicate1} ?{rel_col}.}}
                                 UNION
                              {{?{col}Node {predicate2} ?{rel_col}.}}
                              FILTER(isLiteral(?{rel_col})).
                              """

            if "filter" in rel:
                _filter = rel["filter"]
                if not ":" in _filter:
                    _filter = "dbo:" + _filter
                subquery += "?%sNode rdf:type %s.\n" % (rel_col, _filter)

            subquery += "?%sNode rdfs:label ?%s.\n FILTER(lang(?%s) = 'en').\n" % (rel_col, rel_col, rel_col)

            if "filter" in rel:
                final_subquery = subquery
            else:
                final_subquery = "{" + subquery + "}\n UNION\n {" + subquery_literal + "}"

            related_subquery.append(final_subquery)

        related_col_str = " ".join(related_cols)
        related_sq_str = "\n".join(related_subquery)

        self.query = f"""
        SELECT DISTINCT  ?{col} {related_col_str}
        WHERE {{ 
             ?{col}Node rdf:type {main_type}.
             ?{col}Node rdfs:label ?{col}.
              FILTER(lang(?{col}) = 'en').

              {related_sq_str}
        }}
        """

        # print(self.query)
        databank = self.generate_data_bank()

        if len(databank) == 0:
            # Check if mistake in filters
            pred_bad_values = []

            for rel in related_entities:
                predicate = rel["predicate"]
                _filter = rel["filter"] if "filter" in rel else None

                if "dbp:" in predicate or "dbo:" in predicate:
                    subquery = f"""{{?outNode {predicate} ?mainNode.}}
                                     UNION
                                  {{?mainNode {predicate} ?outNode.}}"""
                else:
                    predicate1 = "dbp:" + predicate
                    predicate2 = "dbo:" + predicate
                    subquery = f"""{{?outNode {predicate1} ?mainNode.}}
                                     UNION
                                  {{?mainNode {predicate1} ?outNode.}}
                                     UNION
                                  {{?outNode {predicate2} ?mainNode.}}
                                     UNION
                                  {{?mainNode {predicate2} ?outNode.}}"""

                q = f"""
                       SELECT DISTINCT ?outNode
                       WHERE {{ 
                            ?mainNode rdf:type {main_type}.
                            {subquery}

                            }}
                    """
                pred_values = self.get_error_outputs(q)
                if len(pred_values) == 0:
                    pred_bad_values.append(predicate)

                if _filter:
                    q = f"""
                       SELECT DISTINCT ?filterType (COUNT(?filterType) as ?count)
                       WHERE {{ 
                            ?mainNode rdf:type {main_type}.
                            {subquery}

                            ?outNode rdf:type ?filterType.
                            }} ORDER BY DESC(?count)
                    """
                    filter_values = self.get_error_outputs(q, type_info="filter")
                    if len(filter_values) > 0 and _filter not in filter_values:
                        print("\nFilter Incorrect for " + rel["col"] + ", try one of the following:")
                        for p in filter_values:
                            print(p)

            if len(pred_bad_values) > 0:
                q = f""" SELECT DISTINCT ?predicate (COUNT(?predicate) AS ?count)
                WHERE {{
                    ?inNode rdf:type {main_type}.
                    {{?inNode ?predicate ?outNode.}}
                        UNION
                    {{?outNode ?predicate ?inNode.}}

                    }} ORDER BY DESC(?count)
                """
                pred_values = self.get_error_outputs(q, type_info="multi_predicate")
                if len(pred_values) > 0:
                    print("\nThe following predicates are incorrect:")
                    for p in pred_bad_values:
                        print("    " + p)
                    print("Try replacing with the following examples (this is a sample of the potential "
                          "predicates, check DBpedia for more options if necessary):")
                    x = 0
                    for p in pred_values:
                        print("    " + p)
                        x += 1
                        if x == 100:
                            break
                else:
                    print("\nmain_type is incorrect, no associated predicates. Try another type.")

        return databank

    def generate_data_bank(self):
        databank = []
        self.sparql.setQuery(self.query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query()
        resultdict = results.convert()
        result_binds = resultdict['results']['bindings']
        for result_bind in result_binds:
            instance = {}
            for colname in self.colnames:
                instance[colname] = result_bind[colname]["value"]
            databank.append(instance)
        return databank

    def generate(self, context=None):
        return random.choice(self.databank)
