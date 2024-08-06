# LibraryApp
In this work has been implemented electronic library.

## Getting Started

To initialize the project, follow these steps:

1. Clone the repository: `git clone https://github.com/DanilHushchyn/LibraryApp.git .`
2. Ensure you have Poetry installed. 
   You can install Poetry using the following command:
    ```
    pip install poetry
    ```
3. Install the requirements: `poetry install`
4. Copy env sample file: `cp example.env .env`
5. Initialize the project: `make init`
6. Next time you want to start the project, just run `make run`

## Credentials
### Admin 
   - username: admin
   - password: sword123
### Librarian 
   - username: librarian
   - password: sword123
### Visitor 
   - username: librarian
   - password: sword123

## Login Page: 
  - http://127.0.0.1:8000/
   
## Admin Page: 
  - http://127.0.0.1:8000/admin


## API Page: 
  - http://127.0.0.1:8000/api/docs/schema/swagger-ui/

### If you need to refresh db, just run `make fix`