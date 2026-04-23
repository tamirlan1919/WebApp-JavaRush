import pytest
from decimal import Decimal
from orders.cart import Cart


@pytest.mark.django_db
class TestCart:
    def test_cart_initialization(self, mock_request):
        cart = Cart(mock_request)
        assert cart.cart == {}

    def test_cart_add_product(self, mock_request, product):
        cart = Cart(mock_request)
        cart.add(product=product, quantity=2)
        assert str(product.id) in cart.cart
        assert cart.cart[str(product.id)]['quantity'] == 2
        assert Decimal(cart.cart[str(product.id)]['price']) == product.price

    def test_cart_remove_product(self, mock_request, product):
        cart = Cart(mock_request)
        cart.add(product=product, quantity=2)
        cart.remove(product)
        assert str(product.id) not in cart.cart

    def test_cart_total_price(self, mock_request, product):
        cart = Cart(mock_request)
        cart.add(product=product, quantity=3)
        total_price = cart.get_total_price()
        expected_price = Decimal('17.97')
        assert total_price == expected_price
