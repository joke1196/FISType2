import numpy as np
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import linguistic_variable as lv

class FuzzyRule:
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
        self.consequent_activation = np.zeros(len(consequent[0].input_values))
    
    def __str__(self):
        to_return = 'Fuzzy rule:\n\tIF '
        for i, pair in enumerate(self.antecedent):
            to_return += pair[0].name + ' IS ' + pair[1]
            if i < (len(self.antecedent) - 1):
                to_return += ' ' + self.__fuzzy_operations_names[self.operation] + ' '
        to_return += '\n\tTHEN ' + self.consequent[0].name + ' is ' +  self.consequent[1]
        to_return += '\n\tAntecedent activation: ' + str(self.antecedent_activation)
        return to_return
    
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
            self.antecedent_activation = self.__fuzzy_operations[self.operation](temp)
        return self.antecedent_activation
    
    def compute_consequent_activation(self):
        """
        This function applies the causal implication operator in order to compute
        the activation of the rule's consequent.
        """
        self.consequent_activation = self.consequent[0].get_linguistic_value(self.consequent[1])
        self.consequent_activation = self.__fuzzy_implication[self.implication](self.antecedent_activation, self.consequent_activation)
        return self.consequent_activation
    
    def plot(self):
        pl.plot(self.consequent[0].input_values, self.consequent_activation, label=self.consequent[1])
        pl.ylim(0, 1.05)
        pl.legend()
        pl.title(self.consequent[0].name)
        pl.grid()

    def plot2D(self, ax=None):
        """
        Only works if the rule has two input variables!
        """
        assert len(self.antecedent) == 2
        
        var1 = self.antecedent[0][0]
        var2 = self.antecedent[1][0]
        n_var1 = len(var1.input_values)
        n_var2 = len(var2.input_values)
        val1 = self.antecedent[0][1]
        val2 = self.antecedent[1][1]
        
        membership_var1 = var1.get_linguistic_value(val1)
        membership_var2 = var2.get_linguistic_value(val2)
        membership_var1_2D = np.tile(membership_var1, n_var2).reshape(n_var2, n_var1)
        membership_var2_2D = np.tile(membership_var2, n_var1).reshape(n_var1, n_var2).T
        
        X, Y = np.meshgrid(var1.input_values, var2.input_values)
        Z = np.reshape(map(self.__fuzzy_operations[self.operation], zip(membership_var1_2D.flatten(), membership_var2_2D.flatten())), membership_var1_2D.shape)

        if ax is None:
            ax = pl.gca(projection='3d')
        ax.plot(var1.input_values, np.zeros(n_var1), membership_var1, 'r--')
        ax.plot(var1.input_values, max(var2.input_values)*np.ones(n_var1), membership_var1, 'r--')
        ax.plot(np.zeros(n_var2), var2.input_values, membership_var2, 'b--')
        ax.plot(max(var1.input_values)*np.ones(n_var2), var2.input_values, membership_var2, 'b--')
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        ax.set_xlabel(var1.name)
        ax.set_ylabel(var2.name)
        ax.set_zlabel(self.operation)