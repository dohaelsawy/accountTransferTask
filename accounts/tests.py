from django.test import TestCase
from .models import Account

class AccountTests(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create(id="cc26b56c-36f6-41f1-b689-d1d5065b95af",name="person1", balance=500)
        self.account2 = Account.objects.create(id="121b8a59-2b95-4009-925d-962425ab3fd8",name="person2", balance=300)

    def test_transfer_funds_success(self):
        response = self.client.post(
            path='/accounts/transfer_funds/',
            data={
                "from_account_id": "cc26b56c-36f6-41f1-b689-d1d5065b95af",
                "to_account_id": "121b8a59-2b95-4009-925d-962425ab3fd8",
                "amount": 200,
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code,200)

        response_data = response.json()
        self.assertEqual(response_data['message'],"Transfer successful!")

    def test_transfer_funds_fails(self):
        response = self.client.post(
            path='/accounts/transfer_funds/',
            data={
                "from_account_id": "cc26b56c-36f6-41f1-b689-d1d5065b95af",
                "to_account_id": "121b8a59-2b95-4009-925d-962425ab3fd8",
                "amount": 700,
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code,400)

        response_data = response.json()
        self.assertEqual(response_data['error'],"Insufficient balance")

    def test_list_all_accounts_success(self):
        response = self.client.get(
            path='/accounts/',
            content_type='application/json'
        )

        self.assertEqual(response.status_code,200)

        response_data = response.json()
        self.assertEqual(len(response_data), 2)


    def test_retrieve_account_success(self):
        response = self.client.get(
            path='/accounts/cc26b56c-36f6-41f1-b689-d1d5065b95af/',
            content_type='application/json'
        )

        self.assertEqual(response.status_code,200)

        response_data = response.json()
        self.assertEqual(response_data['id'], 'cc26b56c-36f6-41f1-b689-d1d5065b95af')
        self.assertEqual(response_data['name'], 'person1')
        self.assertEqual(response_data['balance'], '500.00')


    