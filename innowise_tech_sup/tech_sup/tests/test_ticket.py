import json

import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from innowise_tech_sup.tech_sup.models import Ticket

pytestmark = pytest.mark.django_db


class TestTicketEndpoints:
    endpoint = '/api/tickets/'

    def test_list(self, api_client):
        baker.make(User, _quantity=3)

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client):
        ticket = baker.prepare(Ticket)
        expected_json = {
            'status': ticket.status,
            'title': ticket.title,
            'body': ticket.body
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_retrieve(self, api_client):
        ticket = baker.make(Ticket)
        expected_json = {
            'status': ticket.status,
            'title': ticket.title,
            'body': ticket.body
        }
        url = f'{self.endpoint}{ticket.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, rf, api_client):
        old_ticket = baker.make(Ticket)
        new_ticket = baker.prepare(Ticket)
        ticket_dict = {
            'status': new_ticket.status,
            'title': new_ticket.title,
            'body': new_ticket.body
        }

        url = f'{self.endpoint}{old_ticket.id}/'

        response = api_client().put(
            url,
            ticket_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content) == ticket_dict

    @pytest.mark.parametrize('field', [
        ('status'),
        ('title'),
        ('body'),
    ])
    def test_partial_update(self, mocker, rf, field, api_client):
        ticket = baker.make(Ticket)
        ticket_dict = {
            'status': ticket.status,
            'title': ticket.title,
            'body': ticket.body
        }
        valid_field = ticket_dict[field]
        url = f'{self.endpoint}{ticket.id}/'

        response = api_client().patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field

    def test_delete(self, mocker, api_client):
        ticket = baker.make(Ticket)
        url = f'{self.endpoint}{ticket.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Ticket.objects.all().count() == 0
