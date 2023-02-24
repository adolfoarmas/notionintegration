import sys, os
import ast
import requests
import json
from . import urls
from dotenv import dotenv_values
from os.path import join, dirname
sys.path.append('..')
from textAnalizer import TextAnalizer
from .apiConnectionHeaderDefinition import ApiConnectionHeaderDefinition

dotenv_path = join(dirname(__file__), '.env')
env_values = dotenv_values(dotenv_path)
PARENT_ID = env_values['PARENT_ID']

class DataBase:
    """DataBase object definition, needed to create a Notion Data Base or to use a existing one."""

    def __init__(self, parent_id:str, database_name:str, properties:list = {}):
        """Constructor Method

        Args:
            parent_id (str): Database Parent Id in Notion. i.e.: xxxxxxxxx-xxxx-xxxx-xxxxx-xxxxxxxxxxxx; where x is hexadecimal digit
            database_name (str): Given name to database.
            properties (list, optional):List of properties (column, titles, filter, etc.) required for the database only when one of it is being created. Defaults to {}.
        """
        self.parent_id = parent_id
        self.database_name = database_name
        self.properties = properties
        self.api_connection_header_definition = ApiConnectionHeaderDefinition()
        self.headers = self.api_connection_header_definition.get_header()
        self.database_id = ''
        self.database_dictionary = {}

        if not properties:
            self.database_dictionary = self.get_existing_database()

    def get_database_id(self):
        """getter method for de DB id

        Returns:
            str: DB id provided by Notion API
        """
        return self.database_id

    def get_databases(self):
        """getter method for de DB object

        Returns:
            object: DB data in JSON format.
        """
        url = urls.DATABASE_OR_PAGE_SEARCH
        search_params = {'filter': {'value': 'database', 'property': 'object'}}

        try:
            search_response = requests.post(
                url, 
                json=search_params, headers=self.headers)
        except Exception:
            client_error = {'object':'error', 'status':'400', 'code':'client error', 'message':'unable to connect to API'}
            return client_error
            
        return search_response.json()

    
    def get_existing_database(self):
        """getter of DB object if it exists in Notion

        Returns:
            dictionary: 'object' == 'error' || 'object'=='boolean'; 'result' == True if DB exists; 'database' == DB object data if exists
        """
        database_results = self.get_databases()

        if database_results['object'] == 'error':
            error_dict_str = "{'object': 'error','message' : 'Error: status={error_status}, code={error_code}, message={error_message}".format(error_status = database_results['status'], error_code = database_results['code'], error_message=database_results['message'])
            error_dict = ast.literal_eval(error_dict_str)
            return error_dict

        #navigate json response 
        databases_results = database_results['results']

        for database in databases_results:
            title = database['title'][0]['text']['content']
            if title == self.database_name:
                database_exists_object = {'object':'boolean', 'results' : True, 'message':'database name you provided already exists', 'database': database}
                self.database_id = database['id']
                return database_exists_object
        
        database_does_not_exists_object = {'object':'boolean', 'results': False, 'message':'database name you provided do not exists', 'database':None}
        return database_does_not_exists_object


    def get_database_parent_data(self):
        """getter of DB parent data, defined in Notion configuration.

        Returns:
            dictionary: dictionary configuration, 'type' of parent; 'page_id' = string Notion page ID format
        """
        return {
                'type' : 'page_id',
                'page_id' : self.parent_id
            }

    def get_database_title_data_to_payload(self):
        """getter of DB title object, with format parameters
        TO_REFACTOR: decuple each parameter.

        Returns:
            list: list of objects as needed by API
        """
        return [
                {
                    'type' : 'text',
                    'text' : {
                        'content' : self.database_name,
                        'link' : None
                    },
                    'plain_text': self.database_name,
                    'href': None,
                    'annotations': {
                        'bold': False,
                        'italic': False,
                        'strikethrough': False,
                        'underline': False,
                        'code': False,
                        'color': 'default'
                    },
                }
            ]
    
    def get_database_properties_data(self):
        """getter of database properties defined by user

        Returns:
            dictionary: properties defined by user.
        """
        properties_object = {}
        for propertie in self.properties:
            properties_object.update(propertie)
        
        return properties_object

    def get_database_payload(self):
        """getter of HTTP request payload as required by API

        Returns:
            dictionary: dictionary of parent, title and properties data as defined in the rest of getters
        """

        return {'parent': self.get_database_parent_data(),
                'title': self.get_database_title_data_to_payload(),
                'properties': self.get_database_properties_data()
                }

    def set_database_id(self, database_id:str):
        """setter method for database id in an already instanciated DataBase Object once it has been created

        Args:
            database_id (str): string with DB id provided by Notion API

        Returns:
            str: informative text with new database id
        """
        self.database_id = database_id
        return "database id {db_id} registered".format(db_id=self.database_id)    

    def create_database_if_not_exists(self):
        """function to create DB validating before if it does not exist in Notion.

        Returns:
            JSON: respose from API after HTTP request (POST) to create a new DB.
        """

        #error triying to querying if db exists
        database_exist_validation = self.get_existing_database()
        if database_exist_validation['object'] == 'error':
            return database_exist_validation
        
        #db already exists
        if database_exist_validation['object'] == 'boolean':
            if database_exist_validation['results']:
                return database_exist_validation

        url = urls.DATABASES
        payload = self.get_database_payload()
        header = self.headers

        response = requests.post(url, json=payload, headers=header)

        response_json = response.json()

        if response_json['object'] == 'database':
            self.set_database_id(response_json['id'])
        
        #API response format
        return response_json

class Page:
    """Page definition, page instance is a row register in a DB required object"""
    def __init__(self, database_object):
        self.database_object = database_object
        self.api_connection_header_definition = ApiConnectionHeaderDefinition()
        self.headers = self.api_connection_header_definition.get_header()
        ...

    def add_row_to_ratabase(self, row_data:dict):
        """new row data to be added to a DB
        
        REFACTOR: Decouple specific data format from this class method

        Args:
            row_data (dict): key:value dictionary regarding to DB object's columns
        """
        book_title=row_data['Book Title']
        author=row_data['Author']
        type_of_element=row_data['Type of Element']
        position=row_data['Position']
        highlighted_text=row_data['Highlignted Text']
        page=row_data['page']
        date=row_data['Date' ]
        
        data = {
            'Book Title': {'title': [{'text': {'content': book_title}}]},
            'Author': {'rich_text': [{'text': {'content': author}}]},
            'Type of Element': {'select': {'name': type_of_element['name']}},
            'page': {'number': page},
            'Position':  {'rich_text': [{'text': {'content': position}}]},
            'Highlignted Text': {'rich_text': [{'text': {'content': highlighted_text}}]},
            'Date': {'date': {'start': date, 'end': None}},
        }

        url = urls.PAGES
        print(self.database_object.get_database_id())
        payload = {'parent':{'database_id': self.database_object.database_id}, 'properties': data}

        response = requests.post(url=url, json=payload, headers=self.headers)
        print(response.json())