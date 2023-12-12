from pathlib import Path
from typing import Optional

from rich.console import Console

from ids_validator.models.validator_parameters import IdsArtifact, ValidatorParameters
from ids_validator.validator import Validator, default_console


def validate_ids(
    ids_dir: Path,
    previous_ids_dir: Optional[Path] = None,
    console: Console = default_console,
) -> bool:
    """Run IDS validator and print warnings / failures to console

    Args:
        previous_ids_dir: (Path): Path to folder with previous version of IDS
        ids_dir (Path): Path to IDS folder
        version (Optional[str], optional): It accepts following values:
        - `generic`
        - a supported `idsConventionVersion` eg v1.0.0
        - `None`: In this case `@idsConventionVersion` will be read from `schema.json`.
        If it is not defined, `generic` will be used as `version`

    Returns:
        bool: True if IDS is valid else False
    """
    schema_path = ids_dir / "schema.json"

    if previous_ids_dir is not None:
        parameters = ValidatorParameters(
            artifact=IdsArtifact.from_schema_path(schema_path=schema_path),
            previous_artifact=IdsArtifact.from_schema_path(
                previous_ids_dir / "schema.json"
            ),
        )
    else:
        parameters = ValidatorParameters(
            artifact=IdsArtifact.from_schema_path(schema_path=schema_path)
        )

    validator = Validator(parameters, console=console)
    validator.validate_ids()

    if validator.has_critical_failures:
        validator.console.print(
            "[b i red]\nValidation Failed with critical error.[/b i red]"
        )
        return False

    validator.console.print(
        "[b i green]Validation Complete. No error found.[/b i green]"
    )

    return True
