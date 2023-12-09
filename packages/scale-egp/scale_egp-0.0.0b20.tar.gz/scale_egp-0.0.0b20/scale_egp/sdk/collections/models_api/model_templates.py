from typing import List, Optional

import httpx
from scale_egp.sdk.models.model_schemas.parameter_schema import ParameterSchema
from scale_egp.utils.model_utils import dict_without_none_values, make_partial_model
from scale_egp.sdk.models.model_vendor_configuration import ModelVendorConfiguration

from scale_egp.sdk.models.model_api_models import (
    ModelEndpointType,
    ModelTemplateRequest,
    ModelTemplate,
    ModelType,
)
from scale_egp.utils.api_utils import APIEngine, long_timeout


PartialModelTemplateRequest = make_partial_model(ModelTemplateRequest)


class ModelTemplateCollection(APIEngine):
    """
    Collections class for EGP Models.
    """

    _sub_path = "v3/model-templates"

    def create(
        self,
        name: str,
        endpoint_type: ModelEndpointType,
        model_type: ModelType,
        vendor_configuration: ModelVendorConfiguration,
        model_creation_parameters_schema: Optional[ParameterSchema] = None,
        model_request_parameters_schema: Optional[ParameterSchema] = None,
        account_id: Optional[str] = None,
    ) -> ModelTemplate:
        """
        Create a new EGP Model.
        """
        response = self._post(
            sub_path=self._sub_path,
            request=ModelTemplateRequest(
                name=name,
                endpoint_type=endpoint_type,
                model_type=model_type,
                vendor_configuration=vendor_configuration,
                model_creation_parameters_schema=model_creation_parameters_schema,
                model_request_parameters_schema=model_request_parameters_schema,
                account_id=account_id or self._api_client.account_id,
            ),
            timeout=long_timeout,
        )
        return ModelTemplate.from_dict(response.json())

    def get(
        self,
        id: str,
    ) -> ModelTemplate:
        """
        Get a Model by ID.
        """
        response = self._get(
            sub_path=f"{self._sub_path}/{id}",
        )
        return ModelTemplate.from_dict(response.json())

    def update(
        self,
        id: str,
        *,
        name: str,
        endpoint_type: Optional[ModelEndpointType] = None,
        model_type: Optional[ModelType] = None,
        vendor_configuration: Optional[ModelVendorConfiguration] = None,
        model_creation_parameters_schema: Optional[ParameterSchema] = None,
        model_request_parameters_schema: Optional[ParameterSchema] = None,
    ) -> ModelTemplate:
        """
        Update a Model by ID.

        """
        response = self._patch(
            sub_path=f"{self._sub_path}/{id}",
            request=PartialModelTemplateRequest(
                **dict_without_none_values(
                    dict(
                        name=name,
                        endpoint_type=endpoint_type,
                        model_type=model_type,
                        vendor_configuration=vendor_configuration,
                        model_creation_parameters_schema=model_creation_parameters_schema,
                        model_request_parameters_schema=model_request_parameters_schema,
                    )
                )
            ),
        )
        return ModelTemplate.from_dict(response.json())

    def delete(
        self,
        id: str,
    ) -> bool:
        """
        Delete a Studio Project by ID.

        """
        response = self._delete(
            sub_path=f"{self._sub_path}/{id}",
        )
        return response.status_code == httpx.codes.ok

    def list(
        self,
    ) -> List[ModelTemplate]:
        """
        List all Studio Projects.

        Returns:
            A list of Studio Projects.
        """
        response = self._get(
            sub_path=self._sub_path,
        )
        return [ModelTemplate.from_dict(model_template) for model_template in response.json()]
