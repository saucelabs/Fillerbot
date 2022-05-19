<H1> Sauce Labs Synthetic Data Generation : Generator Specification JSON Writing Guide </H1>

In this guide we will cover how to create data generator specifications using our JSON-based language, this document shows interactive examples of how  to build a generator specification, what kinds of synthetic data generators can be used and how to configure them, advanced features such as dependencies, CSV import, and python expressions. 

### What kind of data types can I generate with Fillerbot? ###

Fillerbot has support for the following synthetic data types:
- The Faker library wrapper can instantiate common semantic data types like addresses, emails, and names.
- Custom data types like product names and larger text such as reviews or comments using generative grammars powered by the Tracery library wrapper.
- Randomized numeric data (both integer and floating-point) sampled from different distributions such as the Normal, Weibull, Uniform, and Pareto distributions.
- Complex calculated fields using Python expressions with support for reading synthetically generated values. CSV data column sampling from an external file.
- Create complex multi-field objects using a combination of any of the above.
- Machine learning-based generators based on models like AI21's Jurassic-1 for high-quality complex text data.
- The integrated DBPedia wrapper allows for the generation of real-world knowledge-based data using SPARQL queries

<H2> Generator Specifications </H2> 

A generator specification is a JSON-based specification of a data table, in this definition there exist three main components:
<ul> 
    <li> A name to identify the generator specification: This can be something like "Reservations Test Case Sign Up Form" or "Login Data" </li> 
    <li> A number of data rows to be generated: If it is not set, it will default to 100</li> 
    <li> A list of fields (columns) to be generated: These fields are composed of generators of many kinds, we will illustrate how each one works in the sections below </li> 
</ul> 
The next code snippet shows an example of a simple 8 column table with 100 rows. 

```python
    {
      "name": "SchoolExample",
      "n_items": 100,
      "fields": [
        {
          "name": "first_name",
          "aliases": [],
          "generator_type": "FakerGenericGenerator",
          "generator_params": {
            "function_name": "first_name"
          }
        },
        {
          "name": "last_name",
          "aliases": [],
          "generator_type": "FakerGenericGenerator",
          "generator_params": {
            "function_name": "last_name"
          }
        },
        {
          "name": "english_grade",
          "aliases": [],
          "generator_type": "IntegerRangeGenerator",
          "generator_params": {
            "begin": 0,
            "end": 100
          },
          "constraints": [
            {
              "expression": " True if english_grade > 40 else False ",
              "names": {},
              "output_name": "passed_english",
              "return": true
            }
          ]
        },
        {
          "name": "maths_grade",
          "aliases": [],
          "generator_type": "IntegerRangeGenerator",
          "generator_params": {
            "begin": 0,
            "end": 100
          },
          "constraints": [
            {
              "expression": " True if maths_grade > 40 else False ",
              "names": {},
              "output_name": "passed_maths",
              "return": true
            }
          ]
        },
        {
          "name": "mathpass",
          "aliases": [],
          "generator_type": "IntegerRangeGenerator",
          "generator_params": {
            "begin": 0,
            "end": 100
          },
          "constraints": [
            {
              "expression": " True if mathpass > 40 else False ",
              "names": {},
              "output_name": "mathpass",
              "return": true
            }
          ]
        },
        {
          "name": "social_sciences_grade",
          "aliases": [],
          "generator_type": "IntegerRangeGenerator",
          "generator_params": {
            "begin": 0,
            "end": 100
          },
          "constraints": [
            {
              "expression": " True if social_sciences_grade > 40 else False ",
              "names": {},
              "output_name": "passed_soc_sci",
              "return": true
            }
          ]
        },
        {
          "name": "result",
          "aliases": [],
          "generator_type": "ExpressionGenerator",
          "generator_params": {
            "expression": " (english_grade + maths_grade + social_sciences_grade)/3 ",
            "names": {}
          },
          "constraints": [
            {
              "expression": " True if result > 40 else False ",
              "names": {},
              "output_name": "is_passing",
              "return": true
            }
          ]
        },
        {
          "name": "total_passed",
          "aliases": [],
          "generator_type": "ExpressionGenerator",
          "generator_params": {
            "expression": " True if (passed_maths == True and passed_english == True and passed_soc_sci == True) else False",
            "names": {}
          }
        }
      ]
    }

```
As illustrated by the example above, you can see the three components that we we have in our generator specification, our name, and a list of field definitions. These fields refer to a set of generators. These generators can be anything, they can pick a value from a list, use a library such as Faker to create synthetic data, amongst others. 

<H2> Field Definitions </H2> 

A field definition has a set of different properties that represent how they are configured in our generator specification, these properties are the following:

<ul> 
    <li> A name : An identifying name based on the element it will inject data into </li> 
    <li> A set of aliases: This allows for the same generator to be injected into more fields of the same type </li> 
    <li> A generator type: We will detail what generator types exist in the following subsections </li> 
    <li> Generator parameters: These vary from generator to generator, and will be detailed in the following subsections </li> 
    <li> Constraints: Generator output can be controlled by specifying specific limits and transformations, the constraints section will contain a larger explanation of the topic </li> 
</ul> 

The following code snippet shows an example of a field definition:


```python



    {
      "name": "english_grade",
      "aliases": [],
      "generator_type": "IntegerRangeGenerator",
      "generator_params": {
        "begin": 0,
        "end": 100
      },
      "constraints": [
        {
          "expression": " True if english_grade > 40 else False ",
          "names": {},
          "output_name": "passed_english",
          "return": true
        }
      ]
    }

```

This example shows a generator that will generate a grade (a number between 0 and 100), with the constraint of that whenever the generated grade is above 40, it will store the condition's value in a field called "passed_english". 

The following code snippet shows the output of the generator.

    The value for english_grade is: 17

Having shown an example of what a generator definition looks like, we proceed to show the diverse kinds of generators that exist in our system. Please refer to the following documents to see how different generator types are built in Fillerbot. 

- Basic Generators are covered in [Basic Generators: Text and Numerical](basicgen.md).
- Faker generators are covered in [Library Generators: Faker](faker.md). 
- Tracery generators are covered in [Library Generators: Tracery](tracery.md). 
- CSV import and Python expressions are covered in [Data-driven and Advanced Generators](dataadvanced.md).
- SPARQL and DBPedia are covered [DBPedia Generators](dbpedia.md).
- ML-Based language model generators are covered in [Language MOdel Generators](language_model.md)


