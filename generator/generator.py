import datetime
import json
import logging
import os
import random
import uuid

class Generator:
    """
    Top level abstract class for Generators

    name - human readable name
    description - human readable description
    gen_id - a UUID that uniquely identifies this generator instance (will create one if none is provided)
    
    """
    def __init__(self, name, description=None, gen_id=None, var_name=None, create_date=None):
        self.name = name
        self.type_label = type(self).__name__
        self.description = description
        if gen_id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = gen_id
        self.var_name = var_name   # name used for variable name in template expansion
        self.var_type = None   # type of data created by generator

        if create_date is None:
            now = datetime.datetime.now()
            current_time = str(now)
            current_time = current_time.replace(" ", "_")
            self.creation_date = current_time
        else:
            self.creation_date = create_date
        self.last_item_generated = None

    def generate(self,context=None):
        """  Returns one example of generated data """
        return None

    def size(self):
        """
        The number of possible items that the generator can create.
        Typically 1, length of a list of options, or some arbitrarily large integer (for countably infinite)
        """
        return 0

    def last_generated(self):
        """ Return the most recently generated item by this generator """
        return self.last_item_generated

    def serialize(self):
        """ Converts generator state into a dictionary suitable for conversion to JSON """
        return {'name': self.name, 'description': self.description, 'type_label': self.type_label, 'gen_id': self.id,
                'var_name': self.var_name, 'var_type': self.var_type, 'size': self.size(), 'data': "",
                'creation_date': self.creation_date}



class StaticItem(Generator):
    """
    A 'generator' that doesn't actually generate any data, and instead just returns the
    same data item each time

    name - human readable name for the generator
    desc - human readable description for the generator
    gen_id - a UUID that uniquely identifies this generator instance (will create one if none is provided)
    var_name - a name used as a variable name in template expansion (e.g., $FOO for varname of 'FOO')

    """
    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(StaticItem, self).__init__(name, desc, gen_id, var_name, create_date)
        self.data = data_item['value']
        self.var_type = str(type(data_item).__name__)

    def generate(self,context=None):
        self.last_item_generated = self.data
        return self.data

    def size(self):
        return 1

    def serialize(self):
        o = super(StaticItem, self).serialize()
        o['data'] = self.data
        return o


