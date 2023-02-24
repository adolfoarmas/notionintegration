from dotenv import dotenv_values
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
env_values = dotenv_values(dotenv_path)

class ApiConnectionHeaderDefinition:
    """Returns an object through get_header() method with header definitions needed to add to HTTP requests to be made to the API."""

    def __init__(self):
        """Constructor method"""
        NOTIONKEY = env_values['NOTIONKEY']
        NOTIONVERSION = env_values['NOTIONVERSION']

        self.authorization = f'Bearer {NOTIONKEY}'
        self.content_type = 'application/json'
        self.notion_version = NOTIONVERSION
        
    def get_header(self):
        """getter function to asemble and return header definitions
        Returns:
            object: key:value of Autorization, Content-Type ando Notion-Version parameters.
        """
        return {
                'Authorization': self.authorization,
                'Content-Type': self.content_type,
                'Notion-Version': self.notion_version,
              }