# sqlite viewer
A little python script for running a query against a sqlite database and printing the results.

Created because I got tired of this mess:

![sqlite3](images/sqlite3.png)

and this mess:

![litecli](images/litecli.png)

here's what it looks like:
![sqlite-viewer](images/sqlite-viewer.png)

It's very simple (and dumb). It wraps the text in the column with the longest
values, so all of the columns stay vertically align in the output.

## setup
The .py script has a hashbang, so you can symlink it to somewhere on your path like follows:

    $ ln -s ./sqlite-viewer.py ~/.local/bin/sql
    $ chmod +x ~/.local/bin/sql

then you can run it like so:

    $ sql example.db "select * from data"

## usage
Simple usage to run a query against a database:

    sql database command

This will return up to 25 rows. If you need to see more, use `LIMIT` with an `OFFSET`.

I've included the example database from the above screenshots, for testing/playing around purposes.

## counting
I find myself writing queries to count the number of values in a set of columns a lot, so I've included a parameter that can build these queries for you:

    sql database -count table:columns

For example, I have a database containing all of my nginx access logs. If I want to see which URLs are most frequently accessed and by which HTTP method, I can do this:

    $ sql logs.db -count logs:request,method
    request                      method  count  
    /                            GET     14660  
    /robots.txt                  GET     5503
    ...

which will expand to this query:

    SELECT request, method count(1) AS count
    FROM logs
    GROUP BY request, method
    ORDER BY count(1) DESC
