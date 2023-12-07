"""
Test for steamaco_balance_helper
"""
import logging
import re
import os
import json
from unittest import mock
import httpretty
import pytest
import requests
from requests import Timeout

from icecommercialpower.steamaco import (
    SteamaCoClient,
    ObtainTokenError,
    MeterRecord,
    Tag,
)
from .steamaco_test_utils import (
    setup_steamaco_env_vars,
    register_auth_request,
    TOKEN_VALUE,
)


@pytest.fixture(autouse=True)
def setup_function(monkeypatch):
    """
    Setup function for the steamaco tests
    """
    # pylint: disable=protected-access
    SteamaCoClient._cached_token.reset()

    setup_steamaco_env_vars(monkeypatch)


def assert_all_get_requests_are_authenticated() -> None:
    """
    Asserts that all get requests are authenticated
    """
    get_requests = list(
        filter(lambda r: r.method == httpretty.GET, httpretty.latest_requests())
    )
    assert len(get_requests) > 0
    assert all(
        r.headers["Authorization"] == f"Token {TOKEN_VALUE}" for r in get_requests
    )


@httpretty.activate(verbose=True, allow_net_connect=False)
@pytest.mark.parametrize("status_code", [400, 401, 403, 404])
def test_get_all_bad_response_status(status_code: int):
    """
    Test get_all() with bad response status
    """

    # Arrange
    register_auth_request()
    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_api_get_customers_url = f"{steamaco_api_url}customers/"

    httpretty.register_uri(
        httpretty.GET,
        steamaco_api_get_customers_url,
        body=json.dumps({"detail": "Bad request"}),
        status=status_code,
    )

    # Act
    with pytest.raises(requests.HTTPError):
        SteamaCoClient().get_all("customers/")


