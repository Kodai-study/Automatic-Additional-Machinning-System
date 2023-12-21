import configparser

class ConfigReader:
    def __init__(self, config_file_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_file_path, encoding='utf-8')

    def get_camera_info(self, inspection_type):
        try:
            section_name = f"{inspection_type}"
            serial_number = self.config.get(section_name, "serial_number")
            model_number = self.config.get(section_name, "model_number")
            return serial_number, model_number
        except configparser.NoSectionError:
            raise ValueError(f"指定されたセクションが存在しません: {section_name}")

    def get_light_info(self, inspection_type):
        try:
            section_name = f"{inspection_type}"
            pin_number = self.config.getint("Light_information", f"{section_name}_pinnumber")
            return pin_number
        except (configparser.NoSectionError, configparser.NoOptionError):
            raise ValueError(f"指定されたセクションまたはオプションが存在しません: {section_name}")

    def get_gpio_info(self):
        try:
            ioboard_pid = self.config.getint("gpio", "IOBOARD_PID")
            ioboard_vid = self.config.getint("gpio", "IOBOARD_VID")
            return ioboard_pid, ioboard_vid
        except (configparser.NoSectionError, configparser.NoOptionError):
            raise ValueError("指定されたセクションまたはオプションが存在しません: gpio")

    def get_on_off_values(self):
        try:
            on_value = self.config.getint("Light_information", "ON")
            off_value = self.config.getint("Light_information", "OFF")
            return on_value, off_value
        except (configparser.NoSectionError, configparser.NoOptionError):
            raise ValueError("指定されたセクションまたはオプションが存在しません: Light_information")

# 使用例
config_file_path = "ImageInspectionController/test/kensa.conf"  # 実際のファイルパスに置き換えてください
config_reader = ConfigReader(config_file_path)

# TOOL_INSPECTIONの情報を取得
try:
    tool_serial, tool_model = config_reader.get_camera_info("TOOL_INSPECTION")
    tool_pin = config_reader.get_light_info("TOOL_INSPECTION")
    print("TOOL_INSPECTION:")
    print(f"Serial Number: {tool_serial}")
    print(f"Model Number: {tool_model}")
    print(f"Pin Number: {tool_pin}")
except ValueError as e:
    print(e)
