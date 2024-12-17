# :money_with_wings: Account Transfer Task
a small web app using Django that handles fund transfers between two accounts.

## :dizzy: Features
- List all accounts.
- Import accounts fron csv files.
- Get account information.
- Transfer funds between two accounts.

## :computer: Technology Stack

- Backend Framework: Django framework, Django RESTful framework
- Database: SQLite
- Containerization: Docker

## :hammer_and_wrench: Prerequisites

- Docker
- Docker Compose
- python 

## :wrench: Installation
- Clone the project using
```
git clone https://github.com/dohaelsawy/accountTransferTask.git
```
- Navigate to project directory
```py
cd accountTransferTask
```
- Run docker-compose:
```py
make up
```
this command will build and run docker container and establish the project
- Access project's APIs on the following url:
```
http://0.0.0.0:8000/accounts/
```
- Run unit tests using following command:
```py
make test
```
