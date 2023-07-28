import pytest
from brownie import (
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)
from scripts.helpful_scripts import get_account, enconde_function_data, upgrade


def test_proxy_delegates_calls():
    # Assert
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = enconde_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    # Act
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    # Assert
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account})
    assert proxy_box.retrieve() == 1
    with pytest.raises(AttributeError):
        proxy_box.increment({"from": account})
