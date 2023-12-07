"""
Test for Feature flag Handler
"""
# pylint: disable=line-too-long

import json
from unittest import mock
import pytest
from azure.appconfiguration import (
    FeatureFlagConfigurationSetting,
    FILTER_TARGETING,
    FILTER_TIME_WINDOW,
    FILTER_PERCENTAGE,
)
from icecommercialpower.feature_flags import (
    FeatureFlagHelper,
    UnknownFeatureFlagFilterError,
    FeatureFlags,
)


def create_feature_flag(
    key, enabled=False, ice_employee_percentage=100, beta_tester_percentage=0
):
    """
    Helper method to create a valid feature flag for mocking
    """
    groups = [
        {"Name": "ice-employee", "RolloutPercentage": ice_employee_percentage},
        {"Name": "beta-tester", "RolloutPercentage": beta_tester_percentage},
    ]
    config_setting = FeatureFlagConfigurationSetting(key, enabled=enabled)
    config_setting.value = json.dumps(
        {
            "conditions": {
                "client_filters": [
                    {
                        "name": FILTER_TARGETING,
                        "parameters": {
                            "Audience": {
                                "DefaultRolloutPercentage": 100,
                                "Groups": groups,
                                "Users": [],
                            }
                        },
                    }
                ]
            },
            "description": "",
            "enabled": enabled,
            "id": key,
        }
    )
    return config_setting


@pytest.mark.parametrize(
    "test_case",
    [
        # feature, enabled, given_groups, ice_employee_percentage, beta_tester_percentage, expected_result
        [FeatureFlags.USSD_PAYMENT, True, ["ice-employee"], 100, 100, True],
        [FeatureFlags.USSD_PAYMENT, True, ["beta-tester"], 100, 100, True],
        [FeatureFlags.USSD_PAYMENT, False, ["ice-employee"], 100, 100, False],
        [FeatureFlags.USSD_PAYMENT, False, ["beta-tester"], 100, 100, False],
        [
            FeatureFlags.USSD_PAYMENT,
            True,
            ["ice-employee", "beta-tester"],
            100,
            100,
            True,
        ],
        [
            FeatureFlags.USSD_PAYMENT,
            True,
            ["ice-employee", "beta-tester"],
            100,
            0,
            True,
        ],
        [
            FeatureFlags.USSD_PAYMENT,
            True,
            ["ice-employee", "beta-tester"],
            0,
            100,
            True,
        ],
        [FeatureFlags.USSD_PAYMENT, True, ["ice-employee", "beta-tester"], 0, 0, False],
        [
            FeatureFlags.USSD_PAYMENT,
            False,
            ["ice-employee", "beta-tester"],
            100,
            100,
            False,
        ],
        [
            FeatureFlags.USSD_PAYMENT,
            False,
            ["ice-employee", "beta-tester"],
            0,
            0,
            False,
        ],
        [FeatureFlags.USSD_PAYMENT, True, ["group1", "group2"], 100, 100, False],
        [FeatureFlags.USSD_PAYMENT, True, ["group1", "group2"], 0, 0, False],
        [FeatureFlags.USSD_PAYMENT, True, [], 100, 100, False],
        [FeatureFlags.USSD_PAYMENT, True, [], 0, 0, False],
    ],
)
def test_feature_flag_handler_has_feature_enabled_and_uses_cache(test_case):
    """
    Tests if get feature flags with valid groupname succeeds.
    """
    (
        feature,
        enabled,
        given_groups,
        ice_employee_percentage,
        beta_tester_percentage,
        expected_result,
    ) = test_case

    # Arrange
    feature_flag = create_feature_flag(
        "payment", enabled, ice_employee_percentage, beta_tester_percentage
    )
    mock_app_config_client = mock.MagicMock()
    mock_app_config_client.get_configuration_setting = mock.MagicMock(
        return_value=feature_flag
    )

    feature_flag_handler = FeatureFlagHelper(mock_app_config_client)

    # Act
    # pylint: disable=invalid-name
    for _ in range(5):
        actual_result = feature_flag_handler.has_feature_enabled(
            groupnames=given_groups, feature_flag=feature
        )

        # Assert
        assert actual_result == expected_result

        feature_flag_handler.has_feature_enabled(
            groupnames=given_groups, feature_flag="testing"
        )

    assert mock_app_config_client.get_configuration_setting.call_count == 2


@pytest.mark.parametrize(
    "test_case",
    [
        # feature, given_groups
        ["feature1", ["ice-employee"]],
        ["feature2", ["beta-tester"]],
        ["feature3", ["ice-employee", "beta-tester"]],
        ["feature4", []],
        ["feature5", []],
    ],
)
def test_unknown_feature_flag_returns_disabled(test_case):
    """
    Tests if get feature flags with valid groupname succeeds.
    """
    feature, given_groups = test_case

    # Arrange
    mock_app_config_client = mock.MagicMock()
    mock_app_config_client.get_configuration_setting = mock.MagicMock(return_value=None)

    feature_flag_handler = FeatureFlagHelper(mock_app_config_client)

    # Act
    actual_result = feature_flag_handler.has_feature_enabled(
        groupnames=given_groups, feature_flag=feature
    )

    # Assert
    assert actual_result is False


