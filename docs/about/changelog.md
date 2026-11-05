# Changelog

For a detailed list of changes, please refer to the [git commit history](https://github.com/kairo-solutions/configmate/commits/master).

## Recent Changes

- Added Stellar configuration support (StellarConfig class)
- Custom Stellar networks no longer inherit Testnet endpoints; each endpoint
  getter raises `StellarEndpointError` when its custom URL is missing
- Updated documentation to include Stellar-specific usage
- Added keywords for Stellar in pyproject.toml
- Added tests for StellarConfig

## All Changes

See the [full commit history](https://github.com/kairo-solutions/configmate/commits/master) for all changes.