"""
Stellar configuration extension for ConfigMate.
"""

from typing import Any, Dict

from .config import Config


class StellarEndpointError(ValueError):
    """Raised when a Stellar endpoint URL cannot be resolved.

    Custom network names are supported, but ConfigMate does not guess an
    endpoint for them. When a network other than Testnet, Mainnet, or
    Futurenet is selected, the matching endpoint URL must be supplied
    explicitly.
    """


class StellarConfig(Config):
    """A configuration manager with Stellar-specific defaults and validation."""

    # Default Horizon URLs for known networks
    _NETWORK_HORIZON_URLS = {
        'testnet': 'https://horizon-testnet.stellar.org',
        'mainnet': 'https://horizon.stellar.org',
        'futurenet': 'https://horizon-futurenet.stellar.org',
    }
    _NETWORK_SOROBAN_RPC_URLS = {
        'testnet': 'https://soroban-testnet.stellar.org',
        'mainnet': 'https://soroban-rpc.stellar.org',
        'futurenet': 'https://rpc-futurenet.stellar.org',
    }

    _NETWORK_KEY = 'stellar.network'
    _HORIZON_URL_KEY = 'stellar.horizon_url'
    _SOROBAN_RPC_URL_KEY = 'stellar.soroban_rpc_url'
    _HORIZON_ENV_VAR = 'STELLAR_HORIZON_URL'
    _SOROBAN_RPC_ENV_VAR = 'STELLAR_SOROBAN_RPC_URL'

    def __init__(self):
        """Initialize Stellar configuration with Testnet defaults."""
        super().__init__()
        self._explicit_endpoint_urls = {
            self._HORIZON_URL_KEY: False,
            self._SOROBAN_RPC_URL_KEY: False,
        }
        self.set_default(self._NETWORK_KEY, 'testnet', str)
        self.set_default(
            self._HORIZON_URL_KEY,
            self._NETWORK_HORIZON_URLS['testnet'],
            str,
        )
        self.set_default(
            self._SOROBAN_RPC_URL_KEY,
            self._NETWORK_SOROBAN_RPC_URLS['testnet'],
            str,
        )
        self.validate(self._NETWORK_KEY, self._validate_network)

    def _validate_network(self, value: str) -> bool:
        """Validate that the network is a string.

        Any name is accepted so local and provider-specific networks remain
        supported. Unknown names must provide explicit endpoint URLs, which
        the endpoint getters enforce.
        """
        return isinstance(value, str)

    @staticmethod
    def _is_url_value(value: Any) -> bool:
        """Return True when a configured value can be used as an endpoint URL."""
        return isinstance(value, str) and value != ''

    def set(self, key: str, value: Any) -> None:
        """Set a value and keep endpoint defaults aligned with the network.

        Explicitly configured endpoint URLs are never overwritten. Known
        networks receive their matching defaults, while any other network
        clears the defaults so a Testnet URL is never assumed.
        """
        if key in self._explicit_endpoint_urls:
            self._explicit_endpoint_urls[key] = self._is_url_value(value)
        elif key == self._NETWORK_KEY and isinstance(value, str):
            self._sync_endpoint_defaults(value)
        super().set(key, value)

    def _sync_endpoint_defaults(self, network: str) -> None:
        """Apply network-matched defaults to endpoints that were not overridden."""
        if not self._explicit_endpoint_urls[self._HORIZON_URL_KEY]:
            super().set(self._HORIZON_URL_KEY,
                        self._NETWORK_HORIZON_URLS.get(network))
        if not self._explicit_endpoint_urls[self._SOROBAN_RPC_URL_KEY]:
            super().set(self._SOROBAN_RPC_URL_KEY,
                        self._NETWORK_SOROBAN_RPC_URLS.get(network))

    def load_from_env(self, prefix: str = 'STELLAR_', lowercase_keys: bool = True,
                      separator: str = '__') -> None:
        """Load configuration from environment variables with a Stellar prefix.

        Args:
            prefix: The prefix for environment variables (default: 'STELLAR_').
            lowercase_keys: Whether to convert keys to lowercase.
            separator: The separator used in nested keys (default: '__').
        """
        self._load_from_env(
            prefix,
            lowercase_keys,
            separator,
            key_prefix='stellar',
        )

    def _resolve_endpoint(
        self,
        key: str,
        network_urls: Dict[str, str],
        env_var: str,
        endpoint_name: str,
    ) -> str:
        """Resolve an endpoint URL, refusing to guess for custom networks."""
        value = self.get(key)
        if self._is_url_value(value):
            return value

        network = self.get(self._NETWORK_KEY)
        if isinstance(network, str) and network in network_urls:
            return network_urls[network]

        raise StellarEndpointError(
            f"No {endpoint_name} URL is configured for network {network!r}. "
            f"Custom networks must set '{key}' (for example with the "
            f"{env_var} environment variable) to the {endpoint_name} "
            f"endpoint for that network."
        )

    def get_horizon_url(self) -> str:
        """Get the horizon URL for the current network.

        Returns:
            The configured Horizon URL, or the default for a known network.

        Raises:
            StellarEndpointError: If the network is not a known network and no
                custom Horizon URL is configured.
        """
        return self._resolve_endpoint(
            self._HORIZON_URL_KEY,
            self._NETWORK_HORIZON_URLS,
            self._HORIZON_ENV_VAR,
            'Horizon',
        )

    def get_soroban_rpc_url(self) -> str:
        """Get the Soroban RPC URL for the current network.

        Returns:
            The configured Soroban RPC URL, or the default for a known network.

        Raises:
            StellarEndpointError: If the network is not a known network and no
                custom Soroban RPC URL is configured.
        """
        return self._resolve_endpoint(
            self._SOROBAN_RPC_URL_KEY,
            self._NETWORK_SOROBAN_RPC_URLS,
            self._SOROBAN_RPC_ENV_VAR,
            'Soroban RPC',
        )

    def is_known_network(self) -> bool:
        """Check if the current network is a known network (testnet, mainnet, futurenet).

        Returns:
            True if the network is known, False otherwise.
        """
        network = self.get(self._NETWORK_KEY)
        return isinstance(network, str) and network in self._NETWORK_HORIZON_URLS
