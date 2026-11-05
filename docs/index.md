# ConfigMate

Configuration that fits your Python application.

ConfigMate loads settings from environment variables and files, supports nested
keys, and validates values without adding required runtime dependencies.

<div class="docs-hero" markdown>

<div class="docs-hero__intro" markdown>

**PYTHON CONFIGURATION**

## Keep application settings clear and predictable

Start with a small API, then add typed defaults, validation, and environment
overrides as your application needs them.

[Read the configuration guide](configuration/usage.md){ .md-button .md-button--primary }
[Browse the API](api/config.md){ .md-button }

</div>

<div class="docs-hero__example" markdown>

**A quick look**

```python
from configmate import Config

config = Config()
config.set_default("debug", False, bool)
config.load_from_env(prefix="APP_")

if config.get("debug"):
    print("Debug mode is enabled")
```

</div>

</div>

## A practical configuration toolkit

<div class="docs-capabilities" markdown>

<div markdown>

### Multiple sources

Load values from environment variables and JSON files. YAML support is
available as an optional extra.

</div>

<div markdown>

### Nested settings

Use dot notation such as `database.host` in your code and double underscores
such as `APP_DATABASE__HOST` in the environment.

</div>

<div markdown>

### Validation built in

Declare required keys, type hints, and custom validators, then collect
configuration errors with `validate_all()`.

</div>

</div>

## Find your next step

<div class="docs-paths" markdown>

<div markdown>

### Guides

Set up configuration from files or environment variables. Stellar Python
applications can use `StellarConfig` to select network-matched Horizon and
Soroban RPC defaults, or to supply explicit endpoint URLs for custom networks.

[Configuration guide](configuration/usage.md) ·
[Stellar configuration](configuration/stellar.md)

</div>

<div markdown>

### Reference and examples

Explore the public API and copy working examples into your project.

[API reference](api/config.md) ·
[Basic example](examples/basic.md) ·
[Stellar example](examples/stellar.md)

</div>

</div>

## Install

The PyPI name `configmate` belongs to another project. This project uses
`kairo-configmate`; its first PyPI release has not been published yet. From a
source checkout:

```bash
pip install .
```

After release, install from PyPI with `pip install kairo-configmate`.

For YAML configuration files, install the optional extra:

```bash
pip install "kairo-configmate[yaml]"
```

ConfigMate is maintained by **Kairo Solutions** and released under the MIT
license. Contributions are welcome; see the
[contributor guide](about/contributing.md).