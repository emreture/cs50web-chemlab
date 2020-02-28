from django.test import TestCase
from .models import Customer
from django.contrib.auth import get_user_model

# Create your tests here.


class ModelsTestCase(TestCase):
    def setUp(self) -> None:
        # Create users
        alice = get_user_model().objects.create_user("alice_astor")
        bob = get_user_model().objects.create_user("bob_astor")
        charlie = get_user_model().objects.create_user("charlie_emek")
        david = get_user_model().objects.create_user("david_both")

        # Create customers
        astor = Customer.objects.create(name="Astor A.Ş.", address="Planet Earth")
        emek = Customer.objects.create(name="Emek A.Ş.", address="Planet Mars")

        astor.users.add(alice)
        astor.users.add(bob)
        astor.users.add(david)
        emek.users.add(charlie)
        emek.users.add(david)

    def test_users_count(self):
        users = get_user_model().objects
        self.assertEqual(users.count(), 4)

    def test_customers_count(self):
        customers = Customer.objects
        self.assertEqual(customers.count(), 2)

    def test_customer_users_count(self):
        astor = Customer.objects.get(name="Astor A.Ş.")
        emek = Customer.objects.get(name="Emek A.Ş.")
        david = get_user_model().objects.get(username="david_both")
        self.assertEqual(astor.users.count(), 3)
        self.assertEqual(emek.users.count(), 2)
        self.assertEqual(david.organization.count(), 2)

    def test_object_name(self):
        customer = Customer.objects.get(name="Astor A.Ş.")
        expected_name = customer.name
        self.assertEqual(expected_name, str(customer))
