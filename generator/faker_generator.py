from .generator import Generator
from faker import Faker

###Standard Faker Generator Interface 
class FakerGenerator(Generator):
    """
    FakerGenerator
    """

    def __init__(self, name, desc=None, locale=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(FakerGenerator, self).__init__(name, desc, gen_id, var_name, create_date)

        self.locale = None
        self.data = data_item
        self.var_type = str(type(self.data).__name__)

    def generate(self,context=None):
        return self.data

    def size(self):
        return -1

    def serialize(self):
        o = super(FakerGenerator, self).serialize()
        o['data'] = self.data
        o['locale'] = self.locale
        return o

##New Faker Generator Interface
###Generic Faker Generators assume that there will be one and only one Faker object in the system at runtime. 
# Since we are not storing the faker object here, we just return the function name we will call. 
class FakerGenericRefGenerator(FakerGenerator):
    def __init__(self, name, desc=None, locale=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(FakerGenericRefGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.description = 'Faker Generic Function Reference' + (' with a locale of ' + locale if locale else '')
        self.locale = '' + locale if locale else ''
        self.type_label = 'FakerGenericRefGenerator'
        self.funcname = data_item['function_name']
    
#Breaks the design, but will let us return the function name to our main provider. 
    def generate(self,context=None):
        return self.funcname


##Another way of doing it is like the classic but with some extra steps. 
class FakerGenericGenerator(FakerGenerator):
    def __init__(self, name, desc=None, locale=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(FakerGenericGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.description = 'Faker Generic Object' + (' with a locale of ' + locale if locale else '')
        self.locale = '' + locale if locale else ''
        self.type_label = 'FakerGenericGenerator'
        self.faker = Faker(locale)
        self.funcname = data_item['function_name']
    
    def generate(self,context=None):
        method = None
        try:
            method = getattr(self.faker, self.funcname)
        except AttributeError:
            raise NotImplementedError("Class `{}` does not implement `{}`".format(self.faker.__class__.__name__, self.funcname)) 
        return method()
    
#This is our Faker fallback, we use the bothify method to generate basic pattern-based stuff. 
class FakerFallbackGenerator(FakerGenerator):

    def __init__(self, name='FakerFallbackGenerator', desc=None, locale=None,  gen_id=None,
                 var_name='FakerFallback', data_item=None, create_date=None):
        super(FakerFallbackGenerator, self).__init__(name, desc, locale, gen_id, var_name, data_item, create_date)
        self.description = 'Pattern-based text generated with Faker' + (' with a locale of ' + locale if locale else '')
        self.locale = '' + locale if locale else ''
        self.type_label = 'FakerFallbackGenerator'
        self.faker = Faker(locale)
        self.data = data_item['pattern']

    def generate(self,context=None):
        return self.faker.bothify(text=self.data)
    
