"""
Components to gather data from a component or service.
"""

import threading
import time
from .service_info import DynamicServiceInfo
from .component_details import DynamicComponentsDetails
from .data_trigger import DataTrigger


class HealthMonitor(threading.Thread):
    """
    Class responsible for periodically executing a particular function to
    get variable measurements, such as memory consumption.
    """

    def __init__(self,
                 periodicity: int,
                 dynamic_component_details: DynamicComponentsDetails,
                 data_trigger: DataTrigger,
                 collect_func):
        threading.Thread.__init__(self)
        self.dynamic_component_details = dynamic_component_details
        self.data_trigger = data_trigger
        self.collect_func = collect_func
        self.periodicity = periodicity
        self.should_stop = False
        self.lock = threading.RLock()

    def run(self):
        """
        Start retrieving monitor data
        """
        self.lock.acquire()
        while self.should_stop is False:
            self.lock.release()
            self.dynamic_component_details.observed_value = self.collect_func(
                self.data_trigger)
            time.sleep(self.periodicity)
            self.lock.acquire()
        self.lock.release()

    def stop(self):
        """
        Stop this monitor.

        Actually this will indicate that the thread should exit. It doesn't
        force the thread to be killed.
        """
        self.lock.acquire()
        self.should_stop = True
        self.lock.release()


class HealthChecker:
    """
    Class responsible for starting and stopping monitors.
    """

    def __init__(self, service_info: DynamicServiceInfo):
        self.service_info = service_info
        self.threads = []

    def create_monitor(self,
                       component_details: DynamicComponentsDetails,
                       collect_func=None,
                       periodicity=None):
        """
        Register a new monitor to be executed.

        If collect_func and periodicity are *both* set, then a new thread is
        started executing the function in a perioci way. If not, nothing happens
        and the returned DataTrigger object should be used whenever the observed
        value changes.

        :type component_details: DynamicComponentsDetails
        :param component_details: The component details object to be associated
        to the new monitor
        :type collect_func: (dataTrigger: DataTriger) => any
        :param collect_func: The function to be executed when getting the data
        :type periodicity: int
        :param periodicity: Time in seconds between each callback execution.
        """
        monitor_id = f'{component_details.component_name}:{component_details.measurement_name}'
        if self.service_info.detail is None:
            self.service_info.detail = {}

        self.service_info.detail[monitor_id] = component_details
        data_trigger = DataTrigger(self.service_info, self.service_info.detail[monitor_id])
        if (collect_func is not None) and (periodicity is not None):
            # Start collect thread
            thr = HealthMonitor(
                periodicity, self.service_info.detail[monitor_id], data_trigger, collect_func)
            self.threads.append(thr)
            thr.start()
        return data_trigger

    def stop_monitor(self):
        """
        Stop all monitors
        """
        for thread in self.threads:
            thread.stop()
