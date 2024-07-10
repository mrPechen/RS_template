USER_1_CACHE_AUTH = 'auth_user_1_data'

USER_2_CACHE_AUTH = 'auth_user_2_data'

CREATE_USER_1_BODY = {
    'username': 'user1',
    'password': '654321Qq',
}

CREATE_USER_2_BODY = {
    'username': 'user2',
    'password': '654321Qq',
}

ASSERTION_DATA_FOR_GET_USER_ID1 = {
    "id": 1,
    "login": "user1",
    "email": "",
    "phone": None,
    "role": "user",
    "password": "654321Qq"
}

ASSERTION_DATA_FOR_GET_USER_ID2 = {
    "id": 2,
    "login": "user2",
    "email": "",
    "phone": None,
    "role": "user",
}

PATCH_BODY_USER_1 = {
    "id": 1,
    "login": "user11",
    "email": "user1@email.com",
    "phone": "71231231212",
    "role": "mentor",
    "mentored_users": [2]
}

ASSERTION_AFTER_PATCH_BODY_USER_1 = {
    "id": 1,
    "login": "user11",
    "email": "user1@email.com",
    "phone": "71231231212",
    "role": "mentor",
    "password": "654321Qq",
    "mentored_users": ['user2']
}

ASSERTION_AFTER_PATCH_BODY_USER_2 = {
    "id": 2,
    "login": "user2",
    "email": "",
    "phone": None,
    "role": "user",
    "mentor": "user11"
}
