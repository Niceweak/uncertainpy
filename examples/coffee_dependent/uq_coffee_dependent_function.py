import uncertainpy as un
import chaospy as cp
import numpy as np

from coffee_cup_dependent_function import coffee_cup_dependent

# Create the distributions
T_env_dist = cp.Uniform(15, 25)
alpha_dist = cp.Uniform(0.5, 1.5)
kappa_hat_dist = cp.Uniform(-0.075, -0.025)/alpha_dist

# Define a parameter list and use it to create the Parameters
parameter_list = [["alpha", None, alpha_dist],
                  ["kappa_hat", None, kappa_hat_dist],
                  ["T_env", None, T_env_dist]]
parameters = un.Parameters(parameter_list)

model = un.Model(coffee_cup_dependent, labels=["time [s]", "Temperature [C]"])


# Perform the uncertainty quantification using the rosenblatt transformation
UQ = un.UncertaintyQuantification(model=model,
                                  parameters=parameters)

UQ.quantify(rosenblatt=True,
            output_dir_figures="figures_coffee_dependent",
            filename="coffee_dependent")

# # C = [[.0001, 0, 0.0005],
# #      [0, 5, 0],
# #      [0.0005, 0, .01]]
# # mu = [-0.05, 20, 1]
# # dist = cp.MvNormal(mu, C)
# C = [[.001, 0, 0.0005],
#      [0, 1, 0],
#      [0.0005, 0, .001]]
# mu = [-0.22, 20, 0.22]
# dist = cp.MvNormal(mu, C)

# UQ.parameters.distribution = dist
# UQ.quantify(rosenblatt=True,
#                                        output_dir_figures="figures_coffee_dependent_small_correlation",
#                                        filename="coffee_dependent_small_correlation")



# C = [[.001, 0, 0.0009],
#      [0, 1, 0],
#      [0.0009, 0, .001]]
# mu = [-0.22, 20, 0.22]
# dist = cp.MvNormal(mu, C)

# UQ.parameters.distribution = dist
# UQ.quantify(rosenblatt=True,
#                                        output_dir_figures="figures_coffee_dependent_medium_correlation",
#                                        filename="coffee_dependent_medium_correlation")


# # C = [[.0001, 0, 0.00099999],
# #      [0, 5, 0],
# #      [0.00099999, 0, .01]]
# # mu = [-0.05, 20, 1]
# # dist = cp.MvNormal(mu, C)

# # C = [[.001, 0, 0.00099999],
# #      [0, 1, 0],
# #      [0.00099999, 0, .001]]
# # mu = [-0.22, 20, 0.22]
# # dist = cp.MvNormal(mu, C)

# C = [[.001, 0, 0.00099],
#      [0, 1, 0],
#      [0.00099, 0, .001]]
# mu = [-0.22, 20, 0.22]
# dist = cp.MvNormal(mu, C)

# UQ.parameters.distribution = dist
# UQ.quantify(rosenblatt=True,
#                                        output_dir_figures="figures_coffee_dependent_large_correlation",
#                                        filename="coffee_dependent_large_correlation")


# # C = [[.0001, 0, -0.00099999],
# #      [0, 5, 0],
# #      [-0.00099999, 0, .01]]
# # mu = [-0.05, 20, 1]
# # dist = cp.MvNormal(mu, C)

# C = [[.001, 0, -0.0009],
#      [0, 1, 0],
#      [-0.0009, 0, .001]]
# mu = [-0.22, 20, 0.22]
# dist = cp.MvNormal(mu, C)

# UQ.parameters.distribution = dist
# UQ.quantify(rosenblatt=True,
#                                        output_dir_figures="figures_coffee_dependent_large_reverse_correlation",
#                                        filename="coffee_dependent_large_reverse_correlation")

# T_env_dist = cp.Uniform(18, 22)
# alpha_dist = cp.Uniform(0.9, 1.1)
# beta_dist = cp.Uniform(-0.075, -0.025)

