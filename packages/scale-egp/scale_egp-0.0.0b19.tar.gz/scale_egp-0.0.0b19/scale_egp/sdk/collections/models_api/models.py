from typing import Any, List, Optional, Dict

import httpx

from scale_egp.utils.model_utils import dict_without_none_values, make_partial_model
from scale_egp.sdk.models.model_api_models import ModelAlias, ModelAliasRequest, ModelState
from scale_egp.sdk.models.vendor_configuration import ModelVendor

from scale_egp.utils.api_utils import APIEngine


# Rename ModelAlias to Model in the SDk
class Model(ModelAlias):
    pass


PartialModelAliasRequest = make_partial_model(ModelAliasRequest)


class ModelCollection(APIEngine):
    """
    Collections class for EGP Models.
    """

    _sub_path = "v2/model-catalog"

    def create(
        self,
        name: str,
        model_template_id: str,
        model_state: ModelState = ModelState.DISABLED,
        base_model_id: Optional[str] = None,
        user_parameter_values: Optional[Dict[str, Any]] = None,
    ) -> ModelAlias:
        """
        Create a new EGP Model.
        """
        response = self._post(
            sub_path=self._sub_path,
            request=ModelAliasRequest(
                name=name,
                model_template_id=model_template_id,
                model_state=model_state,
                base_model_id=base_model_id,
                user_parameter_values=user_parameter_values or {},
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

    def update(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        model_state: Optional[ModelState] = None,
        vendor: Optional[ModelVendor] = None,
        vendor_name: Optional[str] = None,
        base_model_id: Optional[str] = None,
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
                        model_state=model_state,
                        vendor=vendor,
                        vendor_name=vendor_name,
                        base_model_id=base_model_id,
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
