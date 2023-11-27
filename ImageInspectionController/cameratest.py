#
# grab_software_trigger_ndarray.py (for Python 3)
#
# Copyright (c) 2020 Toshiba-Teli Corporation
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import sys
import numpy as np
import pytelicam
import yaml
import cv2


# It is recommended that the settings of unused interfaces be removed.
#  (U3v / Gev / GenTL)
def initial_cam_setting(cam_num=3)->pytelicam.pytelicam.CameraSystem:
    cam_system = pytelicam.get_camera_system( \
    int(pytelicam.CameraType.U3v) | \
    int(pytelicam.CameraType.Gev))
    find_cam_num = cam_system.get_num_of_cameras()
    if find_cam_num != cam_num:
        print('Camera number is No')
        return None
    return cam_system

def setting_cam(serial_num:str,model:str,cam_system:pytelicam.pytelicam.CameraSystem)\
    ->(pytelicam.pytelicam.CameraDevice,pytelicam.pytelicam.SignalHandle):
    cam_device = cam_system.create_device_object_from_info(serial_num,model,"")
    cam_device.open()

    res = cam_device.genapi.set_enum_str_value('TriggerMode', 'On')
    if res != pytelicam.CamApiStatus.Success:
        raise Exception("Can't set TriggerMode.")

    res = cam_device.genapi.set_enum_str_value('TriggerSource', 'Software')
    if res != pytelicam.CamApiStatus.Success:
        raise Exception("Can't set TriggerSource.")

    res = cam_device.genapi.set_enum_str_value('TriggerSequence', 'TriggerSequence0')
    receive_signal = cam_system.create_signal()

    cam_device.cam_stream.open(receive_signal)
    return cam_device,receive_signal

def take_picture(cam_device,cam_system,receive_signal) -> np.ndarray:

    cam_device.cam_stream.start()


    res = cam_device.genapi.execute_command('TriggerSoftware')
    if res != pytelicam.CamApiStatus.Success:
        raise Exception("Can't execute TriggerSoftware.")

    res = cam_system.wait_for_signal(receive_signal)
    if res != pytelicam.CamApiStatus.Success:
        print('Grab error! status = {0}'.format(res))
        return 
    else:
        # If you don't use 'with' statement, image_data.release() must be called after using image_data.
        with cam_device.cam_stream.get_current_buffered_image() as image_data:
            if image_data.status != pytelicam.CamApiStatus.Success:
                print('Grab error! status = {0}'.format(image_data.status))
                return
            else:
                return image_data.get_ndarray(pytelicam.OutputImageType.Bgr24)  



try:
    cam_system=initial_cam_setting(1)
    cam_device,receive_signal=setting_cam("1000143","BU602M",cam_system)
    print('---------------------------------------------------------------------')
    print('Press \'0\' + \'Enter\' key to issue \"Software Trigger\" and grab a frame.')
    print('Press \'9\' + \'Enter\' key to quit application.');
    print('---------------------------------------------------------------------')

    while True:
        key = input()
        if key == '0':
            np_arr = take_picture(cam_device,cam_system,receive_signal)
            print('shape      : {0}'.format(np_arr.shape))
            print('image data :\n {0}'.format(np_arr[0,]))
            print('average    : {0}\n'.format(np.average(np_arr)))
            # グレースケール画像の保存
            cv2.imwrite('grayscale_image.png', np_arr)

        elif key == '9':
            break

except pytelicam.PytelicamError as teli_exception:
    print('An error occurred!')
    print('  message : {0}'.format(teli_exception.message))
    print('  status  : {0}'.format(teli_exception.status))
except Exception as exception:
    print(exception)

finally:
    if 'cam_device' in globals():
        if cam_device.cam_stream.is_open == True:
            cam_device.cam_stream.stop()
            cam_device.cam_stream.close()

        if cam_device.is_open == True:
            cam_device.close()

    if 'receive_signal' in globals():
        cam_system.close_signal(receive_signal)

    cam_system.terminate()
    print('Finished.')

'''
#
# grab_software_trigger_ndarray.py (for Python 3)
#
# Copyright (c) 2020 Toshiba-Teli Corporation
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import sys
import numpy as np
import pytelicam


# It is recommended that the settings of unused interfaces be removed.
#  (U3v / Gev / GenTL)
cam_system = pytelicam.get_camera_system( \
    int(pytelicam.CameraType.U3v) | \
        
    int(pytelicam.CameraType.Gev))

try:
    cam_num = cam_system.get_num_of_cameras()
    if cam_num == 0:
        print('Camera not found.')
        sys.exit()

    print('{0} camera(s) found.'.format(cam_num))

    # Open camera that is detected first, in this sample code.
    cam_no = 0
    cam_device = cam_system.create_device_object(cam_no)
    
    cam_device.open()

    res = cam_device.genapi.set_enum_str_value('TriggerMode', 'On')
    if res != pytelicam.CamApiStatus.Success:
        raise Exception("Can't set TriggerMode.")

    res = cam_device.genapi.set_enum_str_value('TriggerSource', 'Software')
    if res != pytelicam.CamApiStatus.Success:
        raise Exception("Can't set TriggerSource.")

    res = cam_device.genapi.set_enum_str_value('TriggerSequence', 'TriggerSequence0')
    #if res != pytelicam.CamApiStatus.Success:
    #    raise Exception("Can't set TriggerSequence.")

    receive_signal = cam_system.create_signal()

    cam_device.cam_stream.open(receive_signal)
    cam_device.cam_stream.start()

    print('---------------------------------------------------------------------')
    print('Press \'0\' + \'Enter\' key to issue \"Software Trigger\" and grab a frame.')
    print('Press \'9\' + \'Enter\' key to quit application.');
    print('---------------------------------------------------------------------')


    while True:
        key = input()

        if key == '0':
            res = cam_device.genapi.execute_command('TriggerSoftware')
            if res != pytelicam.CamApiStatus.Success:
                raise Exception("Can't execute TriggerSoftware.")

            res = cam_system.wait_for_signal(receive_signal)
            if res != pytelicam.CamApiStatus.Success:
                print('Grab error! status = {0}'.format(res))
                break
            else:
                # If you don't use 'with' statement, image_data.release() must be called after using image_data.
                with cam_device.cam_stream.get_current_buffered_image() as image_data:
                    if image_data.status != pytelicam.CamApiStatus.Success:
                        print('Grab error! status = {0}'.format(image_data.status))
                        break
                    else:
                        np_arr = image_data.get_ndarray(pytelicam.OutputImageType.Bgr24)  
                        print('shape      : {0}'.format(np_arr.shape))
                        print('image data :\n {0}'.format(np_arr[0,]))
                        print('average    : {0}\n'.format(np.average(np_arr)))

        elif key == '9':
            break

except pytelicam.PytelicamError as teli_exception:
    print('An error occurred!')
    print('  message : {0}'.format(teli_exception.message))
    print('  status  : {0}'.format(teli_exception.status))
except Exception as exception:
    print(exception)

finally:
    if 'cam_device' in globals():
        if cam_device.cam_stream.is_open == True:
            cam_device.cam_stream.stop()
            cam_device.cam_stream.close()

        if cam_device.is_open == True:
            cam_device.close()

    if 'receive_signal' in globals():
        cam_system.close_signal(receive_signal)

    cam_system.terminate()

    print('Finished.')
'''