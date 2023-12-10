from datetime import date, datetime
from typing import List, Optional, Union

from benchling_api_client.v2.beta.models.app_config_field_type import AppConfigFieldType
from benchling_api_client.v2.beta.models.base_manifest_config import BaseManifestConfig
from benchling_api_client.v2.beta.models.dropdown_dependency import DropdownDependency
from benchling_api_client.v2.beta.models.dropdown_dependency_types import DropdownDependencyTypes
from benchling_api_client.v2.beta.models.entity_schema_dependency import EntitySchemaDependency
from benchling_api_client.v2.beta.models.entity_schema_dependency_type import EntitySchemaDependencyType
from benchling_api_client.v2.beta.models.field_definitions_manifest import FieldDefinitionsManifest
from benchling_api_client.v2.beta.models.manifest_array_config import ManifestArrayConfig
from benchling_api_client.v2.beta.models.manifest_float_scalar_config import ManifestFloatScalarConfig
from benchling_api_client.v2.beta.models.manifest_integer_scalar_config import ManifestIntegerScalarConfig
from benchling_api_client.v2.beta.models.manifest_scalar_config import ManifestScalarConfig
from benchling_api_client.v2.beta.models.manifest_text_scalar_config import ManifestTextScalarConfig
from benchling_api_client.v2.beta.models.resource_dependency import ResourceDependency
from benchling_api_client.v2.beta.models.resource_dependency_types import ResourceDependencyTypes
from benchling_api_client.v2.beta.models.scalar_config_types import ScalarConfigTypes
from benchling_api_client.v2.beta.models.schema_dependency import SchemaDependency
from benchling_api_client.v2.beta.models.schema_dependency_subtypes import SchemaDependencySubtypes
from benchling_api_client.v2.beta.models.schema_dependency_types import SchemaDependencyTypes
from benchling_api_client.v2.beta.models.workflow_task_schema_dependency import WorkflowTaskSchemaDependency
from benchling_api_client.v2.beta.models.workflow_task_schema_dependency_output import (
    WorkflowTaskSchemaDependencyOutput,
)
from benchling_api_client.v2.beta.models.workflow_task_schema_dependency_type import (
    WorkflowTaskSchemaDependencyType,
)
from benchling_api_client.v2.extensions import UnknownType
from benchling_api_client.v2.stable.extensions import NotPresentError

from benchling_sdk.apps.config.scalars import JsonType
from benchling_sdk.models import (
    AaSequence,
    AssayResult,
    AssayRun,
    Box,
    Container,
    CustomEntity,
    DnaOligo,
    DnaSequence,
    Entry,
    Location,
    Mixture,
    Molecule,
    Plate,
    Request,
    RnaOligo,
    RnaSequence,
    WorkflowTask,
)

_MODEL_TYPES_FROM_SCHEMA_TYPE = {
    SchemaDependencyTypes.CONTAINER_SCHEMA: Container,
    SchemaDependencyTypes.PLATE_SCHEMA: Plate,
    SchemaDependencyTypes.BOX_SCHEMA: Box,
    SchemaDependencyTypes.LOCATION_SCHEMA: Location,
    SchemaDependencyTypes.ENTRY_SCHEMA: Entry,
    SchemaDependencyTypes.REQUEST_SCHEMA: Request,
    SchemaDependencyTypes.RESULT_SCHEMA: AssayResult,
    SchemaDependencyTypes.RUN_SCHEMA: AssayRun,
    SchemaDependencyTypes.WORKFLOW_TASK_SCHEMA: WorkflowTask,
}


_SCALAR_TYPES_FROM_CONFIG = {
    ScalarConfigTypes.BOOLEAN: bool,
    ScalarConfigTypes.DATE: date,
    ScalarConfigTypes.DATETIME: datetime,
    ScalarConfigTypes.FLOAT: float,
    ScalarConfigTypes.INTEGER: int,
    ScalarConfigTypes.JSON: JsonType,
    ScalarConfigTypes.TEXT: str,
}


_FIELD_SCALAR_TYPES_FROM_CONFIG = {
    AppConfigFieldType.BOOLEAN: bool,
    AppConfigFieldType.DATE: date,
    AppConfigFieldType.DATETIME: datetime,
    AppConfigFieldType.FLOAT: float,
    AppConfigFieldType.INTEGER: int,
    AppConfigFieldType.JSON: JsonType,
    AppConfigFieldType.TEXT: str,
}


ModelType = Union[AssayResult, AssayRun, Box, Container, Entry, Location, Plate, Request]

_INSTANCE_FROM_SCHEMA_SUBTYPE = {
    SchemaDependencySubtypes.AA_SEQUENCE: AaSequence,
    SchemaDependencySubtypes.CUSTOM_ENTITY: CustomEntity,
    SchemaDependencySubtypes.DNA_SEQUENCE: DnaSequence,
    SchemaDependencySubtypes.DNA_OLIGO: DnaOligo,
    SchemaDependencySubtypes.MIXTURE: Mixture,
    SchemaDependencySubtypes.MOLECULE: Molecule,
    SchemaDependencySubtypes.RNA_OLIGO: RnaOligo,
    SchemaDependencySubtypes.RNA_SEQUENCE: RnaSequence,
}

