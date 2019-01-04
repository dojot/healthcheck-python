"""
Healthcheck general types
"""

import enum

class ServiceStatus(enum.Enum):
    """
    Possible service status
    """
    systemOk = "pass"
    systemFail = "fail"
    systemWarning = "warn"
