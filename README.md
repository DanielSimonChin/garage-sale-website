# dw-prj2-grp5-Chin
Project 2: Website django development

Heroku website URL : https://vente-de-garage.herokuapp.com/

The project contains 4 sub apps:

1.database: contains the models that will be used in other apps (User, Item, Comment, Reply)

2.authentication: relates to every action that requires a user authentication such as login, logout, register, updating an item, creating an item listing, etc.
  contains the static folder which holds the css and static image files that are uploaded by the user.

3.blog: contains the views for users to comment, reply and like a selected item. Only authenticated users can comment and reply as many times as they please.
  A authenticated user can only like an item once, if a user likes an item a second time, nothing happens.

4.itemManagement: contains the forms and views and templates relating to user's interaction with items on the website. Has the Index view with all items, the detail view of every 
  item, item creation, item updating, item deletion, and item purchase.

Admin functionality: 

The heroku website contains 5 customers, 2 regular admins and 1 super user.

Administrative users who are logged in will have an "Admin" button on the website's NAV bar which brings them directly to the admin page.
Customers cannot access the admin page.

What the user sees will vary depending on the authentication privileges and if the user is logged in or not. Visitors who aren't logged in 
cannot do anything but view items.

Users can set a profile image in the "Account" NAV page. Users can also change their passwords in the Account page by clicking on the "Change Password" button.

Users begin with a default $1000 dollars and will be presented with a message page if they do not have sufficient funds to buy an item.

The app contains a filtering feature where users can search for items by title (case-insensitive) and filtering by Most recent, oldest, most popular, liked owned items.

The created accounts for the website are in "heroku website users.txt" that is in the root of the project.



