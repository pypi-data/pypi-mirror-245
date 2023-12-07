"""Test payment verification"""
# pylint: disable=too-many-arguments
from typing import Optional
import uuid
from datetime import datetime
import logging
from pytest import mark

from icecommercialpower.payments.payment import (
    PaymentStatus,
    Payment,
    NotificationStatus,
)
from icecommercialpower.flutterwave.flutterwave import (
    FwPaymentType,
    FwTransactionStatus,
    FwTransaction,
)
from icecommercialpower.utils.payment_verification import (
    is_paid_in_full,
    payment_matches_flutterwave_tx,
)


def _create_sample_payment(
    amount: int,
    tx_ref: str = None,
    currency: str = "NGN",
    status: PaymentStatus = PaymentStatus.PENDING,
    app_fee: float = 0,
    merchant_fee: float = 0,
) -> Payment:
    return Payment(
        id=tx_ref or str(uuid.uuid4()),
        date_created=datetime.utcnow(),
        customer_phone_number="",
        customer_email="",
        customer_name="",
        customer_id=0,
        status=status,
        notification=NotificationStatus.NOT_STARTED,
        amount=amount,
        currency=currency,
        external_id=0,
        external_ref="",
        app_fee=app_fee,
        merchant_fee=merchant_fee,
    )


def _create_sample_flutterwave_transaction(
    amount: int,
    status: FwTransactionStatus,
    app_fee: float = 0,
    merchant_fee: float = 0,
    currency: str = "NGN",
    tx_ref: str = None,
    amount_settled: Optional[int] = None,
) -> FwTransaction:
    return FwTransaction(
        transaction_id=100,
        flw_ref="REF000012222",
        status=status,
        tx_ref=tx_ref or str(uuid.uuid4()),
        currency=currency,
        amount=amount,
        charged_amount=amount + app_fee + merchant_fee,
        amount_settled=amount_settled,
        app_fee=app_fee,
        merchant_fee=merchant_fee,
        customer_id=1000,
        customer_email="test@email.com",
        customer_phone="01234657989",
        customer_name="Test User",
        created_at=datetime.utcnow(),
        payment_type=FwPaymentType.USSD.value,
    )


@mark.parametrize(
    ["requested_amount", "paid_amount", "amounts_match"],
    [
        (300, 300, True),
        (300, 300.1, True),
        (300.1, 300, False),
        # the number of the right can only be a result of a precision error
        # in floating point arithmetics. We don't want to reject such a payment:
        (10000000, 9999999.999999, True),
    ],
)
@mark.parametrize(
    ["requested_tx_ref", "paid_tx_ref", "refs_match"],
    [
        ("SVEE5831316383695547", "SVEE5831316383695547", True),
        ("SVEE5831316383695547", "5d4abb1c-a4a6-4d19-bb77-b0e70d4bd314", False),
    ],
)
@mark.parametrize(
    ["requested_currency", "paid_currency", "currencies_match"],
    [
        ("NGN", "NGN", True),
        ("NGN", "GBP", False),
    ],
)
@mark.parametrize(
    ["fw_status", "status_is_right"],
    [
        (FwTransactionStatus.SUCCESSFUL, True),
        (FwTransactionStatus.ABANDONED, False),
        (FwTransactionStatus.CANCELLED, False),
        (FwTransactionStatus.VOIDED, False),
        (FwTransactionStatus.PENDING, False),
    ],
)
def test_payment_verification_is_paid_in_full(
    requested_amount,
    paid_amount,
    amounts_match,
    requested_tx_ref,
    paid_tx_ref,
    refs_match,
    requested_currency,
    paid_currency,
    currencies_match,
    fw_status,
    status_is_right,
):
    """Test payment verification"""
    expected_result = (
        amounts_match and refs_match and currencies_match and status_is_right
    )
    db_payment = _create_sample_payment(
        tx_ref=requested_tx_ref,
        status=PaymentStatus.PENDING,
        amount=requested_amount,
        currency=requested_currency,
    )

    flutterwave_transaction = _create_sample_flutterwave_transaction(
        status=fw_status,
        tx_ref=paid_tx_ref,
        currency=paid_currency,
        amount=paid_amount,
        amount_settled=paid_amount,
    )
    assert expected_result == is_paid_in_full(db_payment, flutterwave_transaction)


