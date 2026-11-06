# Config Class

The main configuration manager class.

## API Reference

For the full API, see the [source code](https://github.com/kairo-solutions/configmate/blob/master/configmate/config.py).

## Key Methods

- `set_default(key, value, type_hint=str)`: Set a default value for a configuration key.
- `require(key)`: Mark a configuration key as required.
- `validate(key, validator)`: Add a validation function for a configuration key.
- `load_from_env(prefix='', lowercase_keys=True, separator='__')`: Load configuration from environment variables.
- `load_from_file(file_path)`: Load JSON (`.json`) or YAML (`.yaml`, `.yml`, requires
  PyYAML). Extensions are case-insensitive. Unsupported formats, including
  `.jsonc`, raise `ValueError: Unsupported file format: <suffix>` for existing
  files. See [supported file formats](../configuration/usage.md#supported-file-formats).
- `get(key, default=None)`: Get a configuration value, supporting nested keys.
- `set(key, value)`: Set a configuration value, supporting nested keys.
- `validate_all()`: Validate all configuration and return list of errors.
- `to_dict()`: Return an independent snapshot of the entire configuration as an
  ordinary `dict`. Nested `dict` and `list` values are copied recursively, so
  mutating them in the result never changes the `Config` instance. Other value
  types (scalars, tuples, sets, custom objects) are returned by reference and
  are not serialized, so an in-place mutation of such a value is visible to both
  objects; `to_dict()` does not implicitly deep-copy or convert them. Use
  `copy.deepcopy(config.to_dict())` if you need those values isolated too.

## Nested Keys

ConfigMate supports nested keys using dot notation (e.g., `database.host`).

## Example

```python
from configmate import Config

config = Config()
config.set_default('debug', False, bool)
config.set_default('database.host', 'localhost', str)
config.load_from_env()  # Loads from environment variables

debug = config.get('debug')
host = config.get('database.host')
```