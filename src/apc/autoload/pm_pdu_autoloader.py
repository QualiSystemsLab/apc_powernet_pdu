from apc.snmp_handler import SnmpHandler
from cloudshell.shell.core.context import AutoLoadResource, AutoLoadDetails, AutoLoadAttribute
from log_helper import LogHelper


class PmPduAutoloader:
    def __init__(self, context):
        self.context = context
        self.logger = LogHelper.get_logger(self.context)
        self.snmp_handler = SnmpHandler(self.context).get_raw_handler('get')

    def autoload(self):
        rv = AutoLoadDetails()
        rv.resources = []
        rv.attributes = []

        # rv.attributes.append(self.makeattr('', 'Location', self.snmp_handler.get_property('SNMPv2-MIB', 'sysLocation', 0)))
        # this should be correct - issues in the Gen1Shell & the modeling did allow for testing:
        rv.attributes.append(self.makeattr('', 'Location', self.snmp_handler.get_property('PowerNet-MIB', 'rPDU2IdeLocationnt', 0)))
        rv.attributes.append(self.makeattr('', 'Model', self.snmp_handler.get_property('PowerNet-MIB', 'sPDUIdentModelNumber', 0)))
        # optional (Serial Number not part of the standard):
        # rv.attributes.append(self.makeattr('', 'Serial Number', self.snmp_handler.get_property('PowerNet-MIB', 'sPDUIdentSerialNumber', 0)))
        rv.attributes.append(self.makeattr('', 'Vendor', 'APC'))
        rv.attributes.append(self.makeattr('', 'Firmware Version', self.snmp_handler.get_property('PowerNet-MIB', 'sPDUIdentFirmwareRev', 0)))

        pdu_name = self.snmp_handler.get_property('PowerNet-MIB', 'sPDUMasterConfigPDUName', 0)

        outlet_table = self.snmp_handler.get_table('PowerNet-MIB', 'sPDUOutletControlTable')
        for index, attribute in outlet_table.iteritems():
            name = 'Outlet %s' % index
            relative_address = index
            unique_identifier = '%s.%s' % (pdu_name, index)

            rv.resources.append(self.makeres(name, 'Generic Power Socket', relative_address, unique_identifier))
            # need to check this line too:
            rv.attributes.append(self.makeattr(relative_address, 'Port Description', attribute['memOutletStatusOutletName']))

        return rv

    def makeattr(self, relative_address, attribute_name, attribute_value):
        a = AutoLoadAttribute()
        a.relative_address = relative_address
        a.attribute_name = attribute_name
        a.attribute_value = attribute_value
        return a

    def makeres(self, name, model, relative_address, unique_identifier):
        r = AutoLoadResource()
        r.name = name
        r.model = model
        r.relative_address = relative_address
        r.unique_identifier = unique_identifier
        return r
