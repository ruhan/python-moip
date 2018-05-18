from jsonobject import (JsonObject, StringProperty, IntegerProperty,
                        ObjectProperty, ListProperty, DateProperty)


# Create Order
class Subtotals(JsonObject):
    shipping = IntegerProperty()
    addition = IntegerProperty()
    discount = IntegerProperty()


class Amount(JsonObject):
    currency = StringProperty(exclude_if_none=True)
    subtotals = ObjectProperty(Subtotals, required=True)


class Item(JsonObject):
    product = StringProperty(required=True)
    quantity = IntegerProperty(required=True)
    detail = StringProperty(exclude_if_none=True)
    price = IntegerProperty(required=True)


class TaxDocument(JsonObject):
    type = StringProperty(required=True)
    number = StringProperty(required=True)


class Phone(JsonObject):
    countryCode = StringProperty(required=True)
    areaCode = StringProperty(required=True)
    number = StringProperty(required=True)


class ShippingAddress(JsonObject):
    street = StringProperty(required=True)
    streetNumber = StringProperty(required=True)
    complement = IntegerProperty(exclude_if_none=True)
    district = StringProperty(required=True)
    city = StringProperty(required=True)
    state = StringProperty(required=True)
    country = StringProperty(required=True)
    zipCode = StringProperty(required=True)


class Customer(JsonObject):
    ownId = StringProperty(required=True)
    fullname = StringProperty(required=True)
    email = StringProperty(required=True)
    birthDate = StringProperty(required=True)
    taxDocument = ObjectProperty(TaxDocument, required=True)
    phone = ObjectProperty(Phone, required=True)
    shippingAddress = ObjectProperty(ShippingAddress, required=True)


class RedirectUrls(JsonObject):
    urlSuccess = StringProperty(default=None)
    urlFailure = StringProperty(default=None)


class Installment(JsonObject):
    quantity = ListProperty(int, required=True)
    discount = IntegerProperty(exclude_if_none=True)
    addition = IntegerProperty(exclude_if_none=True)


class CheckoutPreferences(JsonObject):
    redirectUrls = ObjectProperty(RedirectUrls)
    installments = ListProperty(Installment, exclude_if_none=True)


class ProtectedSaleOrder(JsonObject):
    ownId = StringProperty(required=True)
    amount = ObjectProperty(Amount, exclude_if_none=True)
    items = ListProperty(Item, required=True)
    customer = ObjectProperty(Customer, required=True)
    checkoutPreferences = ObjectProperty(CheckoutPreferences,
                                         exclude_if_none=True, default=None)


# Filter Orders
class ListOrdersFilters(JsonObject):
    """
    status_choices = ['WAITING', 'NOT_PAID', 'PAID', 'REVERTED']
    paymentMethod = ['DEBIT_CARD', 'BOLETO', 'ONLINE_BANK_FINANCING',
                     'ONLINE_BANK_DEBIT', 'WALLET']
    """
    createdAt = DateProperty(exclude_if_none=True)
    paymentMethod = StringProperty(exclude_if_none=True)
    value = StringProperty(exclude_if_none=True)
    status = StringProperty(exclude_if_none=True)
    limit = IntegerProperty(exclude_if_none=True)
    offset = IntegerProperty(exclude_if_none=True)
