from handwriting_features.features import HandwritingFeatures
from .visualization_tools import *
from .Configs import *


class SimplePlots:

    def __init__(self, input_data, custom_config):
        self.input_data = input_data
        self.custom_config = custom_config

    def _control_input_data(self):
        """TODO: Check if input is Handwriting Features or numpy array and prepare the input data accordingly"""
        self.is_handwriting_features_obj = True if isinstance(self.input_data, HandwritingFeatures) else False

    def plot_x_y(self):
        return vizualize(ConfigsPlotXY(x=self.input_data["x"], y=self.input_data["y"], custom_config=self.custom_config).get_config()).values()



