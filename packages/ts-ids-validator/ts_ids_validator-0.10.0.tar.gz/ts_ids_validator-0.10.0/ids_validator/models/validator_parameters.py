import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ids_validator.convention_versions import Conventions
from ids_validator.ids_node import Node
from ids_validator.utils import (
    IdsIdentity,
    get_ids_identity,
    get_validator_type,
    read_schema,
)


@dataclass
class IdsArtifact:
    schema: dict = field(default_factory=dict)
    athena: dict = field(default_factory=dict)
    elasticsearch: dict = field(default_factory=dict)
    expected: dict = field(default_factory=dict)
    path: Path = Path()

    @staticmethod
    def from_schema_path(schema_path: Path) -> "IdsArtifact":
        """Create validator parameters given the path to schema.json"""

        ids_folder_path = schema_path.parent
        athena_path = ids_folder_path.joinpath("athena.json")
        elasticsearch_path = ids_folder_path.joinpath("elasticsearch.json")
        expected_path = ids_folder_path.joinpath("expected.json")

        missing_files = tuple(
            file.name
            for file in (schema_path, athena_path, elasticsearch_path, expected_path)
            if not file.exists()
        )
        if missing_files:
            raise FileNotFoundError(
                "The following artifact files must exist but were not found: "
                f"{missing_files}. Check the artifact folder: '{schema_path.parent}'."
            )
        schema = read_schema(schema_path)
        athena = json.loads(athena_path.read_text())
        elasticsearch = json.loads(elasticsearch_path.read_text())
        expected = json.loads(expected_path.read_text())

        return IdsArtifact(
            schema=schema,
            athena=athena,
            elasticsearch=elasticsearch,
            expected=expected,
            path=ids_folder_path,
        )

    def get_identity(self) -> IdsIdentity:
        """Populate the IDS identity from the schema."""
        return get_ids_identity(self.schema)


@dataclass
class ValidatorParameters:
    """Class for keeping all parameters that could/would be used by validator"""

    artifact: IdsArtifact = field(default_factory=IdsArtifact)
    previous_artifact: Optional[IdsArtifact] = None

    @property
    def convention_version(self) -> Conventions:
        """Read @idsConventionVersion from the schema."""
        return get_validator_type(self.artifact.schema)

    @staticmethod
    def from_comparative_schema_paths(
        schema_path: Path, previous_schema_path: Path
    ) -> "ValidatorParameters":
        return ValidatorParameters(
            artifact=IdsArtifact.from_schema_path(schema_path),
            previous_artifact=IdsArtifact.from_schema_path(previous_schema_path),
        )

    def root_node(self) -> Node:
        return Node(schema=self.artifact.schema)
