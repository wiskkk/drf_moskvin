import pytest
from model_bakery import baker
from rest_framework.test import APIClient


def utbb():
    def unfilled_ticket_bakery_batch(n):
        utbb = baker.make('tech_sup.Ticket', _quantity=n)
        return utbb

    return unfilled_ticket_bakery_batch


@pytest.fixture
def ftbb():
    def filled_ticket_bakery_batch(n):
        utbb = baker.make('tech_sup.Ticket', _quantity=n)
        return utbb

    return filled_ticket_bakery_batch


@pytest.fixture
def ftb():
    def filled_ticket_bakery():
        utbb = baker.make('tech_sup', user=baker.make('auth.User'))
        return utbb

    return filled_ticket_bakery


@pytest.fixture
def api_client():
    return APIClient
