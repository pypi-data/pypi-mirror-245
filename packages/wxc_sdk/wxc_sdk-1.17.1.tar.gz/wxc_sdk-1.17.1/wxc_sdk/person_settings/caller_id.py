from typing import Optional

from pydantic import Field, field_validator

from .common import PersonSettingsApiChild
from ..base import ApiModel, to_camel, plus1
from ..base import SafeEnum as Enum

__all__ = ['CallerIdApi', 'CallerId', 'ExternalCallerIdNamePolicy', 'CallerIdSelectedType']


class CallerIdSelectedType(str, Enum):
    """
    Allowed types for the selected field.
    """
    #: Outgoing caller ID will show the caller's direct line number and/or extension.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the main number for the location.
    location_number = 'LOCATION_NUMBER'
    #: Outgoing caller ID will show the mobile number for this person.
    mobile_number = 'MOBILE_NUMBER'
    #: Outgoing caller ID will show the value from the customNumber field.
    custom = 'CUSTOM'


class ExternalCallerIdNamePolicy(str, Enum):
    """
    Designates which type of External Caller ID Name policy is used. Default is DIRECT_LINE.
    """
    #: Outgoing caller ID will show the caller's direct line name
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the Site Name for the location.
    location = 'LOCATION'
    #: Outgoing caller ID will show the value from the custom_external_caller_id_name field.
    other = 'OTHER'


class CallerId(ApiModel):
    """
    Caller id settings of a user
    """

    @field_validator('direct_number', 'location_number', 'mobile_number', 'custom_number', mode='before')
    def e164(cls, v):
        """
        :meta private:
        """
        return plus1(v)

    #: Allowed types for the selected field.
    caller_id_types: Optional[list[CallerIdSelectedType]] = Field(alias='types', default=None)
    #: Which type of outgoing Caller ID will be used.
    selected: CallerIdSelectedType
    #: Direct number which will be shown if DIRECT_LINE is selected.
    direct_number: Optional[str] = None
    #: Extension number which will be shown if DIRECT_LINE is selected.
    extension_number: Optional[str] = None
    #: Location number which will be shown if LOCATION_NUMBER is selected.
    location_number: Optional[str] = None
    #: True id the location number is toll free
    toll_free_location_number: Optional[bool] = None
    #: Mobile number which will be shown if MOBILE_NUMBER is selected.
    mobile_number: Optional[str] = None
    #: This value must be an assigned number from the person's location.
    custom_number: Optional[str] = None
    #: Person's Caller ID first name. Characters of %, +, \`, \" and Unicode characters are not allowed.
    first_name: Optional[str] = None
    #: Person's Caller ID last name. Characters of %, +, \`, \" and Unicode characters are not allowed.
    last_name: Optional[str] = None
    #: block caller id in forwarded calls
    block_in_forward_calls_enabled: Optional[bool] = None
    #: Designates which type of External Caller ID Name policy is used. Default is DIRECT_LINE.
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy] = None
    #: Custom External Caller Name, which will be shown if External Caller ID Name is OTHER.
    custom_external_caller_id_name: Optional[str] = None
    #: location external caller ID name
    location_external_caller_id_name: Optional[str] = None

    def configure_params(self) -> dict:
        """
        Get a dict with values that can be used to configure the caller id settings

        :return: dict
        :rtype: dict

        Example:

        .. code-block:: python

            caller_id = wx_api.person_settings.caller_id.read(person_id=...)
            caller_id.first_name = 'Bob'
            wx_api.person_settings.caller_id.configure(person_id=...,
                                                       **caller_id.configure_params())

        """
        data = self.model_dump()
        to_keep = {
            'selected',
            'custom_number',
            'first_name',
            'last_name',
            'external_caller_id_name_policy',
            'custom_external_caller_id_name'}
        result = {k: v for k, v in data.items()
                  if v is not None and k in to_keep}
        return result


class CallerIdApi(PersonSettingsApiChild):
    """
    API for person's caller id settings
    """

    feature = 'callerId'

    def read(self, person_id: str, org_id: str = None) -> CallerId:
        """
        Retrieve a Person's Caller ID Settings

        Caller ID settings control how a person’s information is displayed when making outgoing calls.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return CallerId.model_validate(self.get(ep, params=params))

    def configure(self, person_id: str, org_id: str = None,
                  selected: CallerIdSelectedType = None,
                  custom_number: str = None,
                  first_name: str = None,
                  last_name: str = None,
                  external_caller_id_name_policy: ExternalCallerIdNamePolicy = None,
                  custom_external_caller_id_name: str = None):
        """
        Configure a Person's Caller ID Settings

        Caller ID settings control how a person’s information is displayed when making outgoing calls.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param selected: Which type of outgoing Caller ID will be used.
        :type selected: CallerIdSelectedType
        :param custom_number: This value must be an assigned number from the person\'s location.
        :type custom_number: str
        :param first_name: Person\'s Caller ID first name. Characters of %, +, \`, \" and Unicode characters are not
            allowed.

        :type first_name: str
        :param last_name: Person\'s Caller ID last name. Characters of %, +, \`, \" and Unicode characters are not
            allowed.
        :type last_name: str
        :param external_caller_id_name_policy: Designates which type of External Caller ID Name policy is used.
            Default is DIRECT_LINE.
        :type external_caller_id_name_policy: ExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Custom External Caller Name, which will be shown if External Caller ID
            Name is OTHER.
        :type custom_external_caller_id_name: str

        """
        data = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                if i > 2 and v is not None}
        params = org_id and {'orgId': org_id} or None
        ep = self.f_ep(person_id=person_id)
        self.put(ep, params=params, json=data)

    def configure_settings(self, person_id: str, settings: CallerId, org_id: str = None):
        params = org_id and {'orgId': org_id} or None
        data = settings.model_dump_json(exclude_unset=True, include={'selected': True,
                                                          'custom_number': True,
                                                          'first_name': True,
                                                          'last_name': True,
                                                          'block_in_forward_calls_enabled': True,
                                                          'external_caller_id_name_policy': True,
                                                          'custom_external_caller_id_name': True,
                                                          })
        ep = self.f_ep(person_id=person_id)
        self.put(ep, params=params, data=data)
