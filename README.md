# Admin-Portal


# Installation:
1. sudo apt-get install mysql-server
2. apt-get install python-dev
3. sudo apt-get install libmysqlclient-dev
4. pip install flask_mysqldb
5. pip install wtforms
6. pip install passlib


# *create database*
 1. mysql -u root -p 
 2. (set password to 'root')
 3. create database myflaskapp;
 4. mysql -u root -proot myflaskapp < admin_backup.sql
