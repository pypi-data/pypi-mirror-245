import logging

from .wsHandle import InoDriveWS
from .file import File
from .discoverWs import DiscoverWs
from .IO import IO
from .sysControl import SysControl
from .userApp import UserApp


class InoDrive(object):
    def __init__(self, **kwargs):
        logging.debug('Create InoDrive instance...')
        self._auto_connect = kwargs.get('autoConnect', False)

        # ==============================================================================================================
        # OBJ INSTANCES BEGIN
        # ==============================================================================================================
        self._connection_handle = InoDriveWS(**kwargs)
        self.File = File(connection_handle=self._connection_handle, **kwargs)
        self.Discover = DiscoverWs(connection_handle=self._connection_handle, **kwargs)
        self.IO = IO(connection_handle=self._connection_handle, **kwargs)
        self.SysControl = SysControl(connection_handle=self._connection_handle, **kwargs)
        self.UserApp = UserApp(connection_handle=self._connection_handle, **kwargs)
        # ==============================================================================================================
        # OBJ INSTANCES END
        # ==============================================================================================================

        # ==============================================================================================================
        # CONNECTION BEGIN
        # ==============================================================================================================
        self.on = self._connection_handle.on
        self.connected = self._connection_handle.connected
        self.connect = self._connection_handle.connect
        self.disconnect = self._connection_handle.disconnect
        self.set_target = self._connection_handle.set_target
        # ==============================================================================================================
        # CONNECTION END
        # ==============================================================================================================

        # ==============================================================================================================
        # SYS CONTROL BEGIN
        # ==============================================================================================================
        # self.get_discover_info = self.Discover.get_info
        # self.take_control = self.SysControl.take_control
        # ==============================================================================================================
        # SYS CONTROL END
        # ==============================================================================================================

        # ==============================================================================================================
        # FILE BEGIN
        # ==============================================================================================================
        # self.file_read = self.File.read
        # self.file_write = self.File.write
        # self.delete_uapp = self.File.delete_uapp
        # self.upload_user_app = self.File.upload_user_app
        # self.upload_firmware = self.File.upload_firmware
        # self.read_module_config = self.File.read_module_config
        # self.write_module_config = self.File.write_module_config
        # ==============================================================================================================
        # FILE END
        # ==============================================================================================================

        # ==============================================================================================================
        # IO BEGIN
        # ==============================================================================================================
        # self.get_inputs_data = self.IO.get_inputs_data
        # self.get_outputs_data = self.IO.get_outputs_data
        # self.get_input = self.IO.get_input
        # self.get_output = self.IO.get_output_fault
        # self.get_output_fault = self.IO.get_output_fault
        # self.get_holding_brake_fault = self.IO.get_holding_brake_fault
        # self.get_safety_input = self.IO.get_safety_input
        # self.get_analog_input = self.IO.get_analog_input
        # self.set_input_polarity = self.IO.set_input_polarity
        # self.set_output = self.IO.set_output
        # self.set_holding_brake = self.IO.set_holding_brake
        # ==============================================================================================================
        # IO END
        # ==============================================================================================================

        # ==============================================================================================================
        # USER APP BEGIN
        # ==============================================================================================================
        # self.start_poll = self.UserApp.start_poll
        # self.stop_poll = self.UserApp.stop_poll
        # self.get_variable = self.UserApp.get_variable
        # self.get_all_variables = self.UserApp.get_all_variables
        # self.get_variable_list = self.UserApp.get_variable_list
        # # todo: updateVariablesList has implementation in the JS API
        # self.read_var = self.UserApp.read_var
        # self.write_var = self.UserApp.write_var
        # self.get_var = self.UserApp.get_var
        # self.set_var = self.UserApp.set_var
        # ==============================================================================================================
        # USER APP END
        # ==============================================================================================================

        if self._auto_connect:
            self._connection_handle.connect()

    def __del__(self):
        self.dispose()

    def dispose(self):
        if self.UserApp:
            self.UserApp.dispose()

        if self._connection_handle:
            self._connection_handle.dispose()
