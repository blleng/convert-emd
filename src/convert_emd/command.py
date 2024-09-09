import argparse

def parse():
    parser = argparse.ArgumentParser(description = "Convert .emd file generated by Velox  to images")

    parser.add_argument (
        "-f",
        "--file",
        type = str,
        metavar = "FILE",
        help = "Input *.emd(Velox) filename (without \".emd\" extension)",
        required=True
    )
    parser.add_argument (
        "-o",
        "--out",
        type = str,
        metavar = "TYPE",
        help = "Type of output images.",
        default = "png"
    )
    parser.add_argument (
        "-ns",
        "--no_scale",
        help = "Do not draw scale bar",
        action = "store_true"
    )
    parser.add_argument (
        "-sc",
        "--scale_color",
        type = str,
        metavar = "COLOR",
        help = "Color of scale bar",
        default = "#ffffff"
    )
    parser.add_argument (
        "-s",
        "--scale",
        type = float,
        nargs = 3,
        metavar = "FLOAT",
        help = "The position and width of scale bar (X_POSITION Y_POSITION WIDTH_FACTOR), the width is set as image-height/WIDTH_FACTOR",
        default = [0.75, 0.9167, 150.0]
    )
    parser.add_argument (
        "-e",
        "--eds",
        type = str,
        nargs = "+",
        metavar = "Str",
        help = "The color of elemental mappings (default: gray)",
        default = []
    )
    parser.add_argument (
        "-oe",
        "--overlay",
        type = str,
        nargs = "+",
        metavar = "ELEMENT",
        help = "The elements for overlayed mapping",
        default = []
    )
    parser.add_argument (
        "-oa",
        "--overlay_alpha",
        type = float,
        metavar = "ALPHA",
        help = "Transparency of the overlayed elemental mapping (a value between 0 and 1, 0 means totally transparent)",
        default = "1.0"
    )
    parser.add_argument (
        "-sa",
        "--substrate_alpha",
        type = float,
        metavar = "ALPHA",
        help = "Transparency of the HAADF substrate picture in elemental mapping (a value between 0 and 1, 0 means totally transparent)",
        default = "0.5"
    )
    parser.add_argument (
        "-c",
        "--contrast_stretching",
        type = float,
        nargs = 2,
        metavar = "CONTRAST",
        help = "The parameter for contrast streaching, where the image is rescaled to include all intensities that fall within the given percentiles",
        default = [1, 99]
    )