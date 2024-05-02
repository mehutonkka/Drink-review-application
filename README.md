# Drink review application
Test the application with fly.io:
https://beverage-reviews.fly.dev/

An application for publishing reviews and scores on different **alcoholic drinks**.

User creation and login to keep track of reviews and restrict one review/score per person on each drink. Also to bind reviews to distinct users.

Without login/signup one can only read the reviews but not publish their own.

Review and score giving function and possibility to edit one's review and score afterward.

**Drinks are categorized** based on their type(beer, long drink, seltzer, etc).

**Function to add new drinks** that do not yet appear on the application.

Information about each drink: 
- name
- average score (for example 7/10)
- alcohol percentage
- category
- price
- store(s) from which can be found
- all reviews listed

Browsing option to browse all drinks.

Search system to find drinks based on their name and/or category.

Possibility to find all reviews made by a certain user.

Top 10 list of the best-scoring drinks.

Top 5 list of contributors who have made the most reviews.

Most recent reviews and drinks listed on home page.

Admin to control reviews and other information (only one admin for now).


Current status:
- All functionalities are working as intended
- Code must be made more clean/efficient
- Some styling to be done still


New changes:(these changes do not yet appear on the fly.io website)
- On the give review page users old review and score is shown in the fields so that editing them is easier. If user has not already reviewed the beverage it will show as blank and 1 as a selected score.


