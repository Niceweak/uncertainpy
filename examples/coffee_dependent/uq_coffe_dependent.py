import uncertainpy as un

from coffee_cup_dependent_class import CoffeeCupDependent
from coffee_cup_dependent_function import coffe_cup_dependent

parameterlist = [["kappa", -0.05, None],
                 ["u_env", 20, None],
                 ["alpha", 1, None]]

parameters = un.Parameters(parameterlist)
parameters.set_all_distributions(un.Distribution(0.5).uniform)


# model = CoffeeCupDependent()
model = coffe_cup_dependent

uncertainty = un.UncertaintyEstimation(model=model,
                                       parameters=parameters,
                                       features=None)

uncertainty.uncertainty_quantification(plot_condensed=False, rosenblatt=True)