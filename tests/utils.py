from src.modules.users.schemas.user import UserCreate, UserResponse


def check_user(expected_user: UserCreate, actual_user: UserResponse) -> None:
    assert actual_user.username == expected_user.username
    assert actual_user.full_name == expected_user.full_name
    assert actual_user.email == expected_user.email
    assert actual_user.age == expected_user.age
