from django.urls import reverse


def get_users(request, api_client, auth_cache: str):
    cache = request.config.cache.get(auth_cache, None)
    url = reverse('all_users')
    anon_response = api_client.get(url)
    assert anon_response.status_code == 401
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {cache["access"]}')
    auth_response = api_client.get(url)
    assert auth_response.status_code == 200
    assert len(auth_response.json()) > 0
    api_client.credentials(HTTP_AUTHORIZATION=None)


def get_user(request, api_client, auth_cache: str,
             assertion_data: dict, user_id: int):
    cache = request.config.cache.get(auth_cache, None)
    url = reverse('user_by_id', args=[user_id])
    anon_response = api_client.get(url)
    assert anon_response.status_code == 401
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {cache["access"]}')
    auth_response = api_client.get(url)
    assert auth_response.status_code == 200
    assert auth_response.json() == assertion_data
    api_client.credentials(HTTP_AUTHORIZATION=None)


def patch_user(request, api_client, auth_cache: str,
               user_id: int, body: dict):
    cache = request.config.cache.get(auth_cache, None)
    url = reverse('user_by_id', args=[user_id])
    anon_response = api_client.patch(url, data=body)
    assert anon_response.status_code == 401
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {cache["access"]}')
    bad_id = user_id+1
    bad_url = reverse('user_by_id', args=[bad_id])
    bad_response = api_client.patch(bad_url, data=body)
    assert bad_response.status_code == 403
    auth_response = api_client.patch(url, data=body)
    assert auth_response.status_code == 201
    api_client.credentials(HTTP_AUTHORIZATION=None)
