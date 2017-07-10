# The Log Analysis Project

This reporting tool will show you reports from the news-database, which you can find in this repository. There are three reports you´ll see:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

--------

## How to start the reporting tool

To start the tool, you should install a virtual machine (VM) on your computer. You should use the vagrant-file stored in this repository to be sure having all the programms you need for running the reporting tool. Also you have to run the tool from the commandline.

After setting up your VM with the command "vagrant up" in the directory with the vagrant file, the database and the tool project.py, you can start your VM by typing "vagrant ssh".
Than: Built up the database "news" by changing into the Postgresql-Mode. Type "psql -d news -f newsdata.sql" into your commandline.
After that, start the reporting tool with the command "python project.py".

-----

## What's under the hood?

In the file project.py you'll find three SQL-Queries, who are handling the three reports. You don't have to do anything to start them one after one. After starting project.py, the three queries will be executed automatically.

------------

## Credits
The database "news" was provided by the Udacity Team.