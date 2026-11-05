"""
Tests for StellarConfig
"""

import json

import pytest

from configmate.stellar import StellarConfig, StellarEndpointError


KNOWN_NETWORK_URLS = [
    (
        'testnet',
        'https://horizon-testnet.stellar.org',
        'https://soroban-testnet.stellar.org',
    ),
    (
        'mainnet',
        'https://horizon.stellar.org',
        'https://soroban-rpc.stellar.org',
    ),
    (
        'futurenet',
        'https://horizon-futurenet.stellar.org',
        'https://rpc-futurenet.stellar.org',
    ),
]


def test_defaults():
    """Test default values."""
    config = StellarConfig()
    assert config.get('stellar.network') == 'testnet'
    assert config.get('stellar.horizon_url') == 'https://horizon-testnet.stellar.org'
    assert config.get('stellar.soroban_rpc_url') == 'https://soroban-testnet.stellar.org'
    assert config.get_horizon_url() == 'https://horizon-testnet.stellar.org'
    assert config.get_soroban_rpc_url() == 'https://soroban-testnet.stellar.org'


@pytest.mark.parametrize('network,horizon_url,soroban_rpc_url', KNOWN_NETWORK_URLS)
def test_known_networks_keep_endpoint_defaults(network, horizon_url, soroban_rpc_url):
    """Known networks resolve to their matching Horizon and Soroban RPC URLs."""
    config = StellarConfig()

    config.set('stellar.network', network)

    assert config.get('stellar.horizon_url') == horizon_url
    assert config.get('stellar.soroban_rpc_url') == soroban_rpc_url
    assert config.get_horizon_url() == horizon_url
    assert config.get_soroban_rpc_url() == soroban_rpc_url
    assert config.is_known_network() is True


def test_known_network_defaults_are_used_when_endpoint_is_reset():
    """Resetting an endpoint falls back to the default of a known network."""
    config = StellarConfig()
    config.set('stellar.network', 'mainnet')
    config.set('stellar.horizon_url', 'https://custom.example')

    config.set('stellar.horizon_url', None)

    assert config.get_horizon_url() == 'https://horizon.stellar.org'


def test_explicit_endpoint_overrides_known_network_default():
    """An explicitly configured endpoint is used for known networks too."""
    config = StellarConfig()
    config.set('stellar.network', 'mainnet')
    config.set('stellar.horizon_url', 'https://custom.example')

    assert config.get_horizon_url() == 'https://custom.example'
    assert config.get_soroban_rpc_url() == 'https://soroban-rpc.stellar.org'


def test_soroban_rpc_url_tracks_network_until_overridden():
    config = StellarConfig()

    config.set('stellar.network', 'mainnet')
    assert config.get_soroban_rpc_url() == 'https://soroban-rpc.stellar.org'

    config.set('stellar.network', 'futurenet')
    assert config.get_soroban_rpc_url() == 'https://rpc-futurenet.stellar.org'

    config.set('stellar.soroban_rpc_url', 'https://rpc.custom.example')
    config.set('stellar.network', 'testnet')
    assert config.get_soroban_rpc_url() == 'https://rpc.custom.example'


def test_custom_network_never_inherits_testnet_endpoints():
    """An unrecognized network clears both endpoint defaults."""
    config = StellarConfig()

    config.set('stellar.network', 'local')

    assert config.get('stellar.horizon_url') is None
    assert config.get('stellar.soroban_rpc_url') is None
    assert config.is_known_network() is False

    with pytest.raises(StellarEndpointError) as horizon_error:
        config.get_horizon_url()
    assert "'stellar.horizon_url'" in str(horizon_error.value)
    assert 'STELLAR_HORIZON_URL' in str(horizon_error.value)
    assert 'testnet' not in str(horizon_error.value).lower()

    with pytest.raises(StellarEndpointError) as soroban_error:
        config.get_soroban_rpc_url()
    assert "'stellar.soroban_rpc_url'" in str(soroban_error.value)
    assert 'STELLAR_SOROBAN_RPC_URL' in str(soroban_error.value)

    # The custom endpoint error remains catchable as a ValueError.
    assert isinstance(horizon_error.value, ValueError)


def test_custom_network_with_only_horizon_url():
    """Configuring only the Horizon URL leaves Soroban RPC unresolved."""
    config = StellarConfig()
    config.set('stellar.network', 'local')
    config.set('stellar.horizon_url', 'https://horizon.local.example')

    assert config.get_horizon_url() == 'https://horizon.local.example'

    with pytest.raises(StellarEndpointError):
        config.get_soroban_rpc_url()


def test_custom_network_with_only_soroban_rpc_url():
    """Configuring only the Soroban RPC URL leaves Horizon unresolved."""
    config = StellarConfig()
    config.set('stellar.network', 'local')
    config.set('stellar.soroban_rpc_url', 'https://rpc.local.example')

    assert config.get_soroban_rpc_url() == 'https://rpc.local.example'

    with pytest.raises(StellarEndpointError):
        config.get_horizon_url()


