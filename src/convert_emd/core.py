import os
import re
import matplotlib.pyplot as plt
import convert_emd.function as emdfun
from convert_emd.config import ConvertConfig

class EmdConverter:
    def __init__(self, file_name: str, data, config: ConvertConfig):
        self.file_name = file_name
        self.data = data
        self.config = config
        self.output_dir = file_name + "_out/"
        
        self.mapping_frame = []
        self.HAADF_frame_num = -1
        self.ele_idx = 0
        self.default_colors = emdfun.default_colors()

    def convert(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        for i in range(len(self.data)):
            frame = self.data[i]
            dim = frame["data"].ndim
            title = emdfun.get_title(frame)
            title_attr = str(i) + "_"

            if dim == 1:
                self._process_1d(frame, title, title_attr)
            elif dim == 2:
                self._process_2d(i, frame, title, title_attr)
            elif dim == 3:
                self._process_3d(frame, title, title_attr)

        if self.config.overlay:
            self._process_overlay()

    def _process_1d(self, frame, title, title_attr):
        save_file = open(self.output_dir + title_attr + title + ".txt", "w", encoding="utf-8")
        save_file.write(frame["axes"][0]["name"] + "(" + frame["axes"][0]["units"] + ")" + "\t" + "Intensity(a.u.)" + "\n")
        signal_data = emdfun.signal1d_data(frame)
        emdfun.write_signal1d(save_file, signal_data)
        save_file.close()

    def _process_2d(self, index, frame, title, title_attr):
        cmp = "gray"
        if self.config.overlay:
            if title in self.config.mapping_overlay:
                self.mapping_frame.append(index)
            if title in self.config.eds_colors:
                cmp = emdfun.create_cmp(self.config.eds_colors[title])
            elif title == "HAADF":
                self.mapping_frame.append(index)
                self.HAADF_frame_num = len(self.mapping_frame) - 1
            else:
                cmp = emdfun.create_cmp(self.default_colors[self.ele_idx])
                self.config.eds_colors[title] = self.default_colors[self.ele_idx]
                self.ele_idx += 1
                if self.ele_idx > 9:
                    self.ele_idx = 0

        is_complex = True if frame["data"].dtype == "complex64" else False
        if is_complex:
            idata = [frame["data"].real, frame["data"].imag]
            if not os.path.exists(self.output_dir + title_attr + title + "/"):
                os.makedirs(self.output_dir + title_attr + title + "/")
        else:
            idata = [frame["data"]]

        for j in range(len(idata)):
            if not is_complex:
                idata[j] = emdfun.contrast_stretch(idata[j], self.config.stretch)
            size_x, size_y = emdfun.get_size(frame)
            plt.figure(figsize=(size_x/100, size_y/100), facecolor="black")
            ax = plt.gca()
            plt.imshow(idata[j], cmap=cmp)

            sb_text = ""
            if self.config.scale_bar:
                bar = self._draw_scale_bar(frame, size_x, size_y)
                ax.add_patch(bar[0])
                sb_text = bar[1]

            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.margins(0, 0)
            plt.axis("off")
            plt.savefig(self.output_dir + title_attr + title + str(j) + sb_text + self.config.output_type)
            plt.close()

    def _process_3d(self, frame, title, title_attr):
        if emdfun.is_eds_spectrum(frame):
            save_file = open(self.output_dir + title_attr + title + ".txt", "w", encoding="utf-8")
            save_file.write(frame["axes"][2]["name"] + "(" + frame["axes"][2]["units"] + ")" + "\t" + "Intensity(a.u.)" + "\n")
            signal_data = emdfun.signal3d_to_1d_data(frame)
            emdfun.write_signal1d(save_file, signal_data)
            save_file.close()
        else:
            cmp = "gray"
            size_x, size_y = emdfun.get_size(frame)
            split_frame = emdfun.series_images(frame)
            split_unit = frame["axes"][0]["units"]
            for i in range(frame["axes"][0]["size"]):
                frame["data"][i] = emdfun.contrast_stretch(frame["data"][i], self.config.stretch)
                plt.figure(figsize=(size_x/100, size_y/100), facecolor="black")
                ax = plt.gca()
                plt.imshow(frame["data"][i], cmap=cmp)

                sb_text = ""
                if self.config.scale_bar:
                    bar = self._draw_scale_bar(frame, size_x, size_y)
                    ax.add_patch(bar[0])
                    sb_text = bar[1]

                plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
                plt.margins(0, 0)
                plt.axis("off")
                plt.savefig(self.output_dir + title_attr + title + str(split_frame[i])[:6] + split_unit + sb_text + self.config.output_type)
                plt.close()

    def _process_overlay(self):
        element = ""
        # Check if HAADF frame exists, if not, skip overlay
        if self.HAADF_frame_num == -1:
            return

        HAADF_frame = self.data[self.mapping_frame[self.HAADF_frame_num]]
        size_x, size_y = (HAADF_frame["axes"][1]["size"], HAADF_frame["axes"][0]["size"])

        plt.figure(figsize=(size_x/100, size_y/100), facecolor="black")
        ax = plt.gca()
        HAADF_frame["data"] = emdfun.contrast_stretch(HAADF_frame["data"], self.config.stretch)
        plt.imshow(HAADF_frame["data"], cmap="gray", alpha=self.config.sub_alpha)
        for i in range(len(self.mapping_frame)):
            if i == self.HAADF_frame_num:
                continue
            title = emdfun.get_title(self.data[self.mapping_frame[i]])
            self.data[self.mapping_frame[i]]["data"] = emdfun.contrast_stretch(self.data[self.mapping_frame[i]]["data"], self.config.stretch)
            plt.imshow(self.data[self.mapping_frame[i]]["data"], cmap=emdfun.create_cmp(self.config.eds_colors[title]), alpha=self.config.overlay_alpha)
            element = element + "_" + title

        sb_text = ""
        if self.config.scale_bar:
            bar = self._draw_scale_bar(HAADF_frame, size_x, size_y)
            ax.add_patch(bar[0])
            sb_text = bar[1]

        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        plt.axis("off")
        plt.savefig(self.output_dir + "Overlay" + element + sb_text + self.config.output_type)
        plt.close()

    def _draw_scale_bar(self, frame, size_x, size_y):
        sb_lst = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        scale, unit = emdfun.get_scale(frame)
        if " / " in unit: unit = re.sub(r" / ", "_", unit)
        sb_len_float = size_x * scale / 6
        sb_len = sorted(sb_lst, key=lambda a: abs(a - sb_len_float))[0]
        sb_len_px = sb_len / scale
        sb_start_x, sb_start_y, sb_width = (size_x * self.config.sb_x_start, size_y * self.config.sb_y_start, size_y / self.config.sb_width_factor)
        return [plt.Rectangle((sb_start_x, sb_start_y), sb_len_px, sb_width, color=self.config.sb_color, fill=True), "_" + str(sb_len) + "(" + unit + ")"]