EntitySubtype = Union[
    AaSequence, CustomEntity, DnaOligo, DnaSequence, Mixture, Molecule, RnaOligo, RnaSequence
]

AnyDependency = Union[
    BaseManifestConfig,
    DropdownDependency,
    EntitySchemaDependency,
    FieldDefinitionsManifest,
    ManifestArrayConfig,
    ManifestScalarConfig,
    ResourceDependency,
    SchemaDependency,
    WorkflowTaskSchemaDependency,
]

ArrayElementDependency = Union[
    SchemaDependency,
    EntitySchemaDependency,
    WorkflowTaskSchemaDependency,
    DropdownDependency,
    ResourceDependency,
    ManifestScalarConfig,
]


class UnsupportedSubTypeError(Exception):
    """Error when an unsupported subtype is encountered."""

    pass


def field_definitions_from_dependency(
    dependency: Union[
        EntitySchemaDependency,
        SchemaDependency,
        WorkflowTaskSchemaDependency,
        WorkflowTaskSchemaDependencyOutput,
    ]
) -> List[FieldDefinitionsManifest]:
    """Safely return a list of field definitions from a schema dependency or empty list."""
    try:
        if hasattr(dependency, "field_definitions"):
            return dependency.field_definitions
    # We can't seem to handle this programmatically by checking isinstance() or field truthiness
    except NotPresentError:
        pass
    return []


def element_definition_from_dependency(dependency: ManifestArrayConfig) -> List[ArrayElementDependency]:
    """Safely return an element definition as a list of dependencies from an array dependency or empty list."""
    try:
        if hasattr(dependency, "element_definition"):
            return [
                _fix_element_definition_deserialization(element) for element in dependency.element_definition
            ]
    # We can't seem to handle this programmatically by checking isinstance() or field truthiness
    except NotPresentError:
        pass
    return []


def enum_from_dependency(
    dependency: Union[
        ManifestFloatScalarConfig,
        ManifestIntegerScalarConfig,
        ManifestTextScalarConfig,
    ]
) -> List:
    """Safely return an enum from a scalar config."""
    try:
        if hasattr(dependency, "enum"):
            return dependency.enum
    # We can't seem to handle this programmatically by checking isinstance() or field truthiness
    except NotPresentError:
        pass
    return []


# TODO BNCH-57036 All element definitions currently deserialize to UnknownType. Hack around this temporarily
def _fix_element_definition_deserialization(
    element: Union[UnknownType, ArrayElementDependency]
) -> ArrayElementDependency:
    if isinstance(element, UnknownType):
        if "type" in element.value:
            element_type = element.value["type"]
            if element_type == WorkflowTaskSchemaDependencyType.WORKFLOW_TASK_SCHEMA:
                return WorkflowTaskSchemaDependency.from_dict(element.value)
            elif element_type == EntitySchemaDependencyType.ENTITY_SCHEMA:
                return EntitySchemaDependency.from_dict(element.value)
            elif element_type in [member.value for member in SchemaDependencyTypes]:
                return SchemaDependency.from_dict(element.value)
            elif element_type == DropdownDependencyTypes.DROPDOWN:
                return DropdownDependency.from_dict(element.value)
            elif element_type in [member.value for member in ResourceDependencyTypes]:
                return ResourceDependency.from_dict(element.value)
            elif element_type in [member.value for member in ScalarConfigTypes]:
                return type(element_type).from_dict(element.value)
        raise NotImplementedError(f"No array deserialization fix for {element}")
    return element


def workflow_task_schema_output_from_dependency(
    dependency: WorkflowTaskSchemaDependency,
) -> Optional[WorkflowTaskSchemaDependencyOutput]:
    """Safely return a workflow task schema output from a workflow task schema or None."""
    try:
        if hasattr(dependency, "output"):
            return dependency.output
    # We can't seem to handle this programmatically by checking isinstance() or output truthiness
    except NotPresentError:
        pass
    return None


def options_from_dependency(dependency: DropdownDependency) -> List[BaseManifestConfig]:
    """Safely return a list of options from a dropdown dependency or empty list."""
    try:
        if hasattr(dependency, "options"):
            return dependency.options
    # We can't seem to handle this programmatically by checking isinstance() or field truthiness
    except NotPresentError:
        pass
    return []


def subtype_from_entity_schema_dependency(
    dependency: EntitySchemaDependency,
) -> Optional[SchemaDependencySubtypes]:
    """Safely return an entity schema dependency's subtype, if present."""
    try:
        if hasattr(dependency, "subtype") and dependency.subtype:
            return dependency.subtype
    # We can't seem to handle this programmatically by checking isinstance() or field truthiness
    except NotPresentError:
        pass
    return None
