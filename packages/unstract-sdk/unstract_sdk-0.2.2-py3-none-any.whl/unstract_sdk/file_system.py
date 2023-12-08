import os
from typing import Any, Optional

import requests
from unstract.connectors.constants import Common
from unstract.connectors.filesystems import connectors
from unstract.connectors.filesystems.unstract_file_system import (
    AbstractFileSystem,
    UnstractFileSystem,
)
from unstract_sdk.constants import (
    Connector,
    ConnectorKeys,
    ConnectorType,
    PlatformServiceKeys,
)
from unstract_sdk.helper import SdkHelper
from unstract_sdk.tools import UnstractToolUtils


class UnstractToolFileSystem:
    """Class to handle File connectors for Unstract Tools.

    Notes:
        - PLATFORM_API_KEY environment variable is required.
    """

    def __init__(
        self,
        utils: UnstractToolUtils,
        platform_host: str,
        platform_port: str,
    ) -> None:
        """
        Args:
            utils (UnstractToolUtils): _description_
            platform_host (str): _description_
            platform_port (str): _description_

        Notes:
            - PLATFORM_API_KEY environment variable is required.
            - The platform_host and platform_port are the
                host and port of the platform service.
        """
        self.utils = utils
        self.base_url = SdkHelper.get_platform_base_url(platform_host, platform_port)
        self.bearer_token = os.environ.get(PlatformServiceKeys.PLATFORM_API_KEY)
        self.fs_connectors = connectors

    def get_fsspec(
        self, tool_instance_id: str, connector_type: str = ConnectorType.OUTPUT
    ) -> Optional[AbstractFileSystem]:
        """Get FsSpec for fileSystem
            1. Get the connection settings from platform service
            using the tool_instance_id
            2. Create UnstractFileSystem based object using the settings
                2.1 Find the type of the database (From Connector Registry)
                2.2 Create the object using the type
                (derived class of UnstractFileSystem)
            3. Send Object.get_fsspec_fs() to the caller

        Args:
            tool_instance_id (str): tool Instance Id
            connector_type (str, optional): _description_.
                Defaults to ConnectorType.OUTPUT.

        Returns:
            Any: _description_
        """
        url = f"{self.base_url}/connector_instance/{Connector.FILE_SYSTEM}"
        query_params = {
            ConnectorKeys.TOOL_INSTANCE_ID: tool_instance_id,
            ConnectorKeys.CONNECTOR_TYPE: connector_type,
        }
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        response = requests.get(url, headers=headers, params=query_params)
        if response.status_code == 200:
            connector_data: dict[str, Any] = response.json()
            connector_id = connector_data.get(ConnectorKeys.CONNECTOR_ID)
            connector_instance_id = connector_data.get(ConnectorKeys.ID)
            settings = connector_data.get(ConnectorKeys.CONNECTOR_METADATA)
            self.utils.stream_log(
                "Successfully retrieved connector settings "
                f"for connector: {connector_instance_id}"
            )
            if connector_id in self.fs_connectors:
                connector = self.fs_connectors[connector_id][Common.METADATA][
                    Common.CONNECTOR
                ]
                connector_class: UnstractFileSystem = connector(settings)
                return connector_class.get_fsspec_fs()
            else:
                self.utils.stream_log(
                    f"FileSystem not found for connector: {connector_id}", level="ERROR"
                )
                return None

        elif response.status_code == 404:
            self.utils.stream_log(
                f"connector not found for: for tool instance {tool_instance_id}",
                level="ERROR",
            )
            return None

        else:
            self.utils.stream_log(
                (
                    f"Error while retrieving connector "
                    "for tool instance: "
                    f"{tool_instance_id} / {response.reason}"
                ),
                level="ERROR",
            )
            return None
