## Language Model Generator

Large language models have recently made great improvements to the field of natural language
generation. They use deep learning and massive amounts of natural language data to learn the 
conditional probabilities between tokens. State-of-the-art large language models use the 
Transformer architecture ([Vaswani et al., 2017](https://proceedings.neurips.cc/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)), 
which uses attention to also learn what portions of the input and previously generated text are important
to generate the next token. These models take as input natural language, which can be a paragraph, sentence, 
phrase or word. Then, the model generates a continuation of the input utterance. So given an input 
phrase, the model will generate the rest of the sentence, and potentially additional sentences. 
The exact output will 
also depend on additional input parameters, such as maximum number of tokens to generate. 

We use large language models within Fillerbot to generate more varied and less structured data. 
In order to use these models and generate the output you desire, one must use prompt engineering. 
This is where you carefully structure the prompt to encourage the model to generate the kind of output 
you need. So, if you want to generate a list of items, you will need to start with a description 
of the list as well as one or two example items in the list. For example, if you want a list of fruits, an 
example prompt could be:
```
A list of fruits:
1. banana
2. apple
```
Including both the description and the example item(s) helps the model both recognize that it's supposed to generate 
a list and encourages the model to stay on topic. Using just the example list items in this case can result in 
a list of more than just fruits, such as vegetables. Here is an article on prompt engineering for more information: 
[Prompt Engineering Tips and Tricks with GPT-3](https://blog.andrewcantino.com/blog/2021/04/21/prompt-engineering-tips-and-tricks/).

We are able to generate text from using two different methods. First is a large language model,
[Jurassic-1](https://uploads-ssl.webflow.com/60fd4503684b466578c0d307/61138924626a6981ee09caf6_jurassic_tech_paper.pdf),
which is a freely available language model used for many tasks including text generation
and [Hugging Face](https://huggingface.co/), a data science platform with many pre-trained machine learning
models which are freely available for public use. 

Jurassic-1 is an AI21 studio's model. It comes in two sizes, 178B parameters (J1-Jumbo) and 7B parameters
(J1-Large). J1-Jumbo is one of the largest language models released for general use. Both models are accessible
within Fillerbot. For more information, 
refer to the technical paper and AI21 studio's website linked below. 

Hugging Face, as mentioned before, is a data science platform. They have over 40K pre-trained machine learning models 
for tasks such as summarization and image classification. We have a generator which integrates Hugging Face's 
[text generation models](https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads), which generate
text in the method described above. 

### Generating Large Language Model Outputs with Fillerbot

There are two methods you can use to generate natural language using a large language model:

1. `Jurassic1Generator`
2. `HFTextGenGenerator`

These are input as the `generator_type`. Each has different set of additional parameters. 

#### Jurassic1Generator

In order to use the `Jurassic1Generation`, you will need to have a valid API key. It is free to create an account with
AI21
and use the service, though the free version has a finite number of tokens that you can generate a 
month, so please be aware of this when generating text. 

###### API Key Generation

First, go to [https://studio.ai21.com/sign-up](https://studio.ai21.com/sign-up). This will prompt you to create an 
account with AI21 studio, which you must have to use this generator. 

After you setup your account, go to [https://studio.ai21.com/](https://studio.ai21.com/) amd click the account icon on 
the upper right corner of the screen:

![](images/account_icon.jpg)

Click on the `Account` option from the dropdown. A screen with account details should load, which will have your
API key. Copy that key into the input Json you will create, which will be described in more detail below. 

###### Input Json

Here is an example Json to generate an output using `Jurassic1Generation`. 
```
{
    "name":"JurassicExample",
    "n_items":10,
    "fields":[
        {
            "name":"q1_fruit",
            "aliases":["fruit"],
            "generator_type":"Jurassic1Generator",
            "generator_params": {
                "apitoken": "XXXXXXXX",
                "prompt": "List of fruits:\n1. banana\n2. apple",
                "max_tokens": 64,
                "temperature": 0.7,
                "stop_sequences": ["\n\n"],
                "topKReturn": 1.0,
                "model": "j1-large"
            }
        }
    ]
}
```

The `"XXXXXXXX"` for the `apitoken` field must be replaced with the API token from the previous step. 

`max_tokens` is the 
maximum number of tokens the model will generate for each output. 

`prompt` is the prompt that will be passed to the model which will be used to generate the output.

`temperature` is a representation of how 
random/varied the output will be. The lower the number, the less random, but also less variation the output will be. 
With a temperature of 0, the output will always be the same. If you want a different result each time, having a higher 
temperature is important. 

`stop_sequences` is a list of tokens which will cause the output to stop, regardless of if the max number of tokens has
been reached or not. In this example, two new lines will stop generation since it indicates that the model is no longer 
generating items in the list. If you want to generate a single sentence, having a list of different punctuations (.!?) 
would prevent the model from generating output you will not use. 

`topKReturn` is another way to control the randomness of the generated output. It is the percentile of probability
from which tokens are sampled. So, with a value of less than 1, the model will only sample from the top percentile 
of options that are considered. This will result in more stable, but also more repetitive, outputs. 

`model` is the model you want to use for generation. The three potential inputs for this input are `j1-large` 
(7B parameters), `j1-grande` (17B parameters) and `j1-jumbo` (178B parameters). Each model has a different usage 
limit for a free account, with the smallest model having the most available requests and generated tokens per month. 
Because of 
this, starting with a smaller model and checking if that model can generate the output you require before experimenting
with the larger models is prudent. 


#### HFTextGenGenerator

In order to use the Hugging Face Generator, you need to find an available text generation model. These models are 
listed here: https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads. There are many models
which are trained on different types of data. Some are more general, such as `gpt2`, which was trained on a large 
corpus of data scrapped from the internet, and others are very specific, `google/reformer-crime-and-punishment`, 
which was trained on the novel Crime and Punishment. 

###### Input Json

Here is an example Json to generate an output using `HFTextGenGenerator`. 
```
{
    "name":"HFExample",
    "n_items":5,
    "fields":[
       {
         "name":"q1_fruit",
         "aliases":["fruit"],
         "generator_type":"HFTextGenGenerator",
         "generator_params": {
            "prompt": "List of fruits:\n1. banana\n2. apple",
            "model": "gpt2", 
            "max_tokens": 64,
            "do_sample": true,
            "temperature": 0.7,
            "top_k": 100,
            "top_p": 1.0,
            "repetition_penalty": 75,
            "max_new_tokens": 200,
            "return_full_text": true
           }
       },
    ]
}
```

`prompt` is the prompt that will be passed to the model which will be used to generate the output.

`model` is the model you want to use for generation. The model must be a text generation model on Hugging Face.

`max_tokens` (optional) is the 
maximum number of tokens the model will generate for each output. 

`do_sample` (optional, default: true) is whether or not to use sampling. 

`temperature` (optional, default: 1.0) is a representation of how 
random/varied the output will be. The lower the number, the less random, but also less variation the output will be. 
With a temperature of 0, the output will always be the same. If you want a different result each time, having a higher 
temperature is important. 

`top_k` (optional, default: None) is an integer to define the number of top tokens which will considered 
when creating new text.

`top_p` (optional, default: None) is a float to define the tokens that are within the sample operation of text generation.

`repetition_penalty` (optional, default: None) is how much a word is penalized for having already appeared when 
selecting subsequent words.

`max_new_tokens` (optional, default: None) is the maximum amount of new tokens which will appear in the output. 

`return_full_text` (optional, default: True) is whether the prompt will be prepended to the output or not. 

More details on the parameters are here: https://huggingface.co/docs/api-inference/detailed_parameters#text-generation-task


### Additional Links
* Jurassic-1 technical paper: [https://uploads-ssl.webflow.com/60fd4503684b466578c0d307/61138924626a6981ee09caf6_jurassic_tech_paper.pdf](https://uploads-ssl.webflow.com/60fd4503684b466578c0d307/61138924626a6981ee09caf6_jurassic_tech_paper.pdf)
* AI21 studio playground for Jurassic-1: [https://studio.ai21.com/](https://studio.ai21.com/)
* Prompt Engineering article: https://blog.andrewcantino.com/blog/2021/04/21/prompt-engineering-tips-and-tricks/
* Hugging Face: https://huggingface.co/
* Hugging Face text generation models: https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads