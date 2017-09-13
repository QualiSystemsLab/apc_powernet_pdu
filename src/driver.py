from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.driver_context import InitCommandContext, ResourceCommandContext, AutoLoadResource, \
    AutoLoadAttribute, AutoLoadDetails, CancellationContext
#from data_model import *  # run 'shellfoundry generate' to generate data model classes
from apc.pm_pdu_handler import PmPduHandler
from cloudshell.power.pdu.power_resource_driver_interface import PowerResourceDriverInterface
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.context import AutoLoadDetails, InitCommandContext, ResourceCommandContext
from log_helper import LogHelper

class ApcPowernetPduDriver (ResourceDriverInterface, PowerResourceDriverInterface):

    def __init__(self):
        """
        ctor must be without arguments, it is created with reflection at run time
        """
        pass

    def initialize(self, context):
        """
        Initialize the driver session, this function is called everytime a new instance of the driver is created
        This is a good place to load and cache the driver configuration, initiate sessions etc.
        :param InitCommandContext context: the context the command runs on
        """
        pass

    def cleanup(self):
        """
        Destroy the driver session, this function is called everytime a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files
        """
        pass

    # <editor-fold desc="Discovery">

    def get_inventory(self, context):
        """
        Discovers the resource structure and attributes.
        :param AutoLoadCommandContext context: the context the command runs on
        :return Attribute and sub-resource information for the Shell resource you can return an AutoLoadDetails object
        :rtype: AutoLoadDetails
        """
        handler = PmPduHandler(context)

        return handler.get_inventory()
    # </editor-fold>

    def PowerOn(self, context, ports):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        handler = PmPduHandler(context)

        return handler.power_on(ports)

    def PowerOff(self, context, ports):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        handler = PmPduHandler(context)

        return handler.power_off(ports)

    def PowerCycle(self, context, ports, delay):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        try:
            float(delay)
        except ValueError:
            raise Exception('Delay must be a numeric value')

        handler = PmPduHandler(context)
        return handler.power_cycle(ports, float(delay))
