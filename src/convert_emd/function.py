import matplotlib.colors as mcolors
import numpy as np
from skimage import exposure
from rsciio.emd._emd_velox import FeiEMDReader
import h5py as h5

def get_data(file_name):
    file = h5.File(file_name + ".emd","r")
    emd_reader = FeiEMDReader(
        lazy = False,
        select_type = None,
        first_frame = 0,
        last_frame = None,
        sum_frames = True,
        sum_EDS_detectors = True,
        rebin_energy = 1,
        SI_dtype = None,
        load_SI_image_stack = False,
    )
    emd_reader.read_file(file)
    data = emd_reader.dictionaries
    return data

def data_signal_type(frame):
    return frame["metadata"]["Signal"]["signal_type"]

def is_eds(data):
    return is_eds_spectrum(data[-1])

def is_eds_spectrum(frame):
    spectrum = True if data_signal_type(frame) in ["EDS_TEM", "EDS_SEM"] else False
    return spectrum

def eds_elements(data):
    element = []
    if is_eds(data):
        for i in range(len(data)):
            if data_signal_type(data[i]) == "":
                element.append(get_title(data[i]))
        if len(element) > 0: element.remove("HAADF")
    return element

def get_scale(frame):
    return (frame["axes"][-1]["scale"], frame["axes"][-1]["units"])

def get_title(frame):
    return frame["metadata"]["General"]["title"]

def get_size(frame):
    return (frame["axes"][-1]["size"], frame["axes"][-2]["size"])

def signal1d_data(frame):
    offset = frame["axes"][0]["offset"]
    scale = frame["axes"][0]["scale"]
    size = frame["axes"][0]["size"]
    x_data = np.arange(offset, scale*size+offset, scale)
    y_data = frame["data"]
    return np.asarray([x_data, y_data]).transpose()

def signal3d_to_1d_data(frame):
    offset = frame["axes"][2]["offset"]
    scale = frame["axes"][2]["scale"]
    size = frame["axes"][2]["size"]
    x_data = np.arange(offset, scale*size+offset, scale)
    y_data = frame["data"].sum(axis=(0, 1))
    return np.asarray([x_data, y_data]).transpose()

def series_images(frame):
    offset = frame["axes"][0]["offset"]
    scale = frame["axes"][0]["scale"]
    size = frame["axes"][0]["size"]
    return np.arange(offset, scale*size+offset, scale)

def write_signal1d(file, data):
    return np.savetxt(file, data, delimiter="\t")

def create_cmp(color):
    return mcolors.LinearSegmentedColormap.from_list(
        "", [mcolors.to_rgba(color, 0), mcolors.to_rgba(color, 1)]
    )

def default_colors():
    return list(mcolors.TABLEAU_COLORS.values())

def contrast_stretch(data, stretch):
    low_constrain, high_constrain = np.percentile(data, (stretch[0], stretch[1]))
    return exposure.rescale_intensity(data, in_range=(low_constrain, high_constrain))