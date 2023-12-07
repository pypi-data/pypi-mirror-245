import re
import time
import json
import uuid
import struct
import logging

import msgpack

from .defines import CK


class CkUtils(object):

    def get_token(self, length=8, bytes=True):
        """Returns a random string of length string_length."""

        # Convert UUID format to a Python string.
        random = str(uuid.uuid4())

        # Make all characters uppercase.
        random = random.upper()

        # Remove the UUID '-'.
        random = random.replace("-", "")

        # Return the random string.
        token = random[0:length]
        return token.encode('ascii') if bytes else token

    def get_tlv(self, tlv_type=None, value=None, length=None):
        '''
        Creates -> Type Length CRC32 Value
        CRC32 is calculated over the value only.
        :param tlv_type: TLV type
        :param value: Byte string
        :param length: Optional. Value length
        :return: TLV byte string
        '''
        try:
            if tlv_type is None:
                logging.error('TLV type not provided...')
                return b''

            if value is None:
                # If there is no value size is 0
                return struct.pack('>II', tlv_type, 0)

            if type(value) == dict:
                value = json.dumps(value)

            if type(value) == int:
                value = bytes([value])

            if type(value) == list:
                value = bytes(value)

            if type(value) != bytes:
                value = bytes(str(value), 'utf-8')

            # Value length
            length = length if length else len(value)
            if length > len(value):
                # If required length is larger then value length
                value = (bytes([0] * (length - len(value)))) + value

            return struct.pack('>II', tlv_type, length) + value

        except Exception as ex:
            logging.exception(ex)

        return b''

    def is_proper_c_type(self, data=None, data_type=None):
        try:
            if data is None or data_type is None:
                return False

            types = {
                'int8': 'b',
                's_byte': 'b',
                'uint8': 'B',
                'bool': 'B',
                'u_byte': 'B',
                'int16': 'h',
                's_int': 'h',
                'uint16': 'H',
                'u_int': 'H',
                'int32': 'i',
                's_dint': 'i',
                'uint32': 'I',
                'u_dint': 'I',
                'int64': 'q',
                's_long': 'q',
                'uint64': 'Q',
                'u_long': 'Q',
                'float': 'f',
                'double': 'd',
                'string': True,
                'macAddress': True,
                'ipV4': True,
            }

            if data_type not in types:
                return None

            value = struct.pack(f'{types.get(data_type)}', data)

            return True

        except Exception as ex:
            pass

        return False

    def get_typed_value(self, data=None, data_type=None, endian=False):
        try:
            if type(data) != bytes:
                return None

            types = {
                'int8': 'b',
                's_byte': 'b',
                'uint8': 'B',
                'bool': 'B',
                'u_byte': 'B',
                'int16': 'h',
                's_int': 'h',
                'uint16': 'H',
                'u_int': 'H',
                'int32': 'i',
                's_dint': 'i',
                'uint32': 'I',
                'u_dint': 'I',
                'int64': 'q',
                's_long': 'q',
                'uint64': 'Q',
                'u_long': 'Q',
                'float': 'f',
                'double': 'd',
                'string': True,
                'macAddress': True,
                'ipV4': True,
            }

            if data_type not in types:
                return None

            endian_opt = '<' if endian else '>'

            if data_type == 'string':
                item = data.split(b'\x00')[0]
                return item.decode("utf-8")

            if data_type == 'macAddress':
                items = []
                for item in data:
                    items.append(f'{item:0>2X}')

                return ':'.join(items)

            if data_type == 'ipV4':
                items = []
                for item in data:
                    items.append(str(item))

                return '.'.join(items)

            value = struct.unpack(f'{endian_opt}{types.get(data_type)}', data)[0]
            return value

        except Exception as ex:
            logging.exception(ex)

        return None

    def decode_tlv_message(self, msg=None):
        try:
            if type(msg) != bytes:
                return {'error': 'Message is not bytes'}

            if len(msg) < 8:
                return {'error': 'Message length is less then 8 bytes'}

            # Create decoded response object
            decoded = {'error': None, 'items': []}

            while len(msg) >= 8:
                # Get TLV type
                msg_type = self.get_typed_value(msg[0:4], 'uint32')
                # Get TLV length
                msg_length = self.get_typed_value(msg[4:8], 'uint32')

                data = b''
                if msg_length > 0:
                    data = msg[8:8 + msg_length]

                if msg_type == CK.UNIQUE_TOKEN:
                    decoded.update({'token': data})
                elif msg_type == CK.TYPE.NTP_TIME:
                    seconds = self.get_typed_value(data[0:4], 'uint32')
                    milliseconds = self.get_typed_value(data[4:8], 'uint32')
                    time = seconds + round(milliseconds / pow(2, 32), 3)
                    decoded.update({'ntpTime': time})
                elif msg_type == CK.RESPONSE:
                    resp = self.get_typed_value(data, 'uint8')
                    if resp != 0:
                        decoded.update({'error': resp})

                    decoded.update({
                        'type': msg_type,
                        'response': resp,
                    })
                elif msg_type == CK.SPECIAL.CONSOLE:
                    decoded.update({'type': msg_type})
                elif msg_type == CK.TYPE.MSG_PACK:
                    decoded['items'].append({'ctpType': msg_type, 'ctpLength': msg_length, 'data': self.msg_unpack(data)})
                else:
                    decoded['items'].append({'ctpType': msg_type, 'ctpLength': msg_length, 'data': data})

                # Get the rest of the message
                msg = msg[8 + msg_length:]

            return decoded
        except Exception as ex:
            logging.exception(ex)
            return {'error': str(ex)}

    def msg_pack(self, msg=None):
        try:
            return msgpack.packb(msg, use_bin_type=True)
        except Exception as ex:
            logging.exception(ex)

    def msg_unpack(self, msg=None):
        try:
            return msgpack.unpackb(msg, raw=False)
        except Exception as ex:
            logging.exception(ex)

    def get_msg_pack_tlv(self, payload):
        try:
            return self.get_tlv(CK.TYPE.MSG_PACK, Utils.msg_pack(payload))
        except Exception as ex:
            logging.exception(ex)

        return b''

    def get_var_c_type(self, var_type=None):
        try:
            if var_type is None:
                return None

            for c_type, type_props in CK.API_C_TYPES.items():
                if type_props['type'] == var_type:
                    return c_type
        except Exception as ex:
            logging.exception(ex)

        return None

    def get_target_url(self, target='', props={}):
        try:
            secure = props.get('secure', False)
            port_number = props.get('port')
            if port_number is not None and type(port_number) != int:
                port_number = None

            path = props.get('path')

            if target.find('.local') >= 0:
                target = target.replace('.local', '')

            protocol = 'wss' if secure else 'ws'
            port = None

            if port_number is not None:
                port = f':{port_number}'

            if path is not None:
                path = path.replace('\\', '/')
                if path[0] == '/':
                    path = path[1:]

            cmd_delimiter = '--'
            is_ipv4 = True if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', target) else False

            url = f'{protocol}://{target}'
            if not is_ipv4:
                url += f'{cmd_delimiter}T{int(time.time())}.local'

            url += f'{port if port is not None else ""}/{path if path is not None else ""}'

            return url
        except Exception as ex:
            logging.exception(ex)
            return ''


Utils = CkUtils()
