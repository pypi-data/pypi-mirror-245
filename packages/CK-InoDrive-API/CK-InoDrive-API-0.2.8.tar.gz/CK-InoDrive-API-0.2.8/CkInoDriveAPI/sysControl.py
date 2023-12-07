import logging

from .wsHandle import InoDriveWS
from .defines import CK


class SysControl(object):
    def __init__(self, **kwargs):
        self._connection_handle: InoDriveWS = kwargs.get('connection_handle')

    def console_enable(self, state=False):
        response = self._connection_handle.msg_pack_request([CK.MSG_PACK.CONSOLE_ENABLE, True if state else False])

        if response.get('error'):
            logging.error(f'InoDrive ConsoleEnable Error: {str(response)}')
            return None

        return True

    def take_control(self, state=False):
        response = self._connection_handle.msg_pack_request([CK.MSG_PACK.TAKE_CONTROL, True if state else False])

        if response.get('error'):
            logging.error(f'InoDrive TakeControl Error: {str(response)}')
            return None

        return True

    def get_module_state(self):
        response = self._connection_handle.msg_pack_request([CK.MSG_PACK.MODULE_STATE])

        if response.get('error'):
            logging.error(f'InoDrive TakeControl Error: {str(response)}')
            return None

        return response['data'][0]
