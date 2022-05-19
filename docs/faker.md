<H3> Library Generators: Faker </H3>
One of the features in our data generation system is its interoperability with external libraries such as Faker and Tracery. In this case, we can use the Faker library to generate common text data types such as addresses,names,phone numbers, etc... 

Faker generators come in two flavors FakerGeneric and FakerFallback. Faker Generic Generators call standard Faker providers and generate synthetic data given a locale and faker data type. Faker providers are methods used by the Python Faker library to create synthetic data. The entire set of Faker supported providers can be found in the following link: [Faker Provider List](https://faker.readthedocs.io/en/master/providers.html) On the other hand, Faker Fallback Generators, are regex-like pattern generators which receive a pattern string and then generate data that follows the patterns. 

#### Faker Generic Generators ####

As described above Faker Generic generators utilize the Faker python library to generate human-readable synthetic data across a wide variety of locales and semantic data types. In order to create a FakerGenericGenerator we need two parameters:
- **locale** : The locale of the Faker generator, for a set of supported locales see the following link: [Faker Localized Providers](https://faker.readthedocs.io/en/master/locales.html). This parameter is of type *string*. If the parameter is not set, the Faker locale is set to English (United States). This parameter is of type *string*
- **function_name** : This parameter sets the Faker provider that will be called upon generation. The link in the introduction to this section points to the list of providers offered by the library developers. This pattern is of type *string*

#### Faker Fallback Generators ####
Faker fallback generators are an interface of the "bothify" [method](https://faker.readthedocs.io/en/master/providers/baseprovider.html) which uses a regex-like pattern in which the characters *#* and _?_ are wildcards for either numbers or letters respectively. So for example the pattern ???-#?# would be interpreted as a 3 letters, a "dash" symbol followed by a number, one letter and one number. An example output of this pattern would be XZS-2B4. This style of generator is useful for scenarios in which you need a bespoke pattern such as ID numbers, ZIP codes, License Plate Numbers and more. 

In order to configure a Faker Fallback Generator you only need one parameter:
- **pattern** : This parameter sets the generative pattern for Faker's bothify method to work with. This pattern is of type *string* 

The code below shows examples of a generator of each type:


```
#A generator that outputs full addresses
{"name": "SampleFakerGeneric",
              "aliases": [],
              "generator_type": "FakerGenericGenerator",
              "generator_params":{"function_name":"address"}}

#A generator that generates strings like (405)-655-2222
samplegen2 = {"name": "SampleFakerFallbak",
              "aliases": [],
              "generator_type": "FakerFallbackGenerator",
              "generator_params":{"pattern":"(###)###-####"}}
#Let's build a sample 
sg1 = generator_factory(samplegen1)
print(sg1.generate())

sg2 = generator_factory(samplegen2)
print(sg2.generate())
```

    25170 Taylor Causeway
    Howardmouth, IA 69438
    (706)-332-8492
