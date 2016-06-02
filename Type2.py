import linguistic_variable as lv
import matplotlib as pl
import fuzzy_rule_type2 as fr



temperature = lv.LinguisticVariableT2('temperature', 0, 35, [[[(0,1),(17,1),(20,0)],[(0,0.8),(15, 0.8),(17,0)]],[[(17,0),(20,1),(25,1), (27,0)],[(19,0),(21, 0.5),(25,0.5), (26, 0)]], [[(26,0),(28,1),(30,1)],[(27,0),(29, 0.8),(30,0.8)]]], ['cold', 'warm', 'hot'], res=1.0)
pressure = lv.LinguisticVariableT2('pressure', 0, 35, [[[(0,1),(17,1),(20,0)],[(0,0.8),(15, 0.8),(17,0)]],[[(17,0),(20,1),(25,1), (27,0)],[(19,0),(21, 0.5),(25,0.5), (26, 0)]], [[(26,0),(28,1),(30,1)],[(27,0),(29, 0.8),(30,0.8)]]], ['low', 'medium', 'high'], res=1.0)
release = lv.LinguisticVariableT2('release', 0, 35, [[[(0,1),(17,1),(20,0)],[(0,0.8),(15, 0.8),(17,0)]],[[(17,0),(20,1),(25,1), (27,0)],[(19,0),(21, 0.5),(25,0.5), (26, 0)]], [[(26,0),(28,1),(30,1)],[(27,0),(29, 0.8),(30,0.8)]]], ['low', 'medium', 'high'], res=1.0)



temperature.plot()
# pl.show()

rule = fr.Fuzzy_RuleT2("AND_min", [(temperature, "cold"), (pressure, "medium")] , (release, "low"), 'MIN')

# rule.compute_antecedent_activation()