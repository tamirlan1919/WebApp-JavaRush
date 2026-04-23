import pytest


@pytest.mark.django_db
class TestViews:
    def test_homepage(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_product_detail_view(self, client, product):
        response = client.get(f'/{product.slug}/')
        assert response.status_code == 200
        assert 'Citra Hops' in response.content.decode()

    def test_filter_by_category(self, client, product, category):
        response = client.get(f'/?category={category.slug}')
        assert response.status_code == 200
        assert 'Citra Hops' in response.content.decode()