from typing import Any, List, Optional, Dict

import httpx
from pydantic import BaseModel

from scale_egp.utils.model_utils import dict_without_none_values, make_partial_model
from scale_egp.sdk.models.model_api_models import ModelAlias, ModelAliasRequest
from scale_egp.sdk.models.model_vendor_configuration import ModelVendor
from scale_egp.sdk.models.model_schemas.model_schemas import MODEL_SCHEMAS
from scale_egp.sdk.models.model_schemas.common import BaseModelRequest, BaseModelResponse

from scale_egp.utils.api_utils import APIEngine


# Rename ModelAlias to Model in the SDk
class Model(ModelAlias):
    pass


PartialModelAliasRequest = make_partial_model(ModelAliasRequest)


class ModelCollection(APIEngine):
    """
    Collections class for EGP Models.
    """

    _sub_path = "v3/models"

    def create(
        self,
        name: str,
        model_template_id: str,
        base_model_id: Optional[str] = None,
        model_creation_parameters: Optional[Dict[str, Any]] = None,
        account_id: Optional[str] = None,
    ) -> ModelAlias:
        """
        Create a new EGP Model.
        """
        response = self._post(
            sub_path=self._sub_path,
            request=ModelAliasRequest(
                name=name,
                model_template_id=model_template_id,
                base_model_id=base_model_id,
                model_creation_parameters=model_creation_parameters,
                account_id=account_id or self._api_client.account_id,
            ),
        )
        return Model.from_dict(response.json())

    def get(
        self,
        id: str,
    ) -> Model:
        """
        Get a Model by ID.
        """
        response = self._get(
            sub_path=f"{self._sub_path}/{id}",
        )
        return Model.from_dict(response.json())

    def execute(self, id: str, request: BaseModelRequest) -> BaseModelResponse:
        """
        Get a Model by ID.
        """
        # TODO: verify model_request_parameters matches model template's model_request_parameters_schema if set
        model_alias = self.get(id)
        model_template = self._api_client.model_templates().get(model_alias.model_template_id)
        model_type = model_template.model_type
        model_request_cls, model_response_cls = MODEL_SCHEMAS[model_type]
        assert isinstance(request, model_request_cls)
        response = self._post(
            sub_path=f"{self._sub_path}/{id}/execute",
            request=request,
            timeout=10 * 60,  # 10 minutes
        )
        return model_response_cls(**response.json())

    def update(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        model_template_id: Optional[str] = None,
        base_model_id: Optional[str] = None,
        model_creation_parameters: Optional[dict[str, Any]] = None,
    ) -> Model:
        """
        Update a Model by ID.

        """
        response = self._patch(
            sub_path=f"{self._sub_path}/{id}",
            request=PartialModelAliasRequest(
                **dict_without_none_values(
                    dict(
                        name=name,
                        model_template_id=model_template_id,
                        base_model_id=base_model_id,
                        model_creation_parameters=model_creation_parameters,
                    ),
                )
            ),
        )
        return Model.from_dict(response.json())

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
    ) -> List[Model]:
        """
        List all Studio Projects.

        Returns:
            A list of Studio Projects.
        """
        response = self._get(
            sub_path=self._sub_path,
        )
        return [Model.from_dict(model) for model in response.json()]
