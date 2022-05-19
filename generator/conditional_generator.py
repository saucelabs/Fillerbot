from .generator import Generator,ListGenerator
import simpleeval
import random

###Standard Faker Generator Interface 
class OneToOneGenerator(Generator):
    """
    OneToOneGenerator
    """

    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(OneToOneGenerator, self).__init__(name, desc, gen_id, var_name, create_date)

        self.inputs = data_item["inputs"]
        self.outputs = data_item["outputs"]
        self.data = data_item
        self.expression = self.get_expression(self.inputs,self.outputs)
        self.var_type = str(type(self.data).__name__)

    def get_expression(self,expr_inputs,expr_outputs):
        expr = ""
        for expr_input,expr_output in zip(expr_inputs,expr_outputs):
            expr += "'"+expr_output+"' if exp_inp =="+"'"+expr_input+"' else "
        expr +="'default'"
        return expr
    
    def generate(self,context=None):
        return simpleeval.simple_eval(self.expression,names={"exp_inp":random.choice(self.inputs)})

    def size(self):
        return -1

    def serialize(self):
        o = super(OneToOneGenerator, self).serialize()
        o['data'] = self.data
        o['expression'] = self.expression
        return o


class OneToManyGenerator(Generator):
    """
    OneToOneGenerator
    """

    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(OneToManyGenerator, self).__init__(name, desc, gen_id, var_name, create_date)

        self.inputs = data_item["inputs"]
        self.outputs = data_item["outputs"]
        self.data = data_item
        self.expression = self.get_expression(self.inputs)
        self.var_type = str(type(self.data).__name__)

    def get_expression(self,expr_inputs):
        expr = ""
        for i in range(len(expr_inputs)):
            expr += str(i)+" if exp_inp =="+"'"+expr_inputs[i]+"' else "
        expr +="-1"
        return expr
    
    def generate(self,context=None):
        index =  simpleeval.simple_eval(self.expression,names={"exp_inp":random.choice(self.inputs)})
        return random.choice(self.outputs[index])

    def size(self):
        return -1

    def serialize(self):
        o = super(OneToManyGenerator, self).serialize()
        o['data'] = self.data
        o['expression'] = self.expression
        return o

class SingleDependencyGenerator(Generator):
    """
    OneToOneGenerator
    """

    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(SingleDependencyGenerator, self).__init__(name, desc, gen_id, var_name, create_date)

        self.inputs = data_item["inputs"]
        self.outputs = data_item["outputs"]
        self.dependency = data_item["dependency"]
        self.data = data_item
        self.expression = self.get_expression(self.inputs)
        self.var_type = str(type(self.data).__name__)

    def get_expression(self,expr_inputs):
        expr = ""
        for i in range(len(expr_inputs)):
            expr += str(i)+" if "+self.dependency+" =="+"'"+expr_inputs[i]+"' else "
        expr +="-1"
        return expr
    
    def generate(self,context=None):
        index =  simpleeval.simple_eval(self.expression,names=context)
        return random.choice(self.outputs[index])

    def size(self):
        return -1

    def serialize(self):
        o = super(SingleDependencyGenerator, self).serialize()
        o['data'] = self.data
        o['expression'] = self.expression
        return o
    
class ExpressionGenerator(Generator):
    """
    ExpressionGenerator
    """

    def __init__(self, name, desc=None, gen_id=None, var_name=None, data_item=None, create_date=None):
        super(ExpressionGenerator, self).__init__(name, desc, gen_id, var_name, create_date)

        self.locale = None
        self.data = data_item
        self.expression = data_item["expression"]
        self.names = data_item["names"]
        self.var_type = str(type(self.data).__name__)
    
    def generate(self,context=None):
        self.names.update(context)
        return simpleeval.simple_eval(self.expression,names=self.names)

    def size(self):
        return -1

    def serialize(self):
        o = super(ExpressionGenerator, self).serialize()
        o['data'] = self.data
        o['expression'] = self.expression
        o['names'] = self.names
        return o