import time
import os

import matplotlib.pyplot as plt
import multiprocessing as mp

from uncertainpy import UncertaintyEstimation, Distribution, prettyPlot, prettyBar

class UncertaintyEstimations():
    def __init__(self, model,
                 feature_list=[],
                 features=None,
                 save_figures=False,
                 output_dir_figures="figures/",
                 figureformat=".png",
                 save_data=True,
                 output_dir_data="data/",
                 supress_model_graphics=True,
                 supress_model_output=True,
                 CPUs=mp.cpu_count(),
                 interpolate_union=False,
                 rosenblatt=False,
                 nr_mc_samples=10**2,
                 **kwargs):
        """
        Options can also be sent to the feature
        kwargs:
        feature_options = {keyword1: value1, keyword2: value2}
        """

        # Figures are always saved on the format:
        # output_dir_figures/distribution_interval/parameter_value-that-is-plotted.figure-format

        self.uncertainty_estimations = {}

        # original_parameters, uncertain_parameters, distributions,

        self.model = model

        self.save_figures = save_figures
        self.output_dir_figures = output_dir_figures
        self.save_data = save_data
        self.output_dir_data = output_dir_data

        self.supress_model_graphics = supress_model_graphics
        self.supress_model_output = supress_model_output
        self.CPUs = CPUs
        self.interpolate_union = interpolate_union
        self.rosenblatt = rosenblatt
        self.figureformat = figureformat
        self.features = features
        self.feature_list = feature_list
        self.nr_mc_samples = nr_mc_samples

        self.kwargs = kwargs

        self.t_start = time.time()

        if not os.path.isdir(output_dir_data):
            os.makedirs(output_dir_data)


    def exploreParameters(self, distributions):
        for distribution_function in distributions:
            for interval in distributions[distribution_function]:
                current_output_dir_figures = os.path.join(self.output_dir_figures,
                                                          distribution_function + "_%g" % interval)
                distribution = getattr(Distribution(interval), distribution_function)

                self.model.setAllDistributions(distribution)

                name = distribution_function + "_" + str(interval)
                print "Running for: " + distribution_function + " " + str(interval)

                tmp_output_dir_data = \
                    os.path.join(self.output_dir_data,
                                 distribution_function + "_%g" % interval)

                self.uncertainty_estimations[name] =\
                    UncertaintyEstimation(self.model,
                                          feature_list=self.feature_list,
                                          features=self.features,
                                          save_figures=self.save_figures,
                                          output_dir_figures=current_output_dir_figures,
                                          figureformat=self.figureformat,
                                          save_data=self.save_data,
                                          output_dir_data=tmp_output_dir_data,
                                          output_data_filename=self.model.__class__.__name__,
                                          supress_model_graphics=self.supress_model_graphics,
                                          supress_model_output=self.supress_model_output,
                                          CPUs=self.CPUs,
                                          interpolate_union=self.interpolate_union,
                                          rosenblatt=self.rosenblatt,
                                          nr_mc_samples=self.nr_mc_samples,
                                          **self.kwargs)

                self.uncertainty_estimations[name].singleParameters()
                self.uncertainty_estimations[name].allParameters()



    def compareMC(self, nr_mc_samples):
        run_times = []

        name = "pc"
        output_dir_figures = os.path.join(self.output_dir_figures, name)
        output_dir_data = os.path.join(self.output_dir_data, name)

        self.uncertainty_estimations_pc =\
            UncertaintyEstimation(self.model,
                                  feature_list=self.feature_list,
                                  features=self.features,
                                  save_figures=self.save_figures,
                                  output_dir_figures=output_dir_figures,
                                  figureformat=self.figureformat,
                                  save_data=self.save_data,
                                  output_dir_data=output_dir_data,
                                  output_data_filename=self.model.__class__.__name__,
                                  supress_model_graphics=self.supress_model_graphics,
                                  supress_model_output=self.supress_model_output,
                                  CPUs=self.CPUs,
                                  interpolate_union=self.interpolate_union,
                                  rosenblatt=self.rosenblatt,
                                  **self.kwargs)

        time_1 = time.time()
        self.uncertainty_estimations_pc.allParameters()
        run_times.append(time.time() - time_1)


        for nr_mc_sample in nr_mc_samples:
            print "Running for: " + str(nr_mc_sample)


            name = "mc-_" + str(nr_mc_sample)
            current_output_dir_figures = os.path.join(self.output_dir_figures, name)
            tmp_output_dir_data = os.path.join(self.output_dir_data, name)

            self.uncertainty_estimations[nr_mc_sample] =\
                UncertaintyEstimation(self.model,
                                      feature_list=self.feature_list,
                                      features=self.features,
                                      save_figures=self.save_figures,
                                      output_dir_figures=current_output_dir_figures,
                                      figureformat=self.figureformat,
                                      save_data=self.save_data,
                                      output_dir_data=tmp_output_dir_data,
                                      output_data_filename=self.model.__class__.__name__,
                                      supress_model_graphics=self.supress_model_graphics,
                                      supress_model_output=self.supress_model_output,
                                      CPUs=self.CPUs,
                                      interpolate_union=self.interpolate_union,
                                      rosenblatt=self.rosenblatt,
                                      nr_mc_samples=nr_mc_sample,
                                      **self.kwargs)

            time_1 = time.time()
            self.uncertainty_estimations[nr_mc_sample].allParametersMC()
            run_times.append(time.time() - time_1)


        output_dir_compare = os.path.join(self.output_dir_figures, "MC-compare")
        if not os.path.isdir(output_dir_compare):
            os.makedirs(output_dir_compare)




        for feature in self.uncertainty_estimations_pc.features_2d:
            new_figure = True
            color = 0
            max_var = 0
            min_var = 0
            legend = []
            for mc_estimation in sorted(self.uncertainty_estimations):
                mc = self.uncertainty_estimations[mc_estimation]
                difference_var = mc.Var[feature]/self.uncertainty_estimations_pc.Var[feature]

                if difference_var.max() > max_var:
                    max_var = difference_var.max()

                if difference_var.min() < min_var:
                    min_var = difference_var.min()

                legend.append("MC samples " + str(mc.nr_mc_samples))

                prettyPlot(mc.t[feature], difference_var,
                           new_figure=new_figure, color=color,
                           xlabel="Time", ylabel="Variance, mv",
                           title="MC variance/PC variance(%d), %s" % (self.uncertainty_estimations_pc.nr_pc_samples, feature))
                new_figure = False
                color += 2

            plt.ylim([min_var, max_var])
            plt.legend(legend)
            plt.savefig(os.path.join(output_dir_compare,
                                     "variance-diff-MC-PC_" + feature + self.figureformat))
            # plt.show()
            plt.close()

        for feature in self.uncertainty_estimations_pc.features_1d:
            difference_var = []
            legend = []
            for mc_estimation in sorted(self.uncertainty_estimations):
                mc = self.uncertainty_estimations[mc_estimation]
                difference_var.append(mc.Var[feature]/float(self.uncertainty_estimations_pc.Var[feature]))

                legend.append("MC " + str(mc.nr_mc_samples))

                new_figure = False
                color += 2

            prettyBar(difference_var,
                      xlabels=legend, ylabel="Variance, mv",
                      title="MC variance/PC variance, " + feature)
            plt.savefig(os.path.join(output_dir_compare,
                                     "variance-diff-MC-PC_" + feature + self.figureformat))
            plt.close()








        return run_times



    def timePassed(self):
        return time.time() - self.t_start