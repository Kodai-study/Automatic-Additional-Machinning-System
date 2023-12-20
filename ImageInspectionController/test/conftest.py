import configparser

# 設定ファイルのパス
conf_file_path = 'ImageInspectionController/test/kensa.conf'

# ConfigParser インスタンスの作成
config = configparser.ConfigParser()

# 設定ファイルの読み込み
config.read(conf_file_path)

# セクションごとにデータを取得
tool_inspection_serial_number = config.get('TOOL_INSPECTION', 'serial_number')
tool_inspection_model_number = config.get('TOOL_INSPECTION', 'model_number')

pre_processing_inspection_serial_number = config.get('PRE_PROCESSING_INSPECTION', 'serial_number')
pre_processing_inspection_model_number = config.get('PRE_PROCESSING_INSPECTION', 'model_number')

accuracy_inspection_serial_number = config.get('ACCURACY_INSPECTION', 'serial_number')
accuracy_inspection_model_number = config.get('ACCURACY_INSPECTION', 'model_number')

# Light Information
tool_inspection_pinnumber = config.getint('Light_information', 'TOOL_INSPECTION_pinnumber')
pre_processing_inspection_pinnumber = config.getint('Light_information', 'PRE_PROCESSING_INSPECTION_pinnumber')
accuracy_inspection_pinnumber = config.getint('Light_information', 'ACCURACY_INSPECTION_pinnumber')

on_state = config.getint('Light_information', 'ON')
off_state = config.getint('Light_information', 'OFF')

# GPIO Information
ioboard_pid = config.getint('gpio', 'IOBOARD_PID')
ioboard_vid = config.getint('gpio', 'IOBOARD_VID')

# 結果の表示（この部分は必要に応じて変更してください）
print(f'TOOL_INSPECTION Serial Number: {tool_inspection_serial_number}')
print(f'TOOL_INSPECTION Model Number: {tool_inspection_model_number}')

print(f'PRE_PROCESSING_INSPECTION Serial Number: {pre_processing_inspection_serial_number}')
print(f'PRE_PROCESSING_INSPECTION Model Number: {pre_processing_inspection_model_number}')

print(f'ACCURACY_INSPECTION Serial Number: {accuracy_inspection_serial_number}')
print(f'ACCURACY_INSPECTION Model Number: {accuracy_inspection_model_number}')

print(f'TOOL_INSPECTION Pin Number: {tool_inspection_pinnumber}')
print(f'PRE_PROCESSING_INSPECTION Pin Number: {pre_processing_inspection_pinnumber}')
print(f'ACCURACY_INSPECTION Pin Number: {accuracy_inspection_pinnumber}')

print(f'ON State: {on_state}')
print(f'OFF State: {off_state}')

print(f'IOBOARD_PID: {ioboard_pid}')
print(f'IOBOARD_VID: {ioboard_vid}')
