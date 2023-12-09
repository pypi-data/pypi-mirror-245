import cv2
import time
import hid
import numpy as np
from prettytable import PrettyTable
from threading import Thread


class CustomError(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message
        super().__init__(message)


class Camera_API:
    global RED_TEXT, RESET_COLOR, cam_list, cam_index
    cam_list = []
    cam_index = []
    supported_uvc_properties = None
    uvc_propID = None
    possibleuvclist = None
    support_mode = None
    prop_id = None
    available_properties = None
    current_mode = None

    current_value = None
    supported_mode = None
    default_value = None
    roll_prop = None
    stepping_delta = None
    minimum = None
    maximum = None
    capture_properties = None
    con_prop = None
    gain_prop = None
    supported_properties = None
    iris_prop = None
    focus_prop = None
    tilt_prop = None
    backlight_prop = None
    pan_prop = None
    zoom_prop = None
    exp_prop = None
    gamma_prop = None
    wb_prop = None
    hue_prop = None
    sharp_prop = None
    sat_prop = None
    bri_prop = None
    serial_number = None
    firmware = None
    device = None
    devices = None
    cap = None
    cap2 = None
    cap1 = None
    frame = None

    RED_TEXT = "\033[91m"
    RESET_COLOR = "\033[0m"

    @classmethod
    def get_devices(cls) -> list:
        """
           Get the connected camera list
            usage:
                Getting node for the connected camera
            Returns:
            list: connected camera.
            """
        devices = []
        var = 101
        "Camera not found"

        cls.cap1 = cv2.VideoCapture()
        for i in range(cls.cap1.getDevices()[1]):
            # print(cls.cap1.getDeviceInfo(i))
            print(str(i) + ": " + str(cls.cap1.getDeviceInfo(i)[1]))
            devices.append(cls.cap1.getDeviceInfo(i)[1])
        return devices

    @classmethod
    def open_camera(cls, camera_node: int) -> object:
        """
          Used to assign the camera using OpenCV
           usage:
               Open the camera
           Parameters:
           - node (int): camera node which was get using the get devices.
           Returns:
           object: Assigned camera.
                   """

        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer")

        cls.stop = False
        # cls.cap = cv2.VideoCapture()
        error_code = 101
        error_message = "Camera not found"
        CustomError(error_code, error_message)

        try:
            cls.cap = cv2.VideoCapture(camera_node)
            cam_list.append(cls.cap)
            cam_index.append(camera_node)
            if cls.cap.isOpened():
                return cls.cap
            else:
                print(f"Error code: {error_code} {error_message}")
        except NameError:
            print(f"Error code: {error_code} {error_message}")

    @classmethod
    def get_device_path(cls, camera_node: int) -> str:
        """
          Used to get the device path of the camera for the  give node
           Parameters:
           - node (int): camera node which was get using the get devices.
           Returns:
           str: Device path.
                   """
        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer")
        cls.cap = cv2.VideoCapture()
        print(cls.cap.getDeviceInfo(camera_node)[4])
        # for i in range(cls.cap.getDevices()[1]):
        # if camera_name == cls.cap.getDeviceInfo(i)[1]:
        return cls.cap.getDeviceInfo(camera_node)[4]

    @classmethod
    def get_PID(cls, camera_node: int) -> str:
        """
          Used to get the PID of the camera for the  give node
           Parameters:
           - node (int): camera node which was get using the get devices.
           Returns:
           str: Device path.
                           """

        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer")
        cls.cap = cv2.VideoCapture()
        # for i in range(cls.cap.getDevices()[1]):
        #     if camera_name == cls.cap.getDeviceInfo(i)[1]:
        return cls.cap.getDeviceInfo(camera_node)[3]

    @classmethod
    def get_VID(cls, camera_node: int) -> str:

        """
          Used to get the VID of the camera for the  give node
           Parameters:
           - node (int): camera node which was get using the get devices.
           Returns:
           str: Device path.
                            """
        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer")
        cls.cap = cv2.VideoCapture()
        # for i in range(cls.cap.getDevices()[1]):
        #     if camera_name == cls.cap.getDeviceInfo(i)[1]:
        return cls.cap.getDeviceInfo(camera_node)[2]

    @classmethod
    # Getting the Firmware version from the camera.........
    def get_firmware_version(cls, camera_node: int):
        """
            Used to get the Firmware version of the e-con camera for the  give node using HID commands.
             Parameters:
             - node (int): camera node which was get using the get devices.
             Returns:
             str: Firmware version.
                              """
        var = None
        error_code = 101
        error_message = "Unable to get the Firmware for the given camera."
        CustomError(error_code, error_message)
        cls.firmware = None

        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer")
        try:
            # Open the device using path
            cls.devices = hid.enumerate(
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[2], 16),
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[3], 16))
            if not cls.devices:
                print(f"{RED_TEXT}Error - Unable to get the Firmware for the given camera.{RESET_COLOR}")
                return None
            cls.device = hid.device()
            cls.device.open_path(cls.devices[0]["path"])
            # Refer the HID command.
            command = [0x00, 0x40]
            # Send the command to the camera
            cls.device.write(command)
            # Read the response (adjust the length as per your expected response)
            response = cls.device.read(65, 1000)
            SDK_VER = (response[3] << 8) + response[4]
            SVN_VER = (response[5] << 8) + response[6]
            pMajorVersion = response[1]
            pMinorVersion1 = response[2]
            cls.firmware = str(pMajorVersion) + "." + str(pMinorVersion1) + "." + str(SDK_VER) + "." + str(SVN_VER)
            print("Firmware version :", cls.firmware)
        except ValueError:
            print(f"Error code: {error_code} - {error_message}. Unable to get the Firmware...")
        return cls.firmware

    @classmethod
    def getting_unique_ID(cls, camera_node: int):

        """
            Used to get the Unique ID of the e-con camera for the  give node using HID commands.
             Parameters:
             - node (int): camera node which was get using the get devices.
             Returns:
             str: Unique ID.
                              """

        error_code = 101
        error_message = "Camera not found"
        CustomError(error_code, error_message)
        cls.serial_number = None
        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer")
        try:
            # Open the device using path
            cls.devices = hid.enumerate(
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[2], 16),
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[3], 16))
            if not cls.devices:
                print(f"{RED_TEXT}Error - Unable to get the Firmware for the given camera.{RESET_COLOR}")
                return None
            cls.device = hid.device()
            cls.device.open_path(cls.devices[0]["path"])
            command = [0x00, 0x41, 0x01, 0x00, 0x00, 0x00]
            cls.device.write(command)
            response = cls.device.read(65, 1000)
            cls.serial_number = format(response[1], '02X') + format(response[2], '02X') + format(response[3],
                                                                                                 '02X') + format(
                response[4], '02X')
            print("Serial Number :", cls.serial_number)
        except ValueError:
            print(f"Error code: {error_code} - {error_message}. Unable to get the Firmware...")
        return cls.serial_number

    @classmethod
    def hid_var(cls, camera_node: int, cam_ID: int, set_parameter_ID: int, min_range: int, max_range: int, step: int,
                get_parameter_ID: int, hold: int):

        """

        Used to changing the HID parameter of the e-con camera for the  give node using HID commands. Parameters: -
        camera_node (int): camera node which was get using the get devices. - cam_ID (int): camera ID which was in
        the e-con HID documents. - set_parameter_ID (int): Used to set the parameter value using Parameter ID which
        was in the e-con HID documents. - min_range (int): Minimum supported range in the e-con HID documents. -
        max_range (int): Maximum supported range in the e-con HID documents. - step (int): Used to varying the
        parameter in the given step value. - get_parameter_ID (int): Used to get the parameter using Parameter ID
        which was in the e-con HID documents. - hold (int): After applying the parameter it should wait for given
        duration(in seconds) Returns: str: HID control value.

        """

        error_code = 101
        error_message = "Camera not found"
        CustomError(error_code, error_message)
        try:
            # Open the device using path
            cls.devices = hid.enumerate(
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[2], 16),
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[3], 16))
            if not cls.devices:
                print(f"{RED_TEXT}Error - Unable to get the Firmware for the given camera.{RESET_COLOR}")
                return None
            cls.device = hid.device()
            cls.device.open_path(cls.devices[0]["path"])
            first_byte = 0x00
            second_byte = cam_ID
            third_byte = set_parameter_ID
            if min_range > max_range:
                step = -step

            for i in range(min_range, max_range + 1, step):
                # fourth_byte = b''
                # hexadecimal_value = hex(i)
                # fourth_byte += str(hexadecimal_value).encode('utf-8')  # Convert each number to bytes and append
                command = [first_byte, second_byte, third_byte, i]
                # command = [0x00, 0XBA, 0x08, 0x03]
                cls.device.write(command)
                response = cls.device.read(65, 1000)
                command = [first_byte, second_byte, get_parameter_ID]
                cls.device.write(command)
                response = cls.device.read(65, 1000)
                print(response)
                time.sleep(hold)

            cls.set_hid_default(camera_node, cam_ID)

        except ValueError:
            print(f"Error code: {error_code} - {error_message}. Unable to set the value!")
        # return response

    @classmethod
    def set_hid(cls, camera_node: int, byte_0=0x00, byte_1=0x00, byte_2=0x00, byte_3=0x00, byte_4=0x00, byte_5=0x00,
                byte_6=0x00, byte_7=0x00, byte_8=0x00, byte_9=0x00, byte_10=0x00, byte_11=0x00, byte_12=0x00,
                byte_13=0x00, byte_14=0x00, byte_15=0x00, byte_16=0x00, byte_17=0x00, byte_18=0x00, byte_19=0x00,
                byte_20=0x00, byte_21=0x00, byte_22=0x00, byte_23=0x00, byte_24=0x00, byte_25=0x00,
                byte_26=0x00, byte_27=0x00, byte_28=0x00, byte_29=0x00, byte_30=0x00, byte_31=0x00, byte_32=0x00,
                byte_33=0x00, byte_34=0x00, byte_35=0x00, byte_36=0x00, byte_37=0x00, byte_38=0x00, byte_39=0x00,
                byte_40=0x00, byte_41=0x00, byte_42=0x00, byte_43=0x00, byte_44=0x00, byte_45=0x00, byte_46=0x00,
                byte_47=0x00,  byte_48=0x00,  byte_49=0x00,  byte_50=0x00,  byte_51=0x00,  byte_52=0x00,
                byte_53=0x00, byte_54=0x00, byte_55=0x00, byte_56=0x00, byte_57=0x00, byte_58=0x00, byte_59=0x00,
                byte_60=0x00, byte_61=0x00, byte_62=0x00, byte_63=0x00, byte_64=0x00):

        """

        Used to changing the HID parameter of the e-con camera for the  give node using HID commands. Parameters: -
        camera_node (int): camera node which was get using the get devices. - cam_ID (int): camera ID which was in
        the e-con HID documents. - set_parameter_ID (int): Used to set the parameter value using Parameter ID which
        was in the e-con HID documents. - get_parameter_ID (int): Used to get the parameter using Parameter ID which
        was in the e-con HID documents. Returns: str: HID control value.

        """

        global response
        error_code = 101
        error_message = "Camera not found"
        CustomError(error_code, error_message)
        try:
            # Open the device using path
            cls.devices = hid.enumerate(
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[2], 16),
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[3], 16))
            if not cls.devices:
                print(f"{RED_TEXT}Error - Unable to set the value in the camera.{RESET_COLOR}")
                return None
            cls.device = hid.device()
            cls.device.open_path(cls.devices[0]["path"])
            set_command = [0x00, byte_0, byte_1, byte_2, byte_3, byte_4, byte_5, byte_6, byte_7, byte_8, byte_9,
                           byte_10, byte_11, byte_12, byte_13, byte_14, byte_15, byte_16, byte_17, byte_18, byte_19,
                           byte_20, byte_21, byte_22, byte_23, byte_24, byte_25, byte_26, byte_27, byte_28, byte_29,
                           byte_30, byte_31, byte_32, byte_33, byte_34, byte_35, byte_36, byte_37, byte_38, byte_39,
                           byte_40, byte_41, byte_42, byte_43, byte_44, byte_45, byte_46, byte_47,  byte_48,  byte_49,
                           byte_50, byte_51,  byte_52, byte_53, byte_54, byte_55, byte_56, byte_57, byte_58, byte_59,
                           byte_60, byte_61, byte_62, byte_63, byte_64]
            cls.device.write(set_command)
            return 0
        except ValueError:
            print(f"Error code: {error_code} - {error_message}. Unable to set the value!")
        # return response

    @classmethod
    def get_hid(cls, camera_node: int, byte_0=0x00, byte_1=0x00, byte_2=0x00, byte_3=0x00, byte_4=0x00, byte_5=0x00,
                byte_6=0x00, byte_7=0x00, byte_8=0x00, byte_9=0x00, byte_10=0x00, byte_11=0x00, byte_12=0x00,
                byte_13=0x00, byte_14=0x00, byte_15=0x00, byte_16=0x00, byte_17=0x00, byte_18=0x00, byte_19=0x00,
                byte_20=0x00, byte_21=0x00, byte_22=0x00, byte_23=0x00, byte_24=0x00, byte_25=0x00,
                byte_26=0x00, byte_27=0x00, byte_28=0x00, byte_29=0x00, byte_30=0x00, byte_31=0x00, byte_32=0x00,
                byte_33=0x00, byte_34=0x00, byte_35=0x00, byte_36=0x00, byte_37=0x00, byte_38=0x00, byte_39=0x00,
                byte_40=0x00, byte_41=0x00, byte_42=0x00, byte_43=0x00, byte_44=0x00, byte_45=0x00, byte_46=0x00,
                byte_47=0x00,  byte_48=0x00,  byte_49=0x00,  byte_50=0x00,  byte_51=0x00,  byte_52=0x00,
                byte_53=0x00, byte_54=0x00, byte_55=0x00, byte_56=0x00, byte_57=0x00, byte_58=0x00, byte_59=0x00,
                byte_60=0x00, byte_61=0x00, byte_62=0x00, byte_63=0x00, byte_64=0x00):

        """

        Used to changing the HID parameter of the e-con camera for the  give node using HID commands. Parameters: -
        camera_node (int): camera node which was get using the get devices. - cam_ID (int): camera ID which was in
        the e-con HID documents. - set_parameter_ID (int): Used to set the parameter value using Parameter ID which
        was in the e-con HID documents. - get_parameter_ID (int): Used to get the parameter using Parameter ID which
        was in the e-con HID documents. Returns: str: HID control value.

        """

        global response
        error_code = 101
        error_message = "Camera not found"
        CustomError(error_code, error_message)
        try:
            # Open the device using path
            cls.devices = hid.enumerate(
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[2], 16),
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[3], 16))
            if not cls.devices:
                print(f"{RED_TEXT}Error - Unable to set the value in the camera.{RESET_COLOR}")
                return None
            cls.device = hid.device()
            cls.device.open_path(cls.devices[0]["path"])
            get_command = [0x00, byte_0, byte_1, byte_2, byte_3, byte_4, byte_5, byte_6, byte_7, byte_8, byte_9,
                           byte_10, byte_11, byte_12, byte_13, byte_14, byte_15, byte_16, byte_17, byte_18, byte_19,
                           byte_20, byte_21, byte_22, byte_23, byte_24, byte_25, byte_26, byte_27, byte_28, byte_29,
                           byte_30, byte_31, byte_32, byte_33, byte_34, byte_35, byte_36, byte_37, byte_38, byte_39,
                           byte_40, byte_41, byte_42, byte_43, byte_44, byte_45, byte_46, byte_47, byte_48, byte_49,
                           byte_50, byte_51, byte_52, byte_53, byte_54, byte_55, byte_56, byte_57, byte_58, byte_59,
                           byte_60, byte_61, byte_62, byte_63, byte_64]

            cls.device.write(get_command)
            response = cls.device.read(65, 1000)
            return response
        except ValueError:
            print(f"Error code: {error_code} - {error_message}. Unable to set the value!")

    @classmethod
    def set_hid_default(cls, camera_node: int, cam_ID: int):

        """

        Used to changing the HID parameter of the e-con camera for the  give node using HID commands. Parameters: -
        camera_node (int): camera node which was get using the get devices. - cam_ID (int): camera ID which was in
        the e-con HID documents. - set_parameter_ID (int): Used to set the parameter value using Parameter ID which
        was in the e-con HID documents. - min_range (int): Minimum supported range in the e-con HID documents. -
        max_range (int): Maximum supported range in the e-con HID documents. - step (int): Used to varying the
        parameter in the given step value. - get_parameter_ID (int): Used to get the parameter using Parameter ID
        which was in the e-con HID documents. - hold (int): After applying the parameter it should wait for given
        duration(in seconds) Returns: str: HID control value.

        """

        global response
        error_code = 101
        error_message = "Camera not found"
        CustomError(error_code, error_message)

        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer")

        if not isinstance(cam_ID, int):
            raise TypeError("cam_ID must be an integer")

        try:
            # Open the device using path
            cls.devices = hid.enumerate(
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[2], 16),
                int('0x' + cam_list[cam_index.index(camera_node)].getDeviceInfo(camera_node)[3], 16))
            if not cls.devices:
                print(f"{RED_TEXT}Error - Unable to get the Firmware for the given camera.{RESET_COLOR}")
                return None
            cls.device = hid.device()
            cls.device.open_path(cls.devices[0]["path"])
            first_byte = 0x00
            second_byte = cam_ID
            third_byte = 0xFF

            command = [first_byte, second_byte, third_byte]
            # command = [0x00, 0XBA, 0x08, 0x03]
            cls.device.write(command)
            response = cls.device.read(65, 1000)
        except:
            print("fail")
        return response

    @classmethod
    def getting_supported_uvc_parameter(cls, camera_node: int()):

        """
           Used to getting the UVC supported features of the camera for the  give node.
            Parameters:
            - camera_node (int): camera node which was get using the get devices.
            Returns:
            Dict: Supported UVC features along with minimum, maximum, step, default and current value.
        """

        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer")

        cls.possibleuvclist = ['brightness', 'contrast', 'saturation', 'sharpness', 'hue', 'white_balance_blue_u',
                               'gamma', 'exposure',
                               'gain', 'zoom', 'pan', 'tilt',
                               'backlight', 'focus', 'roll', 'iris']
        cls.supported_uvc_properties = {}
        cls.minimum = -1
        cls.maximum = -1
        cls.stepping_delta = -1
        cls.supported_mode = -1
        cls.current_value = -1
        cls.current_mode = -1
        cls.default_value = -1
        cls.bri_prop = []
        cls.con_prop = []
        cls.sat_prop = []
        cls.sharp_prop = []
        cls.hue_prop = []
        cls.wb_prop = []
        cls.gamma_prop = []
        cls.exp_prop = []
        cls.gain_prop = []
        cls.zoom_prop = []
        cls.pan_prop = []
        cls.tilt_prop = []
        cls.backlight_prop = []
        cls.focus_prop = []
        cls.roll_prop = []
        cls.iris_prop = []
        cls.capture_properties = ['msec', 'frames', 'ratio', 'width', 'height', 'fps', 'fourcc', 'count', 'format',
                                  'mode', 'brightness',
                                  'contrast', 'saturation', 'hue', 'gain', 'exposure', 'convert_rgb',
                                  'white_balance_blue_u', 'rectification',
                                  'monochrome', 'sharpness', 'auto_exposure', 'gamma', 'temperature', 'trigger',
                                  'trigger_delay',
                                  'white_balance_red_v', 'zoom', 'focus', 'guid', 'iso_speed', '', 'backlight', 'pan',
                                  'tilt', 'roll', 'iris',
                                  'settings', 'buffersize', 'autofocus']
        cls.uvc_propID = [cls.bri_prop, cls.con_prop, cls.sat_prop, cls.sharp_prop, cls.hue_prop, cls.wb_prop,
                          cls.gamma_prop, cls.exp_prop, cls.gain_prop, cls.zoom_prop, cls.pan_prop, cls.tilt_prop,
                          cls.backlight_prop, cls.focus_prop, cls.roll_prop, cls.iris_prop]

        cls.supported_properties = []
        cls.support_mode = []
        cls.feature_list = []
        print("-----------Supported UVC parameter-------------")
        x = PrettyTable()
        x.field_names = ["Parameter name", "Min value", "Max value", "Step value", "Default value", "Current value"]
        # checking the availability of the UVC parameter for the connected parameter
        for i in range(38):
            get_availability_properties = (cam_list[cam_index.index(int(camera_node))].get(i))  # 94
            value_notsupported_properties = -1.0
            if get_availability_properties != value_notsupported_properties:
                cls.supported_properties.append(cls.capture_properties[i])
            cls.available_properties = (
                cls.cap.get(i, cls.minimum, cls.maximum, cls.stepping_delta, cls.supported_mode,
                            cls.current_value, cls.current_mode, cls.default_value))  # 132

            if cls.available_properties[0]:
                cls.prop_id = list(cls.available_properties)
                cls.prop_id.append(cls.capture_properties[i])

                if cls.prop_id[4] == 3:
                    cls.support_mode.append(cls.prop_id[-1])

                for uvc_name in range(len(cls.possibleuvclist)):

                    if cls.prop_id[-1] == cls.possibleuvclist[uvc_name]:
                        # cls.feature_list.append(cls.prop_id[-1])
                        cls.uvc_propID[uvc_name].append(cls.prop_id[1])
                        cls.uvc_propID[uvc_name].append(cls.prop_id[2])
                        cls.uvc_propID[uvc_name].append(cls.prop_id[3])
                        cls.uvc_propID[uvc_name].append(cls.prop_id[5])
                        cls.uvc_propID[uvc_name].append(cls.prop_id[7])
                        cls.uvc_propID[uvc_name].append(cls.prop_id[6])
                        cls.uvc_propID[uvc_name].append(cls.prop_id[4])
                        cls.supported_uvc_properties[str(cls.prop_id[-1])] = cls.uvc_propID[uvc_name]
                        x.add_row([cls.prop_id[-1], str(cls.prop_id[1]), str(cls.prop_id[2]), str(cls.prop_id[3]),
                                   str(cls.prop_id[5]), str(cls.prop_id[7])])
        print(x)
        return cls.supported_uvc_properties

    @classmethod
    def get_resolution(cls, camera_node: int):
        """
             Used to getting the supported resolutions of the camera for the  give node.
              Parameters:
              - camera_node (int): camera node which was get using the get devices.
              Returns:
              list: Supported resolutions along with Formats, width, height and FPS.
              """

        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer")
        y = PrettyTable()
        supported_resolution = []
        # cls.cap = cv2.VideoCapture()
        # for i in range(cls.cap.getDevices()[1]):
        #     if cam_node == cls.cap.getDeviceInfo(i)[1]:
        #         cls.cap = cv2.VideoCapture(i)
        print("------Supported Resolutions--------")
        y.field_names = ["Format Type", "Height", "Width", "FPS"]
        for res in range(cam_list[cam_index.index(int(camera_node))].getFormats()[1]):
            supported_resolution.append(cls.cap.getFormatType(res)[1:])
            y.add_row([str(cls.cap.getFormatType(res)[1]), str(cls.cap.getFormatType(res)[2]),
                       str(cls.cap.getFormatType(res)[3]), str(cls.cap.getFormatType(res)[4])])
            # print("Format:"+str(cls.cap.getFormatType(res)[1])+" Height:"+str(cls.cap.getFormatType(res)[2])+ "
            # Width:"+str(cls.cap.getFormatType(res)[3]) +" FPS:"+str(cls.cap.getFormatType(res)[4]))
        print(y)
        return supported_resolution

    @classmethod
    def set_resolution(cls, camera_node: int, height=0, width=0, Format="", FPS=0):

        """
             Used to set the resolutions of the camera for the  give node.
              Parameters:
              - camera_node (int): camera node which was get using the get devices.
              - height (int): Height of the resolution.
              - width (int): Width of the resolution.
              - Format (int): Format of the resolution.
              - FPS (int): FPS of the resolution.
              Returns:
              bool: True/False.
                      """

        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer")
        if not isinstance(height, int):
            raise TypeError("height must be an integer")
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        if not isinstance(Format, str):
            raise TypeError("Format must be a string")
        if not isinstance(FPS, int):
            raise TypeError("FPS must be an integer")

        resolution = (True, Format, height, width, FPS)
        # print(resolution, cam_list[cam_index.index(int(node))].getFormats()[1])
        # cls.cap.setFormatType(5)
        if Format == '' and FPS != 0:
            cam_list[cam_index.index(int(camera_node))].set(3, height)
            cam_list[cam_index.index(int(camera_node))].set(4, width)
            cam_list[cam_index.index(int(camera_node))].set(cv2.CAP_PROP_FPS, FPS)
        elif Format == '' and FPS == 0:
            cam_list[cam_index.index(int(camera_node))].set(3, height)
            cam_list[cam_index.index(int(camera_node))].set(4, width)
        elif Format != '' and FPS == 0:
            cam_list[cam_index.index(int(camera_node))].set(3, height)
            cam_list[cam_index.index(int(camera_node))].set(4, width)
            cam_list[cam_index.index(int(camera_node))].set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*Format))
        else:
            for res in range(cam_list[cam_index.index(int(camera_node))].getFormats()[1]):
                if resolution == cam_list[cam_index.index(int(camera_node))].getFormatType(res):
                    cam_list[cam_index.index(int(camera_node))].setFormatType(res)
                    print(res)
                    # print(cam_list[cam_index.index(int(node))].get(3),cam_list[cam_index.index(int(node))].get(4))
                    return True

    @classmethod
    def uvc_var(cls, camera_node: int, parameter_name: str, min: int, max: int, step: int, hold: int, image_save=False,
                save_format='jpg'):

        """

        Used to varying the give parameter minimum to maximum range with the given step size and save the image in
        the given image save format. Parameters: - camera_node (int): camera node which was get using the get
        devices. - parameter_name (str): Supported UVC parameter name. - min (int): Minimum range of the give
        parameter. - max (int): Maximum range of the give parameter. - step (int): change the value using the step.
        -hold (int): After set the UVC parameter preview will hold for given time duration in seconds. -image_save (
        bool): It used to give input as user need to save the image or not. -save_format (str): Images will be saving
        in the give save format. Returns: bool: True/False.

        """

        supported_image_save_format = ['bmp', 'jpg', 'raw', 'png']
        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer.")
        if not isinstance(parameter_name, str):
            raise TypeError("parameter_name must be an string.")
        if not isinstance(min, int):
            raise TypeError("min must be an integer.")
        if not isinstance(max, int):
            raise TypeError("max must be a integer.")
        if not isinstance(step, int):
            raise TypeError("step must be an integer.")
        if not isinstance(hold, int):
            raise TypeError("hold must be an integer.")
        if not isinstance(image_save, bool):
            raise TypeError("image_save must be an boolean.")
        if not isinstance(save_format, str):
            raise TypeError("image_save must be an string.")

        time.sleep(1)
        UVC_PARAMETER_NAMES = ['BRIGHTNESS', 'CONTRAST', 'SHARPNESS', 'SATURATION', 'HUE', 'WB', 'GAMMA', 'EXPOSURE',
                               'GAIN', 'ZOOM', 'PAN', 'TILT',
                               'FOCUS', 'BACKLIGHT', 'ROLL', 'IRIS']
        CAP_UVCPROPERTIES_NAME = [cv2.CAP_PROP_BRIGHTNESS, cv2.CAP_PROP_CONTRAST, cv2.CAP_PROP_SHARPNESS,
                                  cv2.CAP_PROP_SATURATION, cv2.CAP_PROP_HUE, cv2.CAP_PROP_WHITE_BALANCE_BLUE_U,
                                  cv2.CAP_PROP_GAMMA, cv2.CAP_PROP_EXPOSURE, cv2.CAP_PROP_GAIN, cv2.CAP_PROP_ZOOM,
                                  cv2.CAP_PROP_PAN, cv2.CAP_PROP_TILT, cv2.CAP_PROP_BACKLIGHT, cv2.CAP_PROP_FOCUS,
                                  cv2.CAP_PROP_ROLL, cv2.CAP_PROP_IRIS]
        if parameter_name.upper() in UVC_PARAMETER_NAMES:
            UVC_PARAMETER_NAMES.index(parameter_name.upper())

        for i in range(min, max, step):

            cam_list[cam_index.index(int(camera_node))].set(
                CAP_UVCPROPERTIES_NAME[UVC_PARAMETER_NAMES.index(parameter_name.upper())], i)
            # if cam_list[cam_index.index(int(node))].isOpened():
            try:
                if cls.frame.any():
                    if image_save:
                        if save_format.lower() in supported_image_save_format:
                            cv2.imwrite(parameter_name + "_" + str(i) + "." + save_format, cls.frame)
                        else:
                            raise ValueError("Unknown image save format!")

            except AttributeError:
                raise TypeError("Unable to read the frame!")

            time.sleep(hold)

            print(parameter_name.upper(), cam_list[cam_index.index(int(camera_node))].get(
                CAP_UVCPROPERTIES_NAME[UVC_PARAMETER_NAMES.index(parameter_name.upper())]))
            if cam_list[cam_index.index(int(camera_node))].get(
                    CAP_UVCPROPERTIES_NAME[UVC_PARAMETER_NAMES.index(parameter_name.upper())]) == -1:
                print("Unable to set the " + str(parameter_name) + " value.")
        cam_list[cam_index.index(int(camera_node))].set(
            CAP_UVCPROPERTIES_NAME[UVC_PARAMETER_NAMES.index(parameter_name.upper())], 0)

    @classmethod
    def uvc_multiple_var(cls, camera_node: int, parameter_name1: str, min1: int, max1: int, step1: int,
                         parameter_name2: str,
                         min2: int, max2: int, step2: int, hold: int, image_save=False, save_format='jpg'):

        """
           Used to varying the multiple UVC parameter minimum to maximum range and vice versa with the given step size
           and save the image in the given image save format.
            Parameters:
            - camera_node (int): camera node which was get using the get devices.
            - parameter_name1 (str): Supported UVC first parameter name.
            - min1 (int): Minimum range of the give first parameter.
            - max1 (int): Maximum range of the give first parameter.
            - step1 (int): change the value for first parameter using the step1.
            - parameter_name2 (str): Supported UVC second parameter name.
            - min2 (int): Minimum range of the give second parameter.
            - max2 (int): Maximum range of the give second parameter.
            - step2 (int): change the value for second parameter using the step1.
            -hold (int): After set the UVC parameter preview will hold for given time duration in seconds.
            -image_save (bool): It used to give input as user need to save the image or not.
            -save_format (str): Images will be saving in the give save format.
            Returns:
            bool: True/False.
                            """
        supported_image_save_format = ['bmp', 'jpg', 'raw', 'png']
        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer.")
        if not isinstance(parameter_name1, str):
            raise TypeError("parameter_name1 must be an string.")
        if not isinstance(min1, int):
            raise TypeError("min1 must be an integer.")
        if not isinstance(max1, int):
            raise TypeError("max1 must be a integer.")
        if not isinstance(step1, int):
            raise TypeError("step1 must be an integer.")
        if not isinstance(parameter_name2, str):
            raise TypeError("parameter_name2 must be an string.")
        if not isinstance(min2, int):
            raise TypeError("min2 must be an integer.")
        if not isinstance(max2, int):
            raise TypeError("max2 must be a integer.")
        if not isinstance(step2, int):
            raise TypeError("step2 must be an integer.")
        if not isinstance(hold, int):
            raise TypeError("hold must be an integer.")
        if not isinstance(image_save, bool):
            raise TypeError("image_save must be an boolean.")
        if not isinstance(save_format, str):
            raise TypeError("image_save must be an string.")

        if min1 > max1:
            step1 = -step1
        if min2 > max2:
            step2 = -step2
        UVC_PARAMETER_NAMES = ['BRIGHTNESS', 'CONTRAST', 'SHARPNESS', 'SATURATION', 'HUE', 'WB', 'GAMMA', 'EXPOSURE',
                               'GAIN', 'ZOOM', 'PAN', 'TILT',
                               'FOCUS', 'BACKLIGHT', 'ROLL', 'IRIS']
        CAP_UVCPROPERTIES_NAME = [cv2.CAP_PROP_BRIGHTNESS, cv2.CAP_PROP_CONTRAST, cv2.CAP_PROP_SHARPNESS,
                                  cv2.CAP_PROP_SATURATION, cv2.CAP_PROP_HUE, cv2.CAP_PROP_WHITE_BALANCE_BLUE_U,
                                  cv2.CAP_PROP_GAMMA, cv2.CAP_PROP_EXPOSURE, cv2.CAP_PROP_GAIN, cv2.CAP_PROP_ZOOM,
                                  cv2.CAP_PROP_PAN, cv2.CAP_PROP_TILT, cv2.CAP_PROP_BACKLIGHT, cv2.CAP_PROP_FOCUS,
                                  cv2.CAP_PROP_ROLL, cv2.CAP_PROP_IRIS]
        if parameter_name1.upper() in UVC_PARAMETER_NAMES:
            UVC_PARAMETER_NAMES.index(parameter_name1.upper())

        while (min1 <= max1 or min2 <= max2) or (min1 >= max1 or min2 >= max2):
            if camera_node in cam_list:
                cam_list[cam_index.index(int(camera_node))].set(
                    CAP_UVCPROPERTIES_NAME[UVC_PARAMETER_NAMES.index(parameter_name1.upper())], min1)
                cam_list[cam_index.index(int(camera_node))].set(
                    CAP_UVCPROPERTIES_NAME[UVC_PARAMETER_NAMES.index(parameter_name2.upper())], min2)

                try:
                    if image_save:
                        if save_format.lower() in supported_image_save_format:
                            cv2.imwrite(
                                parameter_name1 + "_" + str(min1) + "_" + parameter_name2 + str(min2) + "_" + str()
                                + "." + save_format, cls.frame)
                        else:
                            raise ValueError("Unknown image save format!")

                except AttributeError:
                    raise TypeError("Unable to read the frame!")
                except ValueError:
                    raise ValueError("Camera not assigned!")
                time.sleep(hold)
                print(parameter_name1, cam_list[cam_index.index(int(camera_node))].get(
                    CAP_UVCPROPERTIES_NAME[UVC_PARAMETER_NAMES.index(parameter_name1.upper())]))
                print(parameter_name2, cam_list[cam_index.index(int(camera_node))].get(
                    CAP_UVCPROPERTIES_NAME[UVC_PARAMETER_NAMES.index(parameter_name2.upper())]))

                min1 += step1
                min2 += step2
            else:
                raise ValueError("Camera not assigned!")

    @classmethod
    def convert_y16_to_rgb(cls, frame):
        '''
        Method Name: convert_y16_to_rgb
        Description: This method converts y16 rgb or y8 for rendering and saving image.
        :param frame: frame which needs to be converted
        :type frame: Mat
        :return: the converted frame
        :rtype: Mat
        '''
        # if cls.y16CameraFlag == cls.SEE3CAM_20CUG:
        return cv2.convertScaleAbs(frame, 0.2490234375)


    @classmethod
    def convert_y12_to_y8(cls, frame):
        '''
        Method Name: convert_y12_to_y8
        Description: This method converts the y12 frame to y8 frame
        :param frame:  which needs to be converted
        :type frame: Mat
        :return: the converted frame
        :rtype: Mat
        '''
        try:
            y8_frame_height = frame.shape[0]
            y8_frame_width = frame.shape[1]
            y8_frame = np.zeros(shape=(y8_frame_height, y8_frame_width), dtype=np.uint8)
            raw_bytes = frame.tobytes() #converting two dimensional mat data to byte array
            # print(raw_bytes)
            row = frame.shape[0]
            column = frame.shape[1]
            filtered_bytes = np.frombuffer(raw_bytes, dtype=np.uint8)
            filtered_bytes = np.reshape(filtered_bytes, (-1, 3))
            filtered_bytes = np.delete(filtered_bytes,2,1)
            filtered_bytes= np.reshape(filtered_bytes,-1)
            m=0
            for i in range(0, row):
                # print(i)
                y8_frame[i,] = filtered_bytes[m:m+column]
                m += column
            return y8_frame  # Converting back to two dimensional Mat
        except:
            print("unable to convert")

    @classmethod
    def show_preview(cls, node, duration, show_FPS):

        global stop_time
        try:
            cls.frame = None
            time_second = 1
            frame_count = 0
            fps_show_time = time.time() + time_second
            fps = ""
            if duration != 0:
                stop_time = int(time.time() + duration)
            while True:
                ret, cls.frame = cam_list[cam_index.index(int(node))].read()
                cls.frame.any()
                frame_count += 1

                if time.time() > fps_show_time:
                    fps = frame_count
                    frame_count = 0
                    fps_show_time = time.time() + time_second
                if show_FPS:
                    cv2.putText(cls.frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if "".join(
                        [chr((int(cam_list[cam_index.index(int(node))].get(cv2.CAP_PROP_FOURCC)) >> 8 * i)
                             & 0xFF) for i in range(4)]) == 'UYVY':
                    frame1 = cv2.cvtColor(cls.frame, cv2.COLOR_YUV2BGR_UYVY)
                elif "".join(
                        [chr((int(cam_list[cam_index.index(int(node))].get(cv2.CAP_PROP_FOURCC)) >> 8 * i)
                             & 0xFF) for i in range(4)]) == 'Y12':
                    frame1 = cls.convert_y12_to_y8(cls.frame)
                elif "".join(
                        [chr((int(cam_list[cam_index.index(int(node))].get(cv2.CAP_PROP_FOURCC)) >> 8 * i)
                             & 0xFF) for i in range(4)]).strip() == 'Y16':
                    frame1 = cls.convert_y16_to_rgb(cls.frame)
                else:
                    frame1 = cls.frame

                try:
                    cv2.imshow("Preview - " + str(node), frame1)
                except cv2.error:
                    pass
                if duration != 0:
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    if stop_time <= int(time.time()):
                        break
                else:
                    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('Q'):
                        break

                # return frame1
        except AttributeError:
            cv2.destroyAllWindows()
            print(f"{RED_TEXT}Error: Please assign the camera!!!{RESET_COLOR}")
        except ValueError:
            cv2.destroyAllWindows()
            print(f"{RED_TEXT}Error in streaming: Please assign the camera!!!{RESET_COLOR}")

    @classmethod
    def streaming(cls, camera_node=-1, duration=0, show_FPS=False):
        """
         Used to stream the camera, and it shows the FPS on the top of the preview
          Parameters:
          - camera_node (int): camera node which was get using the get devices.
          - duration (int): Stream the camera for given duration in seconds.
          - show_FPS (bool): If it is True. It shows the FPS
          Returns:
          bool: frame
        """

        if not isinstance(camera_node, int):
            raise TypeError("camera_node must be an integer.")
        if not isinstance(duration, int):
            raise TypeError("Duration must be an integer.")
        if not isinstance(show_FPS, bool):
            raise TypeError("show_FPS must be an boolean.")
        globals()[f"Thread_{camera_node}"] = Thread(target=cls.show_preview, args=(camera_node, duration, show_FPS))
        globals()[f"Thread_{camera_node}"].start()
