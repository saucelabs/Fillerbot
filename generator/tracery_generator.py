from .generator import Generator,generator_factory
import tracery
from tracery.modifiers import base_english 
from faker import Faker
import simpleeval

class TraceryGenerator(Generator):
    """"
    Tracery Generator: A Generator that uses Tracery to generate data from a JSON string
    """
    def __init__(self,name,desc=None, gen_id=None, var_name=None,data_item=None, create_date=None):
        super(TraceryGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.data = data_item
        self.var_type = str(type(self.data).__name__)
        self.grammar = tracery.Grammar(self.data)
        self.grammar.add_modifiers(base_english)

    # In the meanwhile we always use #origin as our starting symbol.
    def generate(self,context=None):
        tracery_output = self.grammar.flatten("#origin#")
        self.last_item_generated = tracery_output
        return tracery_output
    
    def size(self):
        return -1
    
    def serialize(self):
        o = super(TraceryGenerator,self).serialize()
        o['data'] = self.data
        return o 
        
##This is the class that uses the complex generator. 
class ComplexTraceryGenerator(TraceryGenerator):
    
    def __init__(self,name,desc=None, gen_id=None, var_name=None,data_item=None, create_date=None):
        super(TraceryGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.data = data_item
        self.var_type = str(type(self.data).__name__)
        self.grammar = tracery.Grammar(self.data)
        self.grammar.add_modifiers(base_english)
        self.faker = Faker()
    
    # In the meanwhile we always use #origin as our starting symbol.
    def generate(self,context=None):
        tracery_output = self.grammar.flatten("#origin#")
        #Now here we process the data. 
        splits = tracery_output.split(" ")
        new_tracery_output = ""
        #Now here we replace it and be done with it
        for split in splits:
            if "faker" in split:
                subst = split.split(".")
                method = None
                try:
                    method = getattr(self.faker, subst[1])
                except AttributeError:
                    raise NotImplementedError("Class `{}` does not implement `{}`".format(self.faker.__class__.__name__, subst[1]))
                new_tracery_output += str(method())+" "
            elif "globalcontext" in split:
                subst = split.split(".")
                try:
                    contextvar = context[subst[1]]
                except AttributeError:
                    raise NotImplementedError("Context Name `{}` does not exist".format(subst[1]))
                new_tracery_output += contextvar+" "
            else:
                new_tracery_output += split+" "
        self.last_item_generated = new_tracery_output
        return new_tracery_output

##This is the class that uses the complex generator. 
class ComplexFieldGenerator(TraceryGenerator):
    
    def __init__(self,name,desc=None, gen_id=None, var_name=None,data_item=None, create_date=None):
        super(TraceryGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.data = data_item
        self.var_type = str(type(self.data).__name__)
        #Start setting up parameters and cook generators here.
        self.generators = self.cook_generators(data_item["generators"])
        self.constraints = self.store_constraints(data_item["generators"])
        self.grammar = tracery.Grammar(data_item["pattern"])
        self.grammar.add_modifiers(base_english)
        self.faker = Faker()
        
    
    #use this to set up any generators that might be used.
    def cook_generators(self,generator_list):
        generators = {}
        for generator in generator_list: 
            generators[generator["name"]] = generator_factory(generator)
        return generators
    
    #Use this to set up your constraint lists so you can use them later.
    def store_constraints(self,generator_list):
        constraints = {}
        for generator in generator_list:
            constraints[generator["name"]] = generator["constraints"]
        return constraints
    
    #Take all that has been generated and processed, and now glue it using Tracery magic! 
    def process_pattern_output(self,context=None,localcontext=None):
        tracery_output = self.grammar.flatten("#origin#")
        #Now here we process the data. 
        splits = tracery_output.split(" ")
        new_tracery_output = ""
        #Now here we replace it and be done with it
        for split in splits:
            if "faker" in split:
                subst = split.split(".")
                method = None
                try:
                    method = getattr(self.faker, subst[1])
                except AttributeError:
                    raise NotImplementedError("Class `{}` does not implement `{}`".format(self.faker.__class__.__name__, subst[1]))
                new_tracery_output += str(method())+" "
            elif "globalcontext" in split:
                subst = split.split(".")
                try:
                    contextvar = context[subst[1]]
                except AttributeError:
                    raise NotImplementedError("Context Name `{}` does not exist".format(subst[1]))
                new_tracery_output += contextvar+" "
            elif "localcontext" in split:
                subst = split.split(".")
                try:
                    contextvar = localcontext[subst[1]]
                except AttributeError:
                    raise NotImplementedError("Context Name `{}` does not exist".format(subst[1]))
                new_tracery_output += contextvar+" "
            else:
                new_tracery_output += split+" "
        return new_tracery_output

    # In the meanwhile we always use #origin as our starting symbol.
    def generate(self,context=None):
        #Create an empty localcontext 
        localcontext = {} 
        #Generate things, aand then save into localcontext.
        for key in self.generators.keys():
            localcontext[key] = self.generators[key].generate()
            #Apply any constraints here if you need to. 
            if key in self.constraints.keys():
                for constraint in self.constraints[key]:
                    localcontext[constraint["output_name"]] = simpleeval.simple_eval(constraint["expression"],names=localcontext)
        #Done generating things and now we proceed to glue it all into the pattern/template.
        final_output = self.process_pattern_output(context,localcontext)
        return final_output