import convert_emd.command as com
import convert_emd.function as emdfun
from convert_emd.core import EmdConverter
from convert_emd.config import ConvertConfig

def main():
    args = com.get_parser().parse_args()

    file_name = args.filename
    data = emdfun.get_data(file_name)
    output_type = "." + args.out
    
    scale_bar = not args.no_scale
    sb_color = args.scale_color
    sb_x_start, sb_y_start, sb_width_factor = args.scale
    stretch = args.contrast_stretching
    overlay_alpha = args.overlay_alpha
    sub_alpha = args.substrate_alpha

    eds_colors = {}
    for i in range(len(args.eds) // 2):
        ele = i * 2
        ecolor = ele + 1
        eds_colors[args.eds[ele]] = args.eds[ecolor]
        
    all_elements = emdfun.eds_elements(data)
    mapping_overlay = []
    overlay = False
    
    if len(all_elements) > 0:
        mapping_overlay = args.overlay if len(args.overlay) > 0 else all_elements
        overlay = True

    config = ConvertConfig(
        output_type=output_type,
        scale_bar=scale_bar,
        sb_color=sb_color,
        sb_x_start=sb_x_start,
        sb_y_start=sb_y_start,
        sb_width_factor=sb_width_factor,
        stretch=tuple(stretch),
        overlay_alpha=overlay_alpha,
        sub_alpha=sub_alpha,
        eds_colors=eds_colors,
        mapping_overlay=mapping_overlay,
        overlay=overlay
    )

    converter = EmdConverter(file_name, data, config)
    converter.convert()

if __name__ == "__main__":
    main()