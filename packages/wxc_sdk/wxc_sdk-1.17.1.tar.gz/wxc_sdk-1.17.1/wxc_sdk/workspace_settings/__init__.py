"""
Workspace settings, mostly identical to user settings

"""
from dataclasses import dataclass

from .devices import WorkspaceDevicesApi
from .numbers import WorkspaceNumbersApi
from ..api_child import ApiChild
from ..person_settings.call_intercept import CallInterceptApi
from ..person_settings.call_waiting import CallWaitingApi
from ..person_settings.caller_id import CallerIdApi
from ..person_settings.forwarding import PersonForwardingApi
from ..person_settings.monitoring import MonitoringApi
from ..person_settings.permissions_in import IncomingPermissionsApi
from ..person_settings.permissions_out import OutgoingPermissionsApi
from ..rest import RestSession

__all__ = ['WorkspaceSettingsApi']


@dataclass(init=False)
class WorkspaceSettingsApi(ApiChild, base='workspaces'):
    """
    API for all workspace settings.

    Most of the workspace settings are equivalent to corresponding user settings. For these settings the attributes of
    this class are instances of the respective user settings APIs. When calling endpoints of these APIs workspace IDs
    need to be passed to the ``person_id`` parameter of the called function.
    """
    forwarding: PersonForwardingApi
    call_waiting: CallWaitingApi
    caller_id: CallerIdApi
    monitoring: MonitoringApi
    numbers: WorkspaceNumbersApi
    permissions_in: IncomingPermissionsApi
    permissions_out: OutgoingPermissionsApi
    devices: WorkspaceDevicesApi
    call_intercept: CallInterceptApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.forwarding = PersonForwardingApi(session=session, workspaces=True)
        self.call_waiting = CallWaitingApi(session=session, workspaces=True)
        self.caller_id = CallerIdApi(session=session, workspaces=True)
        self.monitoring = MonitoringApi(session=session, workspaces=True)
        self.numbers = WorkspaceNumbersApi(session=session)
        self.permissions_in = IncomingPermissionsApi(session=session, workspaces=True)
        self.permissions_out = OutgoingPermissionsApi(session=session, workspaces=True)
        self.devices = WorkspaceDevicesApi(session=session)
        self.call_intercept = CallInterceptApi(session=session, workspaces=True)
