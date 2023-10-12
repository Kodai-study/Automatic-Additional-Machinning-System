from light_control import *

light_controller = Light_control()
# 撮影要求が来た
light_controller.light_switch(Camera_type.Accuracy, light_output.ON)

# take picture()
# light_controller.light_switch(Camera_type.Preprocessing, light_output.OFF)
