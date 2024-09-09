import convert_emd.command as com
import convert_emd.function as emdfun
import convert_emd.drawing as draw

def main():
    args = com.parse().parse_args()

    file_name = args.file
    data = emdfun.get_data(file_name)
    output_type = "." + args.out

    if args.no_scale:
        scale_bar = False
    else: scale_bar = True

    sb_color = args.scale_color
    sb_x_start = args.scale[0]
    sb_y_start = args.scale[1]
    sb_width_factor = args.scale[2]

    stretch = args.contrast_stretching

    overlay_alpha = args.overlay_alpha
    sub_alpha = args.substrate_alpha
    eds_color = {}
    for i in range(int(len(args.eds)/2)):
        ele = i * 2
        ele_color = ele + 1
        eds_color[args.eds[ele]] = args.eds[ele_color]
    all_elements = emdfun.eds_elements(data)
    mapping_overlay = []
    if len(all_elements):
        mapping_overlay = args.overlay if len(args.overlay) else all_elements
        overlay = True
    else:
        overlay = False

    draw.convert_emd(file_name, data, output_type, scale_bar, sb_color, sb_x_start, sb_y_start, sb_width_factor, stretch, overlay_alpha, sub_alpha, eds_color, mapping_overlay, overlay)