# notionintegration

Python Integration with Notion API

## Description

Notionintegration is a package with the purpose of creating databases or obtain already existing databases.
Furthermore you will be able to search databases by name, once it is found, you could add new pages.

![Automation to load pages in a database](https://github.com/adolfoarmas/notionintegration/blob/main/media/2023-02-25%2011-40-44.gif)

*** **In "Page" class method "add_row_to_ratabase", "data" object has to be addapted to columns format of your database, in further versions the data dictionary will be decoupled of the particular application it was needed for**.

## Getting Started

### Dependencies

* SO windows / Linux
* Initiate a virtual environment in project folder
* Python 3.11.0
* Install Python packages: requests, dotenv
* Create a ".env" file in "notionintegration" folder with content:
  
  ```
  NOTIONKEY=<secret_key_integration_generated_in_notion_app> #see: https://www.pynotion.com/getting-started-with-python
  NOTIONVERSION='YYYY-MM-dd'
  PARENT_ID=<id_of_parent_of_database> #existing or new
  ```
### Executing program

* Create DataBase

```
#example of database column properties
database_columns_properties =  [
    {'Book Title' : {
        'name': 'Book Title',
        'type': 'title',
        'title': {},
    }},
    {'Author': {
        'name': 'Author',
        'type': 'rich_text',
        'rich_text': {},
    }},
    {'Type of Element': {
        'name': 'Type of Element',
        'type': 'select',
        "select": {
            "options": [
            {
                "id": "note",
                "name": "📝Note",
                "color": "blue"
            },
            {
                "id": "highlight",
                "name": "🖍Highlight",
                "color": "red"
            },
            {
                "id": "marker",
                "name": "📑Marker",
                "color": "yellow"
            }
            ]
        }
    }},
    {'page': {
        'name': 'Page',
        'type': 'number',
        'number': {
            'format': 'number'
        },
    }},
    {'Position': {
        'name': 'Position',
        'type': 'rich_text',
        'rich_text': {},
    }},
    {'Highlignted Text': {
        'name': 'Highlignted Text',
        'type': 'rich_text',
        'rich_text': {},
    }},
    {'Date': {
        'name': 'Date',
        'type': 'date',
        'date': {},
    }}
]

database = DataBase(PARENT_ID, database_name=<str:database_name>, properties=database_columns_properties)
create_database_response = database.create_database_if_not_exists()
```

* Get Existing DataBase

```
database = DataBase(PARENT_ID, database_name=<str:existing_database_name)
```

* Add Page to DataBase

```
database = DataBase(PARENT_ID, database_name=<str:existing_database_name)
page = Page(database) #new Page object which inherits DataBase object previously created
page.add_row_to_database(row)

"""
row must match database cols format.
ie:

row = [
            
            {'Book Title': 'The Little Prince',
            'Author': 'Antoine de Saint-Exupéry',
            'Type of Element': {'id':"highlight", 'name':'🖍Highlight'},
            'page': 48,
            'Position': "250-260",
            'Highlignted Text': "lorem ipsum ... lorem ipsum ...",
            'Date': "2023-02-01"},

            {'Book Title': 'The Phoenix Project',
            'Author': 'Gene Kim, Kevin Behr, George Spafford',
            'Type of Element': {'id':"marker", 'name':'📑Marker'},
            'page': 70,
            'Position': "50-160",
            'Highlignted Text': "",
            'Date': "2022-06-01"},
            
            {'Book Title': 'The Phoenix Project',
            'Author': 'Gene Kim, Kevin Behr, George Spafford',
            'Type of Element': {'id':"note", 'name':'📝Note'},
            'page': 70,
            'Position': "50-160",
            'Highlignted Text': "lorem ipsum ... lorem ipsum ...",
            'Date': "2022-06-01"}
       ]
```

## Authors

Contributors names and contact info

*Adolfo Armas [@adolfoarmasm](https://twitter.com/adolfoarmasm).

## Version History

* 0.1
    * Initial Release: create DBs and its Pages related to a books anotations. FUTURE: package full decoupled from book anotations application

## Acknowledgments

* [pynotion](https://www.pynotion.com/getting-started-with-python)
