import yaml

#with open('camera_setting.yaml', 'r') as yaml_file:
#    data = yaml.safe_load(yaml_file)
file_path = 'ImageInspectionController/camera_setting.yaml'

with open(file_path, 'r') as yaml_file:
    data = yaml.safe_load(yaml_file)
# アクセス例
kougucamera_info = data['camera_information']['kougukensa']
serial_number = kougucamera_info['serial_number']
kataban = kougucamera_info['kataban']
print("Serial Number:", serial_number)
print("Kataban:", kataban)