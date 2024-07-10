import pytest
from rest_framework.test import APIClient
import app_vars as vars
from api.tests.auth import create_user, login
from api.tests.users import get_users, get_user, patch_user


@pytest.fixture(autouse=True)
def init_cache(request):
    request.config.cache.get(vars.USER_1_CACHE_AUTH, None)
    request.config.cache.get(vars.USER_2_CACHE_AUTH, None)


@pytest.fixture(autouse=True)
def api_client():
    return APIClient()


@pytest.mark.django_db
@pytest.mark.order(1)
def test(request, api_client):
    create_user(request, api_client, vars.USER_1_CACHE_AUTH, vars.CREATE_USER_1_BODY)
    create_user(request, api_client, vars.USER_2_CACHE_AUTH, vars.CREATE_USER_2_BODY)
    login(request, api_client, vars.USER_1_CACHE_AUTH)
    get_users(request, api_client, vars.USER_1_CACHE_AUTH)
    get_user(request, api_client, vars.USER_1_CACHE_AUTH,
             vars.ASSERTION_DATA_FOR_GET_USER_ID2, 2)
    get_user(request, api_client, vars.USER_1_CACHE_AUTH,
             vars.ASSERTION_DATA_FOR_GET_USER_ID1, 1)
    patch_user(request, api_client, vars.USER_1_CACHE_AUTH,
               1, vars.PATCH_BODY_USER_1)
    get_user(request, api_client, vars.USER_1_CACHE_AUTH,
             vars.ASSERTION_AFTER_PATCH_BODY_USER_1, 1)
    get_user(request, api_client, vars.USER_1_CACHE_AUTH,
             vars.ASSERTION_AFTER_PATCH_BODY_USER_2, 2)
