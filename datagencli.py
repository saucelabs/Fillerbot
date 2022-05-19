import argparse
import os
import sys
import json
# from generator.datagenmethods import *
from methods import *
import pandas as pd
from art import *

#Initialize parser here.
# Create the parser
arg_parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
arg_parser.add_argument('Path',
                       metavar='path',
                       type=str,
                       help='The path to the JSON definition file to generate data from.')

arg_parser.add_argument('Filetype',
                       metavar='filetype',
                       type=str,
                       help='The file type to which the generated data will be exported to. ')

args = arg_parser .parse_args()


def generate_dataset_from_file(filepath):
    #Load the data
    try:
        with open(filepath) as f:
            data = json.load(f)
            
        #Store the filename
        filename = data["name"]
    except:
        data = {}
        filename = None
        print("Failed to load JSON from file path: {}".format(filepath))

    if data is not None: 
        try:
            dataset = generate_dataset(data["fields"],data["n_items"])
        except:
            dataset = None 
    #Call and return generated dataset. 

    return dataset,filename
    
def export_dataset_to_file(dataset,filetype,filename):
    #Do the export types.
    #First you create the dataframe for export. 
    df = pd.DataFrame(data=dataset)
    if filetype == "csv":
        df.to_csv(filename+".csv")
    elif filetype == "xml":
        df.to_csv(filename+".xml")
    elif filetype == "xlsx":
        df.to_excel(filename+".xlsx")
    else:
        df.to_json(filename+".json")
    
def main():
    print("Opening file from: "+args.Path)
    dataset,filename = generate_dataset_from_file(args.Path)
    #Make sure you have something to return.
    if dataset is not None and filename is not None:
        try:
            export_dataset_to_file(dataset,args.Filetype,filename)
            print("Exported to file: {}.{}".format(filename,args.Filetype))
        except:
            print("Could not export dataset. Please check your data definition JSON file.")
    
if __name__ == "__main__":
    main()