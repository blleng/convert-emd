# Convert-EMD

This script converts 2D signal in .emd files into images.

This project is based on [RosettaSciIO](https://github.com/hyperspy/rosettasciio) and [emd-converter](https://github.com/matao1984/emd-converter)

## Environment Requirenments

`Python >= 3.8`

### Dependencies

With conda:

```bash
conda install -c conda-forge rosettasciio
```

With pip:

```bash
pip install rosettasciio[all]
```

## Usage

```bash
cemd.py [-h] -f FILE [-o TYPE] [-ns] [-sc COLOR] [-s FLOAT FLOAT FLOAT] [-e Str [Str ...]] [-oe ELEMENT [ELEMENT ...]] [-oa ALPHA] [-sa ALPHA] [-c CONTRAST] [-i INT INT]
```

### Basic Usage

```bash
cemd.py -f INPUT_FILE
```

Run `cemd.py -h` for more information.

NOTICE: ".emd" extension should not be included into input filename. For example, if you want to convert "EXEAMPLE.emd", the input should be `cemd.py -f EXAMPLE` rather than `cemd.py -f EXAMPLE.emd`

### Output Type

The `-o`/`--out` option allows users to choose the output image type (default: png).

```bash
cemd.py -f INPUT_FILE -o png ## For PNG type
cemd.py -f INPUT_FILE -o tif ## For TIF type
...
```

### Scale Bar

#### Remove Scale Bar

The `-ns`/`--no_scale` option can be used to remove the scale bar in images.

```bash
cemd.py -f INPUT_FILE -ns ## No scale bar will be shown
```

#### Color of Scale Bar

The `-sc`/`--scale_color` option can be used to choose the color of the scale bar (default: white).

```bash
cemd.py -f INPUT_FILE -sc black ## Black scale bar
cemd.py -f INPUT_FILE -sc "#000000" ## Hex code can also be used
```

#### Position and Width of Scale Bar

The `-s`/`--scale` option can be used to adjust the postion and width of scale bar (default: x: 0.75, y: 0.9167, width-factor: 150)

```bash
cemd.py -f INPUT_FILE -s X Y WIDTH
```

NOTICE: Three arguments are required to specify the position and width of scale bar.

`X` and `Y` should be in `float` type and between 0 and 1. They decide the position of scale bar at (X, Y).

`WIDTH` should be a number more than 1. The width of scale bar is given by this factor as `h/f` (where `h` is the height of the image, `f` is the given WIDTH factor).

### Elemental Mapping

#### Color of Elements

The `-e`/`--eds` option allow users to specify the color of elemental mappings (default: gray).

```bash
cemd.py -f INPUT_FILE -e ELEMENT_1 COLOR_1 ELEMENT_2 COLOR_2 ELEMENT_3 COLOR_3 ...
```

#### Overlayed Mapping

The `-oe`/`--overlay` option decides which elements are overlyed.

```bash
cemd.py -f INPUT_FILE -oe ELEMENT_1 ElEMENT_2 ...
```

NOTICE: The colors in the overlayed mapping are corresponding to the color specified by the `-e` option.

Moreover, `-oa`/`--overlay_alpha` and `-sa`/`--substrate_alpha` options are provided to adjust the transparency of elemental layers (default: 1.0) and the HAADF layer (default: 0.5) respectively. The argument should be a float number between 0 and 1, 0 means totally transparent.

### Contrast (Histogram Equalization)

To improve the contrast (especially for HR-TEM), the `-c`/`--contrast` option is provided to introduce the *scikit-image* [histogram equalization](https://scikit-image.org/docs/stable/auto_examples/color_exposure/plot_equalize.html) method with *contrast streching*.

With this method, the image is rescaled to include all intensities that fall within the given percentiles (default: min = 1, max = 99).

```bash
cemd.py -f INPUT_FILE -c MIN MAX
```
The following example shows how this method helps when the picture contains noises with too high intensity:

|Without Treatment|After Treatment|
|-----------------|---------------|
|![without-treatment](example-images/withou-treatment.png)|![treated-picture](example-images/treated-pic.png)|