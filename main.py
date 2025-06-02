import customtkinter as ctk
from customtkinter import CTk, CTkLabel, CTkFrame, CTkTabview
from read import read_timing
from timings import TIMINGS, apply_formula
import sys, ctypes, os, wmi
class TimingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Timing Viewer")
        self.setup_appearance()
        self.create_widgets()
        self.setup_window_geometry()
        self.load_all_tabs_content()
    def setup_appearance(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg="#1f1f1f")
        self.GLOBAL_FONT_FAMILY = "Roboto"
        self.GLOBAL_FONT_SIZE = 13
        self.GLOBAL_FONT = (self.GLOBAL_FONT_FAMILY, self.GLOBAL_FONT_SIZE)
        self.BG_COLOR = "#202020"
        self.BG_COLOR2 = "#262626"
        self.SECTION_COLOR = "#262626"
        self.ROW_COLOR = "#2a2a2a"
        self.BORDER_COLOR = "#1a1a1a"
        self.TEXT_COLOR = "#FFFFFF"
        self.HIGHLIGHT_COLOR = "#242424"
        self.TAB_SELECTED_COLOR = "#1a3c5d"
        self.TAB_UNSELECTED_COLOR = "#2e2e2e"
        self.TAB_HOVER_COLOR = "#2a5579"
    def get_memory_part_numbers(self):
        """Retrieve memory part numbers, capacity, and memory type using WMI, mapping tags to slots based on MemoryDevices."""
        try:
            w = wmi.WMI()
            memory_arrays = w.Win32_PhysicalMemoryArray()
            if not memory_arrays:
                print("Error: Could not determine number of memory slots.")
                return [], []
            num_slots = memory_arrays[0].MemoryDevices
            memory_info = []
            for memory in w.Win32_PhysicalMemory():
                capacity_bytes = int(memory.Capacity)
                capacity_gb = capacity_bytes // (1024 ** 3)
                memory_type = str(memory.MemoryType)
                part_number = memory.PartNumber.strip() if memory.PartNumber else "Unknown"
                tag = memory.Tag.strip() if memory.Tag else "Unknown"
                memory_info.append({
                    "tag": tag,
                    "part_number": part_number,
                    "capacity": f"{capacity_gb}GB"
                })
            if num_slots == 4:
                slot_mapping = {
                    "Physical Memory 0": "B2",
                    "Physical Memory 1": "B1",
                    "Physical Memory 2": "A2",
                    "Physical Memory 3": "A1"
                }
            elif num_slots == 2:
                slot_mapping = {
                    "Physical Memory 0": "A",
                    "Physical Memory 1": "B"
                }
            else:
                print(f"Unsupported number of memory slots: {num_slots}. Defaulting to empty mapping.")
                slot_mapping = {}
            channel_a = []
            channel_b = []
            for info in memory_info:
                tag = info["tag"]
                slot = slot_mapping.get(tag, "N/A")
                if num_slots == 4:
                    if slot in ["A1", "A2"]:
                        channel_a.append(f"{slot}: {info['part_number']} ({info['capacity']})")
                    elif slot in ["B1", "B2"]:
                        channel_b.append(f"{slot}: {info['part_number']} ({info['capacity']})")
                elif num_slots == 2:
                    if slot == "A":
                        channel_a.append(f"{slot}: {info['part_number']} ({info['capacity']})")
                    elif slot == "B":
                        channel_b.append(f"{slot}: {info['part_number']} ({info['capacity']})")
            channel_a.sort(key=lambda x: x.split(":")[0])
            channel_b.sort(key=lambda x: x.split(":")[0])
            return channel_a, channel_b
        except Exception as e:
            print(f"Error retrieving memory info: {e}")
            return [], []
    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self.root, corner_radius=8, height=50, fg_color=self.BG_COLOR)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.header_label_frame = ctk.CTkFrame(
            self.header_frame,
            corner_radius=8,
            fg_color=self.SECTION_COLOR,
            border_width=2,
            border_color=self.BORDER_COLOR
        )
        self.header_label_frame.pack(fill="x", padx=5, pady=5)
        self.header_label_inner_frame = ctk.CTkFrame(
            self.header_label_frame,
            corner_radius=6,
            fg_color=self.BG_COLOR2,
            border_width=2,
            border_color=self.BORDER_COLOR
        )
        self.header_label_inner_frame.pack(fill="x", padx=5, pady=5)
        self.header_label = ctk.CTkLabel(
            self.header_label_inner_frame,
            text="Timing Viewer",
            font=(self.GLOBAL_FONT_FAMILY, 22, "bold"),
            padx=15,
            pady=10,
            text_color=self.TEXT_COLOR,
            fg_color="transparent"
        )
        self.header_label.pack(fill="x", expand=True)
        self.part_number_frame = ctk.CTkFrame(
            self.header_frame,
            corner_radius=8,
            fg_color=self.SECTION_COLOR,
            border_width=2,
            border_color=self.BORDER_COLOR
        )
        self.part_number_frame.pack(fill="x", padx=5, pady=(0, 5))
        self.part_number_inner_frame = ctk.CTkFrame(
            self.part_number_frame,
            corner_radius=6,
            fg_color=self.BG_COLOR2,
            border_width=2,
            border_color=self.BORDER_COLOR
        )
        self.part_number_inner_frame.pack(fill="x", padx=5, pady=5)
        self.part_number_inner_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.part_number_inner_frame.grid_columnconfigure(1, weight=1, uniform="equal")
        channel_a, channel_b = self.get_memory_part_numbers()
        channel_a_text = "\n".join(channel_a) if channel_a else ""
        self.channel_a_label = ctk.CTkLabel(
            self.part_number_inner_frame,
            text=channel_a_text,
            font=(self.GLOBAL_FONT_FAMILY, 16),
            anchor="center",  
            padx=15,
            pady=8,
            text_color=self.TEXT_COLOR,
            fg_color="transparent"
        )
        self.channel_a_label.grid(row=0, column=0, sticky="nsew")  
        channel_b_text = "\n".join(channel_b) if channel_b else ""
        self.channel_b_label = ctk.CTkLabel(
            self.part_number_inner_frame,
            text=channel_b_text,
            font=(self.GLOBAL_FONT_FAMILY, 16),
            anchor="center",  
            padx=15,
            pady=8,
            text_color=self.TEXT_COLOR,
            fg_color="transparent"
        )
        self.channel_b_label.grid(row=0, column=1, sticky="nsew")  
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=8, fg_color=self.BG_COLOR)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        self.tabview = ctk.CTkTabview(
            self.main_frame,
            fg_color=self.BG_COLOR,
            segmented_button_fg_color=self.BG_COLOR2,
            segmented_button_selected_color=self.TAB_SELECTED_COLOR,
            segmented_button_selected_hover_color=self.TAB_HOVER_COLOR,
            segmented_button_unselected_color=self.TAB_UNSELECTED_COLOR,
            segmented_button_unselected_hover_color="#3a3a3a",
            corner_radius=10,
            border_width=2,
            border_color=self.BORDER_COLOR,
            height=60,
        )
        self.tabview._segmented_button.configure(
            corner_radius=10,
            border_width=2,
            fg_color=self.BG_COLOR,
            selected_color=self.TAB_SELECTED_COLOR,
            selected_hover_color=self.TAB_HOVER_COLOR,
            unselected_color=self.TAB_UNSELECTED_COLOR,
            unselected_hover_color="#3a3a3a",
            text_color=self.TEXT_COLOR,
            font=(self.GLOBAL_FONT_FAMILY, 16, "bold")
        )
        self.tabview._segmented_button._text_color = self.TEXT_COLOR
        self.tabview._segmented_button._selected_text_color = self.TEXT_COLOR
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)
        self.tab_names = ["Timings", "RTL", "Skew", "JEDEC"]
        for name in self.tab_names:
            self.tabview.add(name)
        self.tab_frames = {}
        self.grid_frames = {}
        for name in self.tab_names:
            scrollable = ctk.CTkScrollableFrame(
                self.tabview.tab(name), 
                corner_radius=0, 
                fg_color=self.BG_COLOR
            )
            scrollable.pack(fill="both", expand=True)
            self.tab_frames[name] = scrollable
            frame = ctk.CTkFrame(scrollable, corner_radius=0, fg_color=self.BG_COLOR)
            frame.pack(fill="both", expand=True, padx=5, pady=5)
            frame.grid_columnconfigure(0, weight=1, uniform="equal")
            frame.grid_columnconfigure(1, weight=1, uniform="equal")
            left_frame = ctk.CTkFrame(frame, corner_radius=0, fg_color=self.BG_COLOR)
            left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
            left_frame.grid_columnconfigure(0, weight=1)
            right_frame = ctk.CTkFrame(frame, corner_radius=0, fg_color=self.BG_COLOR)
            right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
            right_frame.grid_columnconfigure(0, weight=1)
            self.grid_frames[name] = {"Left": left_frame, "Right": right_frame}
        self.tabview.configure(command=self.on_tab_change)
    def setup_window_geometry(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        column_width = 350
        window_width = column_width * 2 + 100
        window_height = int(screen_height * 0.83)
        min_height = 500
        window_height = max(window_height, min_height)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(window_width, min_height)
    def load_all_tabs_content(self):
        """Load content for all tabs dynamically based on TIMINGS and balance column heights."""
        for tab_name in self.tab_names:
            tab_timings = [t for t in TIMINGS if t["Tab"] == tab_name]
            categories = []
            current_category = None
            for timing in tab_timings:
                category = timing["Category"]
                if current_category != category:
                    categories.append((category, []))
                    current_category = category
                categories[-1][1].append(timing["name"])
            left_column = []
            right_column = []
            for cat, names in categories:
                timing_entry = next((t for t in tab_timings if t["Category"] == cat), None)
                column = timing_entry.get("Column", "Left") if timing_entry else "Left"
                if tab_name == "RTL":
                    if cat in ["Latency CHA"]:
                        column = "Left"
                    elif cat in ["Latency CHB"]:
                        column = "Right"
                if column == "Left":
                    left_column.append((cat, names))
                else:
                    right_column.append((cat, names))
            section_header_height = 42
            row_height = 30
            section_internal_padding = 10
            section_external_padding = 10
            def calculate_column_height(column_sections):
                total_height = 0
                for cat, names in column_sections:
                    has_dual_addresses = any(
                        ("parameters_a" in timing and "parameters_b" in timing) or
                        ("dynamic_params_a" in timing and "dynamic_params_b" in timing)
                        for timing in TIMINGS
                        if timing["name"].lower() in [name.lower() for name in names] and timing["Category"] == cat
                    )
                    num_rows = len(names)
                    if has_dual_addresses:
                        num_rows += 1  
                    section_height = section_header_height + (num_rows * row_height) + section_internal_padding
                    total_height += section_height
                if column_sections:
                    total_height += section_external_padding * (len(column_sections) - 1)
                return total_height
            left_height = calculate_column_height(left_column)
            right_height = calculate_column_height(right_column)
            height_difference = abs(left_height - right_height)
            if height_difference > 0:
                shorter_column = left_column if left_height < right_height else right_column
                num_sections = len(shorter_column)
                if num_sections > 0:
                    extra_pady_per_section = height_difference / num_sections
                    for i in range(num_sections):
                        current_extra = extra_pady_per_section
                        if i == num_sections - 1:
                            current_extra = height_difference - (extra_pady_per_section * (num_sections - 1))
                        section_name, timing_names = shorter_column[i]
                        pady = (
                            section_external_padding, 
                            section_external_padding + current_extra if i < num_sections - 1 else section_external_padding
                        )
                        if shorter_column is left_column:
                            self.create_section(
                                self.grid_frames[tab_name]["Left"],
                                section_name,
                                timing_names,
                                column=0,
                                row=i,
                                extra_pady=0,
                                return_frame=True,
                                tab_name=tab_name,
                                pady=pady
                            )
                        else:
                            self.create_section(
                                self.grid_frames[tab_name]["Right"],
                                section_name,
                                timing_names,
                                column=0,
                                row=i,
                                extra_pady=0,
                                return_frame=True,
                                tab_name=tab_name,
                                pady=pady
                            )
                taller_column = right_column if left_height < right_height else left_column
                for i, (section_name, timing_names) in enumerate(taller_column):
                    pady = (section_external_padding, section_external_padding)
                    if taller_column is left_column:
                        self.create_section(
                            self.grid_frames[tab_name]["Left"],
                            section_name,
                            timing_names,
                            column=0,
                            row=i,
                            extra_pady=0,
                            return_frame=True,
                            tab_name=tab_name,
                            pady=pady
                        )
                    else:
                        self.create_section(
                            self.grid_frames[tab_name]["Right"],
                            section_name,
                            timing_names,
                            column=0,
                            row=i,
                            extra_pady=0,
                            return_frame=True,
                            tab_name=tab_name,
                            pady=pady
                        )
            else:
                for i, (section_name, timing_names) in enumerate(left_column):
                    self.create_section(
                        self.grid_frames[tab_name]["Left"],
                        section_name,
                        timing_names,
                        column=0,
                        row=i,
                        extra_pady=0,
                        return_frame=True,
                        tab_name=tab_name,
                        pady=(section_external_padding, section_external_padding)
                    )
                for i, (section_name, timing_names) in enumerate(right_column):
                    self.create_section(
                        self.grid_frames[tab_name]["Right"],
                        section_name,
                        timing_names,
                        column=0,
                        row=i,
                        extra_pady=0,
                        return_frame=True,
                        tab_name=tab_name,
                        pady=(section_external_padding, section_external_padding)
                    )
    def create_section(self, parent, section_name, timing_names, column=0, row=0, columnspan=1, extra_pady=0, return_frame=False, tab_name=None, pady=(10, 10)):
        """Create a categorized section block with consistent layout for single or dual-channel timings."""
        section_frame = ctk.CTkFrame(
            parent, 
            corner_radius=8,
            border_width=2,
            fg_color=self.SECTION_COLOR,
            border_color=self.BORDER_COLOR
        )
        section_frame.grid(
            row=row, 
            column=column, 
            columnspan=columnspan,
            padx=5,
            pady=pady,
            sticky="nsew"
        )
        section_frame.grid_columnconfigure(0, weight=1)
        section_frame.grid_rowconfigure(1, weight=1)
        header_frame = ctk.CTkFrame(
            section_frame, 
            corner_radius=6,
            fg_color=self.SECTION_COLOR
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        header = ctk.CTkLabel(
            header_frame,
            text=section_name.upper(),
            font=(self.GLOBAL_FONT_FAMILY, 14, "bold"),  
            anchor="w",
            padx=10,
            pady=6,
            text_color=self.TEXT_COLOR
        )
        header.pack(fill="x", expand=True)
        content_frame = ctk.CTkFrame(
            section_frame, 
            corner_radius=6,
            fg_color=self.BG_COLOR2,
            border_width=2,
            border_color=self.BORDER_COLOR
        )
        content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        section_timings = [t for t in TIMINGS if t["Category"] == section_name and t["name"].lower() in [tn.lower() for tn in timing_names]]
        has_dual_addresses = any(
            ("parameters_a" in timing and "parameters_b" in timing) or
            ("dynamic_params_a" in timing and "dynamic_params_b" in timing)
            for timing in section_timings
        )
        if has_dual_addresses:
            content_frame.grid_columnconfigure(0, weight=4)
            content_frame.grid_columnconfigure(1, weight=1)
            content_frame.grid_columnconfigure(2, weight=1)
            first_dual_timing = next(
                (t for t in section_timings if ("parameters_a" in t and "parameters_b" in t) or ("dynamic_params_a" in t and "dynamic_params_b" in t)),
                None
            )
            if first_dual_timing:
                parameter_header_text = first_dual_timing.get("parameter_name", "Channel")
                a_header_text = first_dual_timing.get("name_a", "A")
                b_header_text = first_dual_timing.get("name_b", "B")
            else:
                parameter_header_text = "Channel"
                a_header_text = "A"
                b_header_text = "B"
            parameter_header = ctk.CTkLabel(
                content_frame,
                text=parameter_header_text,
                font=(self.GLOBAL_FONT_FAMILY, self.GLOBAL_FONT_SIZE, "bold"),  
                anchor="w",
                padx=10,
                pady=4,
                text_color=self.TEXT_COLOR
            )
            parameter_header.grid(row=0, column=0, sticky="ew")
            a_header = ctk.CTkLabel(
                content_frame,
                text=a_header_text,
                font=(self.GLOBAL_FONT_FAMILY, self.GLOBAL_FONT_SIZE, "bold"),  
                anchor="center",
                padx=5,
                pady=4,
                text_color=self.TEXT_COLOR
            )
            a_header.grid(row=0, column=1, sticky="ew")
            b_header = ctk.CTkLabel(
                content_frame,
                text=b_header_text,
                font=(self.GLOBAL_FONT_FAMILY, self.GLOBAL_FONT_SIZE, "bold"),  
                anchor="center",
                padx=5,
                pady=4,
                text_color=self.TEXT_COLOR
            )
            b_header.grid(row=0, column=2, sticky="ew")
            for idx, timing_name in enumerate(timing_names, start=1):
                timing = next(
                    (t for t in TIMINGS if t["name"].lower() == timing_name.lower() and t["Category"] == section_name),
                    None
                )
                if not timing:
                    continue
                bg_color = self.ROW_COLOR if idx % 2 == 0 else self.BG_COLOR2
                name_label = ctk.CTkLabel(
                    content_frame,
                    text=timing["name"],
                    font=self.GLOBAL_FONT,  
                    anchor="w",
                    padx=10,
                    pady=4,
                    text_color=self.TEXT_COLOR,
                    fg_color=bg_color
                )
                name_label.grid(row=idx, column=0, sticky="ew")
                is_dual = ("parameters_a" in timing and "parameters_b" in timing) or ("dynamic_params_a" in timing and "dynamic_params_b" in timing)
                if is_dual:
                    value_a = "N/A"
                    if "read_type_a" in timing and timing["read_type_a"] == "dynamic" and "dynamic_params_a" in timing:
                        raw_value = read_timing(
                            read_type="dynamic",
                            dynamic_params=timing["dynamic_params_a"]
                        )
                        value_a = apply_formula(raw_value, timing.get("Formula"))
                    elif "address_a" in timing and timing["address_a"] is not None:
                        raw_value = read_timing(
                            address=timing["address_a"],
                            bit_start=timing["parameters_a"]["bit_start"],
                            bit_length=timing["parameters_a"]["bit_length"],
                            read_type="standard"
                        )
                        value_a = apply_formula(raw_value, timing.get("Formula"))
                    elif "value" in timing and timing["value"] is not None:
                        value_a = str(timing["value"])
                    value_a_label = ctk.CTkLabel(
                        content_frame,
                        text=value_a,
                        font=self.GLOBAL_FONT,  
                        anchor="center",
                        padx=5,
                        pady=4,
                        text_color=self.TEXT_COLOR,
                        fg_color=bg_color
                    )
                    value_a_label.grid(row=idx, column=1, sticky="ew")
                    value_b = "N/A"
                    if "read_type_b" in timing and timing["read_type_b"] == "dynamic" and "dynamic_params_b" in timing:
                        raw_value = read_timing(
                            read_type="dynamic",
                            dynamic_params=timing["dynamic_params_b"]
                        )
                        value_b = apply_formula(raw_value, timing.get("Formula"))
                    elif "address_b" in timing and timing["address_b"] is not None:
                        raw_value = read_timing(
                            address=timing["address_b"],
                            bit_start=timing["parameters_b"]["bit_start"],
                            bit_length=timing["parameters_b"]["bit_length"],
                            read_type="standard"
                        )
                        value_b = apply_formula(raw_value, timing.get("Formula"))
                    elif "value" in timing and timing["value"] is not None:
                        value_b = str(timing["value"])
                    value_b_label = ctk.CTkLabel(
                        content_frame,
                        text=value_b,
                        font=self.GLOBAL_FONT,  
                        anchor="center",
                        padx=5,
                        pady=4,
                        text_color=self.TEXT_COLOR,
                        fg_color=bg_color
                    )
                    value_b_label.grid(row=idx, column=2, sticky="ew")
                else:
                    value = "N/A"
                    if "read_type" in timing and timing["read_type"] == "dynamic" and "dynamic_params" in timing:
                        raw_value = read_timing(
                            read_type="dynamic",
                            dynamic_params=timing["dynamic_params"]
                        )
                        if raw_value is not None:
                            if timing["name"] == "tWR":
                                raw_value = raw_value & 0xF  
                            value = apply_formula(raw_value, timing.get("Formula"))
                    elif "address" in timing and timing["address"] is not None:
                        raw_value = read_timing(
                            address=timing["address"],
                            bit_start=timing["parameters"]["bit_start"],
                            bit_length=timing["parameters"]["bit_length"],
                            read_type="standard"
                        )
                        value = apply_formula(raw_value, timing.get("Formula"))
                    elif "value" in timing and timing["value"] is not None:
                        value = str(timing["value"])
                    elif "default_value" in timing:
                        value = timing["default_value"]
                    value_label = ctk.CTkLabel(
                        content_frame,
                        text=value,
                        font=self.GLOBAL_FONT,  
                        anchor="center",
                        padx=5,
                        pady=4,
                        text_color=self.TEXT_COLOR,
                        fg_color=bg_color
                    )
                    value_label.grid(row=idx, column=1, sticky="ew")
                    empty_label = ctk.CTkLabel(
                        content_frame,
                        text="",
                        font=self.GLOBAL_FONT,  
                        anchor="center",
                        padx=5,
                        pady=4,
                        fg_color=bg_color
                    )
                    empty_label.grid(row=idx, column=2, sticky="ew")
                if idx < len(timing_names):
                    content_frame.grid_rowconfigure(idx, weight=0, minsize=4 + int(extra_pady))
        else:
            content_frame.grid_columnconfigure(0, weight=3)
            content_frame.grid_columnconfigure(1, weight=1)
            for idx, timing_name in enumerate(timing_names, start=0):
                timing = next(
                    (t for t in TIMINGS if t["name"].lower() == timing_name.lower() and t["Category"] == section_name),
                    None
                )
                if not timing:
                    continue
                bg_color = self.ROW_COLOR if idx % 2 == 0 else self.BG_COLOR2
                name_label = ctk.CTkLabel(
                    content_frame,
                    text=timing["name"],
                    font=self.GLOBAL_FONT,  
                    anchor="w",
                    padx=15,
                    pady=4,
                    text_color=self.TEXT_COLOR,
                    fg_color=bg_color
                )
                name_label.grid(row=idx, column=0, sticky="ew")
                value = "N/A"
                if "read_type" in timing and timing["read_type"] == "dynamic" and "dynamic_params" in timing:
                    raw_value = read_timing(
                        read_type="dynamic",
                        dynamic_params=timing["dynamic_params"]
                    )
                    if raw_value is not None:
                        if timing["name"] == "tWR":
                            raw_value = raw_value & 0xF  
                        value = apply_formula(raw_value, timing.get("Formula"))
                    else:
                        value = "N/A"
                elif "address" in timing and timing["address"] is not None:
                    raw_value = read_timing(
                        address=timing["address"],
                        bit_start=timing["parameters"]["bit_start"],
                        bit_length=timing["parameters"]["bit_length"],
                        read_type="standard"
                    )
                    value = apply_formula(raw_value, timing.get("Formula"))
                elif "value" in timing and timing["value"] is not None:
                    value = str(timing["value"])
                elif "default_value" in timing:
                    value = timing["default_value"]
                value_label = ctk.CTkLabel(
                    content_frame,
                    text=value,
                    font=self.GLOBAL_FONT,  
                    anchor="center",
                    padx=5,
                    pady=4,
                    text_color=self.TEXT_COLOR,
                    fg_color=bg_color
                )
                value_label.grid(row=idx, column=1, sticky="ew")
                if idx < len(timing_names) - 1:
                    content_frame.grid_rowconfigure(idx, weight=0, minsize=4 + int(extra_pady))
        if return_frame:
            return section_frame
    def on_tab_change(self):
        """Handle tab change event if needed"""
        pass
def is_admin():
    """Check if the current process has administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def run_as_admin():
    """Relaunch the script with administrative privileges."""
    if getattr(sys, 'frozen', False):  
        script_path = sys.executable
    else:
        script_path = os.path.abspath(__file__)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
    sys.exit(0)
if __name__ == "__main__":
    if not is_admin():
        print("Admin privileges required. Relaunching with UAC prompt...")
        run_as_admin()
    root = ctk.CTk()
    app = TimingGUI(root)
    root.mainloop()