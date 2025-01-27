class UserTestData:
    TEST_USER_DATA = {
        "username": "test_user",
        "full_name": "fullname",
        "email": "user1@example.com",
        "age": 20,
        "password": "Testpassword_1",
    }

    DUPLICATE_USER_DATA = {
        "username": "test_duplicate_user",
        "email": "user1@example.com",
        "age": 20,
        "password": "Testpassword_2",
    }

    INVALID_USER_DATA = {
        "username": 1,
        "full_name": 1,
        "email": "",
        "age": "dsa",
        "password": "",
    }
