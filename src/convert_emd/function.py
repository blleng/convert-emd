import matplotlib.colors as mcolors
import numpy as np
from skimage import exposure
from rsciio.emd import file_reader

def get_data(file_name):
    return file_reader(file_name + ".emd")

def data_signal_type(frame):
    return frame["metadata"]["Signal"]["signal_type"]

def is_eds(data):
    return is_eds_spectrum(data[-1])

def is_eds_spectrum(frame):
    eds = True if data_signal_type(frame) in ["EDS_TEM", "EDS_SEM"] else False
    return eds

def eds_elements(data):
    element = []
    for i in range(len(data)):
        if data_signal_type(data[i]) == "":
            element.append(get_title(data[i]))
    return element

def get_scale(frame):
    return (frame["axes"][1]["scale"], frame["axes"][1]["units"])

def get_title(frame):
    return frame["metadata"]["General"]["title"]

def get_size(frame):
    return (frame["axes"][1]["size"], frame["axes"][0]["size"])

def create_cmp(color):
    return mcolors.LinearSegmentedColormap.from_list(
        "", [mcolors.to_rgba(color, 0), mcolors.to_rgba(color, 1)]
    )

def contrast_stretch(frame, stretch):
    low_constrain, high_constrain = np.percentile(frame["data"], (stretch[0], stretch[1]))
    return exposure.rescale_intensity(frame["data"], in_range=(low_constrain, high_constrain))