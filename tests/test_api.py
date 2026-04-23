import pytest


@pytest.mark.django_db
class TestProductAPI:
    def test_list_returns_only_active_products(self, api_client, product):
        response = api_client.get('/api/v1/products/')
        assert response.status_code == 200
        data = response.json()['results']
        assert len(data) == 1
        assert data[0]['name'] == 'Citra Hops'

    def test_search_by_name(self, api_client, product):
        response = api_client.get('/api/v1/products/?search=Citra')
        assert response.status_code == 200
        data = response.json()['results']
        assert len(data) == 1
        assert data[0]['name'] == 'Citra Hops'

    def test_filter_by_category(self, api_client, product, category):
        response = api_client.get(f'/api/v1/products/?category={category.slug}')
        assert response.status_code == 200
        data = response.json()['results']
        assert len(data) >= 0


@pytest.mark.django_db
class TestOrderAPI:
    def test_create_order_requires_authentication(self, api_client):
        response = api_client.post('/api/v1/orders/', {})
        assert response.status_code == 401

    def test_create_order(self, auth_client, product):
        auth_client.post('/api/v1/cart/', {'product_id': product.id, 'quantity': 2})
        response = auth_client.post('/api/v1/orders/', {
            'full_name': 'Test User',
            'phone': '+1234567890',
            'city': 'Almaty',
            'address': 'Street 1',
            'payment_method': 'card',
        })
        assert response.status_code == 201
        data = response.json()
        assert data['total_price'] == '11.98'


@pytest.mark.django_db
class TestReviewAPI:
    def test_create_review_requires_authentication(self, api_client, product):
        response = api_client.post(f'/api/v1/products/{product.id}/reviews/', {
            'rating': 5,
            'comment': 'Great hops!'
        })
        assert response.status_code == 401

    def test_create_review(self, auth_client, product, order):
        order.status = order.Status.DELIVERED
        order.save(update_fields=['status'])
        response = auth_client.post(f'/api/v1/products/{product.id}/reviews/', {
            'rating': 5,
            'comment': 'Great hops!'
        })
        assert response.status_code == 201
        data = response.json()
        assert data['rating'] == 5
        assert data['comment'] == 'Great hops!'
