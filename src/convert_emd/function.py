import matplotlib.colors as mcolors
import numpy as np
from skimage import exposure
from rsciio.emd._emd_velox import FeiEMDReader
import h5py as h5

element_table = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
                 "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
                 "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
                 "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
                 "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", 
                 "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
                 "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", 
                 "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", 
                 "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
                 "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", 
                 "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
                 "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]

def Get_data(file_name):
    file = h5.File(file_name,"r")
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

def Data_signal_type(frame):
    return frame["metadata"]["Signal"]["signal_type"]

def Is_eds(data):
    return Is_eds_spectrum(data[-1])

def Is_eds_spectrum(frame):
    spectrum = True if Data_signal_type(frame) in ["EDS_TEM", "EDS_SEM"] else False
    return spectrum

def Eds_elements(data):
    element = []
    if Is_eds(data):
        for i in range(len(data)):
            frame_title = Get_title(data[i])
            if frame_title in element_table: element.append(frame_title)
    return element

def Get_scale(frame):
    return (frame["axes"][-1]["scale"], frame["axes"][-1]["units"])

def Get_title(frame):
    return frame["metadata"]["General"]["title"]

def Get_size(frame):
    return (frame["axes"][-1]["size"], frame["axes"][-2]["size"])

def Signal1d_data(frame):
    offset = frame["axes"][0]["offset"]
    scale = frame["axes"][0]["scale"]
    size = frame["axes"][0]["size"]
    x_data = np.arange(offset, scale*size+offset, scale)
    y_data = frame["data"]
    return np.asarray([x_data, y_data]).transpose()

def Signal3d_to_1d_data(frame):
    offset = frame["axes"][2]["offset"]
    scale = frame["axes"][2]["scale"]
    size = frame["axes"][2]["size"]
    x_data = np.arange(offset, scale*size+offset, scale)
    y_data = frame["data"].sum(axis=(0, 1))
    return np.asarray([x_data, y_data]).transpose()

def Series_images(frame):
    offset = frame["axes"][0]["offset"]
    scale = frame["axes"][0]["scale"]
    size = frame["axes"][0]["size"]
    return np.arange(offset, scale*size+offset, scale)

def Write_signal1d(file, data):
    return np.savetxt(file, data, delimiter="\t")

def Create_cmp(color):
    return mcolors.LinearSegmentedColormap.from_list(
        "", [mcolors.to_rgba(color, 0), mcolors.to_rgba(color, 1)]
    )

def Default_colors():
    return list(mcolors.TABLEAU_COLORS.values())

def Contrast_stretch(data, stretch):
    low_constrain, high_constrain = np.percentile(data, (stretch[0], stretch[1]))
    return exposure.rescale_intensity(data, in_range=(low_constrain, high_constrain))
