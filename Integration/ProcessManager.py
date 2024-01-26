from typing import Tuple
from ImageInspectionController.InspectionResults import ToolInspectionResult
from common_data_type import ToolType


class ProcessManager:
    def __init__(self, tool_stock_informations):
        self.tool_stock_informations = tool_stock_informations
        self.tool_position_number = 1
        self.current_tool_type = None
        self.initial_valiables()

    def initial_valiables(self):
        self.holes_by_size = {}
        self.size_indices = {}
        self.current_size_index = 0
        self.current_hole_index = 0
        self.is_tap_phase = False
        self.process_list_index = 0
        self.switching_process = False
        self.drill_positions = []
        self.current_process = 1

    def start_process(self, process_data):
        self.initial_valiables()
        self.process_data = process_data
        self.drill_positions = self.process_data["holes"]
        self._prepare_data()

    def _prepare_data(self):
        """Organizes holes by size and stores the index of their first occurrence."""
        for index, hole in enumerate(self.process_data['holes']):
            size = hole['size']
            if size not in self.holes_by_size:
                self.holes_by_size[size] = []
                self.size_indices[size] = index
            self.holes_by_size[size].append(hole)
        self.sorted_sizes = sorted(
            self.holes_by_size, key=lambda x: self.size_indices[x])

    def get_first_tool_degrees(self):
        tool_type = self._get_tooltype_with_str(
            self.drill_positions[0]["size"], "DRILL")
        self.current_tool_type = tool_type
        return self._get_rotation_degree(tool_type)

    def get_grip_position(self) -> Tuple[int, int]:
        return self.process_data["gridPoint"]["x"], self.process_data["gridPoint"]["y"]

    def get_work_size(self):
        return self.process_data["workSize"]

    def check_tool_ok(self) -> bool:
        for tool_str in self.holes_by_size.keys():
            drill_tool_type = self._get_tooltype_with_str(tool_str, "DRILL")
            tap_tool_type = self._get_tooltype_with_str(tool_str, "TAP")
            if not self._is_tool_in_stock(drill_tool_type) or\
                    not self._is_tool_in_stock(tap_tool_type):
                return False
        return True

    def _is_tool_in_stock(self, tool_type):
        for tool in self.tool_stock_informations:
            if not isinstance(tool, ToolInspectionResult):
                continue
            if tool.tool_type == tool_type:
                return True
        return False

    def get_next_position(self):
        if self.current_size_index >= len(self.sorted_sizes):
            return None  # Process completed

        size = self.sorted_sizes[self.current_size_index]
        holes = self.holes_by_size[size]

        if self.current_hole_index >= len(holes):
            self.current_hole_index = 0
            self.current_process += 1
            self.switching_process = True

        if self.current_process > 2:
            self.current_process = 1
            self.current_size_index += 1
            self.switching_process = True
            return self.get_next_position()

        hole = holes[self.current_hole_index]
        process_informaiton = (hole["position"]["x"], hole["position"]
                               ["y"], self._get_drill_speed(self.current_tool_type))
        self.current_hole_index += 1

        if self.switching_process:
            self.switching_process = False
            self.current_tool_type = self._get_tooltype_with_str(
                hole["size"], "DRILL" if self.current_process == 1 else "TAP")
            process_informaiton = (
                process_informaiton[0], process_informaiton[1], self._get_drill_speed(self.current_tool_type))
            return process_informaiton, self._get_rotation_degree(self.current_tool_type)
        return process_informaiton, None

    def _get_tooltype_with_str(self, drill_size, tool_type):
        if drill_size == "M2":
            return ToolType.M2_DRILL if tool_type == "DRILL" else ToolType.M2_TAP
        elif drill_size == "M3":
            return ToolType.M3_DRILL if tool_type == "DRILL" else ToolType.M3_TAP
        elif drill_size == "M4":
            return ToolType.M4_DRILL if tool_type == "DRILL" else ToolType.M4_TAP
        elif drill_size == "M5":
            return ToolType.M5_DRILL if tool_type == "DRILL" else ToolType.M5_TAP
        elif drill_size == "M6":
            return ToolType.M6_DRILL if tool_type == "DRILL" else ToolType.M6_TAP
        elif drill_size == "M7":
            return ToolType.M7_DRILL if tool_type == "DRILL" else ToolType.M7_TAP
        elif drill_size == "M8":
            return ToolType.M8_DRILL if tool_type == "DRILL" else ToolType.M8_TAP
        else:
            print("工具の種類が不正です")
            return None

    def _get_rotation_degree(self, tool_type) -> int:
        for i in range(1, len(self.tool_stock_informations)+1):
            if self.tool_stock_informations[i].tool_type == tool_type:
                self.current_tool_type = tool_type
                return i
        print("工具の種類が不正です")

    def _get_drill_speed(self, tool_type):
        if tool_type == ToolType.M2_DRILL or tool_type == ToolType.M2_TAP:
            return 2
        elif tool_type == ToolType.M3_DRILL or tool_type == ToolType.M3_TAP:
            return 3
        elif tool_type == ToolType.M4_DRILL or tool_type == ToolType.M4_TAP:
            return 4
        elif tool_type == ToolType.M5_DRILL or tool_type == ToolType.M5_TAP:
            return 5
        elif tool_type == ToolType.M6_DRILL or tool_type == ToolType.M6_TAP:
            return 6
