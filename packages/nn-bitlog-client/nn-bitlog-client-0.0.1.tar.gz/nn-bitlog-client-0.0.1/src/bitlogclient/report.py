from dataclasses import dataclass

import requests
import logging


@dataclass
class ReportParams:
    """
        This class is used to specify report parameters.

        Attributes:
            name (str): Name of the param. Example: '@from_date'.
            type (str): Type of the param. Example: 'date'.
            value (str): Value of the param. Example: '2021-01-01'.
    """
    name: str
    type: str
    value: str


class Report:
    
    """
        This class is used to fetch data views from a domain.

        Attributes:
            token (str): The authentication token.
            domain (str): The domain from which the reports are fetched.
            url (str): The URL for the API endpoint.
            headers (dict): The headers used for the API requests.

        Methods:
            list_views() -> list[dict]: 
                Lists all views from Bitlog.
            get_view(view_name: str) -> list[dict]: 
                Gets a view from Bitlog.
            get_view_with_params(view_name: str, parameters: list[ReportParams]) -> list[dict]: 
                Gets a view from Bitlog with parameters.
    """
    
    def __init__(self, token: str, domain: str) -> None:
        """
            The constructor for the Report class.

            Parameters:
                token (str): The authentication token.
                domain (str): The domain from which the reports are fetched.
        """
        
        self.token = token
        self.domain = domain
        self.url = f'https://{self.domain}.azurewebsites.net/WmsAPI/api/report'
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        
    def __create_list_of_params(self, params: list[ReportParams]) -> list[dict]:
        return [param.__dict__ for param in params]
    
    def list_views(self) -> list[dict]:
        """
            This method lists all views from Bitlog.

            Returns:
                list[dict]: A list of dictionaries representing all views. If an error occurs during the request, it returns None.
        """
        
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            logging.error(f'Error fetching views from Bitlog \n Response: {response.content}')
            return
        return response.json()

    def get_view(self, view_name: str) -> list[dict]:
        """
            This method fetches a view from Bitlog. An example of a view could be 'BL_MyDataViewManagerView'.

            Parameters:
                view_name (str): The name of the view to fetch.

            Returns:
                list[dict]: A list of dictionaries representing the fetched data. If an error occurs during the request, it returns None.
        """
        
        data = {
            'name': view_name,
            'type':'view'
        }
        
        logging.info(f'Fetching view from Bitlog \n View name: {view_name}')
        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code != 200:
            logging.error(f'Error getting view from Bitlog \n Response: {response.content}')
            return
        
        response = response.json()
        data = response['Table']
        
        return data
    
    def get_view_with_params(self, view_name, parameters: list[ReportParams]) -> list[dict]:
        """
            This method fetches a view from Bitlog with specified parameters. An example of a view could be 'BL_MyDataViewManagerProc'

            Parameters:
                view_name (str): The name of the view to fetch.
                parameters (list[ReportParams]): A list of ReportParams objects representing the parameters for the view.

            Returns:
                list[dict]: A list of dictionaries representing the fetched data. If an error occurs during the request, it returns None.

        """
        
        data = {
            'parameters': self.__create_list_of_params(parameters),
            'name':view_name,
            'type':'Parameterized'
        }
        logging.info(f'Getting view from Bitlog \n View name: {view_name} \n View parameters: \n {parameters}')
        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code != 200:
            logging.error(f'Error getting view from Bitlog \n Response: {response.content}')
            return
        
        response = response.json()
        data = response['Table']
        
        return data