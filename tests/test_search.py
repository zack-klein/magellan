import datetime

from tests.utils import (
    client,
    admin_login,
    get_admin,
    logout,
    build_dummy_data,
)


def test_dummy_data_exists(client):  # noqa
    admin_login(client)
    build_dummy_data(client)
    logout(client)
