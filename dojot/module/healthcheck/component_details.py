"""
Definitions for component details
"""

from marshmallow import Schema, fields

from .types import ServiceStatus


class ComponentDetails:
    """
    ComponentDetails class

    This class is intended to hold all information related to static data
    of a component, such as measurement name, units, and so on.

    For more information about these attributes, check:
    https://datatracker.ietf.org/doc/draft-inadarei-api-health-check/
    """
    def __init__(self,
                 status: ServiceStatus = ServiceStatus.systemOk,
                 component_name: str = None,
                 measurement_name: str = None,
                 component_id: str = None,
                 component_type: str = None,
                 observed_unit: str = None,
                 links: str = None):
        """
        Build a new component detail object
        :type status: ServiceStatus
        :param status: Default component status
        :type component_name: str
        :param component_name: Human-readable name for the component.
        :type measurement_name: str
        :param measurement_name: name of the measurement type (a data point
        type) that the status is reported for.
        :type component_id: str
        :param component_id: a unique identifier of an instance of a specific
        sub-component/dependency of a service.
        :type component_type: str
        :param component_type: type of the component.
        :type observed_unit: str
        :param observed_unit: unit of measurement in which observedValue is
        reported.
        :type links: str
        :param links: links that might contain more information about the
        health of this endpoint.
        """
        self.status = status
        self.component_name = component_name
        self.measurement_name = measurement_name
        self.component_id = component_id
        self.component_type = component_type
        self.observed_unit = observed_unit
        self.links = links

    def __repr__(self):
        return f'<ComponentDetails('\
               f'status={self.status}, '\
               f'componentName={self.component_name}, '\
               f'measurement_name={self.measurement_name}, '\
               f'component_id={self.component_id}, '\
               f'component_type={self.component_type}, '\
               f'observed_unit={self.observed_unit}, '\
               f'links={self.links})>'


class DynamicComponentsDetails(ComponentDetails):
    """
    DynamicComponentDetails class

    This class is intended to hold all information related to dynamic and static
    data of a component, such as measurement values.
    """
    def __init__(self,
                 observed_value=None,
                 output: str = None,
                 time: str = None,
                 **kwargs):
        """
        Build a new component details object

        :type observed_value: any
        :param observed_value: The initial value of a observable entity.
        :type output: str
        :param output: raw output if component status is warn or fail
        :type time: str
        :param time: when did the error or warn occurred (if component status is
        fail or warn)
        """
        self.observed_value = observed_value
        self.output = output
        self.time = time
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<DynamicComponentDetails('\
               f'status={self.status}, '\
               f'componentName={self.component_name}, '\
               f'measurement_name={self.measurement_name}, '\
               f'component_id={self.component_id}, '\
               f'component_type={self.component_type}, '\
               f'observed_unit={self.observed_unit}, '\
               f'links={self.links}, '\
               f'observedValue={self.observed_value}, '\
               f'output={self.output}, '\
               f'time={self.time})>'


class ComponentDetailsSchema(Schema):
    """
    Marshmallow schema for component details
    """
    status = fields.Str(optional=True)
    componentName = fields.Str(optional=True)
    measurement_name = fields.Str(optional=True)
    component_id = fields.Str(optional=True)
    component_type = fields.Str(optional=True)
    observed_unit = fields.Str(optional=True)
    links = fields.Str(optional=True)


class DynamicComponentDetailsSchema(Schema):
    """
    Marshmallow schema for dynamic component details
    """
    status = fields.Str(optional=True)
    componentName = fields.Str(optional=True)
    measurement_name = fields.Str(optional=True)
    component_id = fields.Str(optional=True)
    component_type = fields.Str(optional=True)
    observed_unit = fields.Str(optional=True)
    links = fields.Str(optional=True)
    observedValue = fields.Raw(optional=True)
    output = fields.Str(optional=True)
    time = fields.Str(optional=True)


SCHEMA = ComponentDetailsSchema()

DYNSCHEMA = DynamicComponentDetailsSchema()