# percentage = 0.1
# beta_dist = un.uniform(percentage)(-0.22)
# alpha_dist = un.uniform(percentage)(0.22)
# T_env_dist = un.uniform(percentage)(20)

# parameter_list = [["kappa", -0.05, beta_dist],
#                  ["u_env", 20, T_env_dist],
#                  ["a", 1, alpha_dist]]

# parameters = un.Parameters(parameter_list)

# UQ.parameters = parameters
# UQ.quantify(rosenblatt=True,
#                                        output_dir_figures="figures_coffee_dependent_no_correlation_rosenblatt",
#                                        filename="coffee_dependent_no_correlation_rosenblatt")

# UQ.quantify(rosenblatt=False,
#                                        output_dir_figures="figures_coffee_dependent_no_correlation",
#                                        filename="coffee_dependent_no_correlation")

# parameter_list = [["a", 1, None],
#                  ["u_env", 20, None],
#                  ["kappa", -0.05, None]]

# # C = [[.01, 0, 0.0005],
# #      [0, 5, 0],
# #      [0.0005, 0, .0001]]
# # mu = [1, 20, -0.05]
# # dist = cp.MvNormal(mu, C)

# C = [[.001, 0, 0.0005],
#      [0, 1, 0],
#      [0.0005, 0, .001]]
# mu = [-0.22, 20, 0.22]
# dist = cp.MvNormal(mu, C)

# parameters = un.Parameters(parameter_list)
# parameters.distribution = dist

# UQ.parameters = parameters


# UQ.quantify(rosenblatt=True,
#                                        output_dir_figures="figures_coffee_dependent_reverse_order",
#                                        filename="coffee_dependent_reverse_order")


# parameter_list = [["T_env", 20, None],
#                  ["alpha", 1, None],
#                  ["beta", -0.05, None]]

# # C = [[.01, 0, 0.0005],
# #      [0, 5, 0],
# #      [0.0005, 0, .0001]]
# # mu = [1, 20, -0.05]
# # dist = cp.MvNormal(mu, C)

# C = [[1, 0, 0],
#      [0, .001, .00099],
#      [0, .00099, .001]]
# mu = [20, -0.22, 0.22]
# dist = cp.MvNormal(mu, C)

# # C = [[1, 0, 0],
# #      [0, 0.01, 0.0009],
# #      [0, 0.0009, .0001]]
# # mu = [20, 1, -0.05]
# # dist = cp.MvNormal(mu, C)

# parameters = un.Parameters(parameter_list)
# parameters.distribution = dist

# # UQ.parameters = parameters
# UQ = un.UncertaintyQuantification(model=model,
#                                        parameters=parameters,
#                                        seed=10)


# UQ.quantify(rosenblatt=True,
#                                        output_dir_figures="figures_coffee_dependent_reverse_order_2",
#                                        filename="coffee_dependent_reverse_order_2",
#                                        sensitivity="sensitivity_t")


# parameter_list = [["T_env", 20, None],
#                  ["beta", -0.05, None],
#                  ["alpha", 1, None]]

# C = [[1, 0, 0],
#      [0, .001, .00099],
#      [0, .00099, .001]]
# mu = [20, 0.22, -0.22]
# dist = cp.MvNormal(mu, C)

# # C = [[1, 0, 0],
# #      [0, .0001, 0.0009],
# #      [0, 0.0009, .01]]
# # mu = [20, -0.05, 1]
# # dist = cp.MvNormal(mu, C)


# parameters = un.Parameters(parameter_list)
# parameters.distribution = dist

# # UQ.parameters = parameters
# UQ = un.UncertaintyQuantification(model=model,
#                                        parameters=parameters,
#                                        seed=10)

# UQ.quantify(rosenblatt=True,
#                                        output_dir_figures="figures_coffee_dependent_reverse_order_3",
#                                        filename="coffee_dependent_reverse_order_3",
#                                        sensitivity="sensitivity_t")