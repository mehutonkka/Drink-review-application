# Drink review application
Ideas:
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

Browsing option to browse drinks and the possibility to change the order by alphabetically, price, best score, etc.

Search system to find drinks based on their name or category.

Possibility to find all reviews made by a certain user.

Top 10 list of the best-scoring drinks.

Top 5 list of contributors who have made the most reviews.

Admin to control reviews and other information.


Current status:
- Almost all functionalities are working
- Still need to make sure that users can only put acceptable inputs
- All of the styling must be done
- Code must be made more clean/efficient


New changes:
- Made the whole website look more pleasant
- Divided things into columns
- Changed href link colors
- Added href links to all occurences of drink names and usernames
- Made different classes into base.html
- Coded a functionality into base.html that makes sure that on smaller screens like mobile screens, the columns go over eachother and not to the side
- Other small alterations to styling
