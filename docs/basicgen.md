<H3> Basic Generators: List and Static Item Generators </H3> 

These generators are the simplest generators you can create, the static item generator will generate the same input string every time it is invoked, think of it as the equivalent of a constant in programming. 

The second generator is the list generator, this generator selects an element at random from a sample list. This is useful for scenarios such as picking an element out of a drop-down list, or to pick from a set of custom categorical values. 

The following code samples show one example of each type of generator.
    


```
#A simple generator that only returns the word "Hello!"
{"name": "SampleItem",
              "aliases": [],
              "generator_type": "StaticItem",
              "generator_params":{"value":"Hello!"}}

#A simple list generator that picks one of the values in the list. 
 {"name": "SampleListGenerator",
              "aliases": [],
              "generator_type": "ListGenerator",
              "generator_params":{"values":["Hi!","Hey!","Howdy!","Hello!"]}}

```

    Hello!
    Howdy!


As you can see in the examples above,each generator receives one parameter depending on its type. In this case the received parameters are the following:

<ul> 
    <li> The static item generator receives a parameter called <b> value </b> which is of type <b> string </b> </li>
    <li> The list generator receives a parameter called <b> values </b> which is of type <b> list of strings </b> </li>
</ul> 


<H3> Basic Generators: Number Generators </H3>
In addition to creating text data types, our data generation system allows for the creation of numerical data, this comes in the form of number generators. 

There are two main types of number generators: distribution based, and type-based. Distribution based generators sample a given distribution given its parameters and returns a number within the provided range. On the other hand type generators generate numbers within a range and are defined by their types.

The following distribution generators are available:
- **GaussIntGenerator:** This generator returns an integer sampled from a Gaussian distribution with parameters **mean** and **std_dev** both of type *int*
- **GaussFloatGenerator:** This generator returns a float sampled from a Gaussian distribution with parameters **mean** and **std_dev** both of type *float*
- **WeibullIntGenerator:** This generator returns an integer sampled from a Weibull distribution with parameters **alpha** and **beta** both of type *int*
- **WeibullFloatGenerator:** This generator returns a float sampled from a Weibull distribution with parameters **alpha** and **beta** both of type *float*
- **ParetoIntGenerator:** This generator returns an integer sampled from a Pareto distribution with a single parameter **alpha** of type *int*
- **ParetoFloatGenerator:** This generator returns a float sampled from a Pareto distribution with a single parameter **alpha** of type *float*

In addition, the following type-based generators are available
- **IntegerRangeGenerator:** This generator returns a random integer between two numbers given by the parameters **begin** and **end** both of type *int*
- **FloatRangeGenerator:** This generator returns a random integer between two numbers given by the parameters **begin** and **end** both of type *float*

The code below shows examples of a generator of each type:


```
#A generator that samples a Gaussian Distribution with a mean of 25 and std_dev of 1
{"name": "SampleDist",
              "aliases": [],
              "generator_type": "GaussFloatGenerator",
              "generator_params":{"mean":25,"std_dev":1}}

#A generator that picks an integer between 7 and 21
{"name": "SampleNumberType",
              "aliases": [],
              "generator_type": "IntegerRangeGenerator",
              "generator_params":{"begin":7,"end":21}}

```

    25.152090141781787
    20

