# Fillerbot


## Getting Started

### What is Fillerbot? ###

Fillerbot is a synthetic data generation tool that can create single table data based on a user-defined schema that fits their needs. Users can upload a JSON-based schema of what data they want to generate and how. These schemas contain information about each field; this is analogous to defining columns in a table. These definitions tell us what type of data we generate (i.e., names, numbers, UUIDs). In addition, there are parameters specific to different generator types (i.e., min, max if a number or locales for some data types like names and addresses). Finally, there are "constraints" rules that direct how the data generation proceeds (i.e., if your generated number is >2, then multiply by 5, else multiply by 7). Using these schemas, users can create rich synthetic data that models a wide variety of scenarios. Furthermore, the system can export synthetic data to tabular formats such as CSV or Excel format and semi-structured JSON format data. 

### Who can use Fillerbot? ###

Users across the different development groups can use Fillerbot for a wide variety of scenarios such as:

- **Testers/QA** using Fillerbot's integration in our AutonomIQ product can quickly increase the coverage of test cases by adding synthetic data to their test cases, providing a large amount of test input combinations with minimal effort. In addition, non-AutonomIQ users can easily integrate synthetic data into their manual tests.
-  **General developers** can use synthetic data to pre-populate databases for testing APIs. In addition, developers can create large amounts of artificial logs to test data ingestion engines or create content like synthetic blog posts to test content-driven websites.
- **UX designers** can use realistic-looking synthetic data to create rich data-driven mockups and prototypes. 

These are some example cases on how users across different teams can use the synthetic data output created by Fillerbot, but we hope that a wide array of users can find creative ways to use Fillerbot to simplify their synthetic data generation needs.  

### What kind of data types can I generate with Fillerbot? ###

Fillerbot has support for the following synthetic data types:
- The Faker library wrapper can instantiate common semantic data types like addresses, emails, and names.
- Custom data types like product names and larger text such as reviews or comments using generative grammars powered by the Tracery library wrapper.
- Randomized numeric data (both integer and floating-point) sampled from different distributions such as the Normal, Weibull, Uniform, and Pareto distributions.
- Complex calculated fields using Python expressions with support for reading synthetically generated values. CSV data column sampling from an external file.
- Create complex multi-field objects using a combination of any of the above.Machine learning-based generators based on models like AI21's Jurassic-1 for high-quality complex text data.
- The integrated DBPedia wrapper allows for the generation of real-world knowledge-based data using SPARQL queries

### Prerequisites Installing

### How do I install and run Fillerbot? ###
To run fillerbot please 

First install the requirements with the following command:

```python
pip install -r requirements.txt
```

To run the CLI, navigate to your installation folder on your terminal and run the following command:

```python
python datagencli.py [PATH_TO_FILE] [EXPORT_FORMAT]
```

This command takes two different arguments, one that point to the generator specification JSON (see guide below on how to build one) and one for the export format type you want to export your data to. 

The following snippet shows an example of how you can load a file called "mygenerator.json" and export the results to a CSV type format.

```python
python datagencli.py mygenerator.json csv
```

There are sample JSON data definition files in the examples folder to get you started. These files cover a wide range of common scenarios and provides use case templates for all of our generator types. 

<H4> Export Formats </H4>

Fillerbot can export synthetically generated datasets in the following formats.

- CSV 
- Excel (XLSX) (CLI Only)
- JSON (CLI Only)

### How do I create data specifiations?

Please refer to the JSON data specification [documentation](docs/intro.md) provided in this repo. The documentation contains guides on how to use all of the different types of generators available in fillerbot. 


## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our process for submitting pull requests to us, and please ensure you follow the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to [@PurpleBooth](https://github.com/PurpleBooth) and Zalando for the [original boilerplate](https://github.com/zalando-incubator/new-project)
* Thanks to [@GalaxyKate](https://github.com/galaxykate/) and [@aparrish](https://github.com/aparrish) for creating Tracery and PyTracery
* Thanks to [@danthedeckie](https://github.com/danthedeckie) for creating SimpleEval
* Thanks to [@joke2k](https://github.com/joke2k) for creating Faker
* Thanks to [@dbpedia](https://github.com/dbpedia/) for creating DBPedia
* Thanks to [@huggingface](https://github.com/huggingface/) for creating the Hugging Face API 
* Thanks to [AI 21 Labs](https://www.ai21.com/) for the Jurassic-1 models.


