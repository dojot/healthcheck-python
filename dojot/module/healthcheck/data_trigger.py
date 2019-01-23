"""
Module used for triggering new service/component states
"""

from .types import ServiceStatus
from .service_info import DynamicServiceInfo
from .component_details import DynamicComponentsDetails

import logging

LOGGER = logging.getLogger('healthcheck.' + __name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)


class DataTrigger:
    """
    Class responsible for receiving service/component updates associated
    to monitors.
    """
    def __init__(self,
                 service_info: DynamicServiceInfo,
                 component_details: DynamicComponentsDetails):
        self.component_details = component_details
        self.service_info = service_info

    def trigger(self, data, status: ServiceStatus = None, output: str = None):
        """
        Trigger a new measurement and/or service states.
        This should be used within a measurement worker (the function that
        actually gathers data from the system or component)

        :type data: any
        :param data: The data to be updated
        :type status: ServiceStatus
        :param status: If current measurement should change the state of this
        component or service, this new state is set in status parameter.
        :type output: str
        :param output: If status is warn or fail, this is the raw output to help
        find out what's happening.
        """
        self.component_details.observed_value = data
        self.component_details.status = status if status is not None else ServiceStatus.systemOk
        self.component_details.output = output if output is not None else "no-reason"

        LOGGER.debug(f"Changing component state: {self.component_details}")

        if self.component_details.status != ServiceStatus.systemOk:
            if self.service_info.status != ServiceStatus.systemFail:
                self.service_info.status = self.component_details.status
        else:
            warnings = 0
            failures = 0

            if self.service_info.detail is None:
                return
            for component in self.service_info.detail:
                if self.service_info.detail[component].status == ServiceStatus.systemFail:
                    failures += 1
                elif self.service_info.detail[component].status == ServiceStatus.systemWarning:
                    warnings += 1

                if failures is not 0:
                    self.service_info.status = ServiceStatus.systemFail
                elif warnings is not 0:
                    self.service_info.status = ServiceStatus.systemWarning
                else:
                    self.service_info.status = ServiceStatus.systemOk
