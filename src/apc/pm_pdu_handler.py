from apc.autoload.pm_pdu_autoloader import PmPduAutoloader
from apc.snmp_handler import SnmpHandler
from log_helper import LogHelper
from pysnmp.proto.rfc1902 import Integer
from pysnmp.smi.rfc1902 import ObjectIdentity
from time import sleep


class PmPduHandler:
    class Port:
        def __init__(self, port):
            self.address, port_details = port.split('/')
            self.port_number, self.pdu_number, self.outlet_number = port_details.split('.')

    def __init__(self, context):
        self.context = context
        self.logger = LogHelper.get_logger(self.context)
        self.snmp_handler = SnmpHandler(self.context)

    def get_inventory(self):
        autoloader = PmPduAutoloader(self.context)

        return autoloader.autoload()

    def power_cycle(self, port_list, delay):
        self.logger.info("Power cycle called for ports %s" % port_list)
        for raw_port in port_list:
            self.logger.info("Power cycling port %s" % raw_port)
            port = self.Port(raw_port)
            self.logger.info("Powering off port %s" % raw_port)
            self.snmp_handler.set(ObjectIdentity('.1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.%s' % port.port_number),
                                  Integer(2))
            self.logger.info("Sleeping %f second(s)" % delay)
            sleep(delay)
            self.logger.info("Powering on port %s" % raw_port)
            self.snmp_handler.set(ObjectIdentity('.1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.%s' % port.port_number),
                                  Integer(1))

    def power_off(self, port_list):
        self.logger.info("Power off called for ports %s" % port_list)
        for raw_port in port_list:
            self.logger.info("Powering off port %s" % raw_port)
            port = self.Port(raw_port)
            self.snmp_handler.set(ObjectIdentity('.1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.%s' % port.port_number),
                                  Integer(2))

    def power_on(self, port_list):
        self.logger.info("Power on called for ports %s" % port_list)
        for raw_port in port_list:
            self.logger.info("Powering on port %s" % raw_port)
            port = self.Port(raw_port)
            self.snmp_handler.set(ObjectIdentity('.1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.%s' % port.port_number),
                                  Integer(1))
