from django.urls import reverse


def create_user(request, api_client, auth_cache: str, body: dict):
    url = reverse('registration')
    response = api_client.post(url, data=body)
    assert response.status_code == 201
    request.config.cache.set(auth_cache, body)


def login(request, api_client, auth_cache: str):
    cache = request.config.cache.get(auth_cache, None)
    body = {
        'username': cache['username'],
        'password': cache['password'],
    }
    url = reverse('login')
    response = api_client.post(url, data=body)
    assert response.status_code == 200
    data = response.json()
    body['access'] = data['access']
    body['refresh'] = data['refresh']
    request.config.cache.set(auth_cache, body)
