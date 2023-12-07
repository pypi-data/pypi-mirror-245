import json
import logging

from .wsHandle import InoDriveWS
from .defines import CK
from .utils import Utils


class File(object):
    def __init__(self, **kwargs):
        self._connection_handle: InoDriveWS = kwargs.get('connection_handle')

    def read(self, files=None, transfer_type=None):
        try:
            if files is None:
                logging.error(f'Files is None...')
                return None

            if type(files) != list:
                files = [files]

            files_content = []

            # Upload uApp and firmware are specifying different types
            transfer_type = transfer_type if type(transfer_type) == int else CK.FILE.TRANSFER

            for file in files:
                if type(file) != dict:
                    logging.error(f'File is not a dict...')
                    return None

                file_path = file.get('path')
                content = file.get('content', 'bytes')

                if type(file_path) != str:
                    logging.error(f'File path is not a string...')
                    return None

                file_path = file_path.replace('\\', '/')

                if file_path[0] == '.':
                    file_path = file_path[1:]

                if file_path[0] != '/':
                    file_path = f'/{file_path}'

                file_path = file_path.replace('\\', '/')

                msg = b''
                # file transfer TLV first
                msg += Utils.get_tlv(transfer_type, CK.COMMAND.FILE_READ)
                # Add file path TLV to the message
                msg += Utils.get_tlv(CK.TYPE.STRING, file_path)

                response = self._connection_handle.request(msg)
                if response.get('error'):
                    logging.error('File read error...')
                    return None

                file_content = response['items'][0]['data']
                if content == 'json' or content == 'string':
                    file_content = file_content.decode('utf-8')
                    if content == 'json':
                        file_content = json.loads(file_content)
                files_content.append(file_content)

            if len(files_content) == 0:
                logging.error('There are no file(s) received...')
                return None

            return files_content if len(files_content) > 1 else files_content[0]
        except Exception as ex:
            logging.exception(ex)

        return None

    def write(self, files=None, transfer_type=None):
        try:
            if files is None:
                logging.error(f'Files is None...')
                return False

            if type(files) != list:
                files = [files]

            # Upload uApp and firmware are specifying different types
            transfer_type = transfer_type if type(transfer_type) == int else CK.FILE.TRANSFER

            for file in files:
                if type(file) != dict:
                    logging.error(f'File is not a dict...')
                    return False

                file_path = file.get('path')

                file_path = file_path.replace('\\', '/')

                if file_path[0] == '.':
                    file_path = file_path[1:]

                if file_path[0] != '/':
                    file_path = f'/{file_path}'

                file_path = file_path.replace('\\', '/')

                file_content = file.get('content')

                if type(file_content) == dict:
                    file_content = json.dumps(file_content)

                if type(file_content) == str:
                    file_content = bytes(file_content, 'utf-8')

                if file_content is None or type(file_content) != bytes:
                    logging.error(f'File content is not bytes...')
                    return False

                msg = b''
                # file transfer first
                msg += Utils.get_tlv(transfer_type, CK.COMMAND.FILE_WRITE)
                # Add file path to the message
                msg += Utils.get_tlv(CK.TYPE.STRING, file_path)
                # Add data to the message
                msg += Utils.get_tlv(CK.TYPE.BLOB, file_content)

                # Send request and wait for response
                resp = self._connection_handle.request(msg)

                if resp.get('error'):
                    logging.error(f'File [{file_path}] write error: {resp.get("error")}')
                    return False

            return True
        except Exception as ex:
            logging.exception(ex)

        return False

    def delete_uapp(self):
        try:
            # Send request and wait for response
            resp = self._connection_handle.request(Utils.get_tlv(CK.SPECIAL.DELETE_UAPP))

            if resp.get('error'):
                logging.error(f'Deleting User Application failed...')
                return False

            return True
        except Exception as ex:
            logging.exception(ex)

        return False

    def upload_user_app(self, content=None):
        try:
            return self.write({'path': "/uapp/application.idsol", 'content': content}, CK.FILE.UAPP_TRANSFER)
        except Exception as ex:
            logging.exception(ex)

    def upload_firmware(self, content=None):
        try:
            return self.write({'path': "/firmware/firmware.nhfw", 'content': content}, CK.FILE.FIRMWARE_TRANSFER)
        except Exception as ex:
            logging.exception(ex)

    def read_module_config(self):
        try:
            return self.read({'path': '/config/module_cfg.json', 'content': 'json'})
        except Exception as ex:
            logging.exception(ex)

    def write_module_config(self, content=None):
        try:
            if type(content) != dict:
                logging.error('Content type is not dictionary')
                return False

            return self.write({'path': '/config/module_cfg.json', 'content': content})
        except Exception as ex:
            logging.exception(ex)
