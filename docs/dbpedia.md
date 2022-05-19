## DBpedia

DBpedia is a open knowledge graph derived from Wikipedia content. It is freely available and is periodically updated, capturing changes made to Wikipedia. Knowledge graphs are a kind of database which structures the knowledge to illustrate the relationships between the entities in the database. DBpedia contains information such as the capitals of countries, directors of movies, the genus of plants and many, many more relations between the entities in the database. Entities are objects, people, places and terms which have a Wikipedia page. The data is queriable using the query language [SPARQL](https://www.dbpedia.org/resources/sparql/).

### Generating DBpedia Data with Fillerbot

There are four methods you can use to generate DBpedia data:

1. `raw_query`
2. `hard_coded`
3. `fill_in_single`
4. `fill_in_double`

These are input in the list of `generator_params` in the parameter `gen_type`. Each has different set of additional parameters. 

#### `raw_query`

This method allows you to write your own DBpedia query from scratch. This query must be written in [SPARQL](https://www.dbpedia.org/resources/sparql/) has two required parameters, `query` and `cols`. `query`'s value is a correct SPARQL query. `cols` has an array of column names. These need to match the names of the variables output in the SPARQL query. 

Below is an example of a `raw_query` JSON input:

```
"generator_params": {
	"gen_type": "raw_query",
	"cols": ["city", "zipcode"],
	"query": "SELECT DISTINCT ?city ?zipcode WHERE {?cityNode rdf:type dbo:City. ?cityNode dbp:name ?city. FILTER(lang(?city) = 'en'). ?cityNode dbo:postalCode ?zipcode.}"
}
```

#### `hard_coded`


This method allows you to add generate data from one of our pre-written queries. These are either completely hard-coded or they need one input value. The only required parameter is `query_name`. 

We currently have 6 completely hard-coded queries, which are described here:

* `usa_cities`: list of cities in the USA. Outputs city name, state, zipcode and county.
* `global_cities`: list of cities around the world. Outputs city name, country, country code and zipcode.
* `books`: list of books. Outputs book name, author name, language and page count. 
* `video_games`: list of video games. Outputs game name, platform and publisher.
* `phones`: list of phones. Outputs phone name and OS available on said phone. 
* `airports`: list of airports. Outputs name of airport, city airport is in, country airport is in, and FAA code. 

An example of the `generator_params` for the completely hard-coded input is here:

```
"generator_params": {
	"gen_type": "hard_coded",
	"query_name": "video_games"
}
```

We currently have 1 hard-coded query that takes an input value. Input values are always entities. You can find the label of your entity by searching for the entity on Wikipedia. While you can try to use the common name for your entity this will not always produce accurate results as some entities need to be disambiguated. For example, the city San Francisco, CA is in Wikipedia as just "San Francisco", whereas the city Santa Cruz, CA needs to be disambiguated from the phrase Santa Cruz and is therefore in Wikipedia as "Santa Cruz, California". Neither "San Francisco, California" nor "Santa Cruz" will retrieve the desired entity.  This input is also case-sensitive. Here are the available queries:

* `city_company`: A list of active companies that are located in the given city. Outputs company name. 
	* input: name of city

An example of the `generator_params` for the partially hard-coded input is here:

```
"generator_params": {
	"gen_type": "hard_coded",
	"query_name": "city_company",
	"input": "San Francisco"
}
```

	
#### `fill_in_single` 

`fill_in_single` and `fill_in_multi` each allow you to create your own query without needing any DBpedia or SPARQL knowledge. We have created two types of templates that, given entities, predicates and entity types, will generate a SPARQL query that we will run, returning the desired entities and/or values.

`fill_in_single` collects one type of data about a specific entity. So you can, for example, collect all the actors in The Avengers or all the movies Chris Evans has starred in. Just like above, you need to use the exact label of the entity as presented in Wikipedia, including case and punctuation. `fill_in_single` takes 3 required parameters and 1 optional parameter.

* `input_entity`: the label of the entity you want to get related data about.
* `col`: the label for the output column.
* `predicate`: the relation connecting the input_entity to the desired output data. 
* `filter` (optional): the type of the output entity which will be used to filter out entities that are not of that type.

You know how to get `input_entity` and `col` from the above explanations, now we will explain how to find potential `predicate`s and `filter`s. DBpedia extracts most of its data from infoboxes in Wikipedia, like the example below. The labels in the infobox can help you find the correct label for the predicate you need. 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Lundehund.png/440px-Lundehund.png" width="250">

From the above example, you could use "nickname" and "country" as predicates to get the respective information. Predicates are always in camel case (birthDate). (You can also use 
an example of the potential outputs to find example predicates. For example, you can get all movies Chris Evans has been in using the predicate "starring", an example of which can be seen in the Wikipedia page for [The Avengers](https://en.wikipedia.org/wiki/The_Avengers_(2012_film)).) 

To find a potential filter type, you can use this mapping of DBpedia's [ontology](http://78.46.100.7:9000/), which contains valid filter types that you can use. This field is optional since not all outputs have types and it isn't always necessary to filter by type. Filters are upper camel case (WrittenWork). For both `predicate` and `filter`, if you input an incorrect value you will get an informative error statement which will tell you available predicates or filters. 

An example of the `generator_params` for `fill_in_single` is here:

```
"generator_params": {
	"gen_type": "fill_in_single",
	"input_entity": "Chris Evans (actor)"
	"col": "movie",
	"predicate": "starring",
	"filter": "Film"
}
```

#### `fill_in_multi`

This final method collects multiple columns of data related to an entity type (from DBpedia's [ontology](http://78.46.100.7:9000/)). You can output as many related columns as needed, but each column must be associated with an entity of the input type. For example, you can select the entity type "Person" and output the films that person has been in and their birthdate. The relations do not have to apply to all entities of the given type, the generator will only return entities that have the given types, narrowing down the list of potential entities. The main entity will also be returned, so for the previous example you will get the actor's name, a movie title and their birthdate. You will get one output for each unique combination of data. That means you will have a row for every movie that the actor has starred in, since both name and birthdate should be unique entities. 

There are 3 main inputs:

* `main_type`: the ontological type of the main entity.
* `col`: the column name for the main entity.
* `related_entities`: this is a list of all the related entities. Each relatated entity is another dictionary of parameters
	* `col`: the column name for the related entity
	* `predicate`: the relation connecting the main entity to the related entity.
	* `filter` (optional): the type of the related entity.

`main_type` is from DBpedia's ontology (mentioned above). The `predicate` and `filter` are collected using the same methods as in `fill_in_single`. Each column name needs to be unique. 

An example of the `generator_params` for `fill_in_multi` is here:

```
"generator_params": {
	"gen_type": "fill_in_multi",
	"main_type": "Person"
	"col": "actor",
	"related_entities": [
		{
			"col": "film",
			"predicate": "starring",
			"filter": "Film"
		},
		{
			"col": "birthdate",
			"predicate": "birthDate"
		}
	]
}
```

### Additional Links
* DBpedia: [https://www.dbpedia.org/](https://www.dbpedia.org/)
* DBpedia Lookup: [https://lookup.dbpedia.org/](https://lookup.dbpedia.org/)
* Sparql: [https://www.dbpedia.org/resources/sparql/](https://www.dbpedia.org/resources/sparql/)
* Sparql for DBpedia Guide: [https://medium.com/virtuoso-blog/dbpedia-basic-queries-bc1ac172cc09](https://medium.com/virtuoso-blog/dbpedia-basic-queries-bc1ac172cc09)