class ListGenerator(Generator):
    """
    Return a random choice from a list of data items

    name - human readable name for the generator
    desc - human readable description for the generator
    gen_id - a UUID that uniquely identifies this generator instance (will create one if none is provided)
    var_name - a name used as a variable name in template expansion (e.g., $FOO for varname of 'FOO')
    """
    def __init__(self, name, desc, gen_id=None, var_name=None, data_list=None, create_date=None):
        super(ListGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.data = data_list['values']
        if len(data_list['values']) > 0:
            self.var_type = str(type(data_list['values'][0]).__name__)

    def generate(self,context=None):
        generated_item = random.choice(self.data)
        self.last_item_generated = generated_item
        return generated_item

    def size(self):
        return len(self.data)

    def serialize(self):
        o = super(ListGenerator, self).serialize()
        o['data'] = self.data
        return o


class ReplayGenerator(Generator):
    """ Generator that simply replays the last generated item from another generator """
    def __init__(self, generator):
        super(ReplayGenerator, self).__init__("ReplayGenerator", "Replays a data item", None, None, None)
        self.generator_to_replay = generator

    def generate(self,context=None):
        return self.generator_to_replay.last_item_generated

    def size(self):
        return self.generator_to_replay.size()

    def serialize(self):
        o = super(ReplayGenerator, self).serialize()
        o['replay_generator_id'] = self.generator_to_replay.id

def generator_factory(s, n_items=1):
    """ Recreates a generator from its serialization """
    if s is None:
        return None
    g = None
    generator_type = s['generator_type']

    for key in ('description', 'gen_id', 'var_name', 'creation_date', 'locale'):
        if key not in s.keys():
            s[key] = None
    if generator_type == "Generator":
        g = Generator(s['name'], s['description'], s['gen_id'], s['var_name'], s['creation_date'])
    elif generator_type == "FakerGenerator":
        from .faker_generator import FakerGenerator
        g = FakerGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'], s['creation_date'])
    elif generator_type == "StaticItem":
        g = StaticItem(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'], s['creation_date'])
    elif generator_type == "ListGenerator":
        g = ListGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'], s['creation_date'])
    elif generator_type == "TraceryGenerator":
        from generator.tracery_generator import TraceryGenerator
        g = TraceryGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'], s['creation_date'])
    elif generator_type == "ComplexTraceryGenerator":
        from .tracery_generator import TraceryGenerator, ComplexTraceryGenerator
        g = ComplexTraceryGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'], s['creation_date'])
    elif generator_type == "ComplexFieldGenerator":
        from .tracery_generator import TraceryGenerator, ComplexFieldGenerator
        g = ComplexFieldGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'], s['creation_date'])
    elif generator_type == "TracerySnackGenerator":
        from .tracery_generator import TraceryGenerator, TracerySnackGenerator
        g = TracerySnackGenerator()
    elif generator_type == "FakerGenericGenerator":
        from .faker_generator import FakerGenerator, FakerGenericGenerator
        g = FakerGenericGenerator(s['name'], s['description'], s['locale'], s['gen_id'], s['var_name'], s['generator_params'],s['creation_date'])
    elif generator_type == "FakerGenericRefGenerator":
        from .faker_generator import FakerGenerator, FakerGenericRefGenerator
        g = FakerGenericRefGenerator(s['name'], s['description'], s['locale'], s['gen_id'], s['var_name'], s['generator_params'],s['creation_date'])
    elif generator_type == "FakerFallbackGenerator":
        from .faker_generator import FakerGenerator, FakerFallbackGenerator
        g = FakerFallbackGenerator(s['name'], s['description'], s['locale'], s['gen_id'], s['var_name'], s['generator_params'],s['creation_date'])
    elif generator_type == "OneToOneGenerator":
        from .conditional_generator import OneToOneGenerator
        g = OneToOneGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'],s['creation_date'])
    elif generator_type == "OneToManyGenerator":
        from .conditional_generator import OneToManyGenerator
        g = OneToManyGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'],s['creation_date'])
    elif generator_type == "SingleDependencyGenerator":
        from .conditional_generator import SingleDependencyGenerator
        g = SingleDependencyGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'],s['creation_date'])
    elif generator_type == "ExpressionGenerator":
        from .conditional_generator import ExpressionGenerator
        g = ExpressionGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'],s['creation_date'])
    elif generator_type == "CSVColumnGenerator":
        from .csv_generator import CSVColumnGenerator
        g = CSVColumnGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'],s['creation_date'])
    elif generator_type == "CSVMultiColumnGenerator":
        from .csv_generator import CSVMultiColumnGenerator
        g = CSVMultiColumnGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'],s['creation_date'])
    elif generator_type == "IntegerRangeGenerator":
        from .number_generator import IntegerRangeGenerator
        g = IntegerRangeGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['creation_date'],s['generator_params']['begin'],s['generator_params']['end'])
    elif generator_type == "FloatRangeGenerator":
        from .number_generator import FloatRangeGenerator
        g = FloatRangeGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['creation_date'],s['generator_params']['begin'],s['generator_params']['end'])
    elif generator_type == "GaussFloatGenerator":
        from .number_generator import GaussFloatGenerator
        g = GaussFloatGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['creation_date'],s['generator_params']['mean'],s['generator_params']['std_dev'])
    elif generator_type == "GaussIntGenerator":
        from .number_generator import GaussIntGenerator
        g = GaussIntGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['creation_date'],s['generator_params']['mean'],s['generator_params']['std_dev'])
    elif generator_type == "ParetoFloatGenerator":
        from .number_generator import ParetoFloatGenerator
        g = ParetoFloatGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['creation_date'],s['generator_params']['alpha'])
    elif generator_type == "ParetoIntGenerator":
        from .number_generator import ParetoIntGenerator
        g = ParetoIntGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['creation_date'],s['generator_params']['alpha'])
    elif generator_type == "WeibullFloatGenerator":
        from .number_generator import WeibullFloatGenerator
        g = WeibullFloatGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['creation_date'],s['generator_params']['alpha'],s['generator_params']['beta'])
    elif generator_type == "WeibullIntGenerator":
        from .number_generator import WeibullIntGenerator
        g = WeibullIntGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['creation_date'],s['generator_params']['alpha'],s['generator_params']['beta'])
    elif generator_type == "DBPediaGenerator":
        from .dbpedia_generator import DBPediaGenerator
        g = DBPediaGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'],s['creation_date'])
    elif generator_type == "HFTextGenGenerator":
        from .language_model_generator import HFTextGenGenerator
        g = HFTextGenGenerator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'], s['creation_date'], n_items)
    elif generator_type == "Jurassic1Generator":
        from .language_model_generator import Jurassic1Generator
        g = Jurassic1Generator(s['name'], s['description'], s['gen_id'], s['var_name'], s['generator_params'], s['creation_date'], n_items)
    else:
        logging.error("Unrecognized generator type during deserialization: " + generator_type)
    return g
