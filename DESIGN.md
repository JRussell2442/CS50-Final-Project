Clubs.csv is a list of club names and logos, taken via web scraping from the SOCO website. 
images are the custom images we used for our site (our logo), and logos are the club logos from the SOCO website, taken via web scraping.

project.db:
This is the SQL database file for clubs, reviews, and users. 
Clubs consists of the club names and logos in Clubs.csv. Club logos in the table are represented by the filepath which corresponds to the image locations within this project (the logos are saved in a folder).
Users holds all the user data for registered users so that they can log in once registered. It consists of the user emails, usernames, and password (as a hash of the password).
Reviews holds all of the reviews made by any user logged in to the site. Each entry has the user name and club name, since these must be kept track of in order that each user can only review each club once, and so that we can query all the reviews for a given club. The club review data itself -- numerical ratings for social, workload, and comp difficulty, as well as open text comments -- are also included in this table.

flask: This app runs on flask, much like the Finance PSet. 
sqlite: For SQL queries, we used sqlite (NOT the adapted CS50 library) and as such had to set up the connection and execute statements through sqlite. This was slightly different than using the CS50 library, since in sqlite when you set values using the syntax below, the variables you list after must be wrapped as a tuple, rather than just listing them normally.
VALUES = (?, ?, ?)
Additionally, execute() statements also return tuples and must be indexed in order to get the proper entries, adding a little bit of added difficulty compared to the CS50 way, but working the same way and giving us practice using the standard library. Also, we must use .commit() to save changes to the database whenever we update it.

layout.html:
This is the page extended by most pages in the website. It contains the background image as well as the navbar and other global attributes such as the website title and logo.

/register:
Like in finance, the post method of register is meant to submit a form with entered fields such that a new user can be registered. After confirming that all fields are filled and that a Harvard email is being used, we then need to check if the chosen username is taken by querying the SQL database and checking if the chosen name already exists in the database. If it does, then it will not allow the user to register with that name. If there are no issues with any of the fields, then a SQL INSERT query will add the registered user (email, username, password via hash) into the database

The webpage for register has <input> fields for the email (type email), username (tyep text), password and password confirmation (both of type password so that they accept text but hide the input as *s). The register button is a submit button for these fields.

/login:

The login webpage is very closely related to the register page. In terms of the webpage, we now only need the username and password fields, and a login button as our new submit button. 

The login in app.py first checks that the username is in the query. If the user does exist, then it will check that this password matches the one corresponding to that username in the database. If we pass these two checks, then we are successful. We can store our user's name in session["user_id"] so that the form page can use it, and then we can redirect our user to the full website. 

/review:
This page is simply a list of all clubs and logos, with a few notable elements. First, there is a search bar on top, which we configured to allow you to search for clubs that contain the text you input into the search bar. We did this using the javascript filter() method which was implemented per the w3schools tutorial at https://www.w3schools.com/howto/howto_js_filter_lists.asp
Basically, if something is typed in, this will show only club names which tontain an occurrence of the text in the filter (using indexof() and confirming that it is > -1). 

Other than this, there are two buttons, review and the q. Review opens the form page, and the q opens the page which serves as our q guide, containing the data of past reviews.
The app.py function merely sends the club data to this page to be displayed, using the get_clubs() and get_images() we implemented based on a csv file of our data.

/form:

The form page, linked to the review button, will prompt you to fill out a q guide style club review for the club you clicked on. You can choose numerical ratings for social, workload, and comp difficulty ranging from 1-5 through a <select> form, and you can input a comment through a text <input> field. There is a submit button to submit the form, which will only work if you have filled out all necessary fields. Using session["user_id"] from the login form, we check if the user has already filled out a review for this club. If they have, we will take the data they input and update (replace) their existing review with the new one through an UPDATE query. If they have not reviewd it yet, we will add their review through the INSERT query. 

/theq:

The webpage displays the same stats that the review form contains, except now it is the average of all reviews from all users. The comments listed are from all users. This is a summary of the type of data you would see in the q guide for a class. 

The /theq in app.py queries the average values for all the fields in reviews via sqlite, showing "no reviews" and "no comments" if none have been added for that club. The club, review averages, and comments are sent to the webpage for display.

/logout:
Simply logs the user out in the same way implemented in the Finance PSet.