
import numpy as np

class FIS_T2:

    """
    This class implements a Fuzzy Inference System (FIS).
    Available aggregators are:
    - OR_max: maximum
    - OR_probsum: probabilistic sum
    - OR_boundsum: bounded sum
    Available defuzzifiers are:
    - COA: center of areas
    - MOM: minimum of maximums
    """

    def __mom(v, m):
        i = np.argmax(m)
        y_inf = v[min(i)]
        y_sup = v[max(i)]
        return (y_inf + y_sup) / 2.0

    __fuzzy_aggregators = {'OR_max': np.maximum,
                           'OR_probsum': lambda x,y: np.add(x, y) - np.multiply(x, y),
                           'OR_boundsum': lambda x,y: np.minimum(1, np.add(x, y))}
    __fuzzy_defuzzifiers = {'CENTROID': lambda v,m: np.sum(np.multiply(v,m)) / np.sum(m),
                            'MOM': __mom}

    def __init__(self, rules, aggregator='OR_max', defuzzifier='CENTROID'):
        """
        Three parameters are needed:
        rules: a list of objects of type FuzzyRule containing the rules of the system
        aggregator: the fuzzy operator to be used to aggregate the rules outputs
        defuzzifier: the defuzzifier function to use
        """
        self.rules = rules
        self.input_variables = set()
        for r in self.rules:
            for a in r.antecedent:
                self.input_variables.add(a[0])
            self.output_variable = r.consequent[0]

        assert aggregator in self.__fuzzy_aggregators.keys()
        self.aggregator = self.__fuzzy_aggregators[aggregator]

        assert defuzzifier in self.__fuzzy_defuzzifiers.keys()
        self.defuzzifier = defuzzifier

        self.input_values = dict()
        self.fuzzified_output = np.zeros(len(self.output_variable.input_values))
        self.defuzzified_output = 0.0

    def __str__(self):
        to_return = 'Input variables:\n'
        to_return += '\t' + str([i_v.name for i_v in self.input_variables]) + '\n'
        to_return += 'Output variables:\n'
        to_return += '\t' + self.output_variable.name + '\n'
        to_return += 'Rules:\n'
        for r in self.rules:
            to_return += '\t' + str(r) + '\n'
        return to_return

    def compute_antecedent_activations(self, input_values):
        """
        This function computes the activation of the antecedent of all rules.
        """
        self.input_values = input_values
        for r in self.rules:
            r.compute_antecedent_activation(input_values)

    def compute_consequent_activations(self):
        """
        This function computes the activation of the consequent of all rules.
        """
        for r in self.rules:
            r.compute_consequent_activation()

    def aggregate(self):
        """
        This function performs the aggregation of the rules outputs
        """
        self.fuzzified_output = np.zeros(len(self.output_variable.input_values))
        for r in self.rules:
            self.fuzzified_output = self.aggregator(self.fuzzified_output, r.consequent_activation)

    # ==========================================================================================

    def defuzzify(self):
        """
        This function defuzzifies the fuzzified_output of the system
        """
        self.defuzzified_output = self.__fuzzy_defuzzifiers[self.defuzzifier](self.output_variable.input_values, self.fuzzified_output)
        return self.defuzzified_output

    def Sum(self, y, theta)
        t1, t2 = 0.0, 0.0
        for i in range(100):
            t1 += (y[i] * theta[i])
            t2 += theta[i]
        if t2 == 0:
            return -1
        return t1 / t2

    def computeCentroid(self, y, upperBond, lowerBond, minMax):
        y1, y2 = 0.0, 100.0
        theta, delta, h = np.zeros([100]), np.zeros([100]), np.zeros([100])
        for i in range(100):
            theta[i] = h[i] = (upperBond[i] + lowerBond[i]) / 2
            delta[i] = (upperBond[i] - lowerBond[i]) / 2
        y1 = Sum(y, h)
        cn = 0
        while (abs(y2 - y1) > 0.000000001):
            cn = cn + 1
            if cn > 1:
                y1 = y2
            e = 0
            for i in range(100):
                if y[i] <= y1 and y1 <= y[i + 1]:
                    e = i
                    break
            for i in range(e):
                if minMax > 0:
                    theta[i] = h[i] - delta[i]
                else:
                    theta[i] = h[i] + delta[i]
            for i in range(e, 100):
                if minMax > 0:
                    theta[i] = h[i] + delta[i]
                else:
                    theta[i] = h[i] - delta[i]
            y2 = Sum(y, theta)
        return y2


    # ==========================================================================================

    def plot_variables(self):
        i = 1
        n_lv = len(self.input_variables) + 1
        for i_v in self.input_variables:
            pl.subplot(1, n_lv, i)
            i += 1
            i_v.plot()
        pl.subplot(1, n_lv, i)
        self.output_variable.plot()

    def plot_rules(self):
        n_r = len(self.rules)
        for i, r in enumerate(self.rules):
            pl.subplot(1, n_r, i+1)
            r.plot()

    def plot_output(self):
        pl.plot(self.output_variable.input_values, self.fuzzified_output)
        pl.axvline(self.defuzzified_output, color='black', linestyle='--')
        pl.ylim(0, 1.05)
        pl.grid()
        pl.title(self.output_variable.name + str(self.input_values))

    def plot2D(self, ax=None):
        """
        Only works for systems with two inputs!!
        """

        assert len(self.input_variables) == 2

        vars_list = []
        for v in self.input_variables:
            vars_list.append(v)

        var1 = vars_list[0]
        var2 = vars_list[1]
        n_var1 = len(var1.input_values)
        n_var2 = len(var2.input_values)

        input_values = {var1.name:0, var2.name:0}
        X, Y = np.meshgrid(var1.input_values, var2.input_values)
        Z = np.zeros((n_var2, n_var1))

        for i in np.arange(n_var1):
            for j in np.arange(n_var2):
                input_values[var1.name] = X[j,i]
                input_values[var2.name] = Y[j,i]
                self.compute_antecedent_activations(input_values)
                self.compute_consequent_activations()
                self.aggregate()
                Z[j,i] = self.defuzzify()

        if ax is None:
            ax = pl.gca(projection='3d')
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        ax.set_xlabel(var1.name)
        ax.set_ylabel(var2.name)
        ax.set_zlabel(self.output_variable.name)

    def plot(self, size=None):
        if size is None:
            size = (12,4)
        pl.figure(figsize=size)
        self.plot_variables()
        pl.figure(figsize=size)
        self.plot_rules()
        pl.figure(figsize=size)
        self.plot_output()