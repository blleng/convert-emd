from dataclasses import dataclass, field
from typing import List, Dict, Tuple

@dataclass
class ConvertConfig:
    output_type: str = ".tif"
    scale_bar: bool = True
    sb_color: str = "#ffffff"
    sb_x_start: float = 0.75
    sb_y_start: float = 0.9167
    sb_width_factor: float = 150.0
    stretch: Tuple[float, float] = (1.0, 99.0)
    overlay_alpha: float = 1.0
    sub_alpha: float = 0.5
    eds_colors: Dict[str, str] = field(default_factory=dict)
    mapping_overlay: List[str] = field(default_factory=list)
    overlay: bool = False
