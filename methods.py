import json
from generator.generator import generator_factory
from generator.faker_generator import *
from generator.tracery_generator import *
import pandas as pd 
import random
import re
import simpleeval
import requests


def cook_generators(field_definitions, n_items):
    generators = {}
    for field in field_definitions: 
        generators[field["name"]] = generator_factory(field, n_items)
    return generators

def generate_instance(fields,generators):
    instance = {}
    context = {}
    for field in fields:
        if field["generator_type"] == "CSVMultiColumnGenerator" or field["generator_type"] == "DBPediaGenerator":
            generated_data = generators[field["name"]].generate(context=context)
            flatten_data_into_instance(instance,context,generated_data)
        else:
            #print(context)
            instance[field["name"]] = generators[field["name"]].generate(context=context)
            #Update the global context,add the fields and off you go.
            context[field["name"]] = instance[field["name"]]
        ##Here is where you apply constraints:
        #First you check for expressions
        if "constraints" in field.keys():
            #Create local context and then update it. 
            local_context = {}
            local_context[field["name"]] = instance[field["name"]]
            local_context.update(context)
            #Now for each constraint 
            for constraint in field["constraints"]:
                local_context[constraint["output_name"]] = simpleeval.simple_eval(constraint["expression"],names=local_context)
                if constraint["return"] == True:
                    instance[constraint["output_name"]] = local_context[constraint["output_name"]]
                #Store the variable in the context anyway
                context[constraint["output_name"]] = local_context[constraint["output_name"]]
        #If there are expressions, then you go through each one and 
    return instance

#Simple method to flatten the multifield generators. 
def flatten_data_into_instance(instance,context,generated_data):
    for key in generated_data.keys():
        instance[key] = generated_data[key]
        context[key] = generated_data[key]

def generate_dataset(field_definitions,n_items):
    #Only one fakerobj is needed
    fakerobj = Faker()
    generators = cook_generators(field_definitions, n_items)
    dataset = []
    for i in range(n_items):
        dataset.append(generate_instance(field_definitions,generators))
    return dataset
        
def export_dataset(dataset,export_type="csv",filename="dataset"):
    if export_type == "csv":
        df = pd.DataFrame(data=dataset)
        df.to_csv(filename+".csv")
    else:
        df = pd.DataFrame(data=dataset)
        df.to_json(filename+".json")
