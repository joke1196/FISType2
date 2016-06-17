import linguistic_variable as lv
import matplotlib.pyplot as pl
import FIST2 as fis
import fuzzy_rule_type2 as fr

fh = lv.LinguisticVariableT2('File Hash', 0, 90, [
    [[(0, 1), (10, 1), (30, 0)], [(0, 1), (5, 1), (25, 0)]],
    [[(10, 0), (30, 1), (50, 1), (70, 0)], [(15, 0), (35, 1), (45, 1), (65, 0)]],
    [[(50, 0), (70, 1), (90, 1)], [(55, 0), (75, 1), (90, 1)]]
], ['low', 'medium', 'high'], res=1.0)

ipc = lv.LinguisticVariableT2('IP Connection', 0, 90, [
    [[(0, 1), (10, 1), (30, 0)], [(0, 1), (5, 1), (25, 0)]],
    [[(10, 0), (30, 1), (50, 1), (70, 0)], [(15, 0), (35, 1), (45, 1), (65, 0)]],
    [[(50, 0), (70, 1), (90, 1)], [(55, 0), (75, 1), (90, 1)]]
], ['low', 'medium', 'high'], res=1.0)

sa = lv.LinguisticVariableT2('System Activity', 0, 90, [
    [[(0, 1), (10, 1), (30, 0)], [(0, 1), (5, 1), (25, 0)]],
    [[(10, 0), (30, 1), (50, 1), (70, 0)], [(15, 0), (35, 1), (45, 1), (65, 0)]],
    [[(50, 0), (70, 1), (90, 1)], [(55, 0), (75, 1), (90, 1)]]
], ['low', 'medium', 'high'], res=1.0)

si = lv.LinguisticVariableT2('Similarity', 0, 90, [
    [[(0, 0), (18, 1), (18, 1), (36, 0)], [(6, 0), (18, 1), (18, 1), (30, 0)]],
    [[(30, 0), (45, 1), (45, 1), (60, 0)], [(36, 0), (45, 1), (45, 1), (54, 0)]],
    [[(54, 0), (72, 1), (72, 1), (90, 0)], [(60, 0), (72, 1), (72, 1), (84, 0)]]
], ['low', 'medium', 'high'], res=1.0)

si.plot()
fh.plot()

ipc.plot()
sa.plot()

rules = []

rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "low"), (ipc, "low"), (sa, "low")], (si, 'low'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "low"), (ipc, "low"), (sa, "medium")], (si, 'low'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "low"), (ipc, "low"), (sa, "high")], (si, 'low'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "low"), (ipc, "medium"), (sa, "low")], (si, 'low'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "low"), (ipc, "medium"), (sa, "medium")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "low"), (ipc, "medium"), (sa, "high")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "low"), (ipc, "high"), (sa, "low")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "low"), (ipc, "high"), (sa, "medium")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "low"), (ipc, "high"), (sa, "high")], (si, 'high'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "medium"), (ipc, "low"), (sa, "low")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "medium"), (ipc, "low"), (sa, "medium")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "medium"), (ipc, "low"), (sa, "high")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "medium"), (ipc, "medium"), (sa, "low")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "medium"), (ipc, "medium"), (sa, "medium")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "medium"), (ipc, "medium"), (sa, "high")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "medium"), (ipc, "high"), (sa, "low")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "medium"), (ipc, "high"), (sa, "medium")], (si, 'high'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "medium"), (ipc, "high"), (sa, "high")], (si, 'high'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "high"), (ipc, "low"), (sa, "low")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "high"), (ipc, "low"), (sa, "medium")], (si, 'high'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "high"), (ipc, "low"), (sa, "high")], (si, 'high'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "high"), (ipc, "medium"), (sa, "low")], (si, 'high'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "high"), (ipc, "medium"), (sa, "medium")], (si, 'medium'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "high"), (ipc, "medium"), (sa, "high")], (si, 'high'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "high"), (ipc, "high"), (sa, "low")], (si, 'high'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "high"), (ipc, "high"), (sa, "medium")], (si, 'high'), 'MIN'))
rules.append(fr.Fuzzy_RuleT2("AND_min", [(fh, "high"), (ipc, "high"), (sa, "high")], (si, 'high'), 'MIN'))

value = {'File Hash': 12, 'IP Connection': 88, 'System Activity': 26}

testFIS = fis.FIS_T2(rules)

testFIS.compute_antecedent_activations(value)
testFIS.compute_consequent_activations()
testFIS.aggregate()

# testFIS.plot_rules()
# testFIS.plot_output()

# retourne le centre de l'intervalle de la centroide
print(testFIS.defuzzify())

# pl.show()