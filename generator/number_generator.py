from .generator import Generator
import random


class IntegerRangeGenerator(Generator):
    """
    Generate a random integer in the range between begin and end (inclusive).
    Begin and end must be integers. Wraps a call to random.randint(begin, end)
    Probability distribution is uniform.
    """
    def __init__(self, name, desc=None, gen_id=None, var_name=None, create_date=None, begin=0, end=10):
        super(IntegerRangeGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.begin = begin
        self.end = end

    def generate(self,context=None):
        r_int = random.randint(self.begin, self.end)
        self.last_item_generated = r_int
        return r_int

    def size(self):
        return 1

    def serialize(self):
        o = super(IntegerRangeGenerator, self).serialize()
        o['begin'] = self.begin
        o['end'] = self.end
        return o


class FloatRangeGenerator(Generator):
    """
    Generate a random floating point number in the range between a and b (inclusive).
    a and b may be integers or floats. Wraps a call to random.uniform(a, b)
    Probability distribution is uniform.
    """
    def __init__(self, name, desc=None, gen_id=None, var_name=None, create_date=None, a=0, b=10):
        super(FloatRangeGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.a = a
        self.b = b

    def generate(self,context=None):
        r_float = random.uniform(self.a, self.b)
        self.last_item_generated = r_float
        return r_float

    def size(self):
        return 1

    def serialize(self):
        o = super(FloatRangeGenerator, self).serialize()
        o['a'] = self.a
        o['b'] = self.b
        return o


class GaussFloatGenerator(Generator):
    """
    Generate a random floating point number following a gaussian distribution,
    centered on mean, with standard deviation of std_dev.
    Wraps a call to random.gauss(mean, std_dev)
    Probability distribution is gaussian.
    """
    def __init__(self, name, desc=None, gen_id=None, var_name=None, create_date=None, mean=5, std_dev=1):
        super(GaussFloatGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.mean = mean
        self.std_dev = std_dev

    def generate(self,context=None):
        r_float = random.gauss(self.mean, self.std_dev)
        self.last_item_generated = r_float
        return r_float

    def size(self):
        return 1

    def serialize(self):
        o = super(GaussFloatGenerator, self).serialize()
        o['mean'] = self.mean
        o['std_dev'] = self.std_dev
        return o


class GaussIntGenerator(Generator):
    """
    Generate a random integer following a gaussian distribution,
    centered on mean, with standard deviation of std_dev.
    Wraps a call to round(random.gauss(mean, std_dev))
    Probability distribution is gaussian.
    """
    def __init__(self, name, desc=None, gen_id=None, var_name=None, create_date=None, mean=5, std_dev=1):
        super(GaussIntGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.mean = mean
        self.std_dev = std_dev

    def generate(self,context=None):
        r_int = round(random.gauss(self.mean, self.std_dev))
        self.last_item_generated = r_int
        return r_int

    def size(self):
        return 1

    def serialize(self):
        o = super(GaussIntGenerator, self).serialize()
        o['mean'] = self.mean
        o['std_dev'] = self.std_dev
        return o


class ParetoFloatGenerator(Generator):
    """
    Generate a random floating point number following a Pareto distribution,
    with alpha parameter.
    Wraps a call to random.paretovariate(alpha)
    Probability distribution is Pareto, which means number cannot be
    less than 1.
    """
    def __init__(self, name, desc=None, gen_id=None, var_name=None, create_date=None, alpha=1):
        super(ParetoFloatGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.alpha = alpha

    def generate(self,context=None):
        r_float = random.paretovariate(self.alpha)
        self.last_item_generated = r_float
        return r_float

    def size(self):
        return 1

    def serialize(self):
        o = super(ParetoFloatGenerator, self).serialize()
        o['alpha'] = self.alpha
        return o


class ParetoIntGenerator(Generator):
    """
    Generate a random integer following a Pareto distribution,
    with alpha parameter.
    Wraps a call to round(random.paretovariate(alpha))
    Probability distribution is Pareto, which means number cannot be
    less than 1.
    """
    def __init__(self, name, desc=None, gen_id=None, var_name=None, create_date=None, alpha=1):
        super(ParetoIntGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.alpha = alpha

    def generate(self,context=None):
        r_int = round(random.paretovariate(self.alpha))
        self.last_item_generated = r_int
        return r_int

    def size(self):
        return 1

    def serialize(self):
        o = super(ParetoIntGenerator, self).serialize()
        o['alpha'] = self.alpha
        return o


class WeibullFloatGenerator(Generator):
    """
    Generate a random floating point number following a Weibull distribution,
    with scale parameter alpha and shape parameter beta.
    Wraps a call to random.weibullvariate(alpha, beta)
    Probability distribution is Weibull.
    """
    def __init__(self, name, desc=None, gen_id=None, var_name=None, create_date=None, alpha=4, beta=1.7):
        super(WeibullFloatGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.alpha = alpha
        self.beta = beta

    def generate(self,context=None):
        r_float = random.weibullvariate(self.alpha, self.beta)
        self.last_item_generated = r_float
        return r_float

    def size(self):
        return 1

    def serialize(self):
        o = super(WeibullFloatGenerator, self).serialize()
        o['alpha'] = self.alpha
        o['beta'] = self.beta
        return o


class WeibullIntGenerator(Generator):
    """
    Generate a random floating point number following a Weibull distribution,
    with scale parameter alpha and shape parameter beta.
    Wraps a call to random.weibullvariate(alpha, beta)
    Probability distribution is Weibull.
    """
    def __init__(self, name, desc=None, gen_id=None, var_name=None, create_date=None, alpha=4, beta=1.7):
        super(WeibullIntGenerator, self).__init__(name, desc, gen_id, var_name, create_date)
        self.alpha = alpha
        self.beta = beta

    def generate(self,context=None):
        r_int = round(random.weibullvariate(self.alpha, self.beta))
        self.last_item_generated = r_int
        return r_int

    def size(self):
        return 1

    def serialize(self):
        o = super(WeibullIntGenerator, self).serialize()
        o['alpha'] = self.alpha
        o['beta'] = self.beta
        return o
