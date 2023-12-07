# Release History
## 0.5.0 (2023-12-06)

- Removed the experimental tags on all entities.
- Fixed a bug that raised an exception when listing Databases and Schemas.

## 0.4.0 (2023-12-04)
- Fixed a bug that had an exception when listing some entities that have non-alphanumeric characters in the names.
- Updated dependency on `snowflake-snowpark-python` to `1.5.0`.
- Added support for Python 3.11.
- Removed the Pydantic types from the model class.
- Renamed exception class names in `snowflake.core.exceptions`.

## 0.3.0 (2023-11-17)

Initial pre-release.
