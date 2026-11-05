# StellarConfig Class

A configuration manager with Stellar-specific defaults and validation.

## API Reference

For the full API, see the [source code](https://github.com/kairo-solutions/configmate/blob/master/configmate/stellar.py).

## Features

- Defaults for `stellar.network` (testnet) and network-matched Horizon and
  Soroban RPC URLs for Testnet, Mainnet, and Futurenet
- Automatic loading from environment variables with `STELLAR_` prefix
- Custom network names with explicit endpoint URLs
- `StellarEndpointError` when a custom endpoint is not configured
- Helper methods like `get_horizon_url()`, `get_soroban_rpc_url()`, and
  `is_known_network()`

## Methods

### `__init__()`

Initialize Stellar configuration with Testnet defaults for the network, Horizon
URL, and Soroban RPC URL.

### `load_from_env(prefix='STELLAR_', lowercase_keys=True, separator='__')`

Load configuration from environment variables with a Stellar prefix.

### `get_horizon_url()`

Get the Horizon URL for the current network.

Returns the configured Horizon URL, or the default for a known network. Raises
`StellarEndpointError` if the network is a custom network and
`stellar.horizon_url` was not set.

### `get_soroban_rpc_url()`

Get the Soroban RPC URL for the current network.

Returns the configured Soroban RPC URL, or the default for a known network.
Raises `StellarEndpointError` if the network is a custom network and
`stellar.soroban_rpc_url` was not set.

### `is_known_network()`

Check if the current network is a known network (testnet, mainnet, futurenet).

Returns True if the network is known, False otherwise.

### `StellarEndpointError`

Raised by the endpoint getters when an endpoint URL cannot be resolved. It is a
subclass of `ValueError` and its message identifies the configuration key and
environment variable to set. Custom networks never fall back to Testnet URLs.

## Example

```python
from configmate import StellarConfig, StellarEndpointError

# Create a Stellar configuration instance
stellar_config = StellarConfig()

# Load from environment variables with STELLAR_ prefix
# e.g., STELLAR_NETWORK=mainnet STELLAR_HORIZON_URL=https://custom.horizon.example
stellar_config.load_from_env()

# Get the horizon URL for the current network
horizon_url = stellar_config.get_horizon_url()

# Check if using a known network
if stellar_config.is_known_network():
    print(f"Using known network: {stellar_config.get('stellar.network')}")
else:
    print(f"Using custom network: {stellar_config.get('stellar.network')}")

# Custom networks need explicit endpoint URLs
try:
    soroban_rpc_url = stellar_config.get_soroban_rpc_url()
except StellarEndpointError as error:
    print(error)

# Access other configuration values as usual
network = stellar_config.get('stellar.network')
```
