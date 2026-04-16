from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from orders.models import Order, OrderItem
from products.models import Category, Product


User = get_user_model()


class CheckoutFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='brewer',
            password='secret123',
        )
        self.category = Category.objects.create(name='Hops', slug='hops')
        self.product = Product.objects.create(
            name='Citra Hops',
            slug='citra-hops',
            description='Popular hop for citrus-forward styles.',
            price='9.99',
            category=self.category,
            stock=5,
            is_active=True,
        )

    def _put_product_in_cart(self, quantity=2):
        session = self.client.session
        session['cart'] = {
            str(self.product.id): {
                'quantity': quantity,
                'price': str(self.product.price),
                'name': self.product.name,
            }
        }
        session.save()

    def test_checkout_creates_order_and_clears_cart(self):
        self.client.force_login(self.user)
        self._put_product_in_cart(quantity=2)

        response = self.client.post(
            reverse('checkout'),
            data={
                'full_name': 'Ivan Ivanov',
                'phone': '+79990000000',
                'city': 'Moscow',
                'address': 'Tverskaya 1',
                'payment_method': 'card',
            },
        )

        order = Order.objects.get()

        self.assertRedirects(response, reverse('success', args=[order.id]))
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.phone, '+79990000000')
        self.assertEqual(order.shipping_address, 'Moscow, Tverskaya 1')
        self.assertEqual(order.status, Order.Status.PENDING)
        self.assertEqual(OrderItem.objects.get().product, self.product)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
        self.assertNotIn('cart', self.client.session)

    def test_cart_add_rejects_quantity_above_stock(self):
        response = self.client.post(
            reverse('cart_add', args=[self.product.id]),
            data={'quantity': 99},
            follow=True,
        )

        self.assertRedirects(response, reverse('products:detail', args=[self.product.slug]))
        self.assertNotIn('cart', self.client.session)