@mark.parametrize("log_non_matching_fields", [True, False])
@mark.parametrize(
    ["requested_amount", "paid_amount", "amounts_match"],
    [
        (300, 300, True),
        (300, 300.1, True),
        (300.1, 300, False),
        # the number of the right can only be a result of a presicion error
        # in floating point arithmetics. We don't want to reject such a payment:
        (10000000, 9999999.999999, True),
    ],
)
@mark.parametrize(
    ["requested_tx_ref", "paid_tx_ref", "refs_match"],
    [
        ("SVEE5831316383695547", "SVEE5831316383695547", True),
        ("SVEE5831316383695547", "5d4abb1c-a4a6-4d19-bb77-b0e70d4bd314", False),
    ],
)
@mark.parametrize(
    ["requested_currency", "paid_currency", "currencies_match"],
    [
        ("NGN", "NGN", True),
        ("NGN", "GBP", False),
    ],
)
@mark.parametrize(
    "fw_status",
    [
        FwTransactionStatus.SUCCESSFUL,
        FwTransactionStatus.ABANDONED,
        FwTransactionStatus.CANCELLED,
        FwTransactionStatus.VOIDED,
        FwTransactionStatus.PENDING,
    ],
)
def test_payment_verification_payment_matches_flutterwave_tx(
    log_non_matching_fields,
    requested_amount,
    paid_amount,
    amounts_match,
    requested_tx_ref,
    paid_tx_ref,
    refs_match,
    requested_currency,
    paid_currency,
    currencies_match,
    fw_status,
    caplog,
):
    """Test payment verification"""
    expected_result = amounts_match and refs_match and currencies_match
    db_payment = _create_sample_payment(
        tx_ref=requested_tx_ref,
        status=PaymentStatus.PENDING,
        amount=requested_amount,
        currency=requested_currency,
    )

    flutterwave_transaction = _create_sample_flutterwave_transaction(
        status=fw_status,
        tx_ref=paid_tx_ref,
        currency=paid_currency,
        amount=paid_amount,
        amount_settled=paid_amount
        if fw_status == FwTransactionStatus.SUCCESSFUL
        else None,
    )
    with caplog.at_level(logging.ERROR):
        assert expected_result == payment_matches_flutterwave_tx(
            db_payment,
            flutterwave_transaction,
            log_non_matching_fields=log_non_matching_fields,
        )

        if log_non_matching_fields:
            if not refs_match:
                assert "Id/Ref is not matching" in caplog.text
            if not currencies_match:
                assert "Currency is not matching" in caplog.text
            if not amounts_match:
                assert "Amount is not matching" in caplog.text
        else:
            if not refs_match:
                assert "Id/Ref is not matching" not in caplog.text
            if not currencies_match:
                assert "Currency is not matching" not in caplog.text
            if not amounts_match:
                assert "Amount is not matching" not in caplog.text


def test_payment_verification_fails_when_no_settled_amount():
    """Test payment verification when not value is settled"""
    payment = _create_sample_payment(
        amount=1000,
    )
    flutterwave_transaction = _create_sample_flutterwave_transaction(
        tx_ref=payment.id,
        amount=1000,
        amount_settled=None,
        status=FwTransactionStatus.SUCCESSFUL,
    )
    assert (
        is_paid_in_full(
            payment_in_db=payment, flutterwave_transaction=flutterwave_transaction
        )
        is False
    )


@mark.parametrize(
    "amount, app_fee, amount_settled, expected_result",
    [
        (1000, 100, 999, False),
        (1000, 100, 999.9999, False),
        (1000, 0, 999, False),
        (1000, 0, 999.9999, False),
        (1000, 100, 0, False),
        (1000, 0, 0, False),
        # Expected result is True because the settled > amount + app_fee
        (1000, 100, 1000, True),
        (1000, 100, 2000, True),
        (1000, 0, 1000, True),
        (1000, 0, 2000, True),
        (1000, 100, 1000.01, True),
        (1000, 100, 2000.01, True),
        (1000, 0, 1000.01, True),
        (1000, 0, 2000.01, True),
    ],
)
def test_not_pending_payment_verification_checks_payment_fees_coverage(
    amount: int,
    app_fee: float,
    amount_settled: float,
    expected_result: bool,
):
    """Test payment verification when not value is settled"""
    payment = _create_sample_payment(
        amount=amount,
    )
    flutterwave_transaction = _create_sample_flutterwave_transaction(
        tx_ref=payment.id,
        amount=amount,
        app_fee=app_fee,
        amount_settled=amount_settled,
        status=FwTransactionStatus.SUCCESSFUL,
    )
    assert expected_result == is_paid_in_full(
        payment_in_db=payment, flutterwave_transaction=flutterwave_transaction
    )