def test_custom_network_with_both_urls():
    config = StellarConfig()
    config.set('stellar.network', 'local')
    config.set('stellar.horizon_url', 'https://horizon.local.example')
    config.set('stellar.soroban_rpc_url', 'https://rpc.local.example')

    assert config.get_horizon_url() == 'https://horizon.local.example'
    assert config.get_soroban_rpc_url() == 'https://rpc.local.example'


def test_switching_back_to_known_network_restores_defaults():
    config = StellarConfig()
    config.set('stellar.network', 'local')
    config.set('stellar.network', 'mainnet')

    assert config.get_horizon_url() == 'https://horizon.stellar.org'
    assert config.get_soroban_rpc_url() == 'https://soroban-rpc.stellar.org'


def test_load_from_env_known_network_defaults(monkeypatch):
    """Environment configuration resolves known network defaults."""
    monkeypatch.setenv('STELLAR_NETWORK', 'mainnet')
    monkeypatch.delenv('STELLAR_HORIZON_URL', raising=False)
    monkeypatch.delenv('STELLAR_SOROBAN_RPC_URL', raising=False)

    config = StellarConfig()
    config.load_from_env()

    assert config.get('stellar.network') == 'mainnet'
    assert config.get_horizon_url() == 'https://horizon.stellar.org'
    assert config.get_soroban_rpc_url() == 'https://soroban-rpc.stellar.org'


def test_custom_network_from_environment_requires_explicit_urls(monkeypatch):
    monkeypatch.setenv('STELLAR_NETWORK', 'local')
    monkeypatch.delenv('STELLAR_HORIZON_URL', raising=False)
    monkeypatch.delenv('STELLAR_SOROBAN_RPC_URL', raising=False)

    config = StellarConfig()
    config.load_from_env()

    assert config.get('stellar.network') == 'local'
    with pytest.raises(StellarEndpointError):
        config.get_horizon_url()
    with pytest.raises(StellarEndpointError):
        config.get_soroban_rpc_url()


def test_custom_network_from_environment_with_one_url(monkeypatch):
    monkeypatch.setenv('STELLAR_NETWORK', 'local')
    monkeypatch.setenv('STELLAR_HORIZON_URL', 'https://horizon.env.example')
    monkeypatch.delenv('STELLAR_SOROBAN_RPC_URL', raising=False)

    config = StellarConfig()
    config.load_from_env()

    assert config.get_horizon_url() == 'https://horizon.env.example'
    with pytest.raises(StellarEndpointError):
        config.get_soroban_rpc_url()


def test_custom_network_from_json_file_requires_explicit_urls(tmp_path):
    path = tmp_path / 'config.json'
    path.write_text(json.dumps({'stellar': {'network': 'local'}}))

    config = StellarConfig()
    config.load_from_file(path)

    with pytest.raises(StellarEndpointError):
        config.get_horizon_url()
    with pytest.raises(StellarEndpointError):
        config.get_soroban_rpc_url()


def test_custom_network_from_json_file_with_one_url(tmp_path):
    path = tmp_path / 'config.json'
    # The explicit URL is listed before the network to prove ordering does not
    # let the network selection clear it.
    path.write_text(json.dumps({
        'stellar': {
            'horizon_url': 'https://horizon.file.example',
            'network': 'local',
        },
    }))

    config = StellarConfig()
    config.load_from_file(path)

    assert config.get_horizon_url() == 'https://horizon.file.example'
    with pytest.raises(StellarEndpointError):
        config.get_soroban_rpc_url()


def test_custom_network_from_yaml_file_with_one_url(tmp_path):
    pytest.importorskip('yaml')
    path = tmp_path / 'config.yaml'
    path.write_text(
        'stellar:\n'
        '  soroban_rpc_url: https://rpc.file.example\n'
        '  network: local\n'
    )

    config = StellarConfig()
    config.load_from_file(path)

    assert config.get_soroban_rpc_url() == 'https://rpc.file.example'
    with pytest.raises(StellarEndpointError):
        config.get_horizon_url()


def test_is_known_network():
    """Test is_known_network method."""
    config = StellarConfig()
    # Default is testnet, which is known
    assert config.is_known_network() is True

    # Set to mainnet
    config.set('stellar.network', 'mainnet')
    assert config.is_known_network() is True

    # Set to futurenet
    config.set('stellar.network', 'futurenet')
    assert config.is_known_network() is True

    # Set to unknown network
    config.set('stellar.network', 'unknown')
    assert config.is_known_network() is False


def test_validation():
    """Test validation of network field."""
    config = StellarConfig()
    # The validation only checks that the network is a string, so custom
    # network names remain supported.
    config.validate('stellar.network', lambda v: isinstance(v, str))
    # This should not raise
    config.set('stellar.network', 'testnet')

    # The type hint is set to str in set_default, so the type check will run
    # and report a non-string network.
    config.set('stellar.network', 123)
    errors = config.validate_all()
    # There should be a type mismatch error
    assert any("Type mismatch for key 'stellar.network'" in err for err in errors)
