"""
This Module contains the OrodhaKeycloakClient class which is a facade
used to interact with a keycloak server via python-keycloak.
"""
import os
import orodha_keycloak.connections.admin
import orodha_keycloak.connections.client
from orodha_keycloak.exceptions import InvalidConnectionException


class OrodhaCredentials:
    """
    A class used to obtain and package credentials for the Orodha system.
    If kwargs are not passed in, The credentials are pulled from the environment.

    Args(as kwargs):
        server_url(str): The url of the server that our keycloak is hosted at
        realm_name(str): The name of the keycloak realm that we are attempting to access.
        client_id(str): The keycloak client_id that we are using for the connection.
        client_secret_key(str): The secret key of the keycloak client.
        username(str) - Optional: The username of the user being impersonated by python-keycloak
        password(str) - Optional: The password of the user being impersonated by python-keycloak

    Raises:
        InvalidConnectionException: If required arguments are not available
            as kwargs or in the environment.
    """

    def __init__(self, **kwargs):
        arg_dict = {
            "orodha_keycloak_server_url": kwargs.get("server_url"),
            "orodha_keycloak_realm_name": kwargs.get("realm_name"),
            "orodha_keycloak_client_id": kwargs.get("client_id"),
            "orodha_keycloak_client_secret_key": kwargs.get("client_secret_key"),
            "orodha_keycloak_username": kwargs.get("username"),
            "orodha_keycloak_password": kwargs.get("password")
        }

        for key, value in arg_dict.items():
            if not value:
                arg_dict[key] = os.environ.get(key.upper())

        required_args_available = arg_dict[
            "orodha_keycloak_server_url"] and arg_dict[
                "orodha_keycloak_realm_name"] and arg_dict["orodha_keycloak_client_id"]

        username_password_auth_available = arg_dict[
            "orodha_keycloak_username"] and arg_dict[
                "orodha_keycloak_password"]

        if not required_args_available:
            raise InvalidConnectionException(
                ["orodha_keycloak_server_url",
                    "orodha_keycloak_realm_name", "orodha_keycloak_client_id"],
                message="All required arguments must be made available as kwargs or" +
                " in the environment."
            )

        self.server_url = arg_dict["orodha_keycloak_server_url"]
        self.realm_name = arg_dict["orodha_keycloak_realm_name"]
        self.client_id = arg_dict["orodha_keycloak_client_id"]

        if not arg_dict["orodha_keycloak_client_secret_key"] and not username_password_auth_available:
            raise InvalidConnectionException(
                ["orodha_keycloak_client_secret_key",
                    "orodha_keycloak_username", "orodha_keycloak_password"],
                message="orodha_keycloak_client_secret_key or orodha_keycloak_username and orodha_keycloak_password " +
                "must be made available in the environment"
            )

        if arg_dict["orodha_keycloak_client_secret_key"]:
            self.client_secret_key = arg_dict["orodha_keycloak_client_secret_key"]
            self.secret_key_available = True
        else:
            self.username = arg_dict["orodha_keycloak_username"]
            self.password = arg_dict["orodha_keycloak_password"]
            self.secret_key_available = False


class OrodhaKeycloakClient:
    """
    Facade class used for connecting to, and interacting with keycloak for the Orodha
    shopping list app.

    Args:
        credentials_object(OrodhaCredentials): An instance of the OrodhaCredentials object containing
            our client information

    Raises:
        InvalidConnectionException: If the connection variables given are invalid
            and do not allow connection.
    """

    def __init__(
        self,
        credentials_object: OrodhaCredentials
    ):
        self.credentials = credentials_object
        try:
            self.client_connection = orodha_keycloak.connections.client.create_client_connection(
                server_url=self.credentials.server_url,
                realm_name=self.credentials.realm_name,
                client_id=self.credentials.client_id,
                client_secret_key=self.credentials.client_secret_key
            )
        except AttributeError:
            self.client_connection = orodha_keycloak.connections.client.create_client_connection(
                server_url=self.credentials.server_url,
                realm_name=self.credentials.realm_name,
                client_id=self.credentials.client_id,
            )
        try:
            if self.credentials.client_secret_key:
                self.admin_connection = orodha_keycloak.connections.admin.create_admin_connection(
                    server_url=self.credentials.server_url,
                    realm_name=self.credentials.realm_name,
                    client_id=self.credentials.client_id,
                    client_secret_key=self.credentials.client_secret_key,
                )
        except AttributeError:
            self.admin_connection = orodha_keycloak.connections.admin.create_admin_connection(
                server_url=self.credentials.server_url,
                realm_name=self.credentials.realm_name,
                username=self.credentials.username,
                password=self.credentials.password
            )

    def add_user(
            self,
            email: str,
            username: str,
            firstName: str,
            lastName: str,
            password: str
    ):
        """
        Adds a user to keycloak with a password.

        Args:
                email(str): The email of the new user.
                username(str): The username of the new user.
                firstName(str): The first name of the new user.
                lastName(str): The last name of the new user.
                password(str): The password of the new user.

        Returns:
            new_user: The new user info genereated by the keycloak server.

        """
        new_user = self.admin_connection.create_user(
            {
                "email": email,
                "username": username,
                "enabled": True,
                "firstName": firstName,
                "lastName": lastName,
                "credentials": [
                    {
                        "value": password,
                        "type": "password",
                    }
                ],
            },
            exist_ok=False,
        )

        return new_user

    def delete_user(self, user_id: str) -> dict:
        """
        Deletes a keycloak user with a given user_id.

        Args:
            user_id(str): The user id of the user to be deleted.

        Returns:
            response: The response from the keycloak server with info about the deletion.
        """
        response = self.admin_connection.delete_user(user_id=user_id)

        return response

    def get_user(self, token: str = None, user_id: str = None):
        """
        Takes either a user_id or a token and returns the user if they exist.

        Args:
            user_id(str): String user id of our user, is used to access keycloak in a query.
            token(str): Our JWT token that we will use to decode and obtain the user from.

        Returns:
            user: The user, if any, that is associated with this user_identification value.
        """

        if token:
            return_value = self.admin_connection.get_user(
                self.decode_jwt(token).get("sub"))
        else:
            return_value = self.admin_connection.get_user(user_id)

        return return_value

    def get_exchange_token(self, target_user: str) -> dict:
        """
        Function which accepts a token from a client and returns a
        new token used for access to a different client.

        Args:
            target_client(str): The client id that is related to the client we are attempting to
                get a token from.
            target_user(str): The user_id of the target user we are attempting to impersonate.

        Returns:
            dict: Dictionary containing our new token and some metadata about said token.
        """
        return self.client_connection.exchange_token(
            token=None,
            audience=self.credentials.client_id,
            subject=target_user
        )

    def decode_jwt(self, token: str) -> dict:
        """
        Small helper function which decodes a JWT token using the client connection.

        Args:
            token(str): A JWT token that we get from keycloak.

        Returns:
            token_info(dict): The decoded information from the token.
        """
        keycloak_public_key = "-----BEGIN PUBLIC KEY-----\n" + \
            self.client_connection.public_key() + "\n-----END PUBLIC KEY-----"
        options = {
            "verify_signature": True,
            "verify_aud": False,
            "verify_exp": True
        }
        token_info = self.client_connection.decode_token(
            token,
            key=keycloak_public_key,
            options=options)
        return token_info
