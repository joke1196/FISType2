import linguistic_variable as lv
import matplotlib.pyplot as pl
import FIST2 as fis
import fuzzy_rule_type2 as fr



temperature = lv.LinguisticVariableT2('temperature', 0, 35, [[[(0,1),(17,1),(20,0)],[(0,0.8),(15, 0.8),(17,0)]],[[(17,0),(20,1),(25,1), (27,0)],[(19,0),(21, 0.5),(25,0.5), (26, 0)]], [[(26,0),(28,1),(30,1)],[(27,0),(29, 0.8),(30,0.8)]]], ['cold', 'warm', 'hot'], res=1.0)
pressure = lv.LinguisticVariableT2('pressure', 0, 35, [[[(0,1),(17,1),(20,0)],[(0,0.8),(15, 0.8),(17,0)]],[[(17,0),(20,1),(25,1), (27,0)],[(19,0),(21, 0.5),(25,0.5), (26, 0)]], [[(26,0),(28,1),(30,1)],[(27,0),(29, 0.8),(30,0.8)]]], ['low', 'medium', 'high'], res=1.0)
release = lv.LinguisticVariableT2('release', 0, 35, [[[(0,1),(17,1),(20,0)],[(0,0.8),(15, 0.8),(17,0)]],[[(17,0),(20,1),(25,1), (27,0)],[(19,0),(21, 0.5),(25,0.5), (26, 0)]], [[(26,0),(28,1),(30,1)],[(27,0),(29, 0.8),(30,0.8)]]], ['low', 'medium', 'high'], res=1.0)



temperature.plot()


rule = fr.Fuzzy_RuleT2("AND_min", [(temperature, "cold"), (pressure, "medium")] , (release, "low"), 'MIN')
rule2 = fr.Fuzzy_RuleT2("AND_min", [(pressure, "high")] , (release, "high"), 'MIN')
rule3 = fr.Fuzzy_RuleT2("AND_min", [(temperature, "hot"), (pressure, "low")] , (release, "medium"), 'MIN')

value = {'temperature': 19.5, 'pressure': 5}

testFIS = fis.FIS_T2([rule, rule2, rule3])

testFIS.compute_antecedent_activations(value)
testFIS.compute_consequent_activations()

testFIS.plot_rules()

pl.show()