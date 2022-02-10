import json
import pytest
from model_bakery import baker
from django.contrib.auth.models import User
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



########################################

#
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
# class TicketTest(APITestCase):
#
#     def setUp(self):
#         user_test = User.objects.create_user(username='wiskkk', password='moskvin1')
#         user_test.save()
#         # self.user = Token.objects.create(user=user_test)
#         # self.user_token = Token.objects.get(user=user_test)
#
#         self.one_ticket = Ticket.objects.create(status='p', title='work', body='i found a good job', owner=user_test)
#         Ticket.objects.create(status='p', title='work', body='i found a good job', owner=user_test)
#
#     # @property
#     # def bearer_token(self):
#     #     user = User.objects.get(id=self.one_ticket.id)
#     #     refresh = RefreshToken.for_user(user)
#     #     return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
#
#     def test_tickets_list(self):
#         response = self.client.get('http://0.0.0.0:8000/api/tickets/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#
#     def test_ticket(self):
#         response = self.client.get(f'http://0.0.0.0:8000/api/tickets/{self.one_ticket.id}/')
#         serializer_data = TicketSerializer(self.one_ticket).data
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(serializer_data, response.data)
#
#     def test_ticket_create_unauthorized(self):
#         response = self.client.post('http://0.0.0.0:8000/api/tickets/', {'status': 'u',
#                                                                          'title': 'relationship',
#                                                                          'body': 'my wife is constantly "tired"'})
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_ticket_create_authorized(self):
#         # self.client.credentials(HTTP_AUTORIZATION='Token' + self.user_token.key)
#         response = self.client.post('http://0.0.0.0:8000/api/tickets/',
#                                     {'status': 'u',
#                                      'title': 'relationship',
#                                      'body': 'my wife is constantly "tired"'})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     # @pytest.fixture
#     # def api_client():
#     #     user = User.objects.create_user(username='john', email='js@js.com', password='js.sj')
#     #     client = APIClient()
#     #     refresh = RefreshToken.for_user(user)
#     #     client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
#     #
#     #     return client
