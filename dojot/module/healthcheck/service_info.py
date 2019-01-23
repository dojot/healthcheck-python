"""
Service info data structures
"""

from marshmallow import Schema, fields
from .types import ServiceStatus


class ServiceInfo:
    """
    Service info data structure"
    """

    def __init__(self,
                 status: ServiceStatus = ServiceStatus.systemOk,
                 version: str = None,
                 release_id: str = None,
                 notes: str = None,
                 links: str = None,
                 description: str = None):
        self.status = status
        self.version = version
        self.release_id = release_id
        self.notes = notes
        self.links = links
        self.description = description

    def __repr__(self):
        return f'<ServiceInfo('\
               f'status={self.status}, '\
               f'version={self.version}, '\
               f'releaseId={self.release_id}, '\
               f'notes={self.notes}, '\
               f'links={self.links}, '\
               f'description={self.description})>'


class DynamicServiceInfo(ServiceInfo):
    """
    Service info data structure, with dynamic attributes
    """

    def __init__(self,
                 detail=None,
                 service_id: str = None,
                 output=None,
                 **kwargs):
        self.detail = detail
        self.service_id = service_id
        self.output = output
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<DynamicServiceInfo('\
               f'status={self.status}, '\
               f'version={self.version}, '\
               f'releaseId={self.release_id}, '\
               f'notes={self.notes}, '\
               f'links={self.links}, '\
               f'description={self.description}, '\
               f'detail={self.detail}, '\
               f'serviceId={self.service_id}, '\
               f'output={self.output})>'


class ServiceInfoSchema(Schema):
    """
    Marshmallow schema for service info
    """
    status = fields.Str()
    version = fields.Str(optional=True)
    release_id = fields.Str(optional=True)
    notes = fields.Str(optional=True)
    links = fields.Str(optional=True)
    description = fields.Str(optional=True)


class DynamicServiceInfoSchema(Schema):
    """
    Marshmallow schema for service info with dynamic attributes
    """
    status = fields.Str()
    version = fields.Str(optional=True)
    release_id = fields.Str(optional=True)
    notes = fields.Str(optional=True)
    links = fields.Str(optional=True)
    description = fields.Str(optional=True)
    detail = fields.Str(optional=True)
    output = fields.Str(optional=True)


SCHEMA = ServiceInfoSchema()
