#-*- encoding: utf-8 -*-
import os
import sys
import unittest

root = os.path.dirname(os.path.abspath(__file__))
os.chdir(root)
sys.path.insert(0, os.path.dirname(root))
sys.path.insert(0, root)

from moip import Moip, MoipAuthorizationException
from moip.models import (ProtectedSaleOrder, Item, Customer, TaxDocument,
                         Phone, ShippingAddress, ListOrdersFilters,
                         CheckoutPreferences, Installment)


token = os.environ.get('MOIP_TOKEN', None)
key = os.environ.get('MOIP_KEY', None)


class MoipTests(unittest.TestCase):
    def _create_basic_protected_sale_order(self):
        item = Item(product='Nexer Pro', quantity=1, price=30000)
        customer = Customer(
            ownId='customerId',
            fullname='Ruhan Bidart',
            email='ruhan@nexer.com.br',
            birthDate='1989-02-03',
            taxDocument=TaxDocument(type='CPF', number='11111111120'),
            phone=Phone(countryCode='55', areaCode='31', number='911111111'),
            shippingAddress=ShippingAddress(
                street='Rua do Jose',
                streetNumber='333',
                district='Bairro',
                city='Belo Horizonte',
                state='MG',
                country='Brasil',
                zipCode='31020110',
            )
        )
        checkout_preferences = CheckoutPreferences(
            installments=[Installment(
                quantity=[1, 6]
            )]
        )
        return ProtectedSaleOrder(
            ownId='myid',
            items=[item],
            customer=customer,
            checkoutPreferences=checkout_preferences,
        )

    def test_list_customers_ok(self):
        moip = Moip(token, key)
        # if there is problem, it will generate an exception
        moip.list_customers()

    def test_list_customers_auth_problem(self):
        moip = Moip('', '')
        self.assertRaises(MoipAuthorizationException, moip.list_customers)

    def test_create_protected_sale_order_type_ok(self):
        moip = Moip(token, key)
        order = self._create_basic_protected_sale_order()
        moip.create_protected_sale_order(order)

    def test_create_protected_sale_order_error(self):
        moip = Moip(token, key)
        self.assertRaises(AssertionError, moip.create_protected_sale_order, {})

    def test_get_order(self):
        """
        It creates a pedido and try to get it, in a way to test if get_pedido
        method works.
        """
        moip = Moip(token, key)

        order_response = moip.create_protected_sale_order(
            self._create_basic_protected_sale_order())
        order = moip.get_order(order_response['id'])
        self.assertEquals(sorted(
            [u'status', u'customer', u'refunds',
             u'receivers', u'items', u'entries', u'events', u'amount', u'_links',
             u'payments', u'updatedAt', u'ownId', u'shippingAddress', u'id',
             u'createdAt', 'escrows', 'checkoutPreferences']), sorted(order.keys()))
        self.assertEquals(
            order_response['checkoutPreferences']['installments'][0]['quantity'],
            [1, 6]
        )

    def test_get_order_with_more_than_one_device(self):
        """
        It creates a pedido and try to get it, in a way to test if get_pedido
        method works.
        """
        moip = Moip(token, key)

        order = self._create_basic_protected_sale_order()
        order.items[0].quantity = 2
        order_response = moip.create_protected_sale_order(order)
        self.assertEqual(order_response['items'][0]['quantity'], 2)

    def test_list_orders(self):
        moip = Moip(token, key)
        order = self._create_basic_protected_sale_order()
        moip.create_protected_sale_order(order)
        result = moip.list_orders()
        self.assertEquals(sorted([u'status', u'customer', u'receivers',
                                  u'items', u'events', u'amount', u'_links',
                                  u'payments', u'updatedAt', u'ownId', u'id',
                                  u'createdAt', u'blocked']),
                          sorted(result['orders'][0].keys()))

    def test_list_orders_with_filters(self):
        moip = Moip(token, key)
        order = self._create_basic_protected_sale_order()
        moip.create_protected_sale_order(order)
        filters = ListOrdersFilters(offset=10)
        result = moip.list_orders(filters)
        self.assertFalse(result['orders'])

    def test_production_sandbox(self):
        moip = Moip(token, key)
        moip.sandbox()
        self.assertEqual(moip._url, Moip.url_sandbox)
        moip.production()
        self.assertEqual(moip._url, Moip.url_production)


if __name__ == '__main__':
    unittest.main()
