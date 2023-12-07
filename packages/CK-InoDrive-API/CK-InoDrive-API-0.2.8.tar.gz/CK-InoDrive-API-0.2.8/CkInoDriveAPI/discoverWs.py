import logging

from .defines import CK
from .utils import Utils
from .wsHandle import InoDriveWS


class DiscoverWs(object):
    def __init__(self, **kwargs):
        self._connection_handle: InoDriveWS = kwargs.get('connection_handle')

    def get_info(self):
        try:
            # Send request and wait for response
            resp = self._connection_handle.request(Utils.get_tlv(CK.SPECIAL.GET_DISCOVER_INFO))

            if resp.get('error'):
                logging.error(f'Retrieving discover info failed...')
                return None

            result = None

            resp_items = resp.get('items')
            if resp_items and len(resp_items) > 0:
                data = resp_items[0].get('data')

                # Discover version
                # =======================================================================
                item_size = 1
                discover_version = Utils.get_typed_value(data[0:item_size], 'uint8')
                data = data[item_size:]
                # =======================================================================

                # SN
                # =======================================================================
                item_size = 25
                sn = Utils.get_typed_value(data[0:item_size], 'string')
                data = data[item_size:]
                # =======================================================================

                # PN
                # =======================================================================
                item_size = 25
                pn = Utils.get_typed_value(data[0:item_size], 'string')
                data = data[item_size:]
                # =======================================================================

                # Name
                # =======================================================================
                item_size = 33
                name = Utils.get_typed_value(data[0:item_size], 'string')
                data = data[item_size:]
                # =======================================================================

                # Firmware version
                # =======================================================================
                item_size = 1
                fw_major = Utils.get_typed_value(data[0:item_size], 'uint8')
                data = data[item_size:]

                item_size = 1
                fw_minor = Utils.get_typed_value(data[0:item_size], 'uint8')
                data = data[item_size:]

                item_size = 1
                fw_build = Utils.get_typed_value(data[0:item_size], 'uint8')
                data = data[item_size:]

                item_size = 1
                fw_type = Utils.get_typed_value(data[0:item_size], 'uint8')
                data = data[item_size:]

                firmware_flags = {
                    'production': True if fw_type & (1 << 6) else False,
                    'failSafe': True if fw_type & (1 << 7) else False,
                }
                # =======================================================================

                # Networking
                # =======================================================================
                item_size = 6
                mac_address = Utils.get_typed_value(data[0:item_size], 'macAddress')
                data = data[item_size:]

                item_size = 4
                ip_address = Utils.get_typed_value(data[0:item_size], 'ipV4')
                data = data[item_size:]

                item_size = 4
                net_mask = Utils.get_typed_value(data[0:item_size], 'ipV4')
                data = data[item_size:]

                item_size = 4
                gateway = Utils.get_typed_value(data[0:item_size], 'ipV4')
                data = data[item_size:]

                item_size = 4
                dns = Utils.get_typed_value(data[0:item_size], 'ipV4')
                data = data[item_size:]
                # =======================================================================

                # PCB Version
                # =======================================================================
                pcb_version = {
                    'major': 1,
                    'minor': 1,
                    'build': 1,
                    'type': 0,
                }

                if discover_version >= 2:
                    item_size = 1
                    pcb_version['major'] = Utils.get_typed_value(data[0:item_size], 'uint8')
                    data = data[item_size:]

                    item_size = 1
                    pcb_version['minor'] = Utils.get_typed_value(data[0:item_size], 'uint8')
                    data = data[item_size:]

                    item_size = 1
                    pcb_version['build'] = Utils.get_typed_value(data[0:item_size], 'uint8')
                    data = data[item_size:]

                    if discover_version >= 3:
                        item_size = 1
                        pcb_version['type'] = Utils.get_typed_value(data[0:item_size], 'uint8')
                        data = data[item_size:]

                # =======================================================================

                result = {
                    'discoverVersion': discover_version,
                    'sn': sn,
                    'pn': pn,
                    'name': name,
                    'firmware': '.'.join([str(fw_major), str(fw_minor), str(fw_build)]),
                    'firmwareFlags': firmware_flags,
                    'network': {
                        'ip': ip_address,
                        'mask': net_mask,
                        'gw': gateway,
                        'dns': dns,
                        'mac': mac_address,
                    },
                    'pcbVersion': '.'.join([str(pcb_version['major']), str(pcb_version['minor']), str(pcb_version['build'])]),
                }

            return result
        except Exception as ex:
            logging.exception(ex)

        return None
