from typing import List, Optional

import httpx

from scale_egp.sdk.models import ApplicationSpec, ApplicationSpecRequest
from scale_egp.utils.api_utils import APIEngine


class ApplicationSpecCollection(APIEngine):

    _sub_path = "v2/application-specs"

    def create(
        self,
        name: str,
        description: str,
    ) -> ApplicationSpec:
        """
        Create a new Application Spec.

        Args:
            name: The name of the Application Spec.
            description: The description of the Application Spec.

        Returns:
            The newly created Application Spec.
        """

        response = self._post(
            sub_path=self._sub_path,
            request=ApplicationSpecRequest(
                name=name,
                description=description,
            ),
        )
        return ApplicationSpec.from_dict(response.json())

    def get(
        self,
        id: str,
    ) -> ApplicationSpec:
        """
        Get an Application Spec by ID.

        Args:
            id: The ID of the Application Spec.

        Returns:
            The Application Spec.
        """
        response = self._get(
            sub_path=f"{self._sub_path}/{id}",
        )
        return ApplicationSpec.from_dict(response.json())

    def update(
        self,
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> ApplicationSpec:
        """
        Update an Application Spec by ID.

        Args:
            id: The ID of the Application Spec.
            name: The name of the Application Spec.
            description: The description of the Application Spec.

        Returns:
            The updated Application Spec.
        """
        response = self._patch(
            sub_path=f"{self._sub_path}/{id}",
            request=ApplicationSpecRequest.partial(
                name=name,
                description=description,
            ),
        )
        return ApplicationSpec.from_dict(response.json())

    def delete(
        self,
        id: str,
    ) -> bool:
        """
        Delete an Application Spec by ID.

        Args:
            id: The ID of the Application Spec.
        """
        response = self._delete(
            sub_path=f"{self._sub_path}/{id}",
        )
        return response.status_code == httpx.codes.ok

    def list(
        self,
    ) -> List[ApplicationSpec]:
        """
        List all Application Specs.

        Returns:
            A list of Application Specs.
        """
        response = self._get(
            sub_path=self._sub_path,
        )
        return [ApplicationSpec.from_dict(spec) for spec in response.json()]
