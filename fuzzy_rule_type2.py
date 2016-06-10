import numpy as np
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import linguistic_variable as lv

class Fuzzy_RuleT2:
    """
    This class implements a fuzzy rule.
    A single type of operation per rule is allowed. Yo can choose between:
    AND - minimum
    AND - product
    AND - bounded product
    OR  - maximum
    OR  - probabilistic sum
    OR  - bounded sum
    """

    __fuzzy_operations_names = {'AND_min':'AND', 'AND_prod':'AND', 'AND_boundprod':'AND', 'OR_max':'OR', 'OR_probsum':'OR', 'OR_boundsum':'OR'}
    __fuzzy_operations = {'AND_min': np.min,
                          'AND_prod': np.prod,
                          'AND_boundprod': lambda x: np.max([0, np.sum(x) - 1]),
                          'OR_max': np.max,
                          'OR_probsum': lambda x: np.sum(x) - np.prod(x),
                          'OR_boundsum': lambda x: np.min([1, np.sum(x)])}
    __fuzzy_implication = {'MIN': np.minimum,
                           'PROD': np.prod}

    def __init__(self, operation, antecedent, consequent, implication):
        """
        Three parameters are needed:
        operation: the fuzzy operation to perform
        antecedent: a list of tuples [(linguistic_variable, linguistic_value),...] defining the input fuzzy condition
        consequent: a tuple (linguistic_variable, linguistic_value) defining the output fuzzy assignement
        """
        assert operation in self.__fuzzy_operations.keys()
        assert implication in self.__fuzzy_implication.keys()
        self.operation = operation
        self.antecedent = antecedent
        self.consequent = consequent
        self.implication = implication
        self.antecedent_activation = 0.0
        self.consequent_activationMin = np.zeros(len(consequent[0].input_values))
        self.consequent_activationMax = np.zeros(len(consequent[0].input_values))


    def compute_antecedent_activation(self, input_values):
        """
        This function computes the activation of the antecedent of the rule.
        The first step is the fuzzification of the input values. Then, the activation
        is computed by applying the fuzzy operation to the values of the  membership functions.
        """
        temp = []
        for pair in self.antecedent:
            val = input_values.get(pair[0].name)
            if val is not None:
                membership_values = pair[0].fuzzify(val)
                temp.append(membership_values[pair[1]])
        if len(temp) == 0:
            self.antecedent_activation = 0.0
        else:
            print temp
            temp2 = []
            for pair in temp:
                if(pair[0] + pair[1] > 0.0):
                    temp2.append(pair)
            if len(temp2) == 0:
                temp2.append((0,0))

            self.antecedent_activation = self.__fuzzy_operations[self.operation](temp2)
        return self.antecedent_activation

    def compute_consequent_activation(self):
        """
        This function applies the causal implication operator in order to compute
        the activation of the rule's consequent.
        """
        self.consequent_activationMax, self.consequent_activationMin = self.consequent[0].get_linguistic_value(self.consequent[1])
        print self.antecedent_activation
        self.consequent_activationMin = self.__fuzzy_implication[self.implication](self.antecedent_activation, self.consequent_activationMin)
        self.consequent_activationMax = self.__fuzzy_implication[self.implication](self.antecedent_activation, self.consequent_activationMax)
        print self.consequent_activationMin
        print self.consequent_activationMax
        return (self.consequent_activationMax , self.consequent_activationMax)

    def plot(self):
        pl.plot(self.consequent[0].input_values, self.consequent_activationMin, label=self.consequent[1])
        pl.plot(self.consequent[0].input_values, self.consequent_activationMax, label=self.consequent[1])
        pl.ylim(0, 1.05)
        pl.legend()
        pl.title(self.consequent[0].name)
        pl.grid()