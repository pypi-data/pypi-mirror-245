from typing import Tuple, Optional
from abc import ABC, abstractmethod
from profiles_rudderstack.recipe import PyNativeRecipe
from profiles_rudderstack.contract import Contract

class MaterializationSpec:
    def __init__(self, output_type: str = "", run_type: str = "", requested_enable_status: str = ""):
        self.output_type = output_type
        self.run_type = run_type
        self.requested_enable_status = requested_enable_status

class BaseModelType(ABC):
    TypeName = "base_model_type"
    # Json Schema
    BuildSpecSchema = {}

    def __init__(self, build_spec: dict, schema_version: int, pb_version: str) -> None:
        self.build_spec = build_spec
        self.schema_version = schema_version
        self.pb_version = pb_version

    def get_contract(self) -> Optional[Contract]:
        """Define the output contract of the model
        
        Returns:
            Optional[Contract]: Output Contract for the model
        """
        return None
    
    def get_entity_key(self) -> Optional[str]:
        """Define the entity key of the model

        Returns:
            str: Entity key of the model
        """
        return None
    
    def get_materialization(self) -> Optional[MaterializationSpec]:
        """Define the materialization of the model

        Returns:
            Optional[MaterializationSpec]: Materialization of the model
        """
        return None
    
    @abstractmethod
    def get_material_recipe(self) -> PyNativeRecipe:
        """Define the material recipe of the model

        Returns:
            Recipe: Material recipe of the model
        """
        raise NotImplementedError()
    
    @abstractmethod
    def validate(self) -> Tuple[bool, str]:
        """Validate the model

        Returns:
            Tuple[bool, str]: Validation result and error message
        """
        if self.schema_version < 43:
            return False, "schema version should >= 43"
        return True, ""