@httpretty.activate(verbose=True, allow_net_connect=False)
@pytest.mark.parametrize("status_code", [400, 401, 403, 404])
def test_get_all_bad_response_status_in_second_page(status_code: int):
    """
    Test get_all() with bad response status
    in second page
    """

    # Arrange
    register_auth_request()
    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_api_get_customers_url = (
        f"{steamaco_api_url}customers/?"
        f"{SteamaCoClient.PAGE_SIZE_PARAM_NAME}={SteamaCoClient.DEFAULT_PAGE_SIZE}"
    )
    steamaco_api_get_customers_page_2_url = (
        f"{steamaco_api_url}customers/?"
        f"page=2&{SteamaCoClient.PAGE_SIZE_PARAM_NAME}={SteamaCoClient.DEFAULT_PAGE_SIZE}"
    )

    customers_page_1 = [
        {"id": 1, "name": "Customer 1"},
        {"id": 2, "name": "Customer 2"},
    ]

    httpretty.register_uri(
        method=httpretty.GET,
        uri=steamaco_api_get_customers_url,
        body=json.dumps(
            {
                "count": 2,
                "next": steamaco_api_get_customers_page_2_url,
                "previous": None,
                "results": customers_page_1,
            }
        ),
        match_querystring=True,
        status=200,
    )

    httpretty.register_uri(
        httpretty.GET,
        steamaco_api_get_customers_page_2_url,
        body=json.dumps({"detail": "Bad request"}),
        status=status_code,
        match_querystring=True,
    )

    # Act
    with pytest.raises(requests.HTTPError):
        SteamaCoClient().get_all("customers/")


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_all_single_page_response():
    """
    Test for get_steamaco_customer_data in the HttpHelperHelper
    """

    retry_count = 0

    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_auth_url = os.environ["STEAMACO_AUTH_URL"]
    steamaco_api_get_token_url = f"{steamaco_api_url}{steamaco_auth_url}"
    steamaco_api_get_customers_url = f"{steamaco_api_url}customers/"

    def cb_auth_handler(request, _, response_headers):
        """
        mocks the http POST request and returns token
        """
        nonlocal retry_count

        if retry_count < 3:
            retry_count += 1
            return [500, response_headers, json.dumps({"error": "unknown"})]

        if request.url == steamaco_api_get_token_url:
            return [200, response_headers, json.dumps({"token": TOKEN_VALUE})]

        assert False

    httpretty.enable()

    httpretty.register_uri(
        httpretty.POST,
        steamaco_api_get_token_url,
        body=cb_auth_handler,
    )

    customers = [{"id": 1, "name": "Customer 1"}, {"id": 2, "name": "Customer 2"}]
    httpretty.register_uri(
        method=httpretty.GET,
        uri=steamaco_api_get_customers_url,
        body=json.dumps(
            {"count": 2, "next": None, "previous": None, "results": customers}
        ),
        status=200,
    )

    sut = SteamaCoClient()
    returned_data = sut.get_all("customers/")

    assert returned_data == customers
    assert retry_count == 3
    assert_all_get_requests_are_authenticated()


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_all_multiple_page_response():
    """
    Test for multiple pages of data
    """

    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_api_get_customers_url = f"{steamaco_api_url}customers/"
    steamaco_api_get_customers_page_2_url = (
        f"{steamaco_api_url}customers/?"
        f"page=2&{SteamaCoClient.PAGE_SIZE_PARAM_NAME}={SteamaCoClient.DEFAULT_PAGE_SIZE}"
    )

    httpretty.enable()

    register_auth_request()

    customers_page_1 = [
        {"id": 1, "name": "Customer 1"},
        {"id": 2, "name": "Customer 2"},
    ]

    httpretty.register_uri(
        method=httpretty.GET,
        uri=steamaco_api_get_customers_url
        + f"?{SteamaCoClient.PAGE_SIZE_PARAM_NAME}={SteamaCoClient.DEFAULT_PAGE_SIZE}",
        body=json.dumps(
            {
                "count": 2,
                "next": steamaco_api_get_customers_page_2_url,
                "previous": None,
                "results": customers_page_1,
            }
        ),
        match_querystring=True,
        status=200,
    )

    customers_page_2 = [
        {"id": 3, "name": "Customer 3"},
        {"id": 4, "name": "Customer 4"},
    ]

    httpretty.register_uri(
        method=httpretty.GET,
        uri=steamaco_api_get_customers_page_2_url,
        match_querystring=True,
        body=json.dumps(
            {
                "count": 2,
                "next": None,
                "previous": steamaco_api_get_customers_url,
                "results": customers_page_2,
            }
        ),
        status=200,
    )

    sut = SteamaCoClient()
    returned_data = sut.get_all("customers/")

    assert returned_data == customers_page_1 + customers_page_2
    assert_all_get_requests_are_authenticated()


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_all_empty_list_result():
    """
    Test for multiple pages of data
    """

    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_api_get_customers_url = f"{steamaco_api_url}customers/"

    httpretty.enable()

    register_auth_request()

    httpretty.register_uri(
        method=httpretty.GET,
        uri=steamaco_api_get_customers_url,
        body=json.dumps({"count": 1, "next": None, "previous": None, "results": []}),
        status=200,
    )

    sut = SteamaCoClient()
    returned_data = sut.get_all("customers/")

    assert len(returned_data) == 0
    assert_all_get_requests_are_authenticated()


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_all_empty_json_result():
    """
    Test for multiple pages of data
    """

    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_api_get_customers_url = f"{steamaco_api_url}customers/"

    httpretty.enable()

    register_auth_request()

    httpretty.register_uri(
        method=httpretty.GET,
        uri=steamaco_api_get_customers_url,
        body="{}",
        status=200,
    )

    sut = SteamaCoClient()
    returned_data = sut.get_all("customers/")

    assert len(returned_data) == 0
    assert_all_get_requests_are_authenticated()


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_all_auth_fails():

    """
    Test for get_steamaco_customer_data in the HttpHelperHelper
    """

    retry_count = 0

    def cb_mock_post_handler(request, _, response_headers):
        """
        mocks the http POST request and returns token
        """
        nonlocal retry_count

        return [
            400,
            response_headers,
            json.dumps(
                {"non_field_errors": ["Unable to log in with provided credentials."]}
            ),
        ]

    httpretty.enable()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(os.environ["STEAMACO_API_URL"] + ".*"),
        body=cb_mock_post_handler,
    )

    sut = SteamaCoClient()

    with pytest.raises(ObtainTokenError):
        sut.get_all("/customers/")


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_all_token_once():
    """
    Test that token is cached
    """
    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_auth_url = os.environ["STEAMACO_AUTH_URL"]
    steamaco_api_get_token_url = f"{steamaco_api_url}{steamaco_auth_url}"
    steamaco_api_get_customers_url = f"{steamaco_api_url}customers/"

    httpretty.enable()

    auth_calls = 0

    def cb_auth_handler(request, _, response_headers):
        nonlocal auth_calls
        auth_calls += 1
        return [200, response_headers, json.dumps({"token": TOKEN_VALUE})]

    httpretty.register_uri(
        httpretty.POST,
        steamaco_api_get_token_url,
        body=cb_auth_handler,
    )

    httpretty.register_uri(
        httpretty.GET,
        steamaco_api_get_customers_url,
        body="{}",
    )

    sut = SteamaCoClient()
    sut.get_all("customers/")
    sut.get_all("customers/")

    assert_all_get_requests_are_authenticated()
    assert auth_calls == 1


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_customers_single_page_response():
    """
    Test for get_customers
    """

    customer_api_data_mock = """{
"count": 7,
"next": null,
"previous": null,
"results": [
    {
        "id": 1000,
        "url": "https://api.steama.co/customers/1000/",
        "transactions_url": "https://api.steama.co/customers/1000/transactions/",
        "utilities_url": "https://api.steama.co/customers/1000/utilities/",
        "messages_url": "https://api.steama.co/customers/1000/messages/",
        "meters_url": "https://api.steama.co/customers/1000/meters/",
        "revenue_url": "https://api.steama.co/customers/1000/revenue/",
        "balances_url": "https://api.steama.co/customers/1000/balances/",
        "audit_log_url": "https://api.steama.co/customers/1000/audit-log/",
        "telephone": "+123456798",
        "first_name": "Testing",
        "last_name": "Tester",
        "account_balance": "80.00",
        "energy_price": "0.00",
        "low_balance_warning": "75.00",
        "low_balance_level": "75.00",
        "site_manager": null,
        "site_manager_name": null,
        "site_manager_url": null,
        "site_manager_telephone": null,
        "site": 100,
        "site_url": "https://api.steama.co/sites/100/",
        "site_name": "Payment Testing",
        "bit_harvester": null,
        "bit_harvester_name": null,
        "bit_harvester_url": null,
        "bit_harvester_telephone": null,
        "control_type": "AUTOC",
        "is_user": true,
        "is_field_manager": false,
        "is_demo": false,
        "language": "ENG",
        "user_type": "NA",
        "payment_plan": "",
        "integration_id": "",
        "utility_use_30_days": {},
        "labels": "",
        "tags_url": "https://api.steama.co/customers/1000/tags/",
        "tags": [],
        "created": "2021-11-30T09:56:44Z",
        "is_archived": false,
        "TOU_hours": ""
    },
    {
        "id": 2000,
        "url": "https://api.steama.co/customers/2000/",
        "transactions_url": "https://api.steama.co/customers/2000/transactions/",
        "utilities_url": "https://api.steama.co/customers/2000/utilities/",
        "messages_url": "https://api.steama.co/customers/2000/messages/",
        "meters_url": "https://api.steama.co/customers/2000/meters/",
        "revenue_url": "https://api.steama.co/customers/2000/revenue/",
        "balances_url": "https://api.steama.co/customers/2000/balances/",
        "audit_log_url": "https://api.steama.co/customers/2000/audit-log/",
        "telephone": "+123456789",
        "first_name": "Jesse",
        "last_name": "Testing",
        "account_balance": "-10.00",
        "energy_price": "0.00",
        "low_balance_warning": "75.00",
        "low_balance_level": "75.00",
        "site_manager": null,
        "site_manager_name": null,
        "site_manager_url": null,
        "site_manager_telephone": null,
        "site": 200,
        "site_url": "https://api.steama.co/sites/200/",
        "site_name": "Payment Testing",
        "bit_harvester": null,
        "bit_harvester_name": null,
        "bit_harvester_url": null,
        "bit_harvester_telephone": null,
        "control_type": "AUTOC",
        "is_user": true,
        "is_field_manager": false,
        "is_demo": false,
        "language": "ENG",
        "user_type": "NA",
        "payment_plan": "",
        "integration_id": "",
        "utility_use_30_days": {},
        "labels": "",
        "tags_url": "https://api.steama.co/customers/2000/tags/",
        "tags": [
            {
                "id": 1000,
                "url": "https://api.steama.co/tags/1000/",
                "name": "ice-employee"
            }
        ],
        "created": "2021-12-03T12:53:47Z",
        "is_archived": false,
        "TOU_hours": ""
    }
    ]
}"""

    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_api_get_customers_url = f"{steamaco_api_url}customers/"

    httpretty.enable()

    httpretty.register_uri(
        httpretty.GET,
        steamaco_api_get_customers_url,
        body=customer_api_data_mock,
    )

    register_auth_request()

    sut = SteamaCoClient()
    actual_customers = sut.get_customers()

    assert len(actual_customers) == 2
    customer_1 = actual_customers[0]
    assert (1000, 80.0) == (customer_1.id, float(customer_1.account_balance))
    assert customer_1.tags == []

    customer_2 = actual_customers[1]
    assert (2000, -10) == (customer_2.id, float(customer_2.account_balance))
    expected_tag = Tag(
        id=1000, name="ice-employee", url="https://api.steama.co/tags/1000/"
    )
    assert [expected_tag] == customer_2.tags


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_meters():
    """
    Test for steamaco_meter_retriever's SteamaCoMeterRetriever
    """

    meter_one = MeterRecord(reference="1", utility=1)
    meter_two = MeterRecord(reference="2", utility=2)

    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_api_get_meters_url = (
        f"{steamaco_api_url}meters/?"
        f"{SteamaCoClient.PAGE_SIZE_PARAM_NAME}={SteamaCoClient.DEFAULT_PAGE_SIZE}"
    )
    steamaco_api_get_meters_page_2_url = (
        f"{steamaco_api_url}meters/?"
        f"page=2&{SteamaCoClient.PAGE_SIZE_PARAM_NAME}={SteamaCoClient.DEFAULT_PAGE_SIZE}"
    )

    httpretty.enable()

    register_auth_request()

    httpretty.register_uri(
        httpretty.GET,
        steamaco_api_get_meters_url,
        body=json.dumps(
            {
                "count": 1,
                "next": steamaco_api_get_meters_page_2_url,
                "results": [meter_one.dict()],
            }
        ),
        match_querystring=True,
    )

    httpretty.register_uri(
        httpretty.GET,
        steamaco_api_get_meters_page_2_url,
        body=json.dumps({"count": 1, "results": [meter_two.dict()]}),
        match_querystring=True,
    )

    sut = SteamaCoClient()
    actual_data = sut.get_meters()

    expected_data = [meter_one, meter_two]
    assert actual_data == expected_data


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_customer_by_phone_number_successful():
    """
    Test for get_customer_by_phone_number
    """
    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_auth_url = os.environ["STEAMACO_AUTH_URL"]
    steamaco_api_get_token_url = f"{steamaco_api_url}{steamaco_auth_url}"
    steamaco_api_get_customers_url = f"{steamaco_api_url}customers/.*"

    customer_api_data_mock = """{
"count": 7,
"next": null,
"previous": null,
"results": [
    {
        "id": 1000,
        "url": "https://api.steama.co/customers/1000/",
        "transactions_url": "https://api.steama.co/customers/1000/transactions/",
        "utilities_url": "https://api.steama.co/customers/1000/utilities/",
        "messages_url": "https://api.steama.co/customers/1000/messages/",
        "meters_url": "https://api.steama.co/customers/1000/meters/",
        "revenue_url": "https://api.steama.co/customers/1000/revenue/",
        "balances_url": "https://api.steama.co/customers/1000/balances/",
        "audit_log_url": "https://api.steama.co/customers/1000/audit-log/",
        "telephone": "+123456798",
        "first_name": "Testing",
        "last_name": "Tester",
        "account_balance": "80.00",
        "energy_price": "0.00",
        "low_balance_warning": "75.00",
        "low_balance_level": "75.00",
        "site_manager": null,
        "site_manager_name": null,
        "site_manager_url": null,
        "site_manager_telephone": null,
        "site": 100,
        "site_url": "https://api.steama.co/sites/100/",
        "site_name": "Payment Testing",
        "bit_harvester": null,
        "bit_harvester_name": null,
        "bit_harvester_url": null,
        "bit_harvester_telephone": null,
        "control_type": "AUTOC",
        "is_user": true,
        "is_field_manager": false,
        "is_demo": false,
        "language": "ENG",
        "user_type": "NA",
        "payment_plan": "",
        "integration_id": "",
        "utility_use_30_days": {},
        "labels": "",
        "tags_url": "https://api.steama.co/customers/1000/tags/",
        "tags": [],
        "created": "2021-11-30T09:56:44Z",
        "is_archived": false,
        "TOU_hours": ""
    }
    ]
}"""

    httpretty.enable()

    httpretty.register_uri(
        httpretty.GET,
        re.compile(steamaco_api_get_customers_url),
        body=customer_api_data_mock,
    )

    httpretty.register_uri(
        httpretty.POST,
        steamaco_api_get_token_url,
        body=json.dumps({"token": TOKEN_VALUE}),
    )

    handler = SteamaCoClient()
    returned_data = handler.get_customer_by_phone_number("PHONE")

    assert returned_data is not None
    assert returned_data.first_name == "Testing"


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_customer_by_phone_number_failure():
    """
    Test for get_customer_by_phone_number
    """
    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_auth_url = os.environ["STEAMACO_AUTH_URL"]
    steamaco_api_get_customers_url = f"{steamaco_api_url}customers/"
    steamaco_api_get_token_url = f"{steamaco_api_url}{steamaco_auth_url}"

    def mock_customers_404_handler(_, __, response_headers):
        """
        mocks the http get customers request to return an error
        """

        customer_api_data_error_mock = """<!doctype html><html lang="en">
            <head><title>Not Found</title></head>
            <body><h1>Not Found</h1><p>The requested resource was not found on this server.</p>
            </body></html>"""

        return [404, response_headers, customer_api_data_error_mock]

    httpretty.enable()

    httpretty.register_uri(
        httpretty.POST,
        steamaco_api_get_token_url,
        body=json.dumps({"token": TOKEN_VALUE}),
    )

    httpretty.register_uri(
        httpretty.GET,
        re.compile(steamaco_api_get_customers_url),
        body=mock_customers_404_handler,
    )

    handler = SteamaCoClient()
    with pytest.raises(requests.exceptions.RequestException):
        handler.get_customer_by_phone_number("PHONE")


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_customer_by_id_succeeds():
    """Test succesfull get_customer_by_id"""
    # Arrange
    customer_id = 1000
    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_auth_url = os.environ["STEAMACO_AUTH_URL"]
    steamaco_api_get_customer_url = f"{steamaco_api_url}customers/{customer_id}"
    steamaco_api_get_token_url = f"{steamaco_api_url}{steamaco_auth_url}"

    httpretty.enable()

    httpretty.register_uri(
        httpretty.POST,
        steamaco_api_get_token_url,
        body=json.dumps({"token": TOKEN_VALUE}),
    )

    httpretty.register_uri(
        httpretty.GET,
        steamaco_api_get_customer_url,
        body="""
{
    "id": 1000,
    "url": "https://api.steama.co/customers/1000/",
    "transactions_url": "https://api.steama.co/customers/1000/transactions/",
    "utilities_url": "https://api.steama.co/customers/1000/utilities/",
    "messages_url": "https://api.steama.co/customers/1000/messages/",
    "meters_url": "https://api.steama.co/customers/1000/meters/",
    "revenue_url": "https://api.steama.co/customers/1000/revenue/",
    "balances_url": "https://api.steama.co/customers/1000/balances/",
    "audit_log_url": "https://api.steama.co/customers/1000/audit-log/",
    "telephone": "+234123456789",
    "first_name": "Test",
    "last_name": "User",
    "account_balance": "70.00",
    "energy_price": "0.00",
    "low_balance_warning": "75.00",
    "low_balance_level": "75.00",
    "site_manager": null,
    "site_manager_name": null,
    "site_manager_url": null,
    "site_manager_telephone": null,
    "site": 200,
    "site_url": "https://api.steama.co/sites/200/",
    "site_name": "Payment Testing",
    "bit_harvester": null,
    "bit_harvester_name": null,
    "bit_harvester_url": null,
    "bit_harvester_telephone": null,
    "control_type": "AUTOC",
    "is_user": true,
    "is_field_manager": false,
    "is_demo": false,
    "language": "ENG",
    "user_type": "NA",
    "payment_plan": "",
    "integration_id": "",
    "utility_use_30_days": {},
    "labels": "",
    "tags_url": "https://api.steama.co/customers/1000/tags/",
    "tags": [
        {
            "id": 100,
            "url": "https://api.steama.co/tags/100/",
            "name": "ice-employee"
        }
    ],
    "created": "2021-11-30T09:56:44Z",
    "is_archived": false,
    "TOU_hours": ""
}""",
    )

    # Act
    handler = SteamaCoClient()
    actual = handler.get_customer_by_id(customer_id)

    # Assert
    assert actual is not None
    assert actual.account_balance == 70.0
    assert actual.first_name == "Test"
    assert actual.last_name == "User"


