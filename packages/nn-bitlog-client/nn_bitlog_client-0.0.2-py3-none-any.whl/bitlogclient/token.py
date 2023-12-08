import requests
import logging

class Token:
    """
    
    
    This class is used to handle the authentication token from a specific domain.

    Attributes:
        domain (str): The domain from which the token is fetched.
        basic_auth_user (str): The username for basic authentication.
        basic_auth_password (str): The password for basic authentication.
        username (str): The username for the token request.
        password (str): The password for the token request.
        token (str): The fetched token. It's None until a token is successfully fetched.
        expires_in (int): The time in seconds when the token expires. It's None until a token is successfully fetched.

    Methods:
        __fetch_token(): Fetches the token from the domain and sets the 'token' and 'expires_in' attributes.
        get_token(): Returns the fetched token.
        get_expires_in(): Returns the time in seconds when the token expires.
    """
    def __init__(self, domain: str, basic_auth_user: str,
                basic_auth_password: str,username: str, password: str):
        """
        The constructor for the Token class.

        Parameters:
            domain (str): The domain from which the token is fetched. Example: 'mycompany6543live'.
            basic_auth_user (str): The username for basic authentication. Example: '6543live'.
            basic_auth_password (str): The password for basic authentication.
            username (str): The username for the token request. From a user in the domain.
            password (str): The password for the token request. From a user in the domain.
        """
        
        self.domain = domain
        self.basic_auth_user = basic_auth_user
        self.basic_auth_password = basic_auth_password
        self.username = username
        self.password = password
        
        self.token = None
        self.expires_in = None
        
        self.__fetch_token()
    
    def __fetch_token(self):
        TOKEN_URL = f'https://{self.domain}.azurewebsites.net/WmsAPI/token'
        credentials = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password}
        
        response = requests.get(
            TOKEN_URL,
            data=credentials,
            auth=(
                self.basic_auth_user,
                self.basic_auth_password))
                
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f'Error when fetching_token: \n {e} \n {response.text}')
            return None
        
        self.token = response.json()['access_token']
        self.expires_in = response.json()['expires_in']
    
    def get_token(self):
        """
        This method returns the fetched token.

        Returns:
            str: The fetched token. If no token has been fetched yet, it returns None.
        """
        
        return self.token
    
    def get_expires_in(self):
        return self.expires_in