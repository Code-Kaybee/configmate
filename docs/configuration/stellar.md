# Stellar Configuration

`StellarConfig` gives Python applications that interact with Stellar one place
to manage the selected network and its Horizon and Soroban RPC endpoints. It
provides matching defaults for Testnet, Mainnet, and Futurenet, while allowing
each endpoint to be overridden for hosted, local, or otherwise custom
networks.

```python
from configmate import StellarConfig

config = StellarConfig()
config.load_from_env()

network = config.get('stellar.network')
horizon_url = config.get_horizon_url()
soroban_rpc_url = config.get_soroban_rpc_url()
```

By default, the network is `testnet`. Changing `stellar.network` to another
known network updates both endpoint defaults together unless you explicitly set
a custom URL. This keeps network selection in application configuration and
avoids hard-coding endpoint URLs across Stellar application code.

## Known networks

These network names always resolve to their matching endpoints:

| Network | Horizon URL | Soroban RPC URL |
| --- | --- | --- |
| `testnet` | `https://horizon-testnet.stellar.org` | `https://soroban-testnet.stellar.org` |
| `mainnet` | `https://horizon.stellar.org` | `https://soroban-rpc.stellar.org` |
| `futurenet` | `https://horizon-futurenet.stellar.org` | `https://rpc-futurenet.stellar.org` |

## Custom networks

Any other network name, such as `local`, `standalone`, or a provider-specific
name, is accepted. ConfigMate has no endpoint defaults for these names, so each
endpoint you use must be configured explicitly. A custom network never inherits
the Testnet URLs; instead, each endpoint getter raises `StellarEndpointError`
when that endpoint has no custom URL:

```python
from configmate import StellarConfig, StellarEndpointError

config = StellarConfig()
config.set('stellar.network', 'local')
config.set('stellar.horizon_url', 'http://localhost:8000')

config.get_horizon_url()      # 'http://localhost:8000'
config.get_soroban_rpc_url()  # raises StellarEndpointError
```

Configuring only one endpoint does not block the other: `get_horizon_url()`
works when `stellar.horizon_url` is set, and `get_soroban_rpc_url()` works when
`stellar.soroban_rpc_url` is set. The error message names the missing key and
the matching environment variable, so a missing custom endpoint fails visibly
instead of silently pointing the application at Testnet.

`StellarEndpointError` is a subclass of `ValueError`.

## Environment variables

`load_from_env()` reads these variables by default:

| Variable | Purpose |
| --- | --- |
| `STELLAR_NETWORK` | Select `testnet`, `mainnet`, `futurenet`, or a custom network name |
| `STELLAR_HORIZON_URL` | Override the Horizon endpoint |
| `STELLAR_SOROBAN_RPC_URL` | Override the Soroban RPC endpoint |

For example, set `STELLAR_NETWORK=mainnet` to use the Mainnet endpoint defaults.
For a custom network, set each endpoint you need as well:

```bash
STELLAR_NETWORK=local
STELLAR_HORIZON_URL=http://localhost:8000
STELLAR_SOROBAN_RPC_URL=http://localhost:8001
```

## Configuration files

`load_from_file()` applies the same endpoint rules for JSON and YAML files:

```json
{
  "stellar": {
    "network": "local",
    "horizon_url": "http://localhost:8000"
  }
}
```

With this file, `get_horizon_url()` returns the configured URL and
`get_soroban_rpc_url()` raises `StellarEndpointError`. Environment variables
and files produce the same endpoint resolution for the same values, and key
order within a file does not matter.

## Features

The `StellarConfig` class extends `Config` and provides:

- Testnet defaults and matching Horizon and Soroban RPC URLs for Testnet,
  Mainnet, and Futurenet
- Automatic loading from environment variables with the `STELLAR_` prefix
- Helpers to retrieve endpoint URLs and identify the three preset networks
- Support for custom network names with explicit endpoint overrides
- Clear errors instead of a Testnet fallback when a custom endpoint is missing

`is_known_network()` only identifies whether the configured name is one of the
three presets; custom names are allowed. ConfigMate manages configuration only:
it does not provide Stellar SDK functionality or test endpoint connectivity.

## API Reference

For the full API reference, see the [StellarConfig API](../api/stellar_config.md).