@pytest.mark.parametrize(
    "test_case",
    [
        # feature, given_groups
        [True, ["ice-employee"]],
        [False, ["ice-employee"]],
        [True, ["beta-tester"]],
        [False, ["beta-tester"]],
        [True, ["ice-employee", "beta-tester"]],
        [False, ["ice-employee", "beta-tester"]],
        [True, ["group1"]],
        [False, ["group1"]],
        [True, []],
        [False, []],
    ],
)
def test_feature_flag_without_filter_returns_enabled_value(test_case):
    """
    Tests that featureflag without filter returns the value of the enabled-flag.
    """
    enabled, given_groups = test_case

    # Arrange
    feature_flag = FeatureFlagConfigurationSetting(
        FeatureFlags.USSD_PAYMENT.value, enabled=enabled
    )
    mock_app_config_client = mock.MagicMock()
    mock_app_config_client.get_configuration_setting = mock.MagicMock(
        return_value=feature_flag
    )

    feature_flag_handler = FeatureFlagHelper(mock_app_config_client)

    # Act
    actual_result = feature_flag_handler.has_feature_enabled(
        groupnames=given_groups, feature_flag=FeatureFlags.USSD_PAYMENT
    )

    # Assert
    assert actual_result == enabled


@pytest.mark.parametrize(
    "filter_type",
    [FILTER_PERCENTAGE, FILTER_TIME_WINDOW],
)
def test_invalid_filter_raises_unknownfeatureflagfiltererror(filter_type):
    """
    Test UnknownFeatureFlagFilterError is raised if wrong filter type
    """

    # Arrange
    enabled = True
    given_groups = ["ice-employee"]
    feature_flag = FeatureFlagConfigurationSetting(
        FeatureFlags.USSD_PAYMENT.value, enabled=enabled
    )
    feature_flag.value = json.dumps(
        {
            "conditions": {
                "client_filters": [
                    {"name": filter_type, "parameters": {}},
                ]
            },
            "description": "",
            "enabled": enabled,
            "id": FeatureFlags.USSD_PAYMENT.value,
        }
    )

    mock_app_config_client = mock.MagicMock()
    mock_app_config_client.get_configuration_setting = mock.MagicMock(
        return_value=feature_flag
    )

    feature_flag_handler = FeatureFlagHelper(mock_app_config_client)

    # Act and Assert
    with pytest.raises(UnknownFeatureFlagFilterError) as excinfo:
        _ = feature_flag_handler.has_feature_enabled(
            groupnames=given_groups, feature_flag=FeatureFlags.USSD_PAYMENT
        )

    assert str(excinfo.value) == f"Only Filter of type {FILTER_TARGETING} supported"


def test_multiple_filters_raises_unknownfeatureflagfiltererror():
    """
    Test that UnknownFeatureFlagFilterError is raised when there are multiple filters
    """

    # Arrange
    enabled = True
    given_groups = ["ice-employee"]
    feature_flag = FeatureFlagConfigurationSetting(
        FeatureFlags.USSD_PAYMENT.value, enabled=enabled
    )
    feature_flag.value = json.dumps(
        {
            "conditions": {
                "client_filters": [
                    {
                        "name": FILTER_TARGETING,
                        "parameters": {
                            "Audience": {
                                "DefaultRolloutPercentage": 100,
                                "Groups": [
                                    {"Name": "ice-employee", "RolloutPercentage": 100},
                                ],
                                "Users": [],
                            }
                        },
                    },
                    {
                        "name": FILTER_TARGETING,
                        "parameters": {
                            "Audience": {
                                "DefaultRolloutPercentage": 100,
                                "Groups": [
                                    {"Name": "beta-tester", "RolloutPercentage": 100},
                                ],
                                "Users": [],
                            }
                        },
                    },
                ]
            },
            "description": "",
            "enabled": enabled,
            "id": FeatureFlags.USSD_PAYMENT.value,
        }
    )

    mock_app_config_client = mock.MagicMock()
    mock_app_config_client.get_configuration_setting = mock.MagicMock(
        return_value=feature_flag
    )

    feature_flag_handler = FeatureFlagHelper(mock_app_config_client)

    # Act and Assert
    with pytest.raises(UnknownFeatureFlagFilterError) as excinfo:
        _ = feature_flag_handler.has_feature_enabled(
            groupnames=given_groups, feature_flag=FeatureFlags.USSD_PAYMENT
        )

    assert str(excinfo.value) == "Only 0 or 1 filters are supported"
