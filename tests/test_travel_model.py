import pytest
from pydantic import ValidationError

from models.travel_model import TravelInfoRequest, TravelInfoResponse

def test_travel_info_request_requires_all_fields():
    with pytest.raises(ValidationError):
        TravelInfoRequest()


def test_travel_info_request_valid_data():
    request = TravelInfoRequest(
        country_from="Israel",
        country_to="Germany",
        is_capital=True,
        is_weather=True,
        is_currency=True
    )

    assert request.country_from == "Israel"
    assert request.country_to == "Germany"
    assert request.is_capital is True
    assert request.is_weather is True
    assert request.is_currency is True


def test_travel_info_request_missing_field():
    with pytest.raises(ValidationError):
        TravelInfoRequest(
            country_from="Israel",
            country_to="Germany",
            is_capital=True,
            is_weather=True
        )


def test_travel_info_request_invalid_country():
    with pytest.raises(ValidationError):
        TravelInfoRequest(
            country_from=123,
            country_to="Germany",
            is_capital=True,
            is_weather=True,
            is_currency=True
        )


def test_travel_info_request_invalid_boolean():
    with pytest.raises(ValidationError):
        TravelInfoRequest(
            country_from="Israel",
            country_to="Germany",
            is_capital="invalid",
            is_weather=True,
            is_currency=True
        )


# Tests for TravelInfoResponse

def test_travel_info_response_requires_countries():
    with pytest.raises(ValidationError):
        TravelInfoResponse()


def test_travel_info_response_valid_data():
    response = TravelInfoResponse(
        country_from="Israel",
        country_to="Germany",
        is_capital="Berlin",
        is_weather="Sunny",
        currency_code_from="ILS",
        currency_code_to="EUR",
        currency_name_from="Israeli Shekel",
        currency_name_to="Euro",
        exchange_rate=0.25
    )

    assert response.country_from == "Israel"
    assert response.country_to == "Germany"
    assert response.is_capital == "Berlin"
    assert response.is_weather == "Sunny"
    assert response.currency_code_from == "ILS"
    assert response.currency_code_to == "EUR"
    assert response.currency_name_from == "Israeli Shekel"
    assert response.currency_name_to == "Euro"
    assert response.exchange_rate == 0.25


def test_travel_info_response_optional_fields():
    response = TravelInfoResponse(
        country_from="Israel",
        country_to="Germany"
    )

    assert response.is_capital is None
    assert response.is_weather is None
    assert response.currency_code_from is None
    assert response.currency_code_to is None
    assert response.currency_name_from is None
    assert response.currency_name_to is None
    assert response.exchange_rate is None


def test_travel_info_response_invalid_currency_code_length():
    with pytest.raises(ValidationError):
        TravelInfoResponse(
            country_from="Israel",
            country_to="Germany",
            currency_code_from="IL"
        )

    with pytest.raises(ValidationError):
        TravelInfoResponse(
            country_from="Israel",
            country_to="Germany",
            currency_code_to="EURO"
        )


def test_travel_info_response_invalid_exchange_rate():
    with pytest.raises(ValidationError):
        TravelInfoResponse(
            country_from="Israel",
            country_to="Germany",
            exchange_rate="invalid"
        )


def test_travel_info_response_invalid_country_type():
    with pytest.raises(ValidationError):
        TravelInfoResponse(
            country_from=123,
            country_to="Germany"
        )