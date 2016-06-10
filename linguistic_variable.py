import numpy as np
import matplotlib.pyplot as pl



class LinguisticVariableT2:
    """
    This class implements a linguistic variable with some constraints
    in the definition in its membership functions.
    Linguistic values are shaped as trapezoidal membership functions,
    each membership function is defined by a a series of 2 or 4 points:
    
    1 _____p[0].  _ _ _ _ _ _      1 _ _ _  p[1].________.p[2] _ _ _ _temperature.fuzzify(19)
                \\                              /          \\
                 \\                            /            \\
                  \\                          /              \\
                   \\                        /                \\
    0 _ _ _ _ _ _ _ \\._______      0 _____./_ _ _ _ _ _ _ _ _ \\.______
                      p[1]                  p[0]                   p[3]
    
    Therefore, linguistic values are defined at initialization by specifying
    their transition points:
    
    1 _______   t[1]_______   t[3]__   t[5]______ . . .
             \\   /         \\   /    \\   / 
              \\ /           \\ /      \\ /
               X             X        X
              / \\           / \\      / \\
    0 _______/   \\_________/   \\____/   \\________ . . .
           t[0]          t[2]     t[4]
    
    """
    def __init__(self, name, x_min, x_max, transitions, level_names=None, res=0.1):
        """
        Four parameters needed:
        name: name of the variable
        v_min: minimum input value
        v_max: maximum input value
        transitions: list of values defining the starting and ending points of the linguistic values
        level_names: optional, name, or list of names of the linguistic values
        res: resolution
        """
        self.name = name
        assert x_min < x_max
        self.x_min = x_min
        self.x_max = x_max
        self.resolution = res
        self.transitionsMax = np.empty([len(transitions)],dtype=tuple)
        self.transitionsMin = np.empty([len(transitions)],dtype=tuple)
        self.transitions = transitions
        self.input_values = np.arange(self.x_min, self.x_max, self.resolution)
        self.__parse_transitions(transitions)
        self.__assert_transitions(self.transitionsMax)
        self.__assert_transitions(self.transitionsMin)
        self.__set_level_names(level_names)
        self.membership_functions = dict()
        self.membership_functions[self.level_names[0]] = (FreeShapeMF([self.transitionsMax[0][0][0], self.transitionsMax[0][1][0],self.transitionsMax[0][2][0]],
                                                                      [self.transitionsMax[0][0][1], self.transitionsMax[0][1][1], self.transitionsMax[0][2][1]]),
                                                          FreeShapeMF([self.transitionsMin[0][0][0], self.transitionsMin[0][1][0], self.transitionsMin[0][2][0]],
                                                                      [self.transitionsMin[0][0][1], self.transitionsMin[0][1][1],self.transitionsMin[0][2][1]]))
        for i in np.arange(1, len(self.level_names) - 1):
            self.membership_functions[self.level_names[i]] = (FreeShapeMF([self.transitionsMax[i][0][0],
                                                                          self.transitionsMax[i][1][0],
                                                                          self.transitionsMax[i][2][0],
                                                                          self.transitionsMax[i][3][0]],
                                                                         [self.transitionsMax[i][0][1],
                                                                          self.transitionsMax[i][1][1],
                                                                          self.transitionsMax[i][2][1],
                                                                          self.transitionsMax[i][3][1]]),\
                                                             FreeShapeMF([self.transitionsMin[i][0][0],
                                                                          self.transitionsMin[i][1][0],
                                                                          self.transitionsMin[i][2][0],
                                                                          self.transitionsMin[i][3][0]],
                                                                         [self.transitionsMin[i][0][1],
                                                                          self.transitionsMin[i][1][1],
                                                                          self.transitionsMin[i][2][1],
                                                                          self.transitionsMin[i][3][1]]))

        self.membership_functions[self.level_names[-1]] = (FreeShapeMF([self.transitionsMax[-1][0][0], self.transitionsMax[-1][1][0],self.transitionsMax[-1][2][0]],
                                                                      [self.transitionsMax[-1][0][1], self.transitionsMax[-1][1][1],self.transitionsMax[-1][2][1]]),
                                                          FreeShapeMF([self.transitionsMin[-1][0][0], self.transitionsMin[-1][1][0], self.transitionsMin[-1][2][0]],
                                                                      [self.transitionsMin[-1][0][1], self.transitionsMin[-1][1][1], self.transitionsMin[-1][2][1]]))
        # self.membership_functions[self.level_names[0]][0].plot(self.transitionsMax[0:-1][0])
        self.input_value = None
        self.membership_values = dict()

    def __assert_transitions(self, transistions):
        for mf in np.arange(0, len(transistions)):
            n_transitions = len(transistions[mf])
            assert n_transitions >= 2
