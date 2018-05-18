# Python Moip Implementation

A modern Python library to communicate with MoIP.
Notice that it is an INCOMPLETE implementation, thus not all methods are done.
Pull requests are welcome!

* Author: Ruhan Bidart
* Contributor: Sadraque Viana


# Installation

The installation can be done via pip:

$ pip install https://github.com/ruhan/python-moip.git

# Use

The simpler way to test is by calling "list_customers" method.

You can do that by:

```python
from moip import Moip
moip = Moip(YOUR_TOKEN, YOUR_KEY)
moip.production() # if you are working in sandbox, just omit this line
moip.list_customers()
```

# Implemented methods:

* list_customers()
* get_order(id)
* list_orders(models.ListOrdersFilters)
* create_protected_sale_order(models.ProtectedSaleOrder)
* create_webhook(events, target_url)
* delete_webhook(notification_id)
* list_webhooks()

To avoid these methods parameters of being complex dicts, we decided
to create a concept of "models". Each model represents this communication
and its class is in moip.models. Check that to use the model each method
calls by.
