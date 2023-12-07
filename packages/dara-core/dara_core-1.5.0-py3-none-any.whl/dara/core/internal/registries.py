"""
Copyright 2023 Impulse Innovations Limited


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from datetime import datetime
from typing import Any, Callable, Mapping, Set

from dara.core.auth import BaseAuthConfig
from dara.core.base_definitions import ActionDef, ActionResolverDef, UploadResolverDef
from dara.core.defaults import CORE_ACTIONS, CORE_COMPONENTS, INITIAL_CORE_INTERNALS
from dara.core.definitions import (
    ComponentTypeAnnotation,
    EndpointConfiguration,
    Template,
)
from dara.core.interactivity.data_variable import DataVariableRegistryEntry
from dara.core.interactivity.derived_variable import (
    DerivedVariableRegistryEntry,
    LatestValueRegistryEntry,
)
from dara.core.internal.registry import Registry, RegistryType
from dara.core.internal.websocket import CustomClientMessagePayload

action_def_registry = Registry[ActionDef](RegistryType.ACTION_DEF, CORE_ACTIONS)   # all registered actions
action_registry = Registry[ActionResolverDef](RegistryType.ACTION)   # functions for actions requiring backend calls
upload_resolver_registry = Registry[UploadResolverDef](
    RegistryType.UPLOAD_RESOLVER
)   # functions for upload resolvers requiring backend calls
component_registry = Registry[ComponentTypeAnnotation](RegistryType.COMPONENTS, CORE_COMPONENTS)
config_registry = Registry[EndpointConfiguration](RegistryType.ENDPOINT_CONFIG)
data_variable_registry = Registry[DataVariableRegistryEntry](RegistryType.DATA_VARIABLE, allow_duplicates=False)
derived_variable_registry = Registry[DerivedVariableRegistryEntry](
    RegistryType.DERIVED_VARIABLE, allow_duplicates=False
)
latest_value_registry = Registry[LatestValueRegistryEntry](RegistryType.LAST_VALUE, allow_duplicates=False)
template_registry = Registry[Template](RegistryType.TEMPLATE)
auth_registry = Registry[BaseAuthConfig](RegistryType.AUTH_CONFIG)
utils_registry = Registry[Any](RegistryType.UTILS, INITIAL_CORE_INTERNALS)
static_kwargs_registry = Registry[Mapping[str, Any]](RegistryType.STATIC_KWARGS)

websocket_registry = Registry[str](RegistryType.WEBSOCKET_CHANNELS)
"""maps session_id -> WS channel"""

sessions_registry = Registry[Set[str]](RegistryType.USER_SESSION)
"""maps user_identifier -> session_ids """

pending_tokens_registry = Registry[datetime](RegistryType.PENDING_TOKENS)
"""map of token -> expiry, for tokens pending connection"""

custom_ws_handlers_registry = Registry[Callable[[str, CustomClientMessagePayload], Any]](
    RegistryType.CUSTOM_WS_HANDLERS
)
"""map of custom kind name -> handler function(channel: str, message: CustomClientMessagePayload)"""