#            assert n_transitions % 2 == 0
            assert self.x_min <= transistions[mf][0][0]
            assert transistions[mf][-1][0] <= self.x_max
            for i in np.arange(1, n_transitions):
                assert transistions[mf][i-1][0] <= transistions[mf][i][0]

    def __parse_transitions(self, transitions):
        for mf in np.arange(0, len(transitions)):
            self.transitionsMax[mf] =transitions[mf][0]
            self.transitionsMin[mf] =transitions[mf][1]


    def __set_level_names(self, level_names):
        if level_names is None:
            level_names = 'V_level_'
        if isinstance(level_names, str):
            level_names = [level_names]
        if (len(level_names) == 1):
            if not level_names[0].endswith('_level_'):
                level_names[0] += '_level_'
            level_names = [level_names[0] + str(i) for i in np.arange((len(self.transitions) / 2) + 1)]
#        assert len(level_names) == (len(self.transitions) / 2) + 1
        self.level_names = level_names

    def get_linguistic_value(self, name):
        assert name in self.level_names
        return (self.membership_functions[name][0].apply_to(self.input_values), self.membership_functions[name][1].apply_to(self.input_values))

    def plot(self):
        for name, mf in self.membership_functions.iteritems():
            mf[0].plot(self.input_values, name=name)
            mf[1].plot(self.input_values)
            if self.input_value:
                activation = mf(self.input_value)
                pl.plot([self.y_min, self.input_value, self.input_value, self.input_value], [activation, activation, 0, activation], 'k--')
        pl.ylim(0, 1.05)
        pl.legend(loc=7)
        pl.grid(True)
        pl.title(self.name)

    def fuzzify(self, value):
        self.fuzzy_value = value
        self.membership_values = dict()
        for name, mf in self.membership_functions.iteritems():
            self.membership_values[name] =(mf[0](self.fuzzy_value), mf[1](self.fuzzy_value))
        print self.membership_values # TODO Remove
        return self.membership_values




class FreeShapeMF:
    """
    This class implements a membership function with free shape.
    The shape of the function is defined by giving a vector of input values
    and a the vector of corresponding membership values.
    Calling this class with a float number as parameter returns the
    degree of activation of the membership function for that value computed
    using interpolations between the two nearest known values.
    """
    def __init__(self, input_values, membership_values):
        """
        Two parameters needed:
        input_values: vector of input values
        membership_values: vector of membership values
        """
        assert len(input_values) == len(membership_values)
        for i in np.arange(1, len(input_values)):
            assert input_values[i-1] <= input_values[i]
        self.input_values = input_values
        self.membership_values = membership_values

    def __call__(self, value):
        if value <= self.input_values[0]:
            return self.membership_values[0]
        elif value >= self.input_values[-1]:
            return self.membership_values[-1]
        else:
            i = 1
            while value > self.input_values[i]:
                i = i + 1
            i_p = (value - self.input_values[i-1]) / float(self.input_values[i] - self.input_values[i-1])
            return i_p * (self.membership_values[i] - self.membership_values[i-1]) + self.membership_values[i-1]

    def apply_to(self, input_values):
        return map(self, input_values)

    def plot(self, input_values, col=None, name=None):
        output_values = self.apply_to(input_values)
        print output_values
        if col:
            pl.plot(input_values, output_values, c=col, label=name)
        else:
            pl.plot(input_values, output_values, label=name)
        pl.ylim(0, 1.05)
        pl.grid(True)





