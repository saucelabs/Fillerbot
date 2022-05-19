## Library Generators: Tracery

[Tracery](http://tracery.io/) is a tool to generate text. It was created by [GalaxyKate](http://www.galaxykate.com/). 
Tracery is a JavaScript library that uses grammars to generate new text. 

With Tracery, you can generate random instances from a list of items and you can generate utterances by replacing
symbols with randomly selected instances from that rule. For example, if you have the sentence:
```buildoutcfg
The #color# #animal#. 
```
and the rules:
```buildoutcfg
"color": ["red", "orange", "yellow", "green", "blue", "purple"],
"animal": ["cat", "pig", "dragon", "wolf", "hawk"]
```

Tracery would match the symbols in the sentence (words surrounded by two hashtags), with the corresponding rule 
and fill in the sentence with randomly selected items from the different rules. 
```buildoutcfg
The red wolf.
The purple dragon.
```
These can also be nested, with rules consisting of phrases which also have symbols in them. 

You can also have multiple sentences to randomly select from. Tracery's output is generated from a 
"start symbol", which can look like this:
```buildoutcfg
"sentence": ["The #color# #animal#.", "The large #color# #animal#.", "The large #animal#.]
```
This start symbol can have as many items as desired. 

Tracery also has modifiers which you can apply to the symbols. This allows you to make changes like capitalizing or 
pluralizing the rule in certain instances. It also allows you to add a/an without having to worry which one is needed.
For example, the following rules:
```buildoutcfg
"sentence": ["#color.a.capitalize# #animal#."],
"color": ["red", "orange", "yellow", "green", "indigo", "purple"],
"animal": ["cat", "pig", "dragon", "wolf", "hawk"]
```
would generate output like:
```buildoutcfg
start symbol: sentence
An indigo pig.
A green cat. 
```

Here is a table with all the available modifiers:

| Description                  | Modifier      |
|------------------------------|---------------|
| add a/an in front            | a             |
| pluralize                    | s             |
| capitalization               | capitalize    |
| capitalizing the entire word | capitalizeAll |

You can also add more modifiers to Tracery using Javascript. 

### Generating Tracey Outputs with Fillerbot

###### Input Json

Here is an example Json to generate an output using `ComplexTraceryGenerator`. 
```
{
    "name":"ComplexTraceryExample",
    "n_items":5,
    "fields":[
       
       {
         "name":"Pizzaorder",
         "generator_type":"ComplexTraceryGenerator",
         "generator_params": {
            "origin": I would like a #pizzasize# #pizzatype# pizza",
            "pizzasize":["large","12-inch","small","medium","14 inch","family size"],
            "pizzatype":["combo","cheese","pepperoni","veggie","mushroom"]
         }
      }
    ]
}
```

The start symbol is `origin` for `ComplexTraceryGenerator`, so it is the only mandatory field to generate using Tracery. 
The rest of the fields are the rules listed above, where the field is the name of the rule and the value is the list 
of potential inputs. So, for the above json, two potential outputs are:
```buildoutcfg
I would like a small pepperoni pizza. 
I would like a 14 inch combo pizza. 
```


#### Tracery Resources ####
Explaining how to build Tracery grammars is an exercise left to the reader, but here are a series of useful resources to learn how to make tracery grammars:
- [Tracery Tutorial](http://www.crystalcodepalace.com/traceryTut.html) This link takes you to a useful Tracery tutorial with visual guides to show you how to build Tracery grammars of different complexities. 
- [Tracery Editor](http://tracery.io/editor/) This link takes you to  the official Tracery editor which provides a way of making Tracery grammars with guiding visualizations of expansions/containers in the grammar.
- [Tracery](https://tracery.io//) 