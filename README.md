# Weddify

## Work In Progress ##

### Description ###

Wedding planner website using Django, HTML and Bootstrap.

This website allows user to view and book variety of photography, wedding venue, catering and bridal services. 

Used Django as Backend; HTML, CSS & Javascript as Frontend and PostgreSQL as Database. It also uses an external API for Email Notification which was also built from scratch using Spring boot.

### Installation ###
1. Clone the repository using command "git clone
2. Install Python 3.6.8
3. Install PostgreSQL 10.10
4. Install requirements.txt using command "pip install -r requirements.txt"
5. Create a database in PostgreSQL named "weddify"
6. Create a user in PostgreSQL named "postgres" with password "sparsh"
7. Run command "python manage.py makemigrations" to create migrations for all the apps.
8. Run command "python manage.py migrate" to migrate all the apps.
9. Run command "python manage.py createsuperuser" to create a superuser.
10. Clone this repository for Email Notification API using command "git clone https://github.com/bluehypergiant/Email-Notification-API.git"
11. Install Java 8
12. Modify the file "application.properties" in the Email Notification API repository to update the sender's email and password.
13. Run mvn clean package to build the project.
14. Copy the jar file from the target folder to the Weddify/emailapi folder.
15. Run command "python manage.py runserver" to start the Django server.

### To-Do ###
1. Dockerize
2. Create separate databases for each app
3. Make PayTm integration work
4. Implement update-services feature