# TetraScience IDS Artifact Validator <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Validate an IDS](#validate-an-ids)
  - [Validate an IDS and check for breaking changes from a previous version](#validate-an-ids-and-check-for-breaking-changes-from-a-previous-version)
- [Validation](#validation)
  - [Generic](#generic)
    - [`schema.json`](#schemajson)
    - [`elasticsearch.json`](#elasticsearchjson)
    - [`athena.json`](#athenajson)
    - [`expected.json`](#expectedjson)
    - [Breaking change validation](#breaking-change-validation)
  - [Tetra Data validation](#tetra-data-validation)
- [Changelog](#changelog)
  - [v0.10.0](#v0100)
  - [v0.9.16](#v0916)
  - [v0.9.15](#v0915)
  - [v0.9.14](#v0914)
  - [v0.9.13](#v0913)
  - [v0.9.12](#v0912)
  - [v0.9.11](#v0911)
  - [v0.9.10](#v0910)
  - [v0.9.9](#v099)
  - [v0.9.8](#v098)
  - [v0.9.7](#v097)
  - [v0.9.6](#v096)

## Overview

The TetraScience IDS Artifact Validator checks that IDS artifacts follow a set of rules which
make them compatible with the Tetra Data Platform, and optionally validates that they are
compatible with additional IDS design conventions.
The validator either passes or fails with a list of the checks which led to the failure.

The validator checks these files in an IDS folder:

- schema.json
- elasticsearch.json
- athena.json

Note that there is a distinction between IDS Artifact validation and IDS instance validation.
This validator checks that the IDS Artifact files listed above are valid; an IDS instance validator would check that a data instance is valid against the corresponding IDS schema using a JSON Schema validator - this package does not do IDS instance validation.

## Version <!-- omit in toc -->

v0.10.0

## Installation

Installing this package requires access to the TetraScience JFrog Artifactory package repository.

Run `pip install ts-ids-validator` in the environment where you want to install the validator.
Or install using a package manager, with `poetry` for example: `poetry add --dev ts-ids-validator`.

This will install a script which can be run from the command line, `validate-ids-artifact`, which is equivalent to running `python -m ids_validator` - see below for usage.

## Usage

Run `validate-ids-artifact -h` to see the help for this command.

### Validate an IDS

With the CLI interface:

```bash
validate-ids-artifact --ids_dir=path/to/ids/folder
```

This will validate that the IDS is compatible with the Tetra Data Platform.

If the schema contains `properties.@idsConventionVersion` with a `const` value of `v1.0.0`, then additional Tetra Data checks will run, validating that the IDS follows certain Tetra Data conventions such as using the standard `samples` component.
Note: in a future version of the validator, these `@idsConventionVersion` checks will be removed

### Validate an IDS and check for breaking changes from a previous version

```sh
validate-ids-artifact --ids_dir=path/to/ids/folder --previous_ids_dir=path/to/previous_ids/folder
```

As well as running the validation of the IDS in `ids_dir`, additional validation will happen using the previous version of the same IDS passed to `previous_ids_dir`.

## Validation

This is an overview of the validation which is run by this IDS Artifact validator.

### Generic

`schema.json`, `expected.json`, `elasticsearch.json` and `athena.json` must be present in the IDS artifact.
The validation of each of them is described below.

#### `schema.json`

`schema.json` is validated against the JSON Schema draft 7 specification using `jsonschema`'s [Validator.check_schema](https://python-jsonschema.readthedocs.io/en/latest/api/jsonschema/protocols/#jsonschema.protocols.Validator.check_schema) method.
This ensures that the JSON Schema vocabulary is being used correctly, including some format validation like the root `$id` and `$schema` being valid URIs.

Additional validation makes sure the schema meets other TDP requirements:

- The top-level IDS object must contain properties `"@idsType"`, `"@idsVersion"` and `"@idsNamespace"`.
  - `"@idsType"` must be a constant with a value consisting of a "v" followed by a valid [semantic version](https://semver.org/), such as `"v1.0.0"`.
- `"$id"` at the root of the schema must follow the format `https://ids.tetrascience.com/<namespace>/<type>/<version>/schema.json` where namespace, type and version are the constant values of the `@idsNamespace`, `@idsType` and `@idsVersion` properties.
- `"$schema"` at the root of the schema must be the URI `"http://json-schema.org/draft-07/schema#"`: draft 7 is the version of JSON Schema supported by TDP.
- All objects must have `additional_properties` set to `false`
- All properties must have a valid JSON Schema type
- An object's `required` properties must be defined in the object's `properties` definition.

`datacubes` must have a schema which is compatible with the platform's requirements:

- `datacubes` type must be an array of objects.
- The properties `name`, `dimensions` and `measures` are present and `required`.
- `minItems == maxItems` for `dimensions` and `measures`.
- `measures.value`:
  - Contains nested arrays so that it is an `N`-dimensional array, with `N` being the number of `dimensions`.
  - The innermost type is either `"number"`, `["number", "null"]`, `"string"`, or `["string", "null"]` (or equivalent).
- `dimensions.scale` must be an array of `number`s.

All properties in the schema must have valid names for mapping to Athena:

- No leading underscores
- No more than 1 consecutive underscore anywhere in the property
- No special characters (allowed characters follow the regular expression `[a-zA-Z0-9_]`).
  - Exceptions to this rule are `@idsNamespace`, `@idsType`, `@idsVersion`, and `@idsConventionVersion` at the root level of the schema, and `@link` anywhere in the schema.
- No two properties in `schema.json` may normalize to the same Athena column name.
  - For example, a property called `name` inside an object `person` will correspond to an Athena column of `person_name`.
    This means there cannot be another property called `person_name` defined at the same level as `person`, because `person_name` would clash with `person.name` when mapping the data to Athena.
- No property may have the name `uuid` or `parent_uuid` because these are reserved for use as Athena column names in TDP.

#### `elasticsearch.json`

`elasticsearch.json`'s `"mapping"` object must match a default ElasticSearch mapping generated from `schema.json`. The diff between the expected and actual `elasticsearch.json` is shown in the validator output, which can be used to update `elasticsearch.json`.

#### `athena.json`

- Partition paths must correspond to valid properties in `schema.json`
- Partition paths cannot point to properties anywhere inside an array
- `partition.name` cannot clash with any normalized property name from `schema.json`. For example, when `schema.json` properties are mapped to Athena, a property `name` inside an object `person` gets a normalized Athena column name of `person_name`, meaning `partition.name` cannot be `person_name` because it would clash with the `person_name` Athena column.

#### `expected.json`

`expected.json` must be a valid instance of `schema.json` using a JSON Schema draft 7 validator.

#### Breaking change validation

Breaking change validation runs if the `--previous_ids_dir` option is defined when calling the validator command.

A change to an IDS artifact is a breaking change if:

- Athena tables would be changed.
- IDS instances which were valid against the previous IDS version are not valid against the new version (excluding the top-level `@idsVersion` property, whose `const` value changes between every IDS version).

The breaking change checks run by the validator are:

- Check that the two IDS artifacts have the same namespace and type, fail if they don't.
- The versions must either be equal (for a documentation-only change), or the new version must be a major/minor/patch bump of the previous version.
- Determine whether the two versions may have breaking changes, according to Semantic Versioning. For example, if the previous IDS was `v1.0.0` and the current IDS is `v1.1.0`, then there should be no breaking changes. If the current IDS were `v2.0.0` instead, then there may be breaking changes.
- If breaking changes are not allowed according to the version change, validate that no breaking changes are included in the current version of the IDS:
  - `schema.json`:
    - All property names and paths must be the same: no properties added, removed or renamed.
    - The type of each property must be the same, or have `"null"` added if it is a primitive type (any type other than `"array"` or `"object"`). For example, a change from `"type": "string"` to `"type": ["string", "null"]` is not considered a breaking change. Note that the opposite, removing `"null"` from the type, is a breaking change.
    - The list of required fields for each object must either stay the same or have items removed. For example, a change from `"required": ["name", "kind"]` to `"required": ["name"]` is not a breaking change. Adding properties to `required` is a breaking change.
  - `athena.json`:
    - Any change to athena.json is a breaking change (not including file formatting changes such as changing whitespace).

> Note: When updating an invalid IDS, such as one which is missing a required artifact file, using the `--previous_ids_dir` option may lead to an error because the breaking change validator expects the previous IDS to be valid.
> In this case, do not use the `--previous_ids_dir` option: just validate the newly updated version of the IDS and consider using a major version bump so that any problems caused by the previous IDS being invalid will not affect the updated IDS.
>
> For example, if the previous version of the IDS is missing `elasticsearch.json` and the `--previous_ids_dir` option is used, an exception will be raised during validation.

### Tetra Data validation

These checks validate that Tetra Data conventions are being followed in this IDS's `schema.json`.
These checks are enabled by including a property `@idsConventionVersion` with a `const` value of `v1.0.0` in `schema.json`.

Note that this Tetra Data specific validation will be removed from this package in a future version, so that it will only validate Tetra Data Platform requirements for IDS Artifacts.

- Properties of objects shouldn't begin with the same string as the object's name, for example an object called `method` shouldn't contain a property called `method_name`.
- Property names should use snake case: entirely lower-case or numeric characters separated by single consecutive underscores.
  - `related_files.pointer`'s `fileId` and `fileKey` properties are excluded from this check. So are any properties whose name starts with `@`.
- For standard Tetra Data components, there is validation that the schema matches the expected component structure, including property names, types and `required` properties. This applies to `samples`, `users`, `systems` and `related_files`.
  The validator output will explain any differences from the expected component structure if this check fails.

## Changelog

### v0.10.0

- Update how to use this package: add a CLI script `validate-ids-artifact` which is equivalent to the previous approach of running `python -m ids_validator`. This previous approach still works as before but may be deprecated in a future version, so switching to the CLI script is recommended.
- Add validation that property names do not contain special characters.
- Add validation for breaking changes between IDS versions which would be incompatible with the Tetra Data Platform
  - Add the new CLI argument `--previous_ids_dir` (which may be omitted) which is the folder containing the previous version of the same IDS namespace and type. Without this CLI argument, breaking change validation does not run.
- Add validation that `expected.json` is a valid instance of `schema.json` using a JSON Schema validator.
- Remove `--version` CLI argument because this information can be retrieved from the IDS artifact being validated.

### v0.9.16

- Remove the upper bound of what properties `samples` may contain for Tetra Data validation. This means the `samples` schema can now include properties other than the ones in the `samples` Tetra Data component, such as primary and foreign key fields.

### v0.9.15

- Limit version of `typing-extensions` in dependencies to avoid a bug which causes the validator to always fail in Python 3.10 or later.

### v0.9.14

- Update `samples[*]` check to optionally allow for it to contain a property `pk_samples` of type `"string"`.

### v0.9.13

- `related_files` is no longer checked against annotation fields like "description".

### v0.9.12

- Update check for `samples[*].labels[*].source.name` type: previously the type was
  required to be `"string"`, now it is required to be either `["string", "null"]` or
  `"string"`, with `"string"` leading to a deprecation warning. This change makes this
  `source` definition the same as `samples[*].properties[*].source` in a
  backward-compatible way.

### v0.9.11

- Fix bug in `AthenaChecker` to allow root level IDS properties as partition paths.
- Update `TypeChecker` to catch errors related to undefined/misspelled `type` key.
- Update `jsonschema` version to fix package installation error

### v0.9.10

- Modify `V1SnakeCaseChecker` to ignore checks for keys present in `definitions` object.
- Add temporary allowance for `@link` in `*.properties`

### v0.9.9

- Lock `jsonschema` version in requirements.txt

### v0.9.8

- Modify `RulesChecker` to log missing and extra properties

### v0.9.7

- Allow properties with `const` values to have non-nullable `type`

### v0.9.6

- Add checker classes for generic validation
- Add checker classes for v1.0.0 convention validation
