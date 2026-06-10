import datetime as dt

import pytest

from app.services import validation as v


def test_dni_accepts_valid_document():
    assert v.dni("12345678") == "12345678"


def test_dni_rejects_short_document():
    with pytest.raises(ValueError):
        v.dni("123")


def test_email_requires_valid_format():
    with pytest.raises(ValueError):
        v.email("cliente.example.com")


def test_appointment_date_rejects_past_dates():
    yesterday = (dt.date.today() - dt.timedelta(days=1)).isoformat()

    with pytest.raises(ValueError):
        v.appointment_date(yesterday)


def test_weight_must_be_positive():
    with pytest.raises(ValueError):
        v.weight(0)


def test_age_rejects_decimal_values():
    with pytest.raises(ValueError):
        v.age(3.5)
