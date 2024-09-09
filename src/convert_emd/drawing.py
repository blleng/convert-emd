import os
import matplotlib.pyplot as plt
import convert_emd.function as emdfun

def draw_scale_bar(frame, size_x, size_y, sb_x_start, sb_y_start, width_factor, sb_color):
    sb_lst = [0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000,2000,5000]
    scale, unit = emdfun.get_scale(frame)
    sb_len_float = size_x * scale / 6
    sb_len = sorted(sb_lst, key=lambda a: abs(a - sb_len_float))[0]
    sb_len_px = sb_len / scale
    sb_start_x, sb_start_y, sb_width = (size_x * sb_x_start , size_y * sb_y_start, size_y / width_factor)
    return [plt.Rectangle((sb_start_x, sb_start_y), sb_len_px, sb_width, color=sb_color, fill=True), "_" + str(sb_len) + unit]

def convert_emd(file_name, data, output_type, scale_bar, sb_color, sb_x_start, sb_y_start, sb_width_factor, stretch, overlay_alpha, sub_alpha, eds_color, mapping_overlay, overlay):
    output_dir = file_name + "/"
    output_name = output_dir + file_name + "_"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    mapping_frame = []
    ele = 0
    default_colors = emdfun.default_colors()

    for i in range(len(data)):
        frame = data[i]
        dim = frame["data"].ndim
        title = emdfun.get_title(frame)

        if dim == 2:
            frame["data"] = emdfun.contrast_stretch(frame, stretch)
            cmp = "gray"
            if overlay and not emdfun.is_eds_spectrum(frame):
                if title in mapping_overlay: mapping_frame.append(i)
                if title in eds_color:
                    cmp = emdfun.create_cmp(eds_color[title])
                elif title == "HAADF":
                    mapping_frame.append(i)
                    HAADF_frame_num = len(mapping_frame) - 1
                else:
                    cmp = emdfun.create_cmp(default_colors[ele])
                    ele += 1
                    if ele > 9: ele = 0

            size_x, size_y = (frame["axes"][1]["size"], frame["axes"][0]["size"])
            plt.figure(figsize=(size_x/100, size_y/100), facecolor="black")
            ax = plt.gca()
            plt.imshow(frame["data"], cmap=cmp)

            if scale_bar == True:
                bar = draw_scale_bar(frame, size_x, size_y, sb_x_start, sb_y_start, sb_width_factor, sb_color)
                ax.add_patch(bar[0])
                sb_text = bar[1]
            
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.margins = (0, 0)
            plt.axis("off")
            if scale_bar == True:
                plt.savefig(output_name + title + "_" + str(i) + sb_text + output_type)
            else:
                plt.savefig(output_name + title + "_" + str(i) + output_type)
            plt.close()

    if overlay:
        element = ""
        HAADF_frame = data[mapping_frame[HAADF_frame_num]]
        size_x, size_y = (HAADF_frame["axes"][1]["size"], HAADF_frame["axes"][0]["size"])

        plt.figure(figsize=(size_x/100, size_y/100), facecolor="black")
        ax = plt.gca()
        plt.imshow(HAADF_frame["data"], cmap="gray", alpha=sub_alpha)
        for i in range(len(mapping_frame)):
            if i == HAADF_frame_num:
                continue
            title = emdfun.get_title(data[mapping_frame[i]])
            plt.imshow(data[mapping_frame[i]]["data"], cmap = emdfun.create_cmp(eds_color[title]), alpha = overlay_alpha)
            element = element + "_" + title

        if scale_bar == True:
            bar = draw_scale_bar(HAADF_frame, size_x, size_y, sb_x_start, sb_y_start, sb_width_factor, sb_color)
            ax.add_patch(bar[0])
            sb_text = bar[1]

        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins = (0, 0)
        plt.axis("off")
        if scale_bar == True:
            plt.savefig(output_name + "Overlay" + element + sb_text + output_type)
        else:
            plt.savefig(output_name + "Overlay" + element + output_type)
        plt.close()