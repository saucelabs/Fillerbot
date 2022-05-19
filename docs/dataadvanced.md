<H3> Data Driven Generators: Read from CSV </H3>
In addition to library support, we allow reading data from CSV files when there are lists of bespoke tabular data that need to be loaded into the data generation tool. For example, users with dumps of production databases, or with specific test case data, in this case there exist two types of generators called CSVColumn and CSVMultiColumn generators, the difference between the two is that the CSVColumn generator only sample one columm, where as the CSV MultiColumnGenerator samples and returns multiple columns.

#### CSV Column Generator ####
The CSV Column Generator takes the following two parameters to be instantiated correctly:
- **csv_path** : This parameter specifies the path of the CSV file to be read (this should not be exposed to users generally), the parameter is of type *string*
- **column** : This parameter specifies which column of the CSV will be sampled, the parameter is of type *string*

#### CSV Multi Column Generator ####
The CSV Multi Column Generator takes the following two parameters to be instantiated correctly:
- **csv_path** : This parameter specifies the path of the CSV file to be read (this should not be exposed to users generally), the parameter is of type *string*
- **columns** : This parameter specifies which columns of the CSV will be sampled, the parameter is of type *list of string*

The following code shows examples for this type of generator:


```
{"name": "SampleSingleCSV",
              "aliases": [],
              "generator_type": "CSVColumnGenerator",
              "generator_params":{"csv_path":"sampledata/CSV/testcsvcolumns.csv","column":"age"}}

 {"name": "SampleMultiCSV",
              "aliases": [],
              "generator_type": "CSVMultiColumnGenerator",
              "generator_params":{"csv_path":"sampledata/CSV/testcsvcolumns.csv","columns":["state","city","zipcode"]}}

```

    16
    {'state': 'CA', 'city': 'Santa Clara', 'zipcode': 95121}


<H3> Advanced Generators: Python Expression Generators </H3>
More advanced users can input pure python expressions to create complex calculated fields, thanks to the SimpleEval library users can create advanced fields that read from other field values in the data generator specification, create new values, and output different data types beyond text and numbers (i.e. boolean fields).

#### Simple Eval Resources ####
- [SimpleEval Project Homepage](https://pypi.org/project/simpleeval/) The project homepage for SimpleEval has the documentation and basic information of what is supported when it comes to basic expression handling with the library.

These generators only require two  parameters called **expression** of type *string* which contains the expression, and one called **names** of type *dict* (names should never be exposed to users)

The examples below show some of the things that can be done with python expressions using SimpleEval


```
#Multiply two random numbers between (0 and 10) and divide them by 5 
 {"name": "SampleExpression1",
              "aliases": [],
              "generator_type": "ExpressionGenerator",
              "generator_params":{"expression":"randint(10)*randint(7)/5","names":{}}}

#Take a variable named age (inserted in names, but in production should be read from the generatiuon process) and tell whether it is an adult or not
 {"name": "SampleExpression2",
              "aliases": [],
              "generator_type": "ExpressionGenerator",
              "generator_params":{"expression":"'Adult' if age >= 18 else 'Not Adult'",
                                  "names":{"age":21}
```

    1.0
    Adult

