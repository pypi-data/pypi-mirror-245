# Orodha-Keycloak

[This package](https://github.com/Edison-Stuart/orodha-deployment/tree/main/orodha-keycloak) is a facade interfacing with [python-keycloak](https://python-keycloak.readthedocs.io/en/latest/) used by
Orodha services in order to make requests to a keycloak server.

## Requirements

Along with the requirements in the requirements.txt file, in order for this package to function properly you need to configure
keycloak in a certain way.

[Here is a tutorial for setting up keycloak clients and service accounts with the keycloak CLI.](https://medium.com/@mihirrajdixit/getting-started-with-service-accounts-in-keycloak-c8f6798a0675)

The long and short of it is that in order for this package to work you need to set up a keycloak Realm, that has at least one client which you configure to use a confidential access type and secret_key, along with the ability to use service accounts.

Once you do this, you have to give you service account the required permissions for

-   creating users
-   deleting users
-   querying users
-   decoding tokens
-   exchanging tokens

## Usage

In order to download this package, you simply have to run the command

`python3 -m pip install orodha-keycloak`

After downloading the package you can import it to a file with the statement

`from orodha_keycloak import OrodhaKeycloakClient`

You can find further descriptions of this class in the following section as well as
the method class and method docstrings for the class.

## Description

This package contains two classes: OrodhaKeycloakClient and OrodhaCredentials.
OrodhaKeycloakClient expects an OrodhaCredentials object loaded with the values needed
by keycloak.
The OrodhaCredentials class expects the following arguments
to be in the environment or passed in as kwargs upon instantiation:

-   server_url: the main url for our keycloak server. example: `http://keycloak:{port}/auth/`
-   realm_name: The name of the keycloak realm that you want to interfacing with.
-   client_id: The client_id of the keycloak client for your service worker you want to use.

The next three are special. in order to create a connection you either have to pass a client_secret_key to the class,
or you have to pass a username and a password to the class. If you do not have one of these two choices you will get an error.

-   client_secret_key: Obtained from keycloak, used for connecting securely to the keycloak client.
-   username / password: The username and password of a keycloak user that you want to log in as in order to
    take actions on the keycloak realm.

If you would like OrodhaCredentials to populate itself from the environment, load these required variables into the environment,
making sure that the keys are capitalized and begin with ORODHA_KEYCLOAK, like so:

`ORODHA_KEYCLOAK_SERVER_URL`

The OrodhaKeycloakClient class is used to make requests and obtain information from our keycloak server.
The current methods available on this class are:

-   add_user: Adds a user to keycloak with a password.
-   delete_user: Deletes a keycloak user with a given user_id.
-   get_user: Takes either a user_id or a token and returns the user if they exist.
-   get_exchange_token: Takes target_user which can either be a keycloak username or user id, and
    returns a token used for impersonating the target_user in requests.
-   decode_jwt: Small helper function which decodes a JWT token using the client connection.

decode_jwt response schema:

```
{'id': 'ddcbcb65-4515-4e72-8b0e-9e844cb7f06a', 'createdTimestamp': 1695143223350, 'username': 'demoadmin', 'enabled': True, 'totp': False, 'emailVerified': False, 'disableableCredentialTypes': [], 'requiredActions': [], 'notBefore': 0, 'access': {'manageGroupMembership': True, 'view': True, 'mapRoles': True, 'impersonate': True, 'manage': True}}
```

More may be added in future versions.
