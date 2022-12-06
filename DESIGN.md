project.db:
This is the SQL database file for clubs, reviews, and users. 
Clubs consists of the club names and logos, which were taken directly from the SOCO website via web scraping. Club logos in the table are represented by the filepath which corresponds to the image locations within this project (the logos are saved in a folder).
Users holds all the user data for registered users so that they can log in once registered. It consists of the user emails, usernames, and password (as a hash of the password).
Reviews holds all of the reviews made by any user logged in to the site. Each entry has the user name and club name, since these must be kept track of in order that each user can only review each club once, and so that we can query all the reviews for a given club. The club review data itself -- numerical ratings for social, workload, and comp difficulty, as well as open text comments -- are also included in this table.

flask: This app runs on flask, much like the Finance PSet. 
sqlite: For SQL queries, we used sqlite (NOT the adapted CS50 library) and as such had to set up the connection and execute statements through sqlite. This was slightly different than using the CS50 library, since in sqlite when you set values using the syntax below, the variables you list after must be wrapped as a tuple, rather than just listing them normally.
VALUES = (?, ?, ?)
Additionally, execute() statements also return tuples and must be indexed in order to get the proper entries, adding a little bit of added difficulty compared to the CS50 way, but working the same way and giving us practice using the standard library.

/register:
Like in finance, the post method of register is meant to submit a form with entered fields such that a new user can be registered. After confirming that all fields are filled and that a Harvard email is being used, we then need to check if the chosen username is taken by querying the SQL database and checking if the chosen name already exists in the database. If it does, then it will not allow the user to register with that name. If there are no issues with any of the fields, then a SQL 
The webpage for register has input fields for the email (type email), username (tyep text), password and password confirmation (both of type password so that they accept text but hide the input as *s)

/login:

/review:
This page is simply a list of all clubs and logos, with a few notable elements. First, there is a search bar on top, which we configured to allow you to search for clubs that contain the text you input into the search bar. We did this using the javascript filter() method which was implemented per the w3schools tutorial at https://www.w3schools.com/howto/howto_js_filter_lists.asp
Basically, if something is typed in, this will show only club names which tontain an occurrence of the text in the filter (using indexof() and confirming that it is > -1). 

Other than this, there are two buttons, review and the q. Review opens the form page, and the q opens the page which serves as our q guide, containing the data of past reviews.

/form:

/theq: