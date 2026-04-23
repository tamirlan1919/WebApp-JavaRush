import pytest
from decimal import Decimal
from django.db import IntegrityError
from products.models import Product, Category
from orders.models import Order
from reviews.models import Review


@pytest.mark.django_db
class TestProductModel:
    def test_str_returns_name(self, product)-> None:
        assert str(product) == 'Citra Hops'

    def test_product_has_correct_fields(self, product: Product, category: Category) -> None:
        assert product.name == 'Citra Hops'
        assert product.slug == 'citra-hops'
        assert product.description == 'Best hops'
        assert product.price == Decimal('5.99')
        assert product.category == category
        assert product.stock == 100
        assert product.is_active is True

    def test_slug_is_unique(self, product: Product) -> None:
        with pytest.raises(IntegrityError):
            Product.objects.create(
                name='Duplicate Slug',
                slug='citra-hops',
                description='Another hops',
                price=4.99,
                category=product.category,
                stock=50,
                is_active=True
            )

    def test_category_str_returns_name(self, category: Category) -> None:
        assert str(category) == 'Hops'


@pytest.mark.django_db
class TestOrderModel:
    def test_str_returns_order_number(self, order: Order) -> None:
        assert str(order) == f'{order.id} - {order.user} '

    def test_order_has_correct_fields(self, order: Order, user) -> None:
        assert order.user == user
        assert Decimal(str(order.total_price)) == Decimal('29.95')
        assert order.status == Order.Status.PENDING


@pytest.mark.django_db
class TestReviewModel:
    def test_str_returns_review_summary(self, review: Review) -> None:
        assert str(review) == f'{review.user} - {review.product} {review.rating}/5'

    def test_review_has_correct_fields(self, review: Review, user, product) -> None:
        assert review.user == user
        assert review.product == product
        assert review.rating == 4
        assert review.comment == 'Great hops for brewing!'

    def test_unique_review_per_user_product(self, review: Review, user, product) -> None:
        with pytest.raises(IntegrityError):
            Review.objects.create(
                user=user,
                product=product,
                rating=5,
                comment='Another review'
            )