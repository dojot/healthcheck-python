"""
Example for dojot.module.healthcheck
"""
from dojot.module.healthcheck import HealthChecker, DynamicComponentsDetails, DynamicServiceInfo, DataTrigger, ComponentDetails, ServiceStatus
from flask import Flask, make_response
from flask.logging import default_handler
import logging

app = Flask(__name__)

logger = logging.getLogger()
logger.addHandler(default_handler)
logger.setLevel(logging.DEBUG)

class Counter:
    def __init__(self):
        self.counter = 0
    def count(self, dataTrigger: DataTrigger):
        self.counter += 1
        logging.debug(f"Count: {self.counter}")
        return self.counter

serviceInfo = DynamicServiceInfo(
    service_id="service-id-001"
)
healthChecker = HealthChecker(serviceInfo)

componentDetails = DynamicComponentsDetails(
    observed_value=0,
    output="",
    time="",
    status=ServiceStatus.systemOk,
    component_name="sample-service",
    measurement_name="memory",
    component_id="xyz",
    component_type="python service",
    observed_unit="MB"
)

counterDetails = DynamicComponentsDetails(
    component_name="counter-trigger",
    measurement_name="number_of_calls"
)

COUNTER = 0
COUNTER_TRIGGER = healthChecker.create_monitor(counterDetails)

@app.route("/healthcheck", methods=["GET"])
def get_healthcheck():
    global COUNTER, healthChecker
    COUNTER += 1
    COUNTER_TRIGGER.trigger(COUNTER)
    if healthChecker.service_info.status == ServiceStatus.systemOk:
        return make_response(f"{healthChecker.service_info}", 200)
    elif healthChecker.service_info.status == ServiceStatus.systemWarning:
        return make_response(f"{healthChecker.service_info}", 200)
    elif healthChecker.service_info.status == ServiceStatus.systemFail:
        return make_response(f"{healthChecker.service_info}", 500)

@app.route("/healthcheck/stop", methods=["POST"])
def stop_healthcheck():
    healthChecker.stop_monitor()
    return make_response("ok", 200)

app.run()
