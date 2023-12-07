import re
import time
import logging
import datetime
import threading
import websocket

from .defines import CK
from .utils import Utils


class InoDriveWS(object):
    def __init__(self, **kwargs):

        # Target module network identifier: IP Address, SN, Name
        self._target = kwargs.get('target')
        if type(self._target) != str:
            raise Exception(f'Target device not provided...')
        self._port = kwargs.get('port')
        # Api path - entry point
        self._path = kwargs.get('path', 'cmd')
        # Secure or non-secure WebSocket
        self._secure = True if kwargs.get('secure') else False
        # Auto connect when instance is created
        self._auto_connect = kwargs.get('autoConnect', False)
        # Timeout notes:
        # connectTimeout should be 3 - 15 seconds. Low values like 3-5 should be good, even over the internet.
        # socketTimeout should be ~10. When a file transfer overwrites a file, there could be 2-3 seconds of
        # filesystem overhead and the transfer of 300k+ firmware file takes 2+ seconds.
        # Maybe we need separate file transfer and variable API timeouts.
        self._connect_timeout = kwargs.get('connectTimeout', 20)
        self._socket_timeout = kwargs.get('socketTimeout', 10)
        self._keep_alive_timeout = kwargs.get('keepAlive', 5)
        self._receive_block_timeout = kwargs.get('receiveTimeout', 0.1)

        self._callbacks = {}

        logging.debug(f'Target device URL: {self._url}')

        self._request_queue = {}

        # WebSocket instance
        self._ws = websocket.WebSocket(enable_multithread=True)
        self._ws_state = 'disconnect'
        self._ws_last_comm = datetime.datetime.now()

        self._thread = threading.Thread(target=self._thread_loop, daemon=True)
        self._thread_running = True
        self._thread.start()

        self._disposed = False

        if self._auto_connect:
            self.connect()

    def __del__(self):
        self.dispose()

    def dispose(self):
        try:
            if self._disposed:
                return

            logging.debug(f'Dispose target [{self._target}] connection...')

            self.disconnect()

            self._thread_running = False
            if self._thread:
                self._thread.join()
                self._thread = None

            self._disposed = True
        except Exception as ex:
            logging.error(str(ex))

    def set_target(self, target=None):
        if type(target) == str:
            self._target = target

    @property
    def connected(self):
        if self._ws:
            return True if self._ws.connected else False
        else:
            return False

    def on(self, *args, **kwargs):
        logging.warning('Implement on method...')
        pass

    def connect(self, timeout=None):
        try:
            if self._disposed:
                return

            prev_state = self._ws_state
            self._ws_state = 'connect'

            if self.connected:
                return True

            if timeout:
                timeout = timeout * 100
            else:
                timeout = self._connect_timeout * 100

            while not self.connected and timeout > 0:
                timeout -= 1
                time.sleep(0.01)

            if timeout <= 0 and not self.connected:
                self._ws_state = prev_state

            return self.connected

        except Exception as ex:
            logging.info(str(ex))

        return False

    def disconnect(self, timeout=None):
        try:
            if self._disposed:
                return

            prev_state = self._ws_state
            self._ws_state = 'disconnect'

            if self.connected is False:
                return True

            self._ws.close()

            if timeout:
                timeout = timeout * 100
            else:
                timeout = self._connect_timeout * 100

            while self.connected and timeout > 0:
                timeout -= 1
                time.sleep(0.01)

            if timeout <= 0 and self.connected:
                self._ws_state = prev_state

            return not self.connected

        except Exception as ex:
            logging.error(str(ex))

        return False

    def request(self, payload=None, timeout=None, blocking=True):
        try:
            if type(payload) != bytes:
                return {'success': False, 'error': 'Payload is None...'}

            token = Utils.get_token(8)

            msg = b''
            msg += Utils.get_tlv(CK.UNIQUE_TOKEN, token)
            msg += payload

            queue_item = {
                'time': datetime.datetime.now(),
                'error': None,
                'response': None,
            }

            if blocking:
                # If we are going to wait for response addi the item to the queue
                self._request_queue.update({token: queue_item})

            if not self._send(msg):
                # Send failed for some reason
                return {'success': False, 'error': 'Send failed...'}

            # If we are not going to wait for response just return success
            if not blocking:
                return {'success': True}

            if timeout:
                timeout = timeout * 100
            else:
                timeout = self._socket_timeout * 100

            while queue_item['response'] is None and timeout > 0:
                timeout -= 1
                time.sleep(0.01)

            if queue_item['response'] is None and timeout <= 0:
                return {'success': False, 'error': 'timeout'}

            response = queue_item['response']

            # Remove this request item from the queue
            self._request_queue.pop(token, None)

            return response

        except Exception as ex:
            logging.error(str(ex))
            return {'success': False, 'error': ex}

    def msg_pack_request(self, msg=[]):
        try:
            msg_tlv = Utils.get_msg_pack_tlv(msg)
            response = self.request(msg_tlv)

            if response.get('error'):
                return {
                    'success': False,
                    'error': response['error'],
                }

            if len(response['items']) == 0:
                return {
                    'success': False,
                    'error': 'Response items are missing...'
                }

            if response['items'][0]['ctpType'] != CK.TYPE.MSG_PACK:
                return {
                    'success': False,
                    'error': 'Response item is not MsgPack...'
                }

            msg_pack_data = response['items'][0]['data']

            if len(msg_pack_data) < 2:
                return {
                    'success': False,
                    'error': 'MsgPack returns less then required two items - success and error'
                }

            if not msg_pack_data[0]:
                # todo: Decode the message -> msg_pack_data[1]
                return {
                    'success': False,
                    'error': msg_pack_data[1],
                }

            response_msg = {
                'success': True,
                'token': response.get('token'),
                'data': msg_pack_data[2:],
            }

            if response.get('ntpTime'):
                response_msg.update({'ntpTime': response['ntpTime']})

            return response_msg
        except Exception as ex:
            return {
                'success': False,
                'error': str(ex)
            }

    @property
    def _url(self):
        return Utils.get_target_url(self._target, {'port': self._port, 'path': self._path, 'secure': self._secure})

    def _send(self, data=None):
        try:
            if self.connected:
                self._ws_last_comm = datetime.datetime.now()
                self._ws.send_binary(data)
                return True
        except Exception as ex:
            logging.error(str(ex))

            return False

    def _send_keep_alive(self):
        self.request(Utils.get_tlv(CK.NOP), blocking=False)

    def _thread_loop(self):
        logging.debug(f'Target [{self._target}] Thread start...')
        while self._thread_running:
            try:
                # If we are not connected - connect
                # =====================================================================================================
                if self._ws_state == 'connect' and self.connected is False:

                    logging.debug(f'Connect to target: {self._url}')
                    try:
                        self._ws.connect(f'{self._url}', timeout=self._connect_timeout / 3)
                        self._ws_last_comm = datetime.datetime.now()
                    except Exception as ex:
                        time.sleep(1)
                    continue
                # =====================================================================================================

                if self.connected is False:
                    time.sleep(0.1)
                    continue

                # Keep alive
                # =====================================================================================================
                current_time = datetime.datetime.now()
                if current_time - self._ws_last_comm > datetime.timedelta(seconds=self._keep_alive_timeout):
                    self._send_keep_alive()
                # =====================================================================================================

                # Wait,read and handle the response
                # =====================================================================================================
                msg = None
                try:
                    msg = self._ws.recv()
                except websocket.WebSocketTimeoutException:
                    pass
                except Exception as ex:
                    self._ws.close()
                    time.sleep(0.1)

                if msg:
                    response = Utils.decode_tlv_message(msg)

                    if type(response) != dict:
                        continue

                    token = response.get('token')
                    if token:
                        queue_item = self._request_queue.get(token)
                        if queue_item:
                            queue_item.update({'response': response})
                # =====================================================================================================

                # Check for orphan requests in the request queue
                # =====================================================================================================
                id_to_remove = []
                cur_time = datetime.datetime.now()
                for id, data in self._request_queue.items():
                    request_time = data.get('time')

                    if request_time is None or cur_time - request_time >= datetime.timedelta(seconds=self._socket_timeout * 2):
                        id_to_remove.append(id)

                for id in id_to_remove:
                    logging.warning(f'Delete request Target:{self._target} ID:{id} -> Orphan request')
                    self._request_queue.pop(id, None)
                    logging.warning(f'Target:{self._target} Queue length: {len(self._request_queue)}')
                # =====================================================================================================
            except Exception as ex:
                logging.error(str(ex))
                # Unhandled exception - give it some time to recover
                time.sleep(1)

        if self._ws and self._ws.connected:
            logging.debug('WS Close...')
            self._ws.close()

        logging.debug(f'Target [{self._target}] Thread exit...')