@pytest.mark.parametrize("status_code", [400, 401, 403])
@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_customer_by_id_bad_status(status_code: int):
    """Test for get_customer_by_id with bad status code"""
    # Arrange
    customer_id = 1000
    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_auth_url = os.environ["STEAMACO_AUTH_URL"]
    steamaco_api_get_customer_url = f"{steamaco_api_url}customers/{customer_id}"
    steamaco_api_get_token_url = f"{steamaco_api_url}{steamaco_auth_url}"

    httpretty.enable()

    httpretty.register_uri(
        httpretty.POST,
        steamaco_api_get_token_url,
        body=json.dumps({"token": TOKEN_VALUE}),
    )

    httpretty.register_uri(
        httpretty.GET, steamaco_api_get_customer_url, body="{}", status=status_code
    )

    # Act & Assert
    handler = SteamaCoClient()
    with pytest.raises(requests.exceptions.RequestException):
        handler.get_customer_by_id(customer_id)


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_get_customer_by_id_not_found():
    """Test for get_customer_by_id when not found"""
    # Arrange
    customer_id = 1000
    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_auth_url = os.environ["STEAMACO_AUTH_URL"]
    steamaco_api_get_customer_url = f"{steamaco_api_url}customers/{customer_id}"
    steamaco_api_get_token_url = f"{steamaco_api_url}{steamaco_auth_url}"

    httpretty.enable()

    httpretty.register_uri(
        httpretty.POST,
        steamaco_api_get_token_url,
        body=json.dumps({"token": TOKEN_VALUE}),
    )

    httpretty.register_uri(
        method=httpretty.GET,
        uri=steamaco_api_get_customer_url,
        body="""{ "detail": "Not found."}""",
        status=404,
    )

    # Act
    handler = SteamaCoClient()
    customer = handler.get_customer_by_id(customer_id)

    # Assert
    assert customer is None


@mock.patch("requests.Session.post")
def test_get_token_timeout(post_mock, caplog):
    """
    Test get_all() with timeout
    """

    # Arrange
    post_mock.side_effect = Timeout

    # Act
    with caplog.at_level(logging.ERROR):
        with pytest.raises(Timeout):
            SteamaCoClient().get_all("customers/")

    assert "Request to SteamaCo API timed out" in caplog.text
    assert "Timeout" in caplog.text


@httpretty.activate(verbose=True, allow_net_connect=False)
@mock.patch("requests.Session.get")
def test_get_all_and_get_timeout(get_mock, caplog):
    """
    Test get_all() with timeout
    """

    register_auth_request()

    # Arrange
    get_mock.side_effect = Timeout

    # Act
    with caplog.at_level(logging.ERROR):
        with pytest.raises(Timeout):
            SteamaCoClient().get_all("customers/")

    assert "Request to SteamaCo API timed out" in caplog.text
    assert "Timeout" in caplog.text

    # Act
    with caplog.at_level(logging.ERROR):
        with pytest.raises(Timeout):
            SteamaCoClient().get_customer_by_id(1000)

    assert "Request to SteamaCo API timed out" in caplog.text
    assert "Timeout" in caplog.text
