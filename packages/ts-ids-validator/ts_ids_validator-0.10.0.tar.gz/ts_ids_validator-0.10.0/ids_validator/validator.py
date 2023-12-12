from typing import Any, Dict, List, Optional, Type

from rich.console import Console

from ids_validator.checks.abstract_checker import AbstractChecker, CheckResults, Log
from ids_validator.checks.generic import (
    AdditionalPropertyChecker,
    AthenaChecker,
    DatacubesChecker,
    RequiredPropertiesChecker,
    RootNodeChecker,
    TypeChecker,
)
from ids_validator.checks.generic.athena_column_name_resolution_check import (
    AthenaColumnNameResolutionCheck,
)
from ids_validator.checks.generic.athena_normalized_field_name import (
    AthenaNormalizedFieldNameChecker,
)
from ids_validator.checks.generic.elasticsearch import validate_elasticsearch_json
from ids_validator.checks.generic.expected import ExpectedChecker
from ids_validator.checks.generic.reserved_property_names import ReservedNameChecker
from ids_validator.checks.generic.root_node import (
    IdChecker,
    IdsVersionChecker,
    MetaSchemaChecker,
)
from ids_validator.checks.generic.schema_breaking_change import (
    SchemaBreakingChangeChecker,
    format_failures,
)
from ids_validator.checks.v1 import (
    V1ChildNameChecker,
    V1ConventionVersionChecker,
    V1RelatedFilesChecker,
    V1RootNodeChecker,
    V1SampleNodeChecker,
    V1SnakeCaseChecker,
    V1SystemNodeChecker,
    V1UserNodeChecker,
)
from ids_validator.convention_versions import Conventions
from ids_validator.ids_node import Node, NodePath
from ids_validator.models.validator_parameters import ValidatorParameters

generic_checks: List[Type[AbstractChecker]] = [
    AdditionalPropertyChecker,
    DatacubesChecker,
    RequiredPropertiesChecker,
    RootNodeChecker,
    IdsVersionChecker,
    IdChecker,
    MetaSchemaChecker,
    TypeChecker,
    ExpectedChecker,
    AthenaChecker,
    AthenaColumnNameResolutionCheck,
    AthenaNormalizedFieldNameChecker,
    SchemaBreakingChangeChecker,
    ReservedNameChecker,
]

v1_checks = generic_checks + [
    V1ChildNameChecker,
    V1ConventionVersionChecker,
    V1RootNodeChecker,
    V1SnakeCaseChecker,
    V1SampleNodeChecker,
    V1SystemNodeChecker,
    V1UserNodeChecker,
    V1RelatedFilesChecker,
]


ROOT_NODE_KEY = "root"
BULK_NODE_KEY = "bulk"


class Validator:
    """Main class that runs validation of IDS."""

    def __init__(
        self,
        validator_parameters: ValidatorParameters,
        checks_list: Optional[List[Type[AbstractChecker]]] = None,
    ):
        if checks_list is not None:
            # A non-standard set of checks has been specified
            self.checks_list = checks_list
        else:
            if validator_parameters.convention_version is Conventions.V1_0_0:
                self.checks_list = v1_checks
            else:
                self.checks_list = generic_checks

        self.parameters = validator_parameters
        self.console = Console()
        self.property_failures: Dict[str, list] = {}
        self.has_critical_failures = False
        self.breaking_change_failures: CheckResults = []

    def _traverse(self, schema: dict, path: NodePath = NodePath((ROOT_NODE_KEY,))):
        node = Node(schema=schema, path=path)

        failures = []
        for checker in self.checks_list:
            if not checker.bulk_checker:
                if checker is SchemaBreakingChangeChecker:
                    self.breaking_change_failures += checker.run(node, self.parameters)
                else:
                    failures += checker.run(node, self.parameters)

        if failures:
            self.property_failures[str(node.path)] = list(failures)
            self.log(failures, str(node.path))

        for key, value in schema.items():
            if isinstance(value, dict):
                self._traverse(value, path=path.join(key))

    def _bulk_validation(self, schema: Dict[str, Any]):
        node = Node(schema=schema, path=NodePath(("root",)))
        failures = []
        for checker in self.checks_list:
            if checker.bulk_checker:
                failures += checker.run(node, context=self.parameters)

        if failures:
            self.property_failures["bulk"] = list(failures)
            self.log(failures, "bulk")

    def validate_ids(self):
        """Validate full IDS using ValidatorParameters passed during class construction."""
        self._traverse(schema=self.parameters.artifact.schema)

        if self.breaking_change_failures:
            check_name = "IDS versioning"
            formatted_failures = [
                format_failures(
                    self.breaking_change_failures,
                    self.parameters.previous_artifact.get_identity(),
                    self.parameters.artifact.get_identity(),
                )
            ]
            self.property_failures[check_name] = formatted_failures
            self.log(formatted_failures, check_name)

        self._bulk_validation(schema=self.parameters.artifact.schema)

        es_validation_errors = validate_elasticsearch_json(self.parameters)
        if es_validation_errors:
            self.log(es_validation_errors, "elasticsearch.json")

    def log(
        self,
        messages: CheckResults,
        property_name: str,
        prop_color: str = "red",
    ):
        """Add message to the validation log."""
        self.console.print(f"[b u  {prop_color}]{property_name}[/b u {prop_color}]:")

        for result in sorted(messages):
            if result.level == Log.CRITICAL:
                self.has_critical_failures = True

            msg_level = (
                "Error" if result.level == Log.CRITICAL else "Warning (may ignore)"
            )
            msg_color = "yellow" if result.level == Log.CRITICAL else "white"
            self.console.print(
                f"[italic {msg_color}]    {msg_level}: {result.message}[italic {msg_color}]"
            )
