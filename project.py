# -*- coding: utf-8 -*-
import psycopg2

# Initialize the connection to the database, defining the cursor
conn = psycopg2.connect(database="news")
cursor = conn.cursor()


# First report - What are the most popular three articles of all time?
# for this exercise I join the articles-table with an virtual table
# created by a subselect. In the subselect (alias counter), I group the single
# articles by the number of views

query1 = """
SELECT CONCAT ('"', articles.title, '" - ', counter.number_views, ' views')
FROM articles
JOIN (
        SELECT path, COUNT (*) AS number_views
        FROM log GROUP BY path ORDER BY number_views DESC) counter
ON articles.slug = replace (counter.path, '/article/', '') LIMIT 3
"""


# Second report - Who are the most popular article authors of all time?
# For this exercise, I used some virtual tables via subselects.
# First I grouped the articles with "STATUS OK" by their number of views (alias
# tab1).
# Then I joined tab1-table with another table from a subselect (alias tab2),
# where I joined the articles-table with tab1 - and with the table authors,
# to get the full names of the authors.
# At the end I grouped the name of the author by all the views of their
# articles, the highest number on top

query2 = """

SELECT CONCAT (tab2.name, ' - ', SUM(tab2.number), ' views')
FROM (
        SELECT author, slug, tab1.views as number, authors.name AS name
        FROM articles
        JOIN (
                SELECT replace(path, '/article/', '') AS path,
                COUNT (*) AS views FROM LOG GROUP BY path, status
                HAVING status = '200 OK'
                ) tab1
        ON tab1.path = articles.slug
        JOIN authors ON articles.author = authors.id
        ) tab2
GROUP BY tab2.name
ORDER BY SUM(tab2.number) DESC
"""


# Third report - On which days did more than 1% of requests lead to errors?
# Here I also used some subselects as virtual tables.
# First I joined two tables into one (alias tab3), tab1 with all the requests
# of every single day,
# tab2 with the requests of every day, that leaded to an error.
# In tab4 I calculated the percent-rate of error-requests.
# At the end, I printed out the results with a CONCAT-command, taking all
# results, where the error-percent-rate is higher than 1.

query3 = """
SELECT CONCAT (tab4.date, ' - ',
ROUND(tab4.percent_negative_requests, 2), ' % errors')
FROM (
        SELECT tab3.date as date, (tab3.log_negative/tab3.all_logs*100)
        AS percent_negative_requests FROM (
                SELECT tab2.daate as date,
                CAST (tab2.loogins AS DECIMAL (10,5)) AS log_negative,
                CAST (tab1.logins AS DECIMAL (10,5)) AS all_logs
                FROM (
                        SELECT To_Char (time, 'fmMonth DD,YYYY') as date,
                        COUNT (*) as logins FROM log GROUP BY date
                     ) tab1
                LEFT JOIN (
                        SELECT To_Char (time, 'fmMonth DD,YYYY') as daate,
                        status, COUNT (*) as loogins FROM log
                        GROUP BY daate, status HAVING status = '404 NOT FOUND'
                     ) tab2
                ON tab1.date = tab2.daate
        ) tab3
) tab4
WHERE tab4.percent_negative_requests > 1
"""

# building a for loop to run all the queries. For that, I put the queries
# into a query_list. Also I give a statement to the user, that the code is
# working on the request.
query_list = [query1, query2, query3]
for query in query_list:
    print("\nSQL-operation in progress... please wait!\n")
    cursor.execute(query)
    results = cursor.fetchall()
    for article in results:
        for elem in article:
            print (elem)
    print("\n\n")

# At the end I am closing the connection
conn.close()
