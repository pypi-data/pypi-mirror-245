"""Helpers for interacting with Google APIs within the Sym SDK."""

from sym.sdk.exceptions import GoogleError  # noqa
from sym.sdk.user import User


def is_user_in_group(user: User, *, group_email: str) -> bool:
    """Checks if the provided user is a member of the specified Google Group.
    Membership may either be direct or indirect.

    **Prerequisites**:

    - To call this method, your ``gcp_connector`` module must have ``enable_google_group_management = true``.

    Args:
        user: The User to check
        group_email: The email identifier of the Google Group

    Returns:
        True if the user is part of the Google Group
    """
