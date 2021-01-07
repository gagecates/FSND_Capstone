# Udacity Full Stack Capstone Project

https://gage-heroku-app.herokuapp.com/
 
This app is a nutritional macro counter. A logged in user can post consumed foods if the food exists in the databse or 
add a food if it does not. Macros can be manually individually posted as well. Once logged in, the user is added to the database and their
macros are tracked and viewable.

# Motivation Behind Project

I chose to do this topic for my fullstack capstone project for a few reasons. 
It was a great way to showcase all that this course has taught me. 
The macro app utilizes the REST API while allowing my to sharpen my skills and interest in full stack development.
Taking personal interest in nutrition and thus the application makes it that much more enjoyable and applicable.


# The Stack
* [Python 3.8.2]
* [Flask - Web Framework]
* [SQLAlechmy ORM]
* [PostgresSQL 12.2]
* [Flask - Migrate]
* RESTful - API
* Authentication - JSON Web Token (JWT) with [Auth0](auth0.com)
* Python virtual environment - [venv]
* Unittest - Flask
* API testing with [Postman]
* Deployment on [Heroku]

# Run on Heroku

Navigate to the login page https://gage-heroku-app.herokuapp.com/

Press login and you will get the Auth0 login window. For full access to the app there are currently
two user/permissions configured. Copy and use the credentials for whichever you would like to explore with. 

**User** (Post consumed foods, post macros manually, add new food to database, view personal macro breakdown)

Login credentials:
```
    email: usertestmacroapp@gmail.com
    password: Usertestmacroapp!
```
                    
**Admin** (User permissions + edit and delete foods)

Login credentials:
```
    email: admintestmacroapp@gmail.com
    password: Admintestmacroapp!
```

Once logged in, you will be redirected to the apps home page. Feel free to check it out from here. 


# Run locally

Install the necessary requirmenets by running:

```
    pip install -r requirements.txt   
```

1. Open a terminal and cd to the project directory and install requirements:
``` 
    cd ~/{ProjectDirectory}
```
# Then
    
```
    pip install -r requirements.txt
```
2. Create capstone database in psql
```
    psql CREATE DATABASE capstone;
```


3. Set up your DATABASE_URL variable depending on OS:

```
    export DATABASE_URL="{DATABASE_URL}"
```

3. Run ALL three migration commands **ONLY** on you first set up:
 
# Run the init command once
```
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
```

# Run the last 2 commands if/when you make changes to database structure


4. Set up FLASK_APP variable depending on OS:
```
    export FLASK_APP=app.py
```

5. To run the app use:
```
    flask run  
```

* By default, the app will run on http://127.0.0.1:5000/ 

# Endpoints and Error Handlers

**ENDPOINTS**

1. Index '/'
2. Login '/login'
3. Callback '/callback'
4. Logout '/logout'
5. GET '/foods'
6. GET '/macros'
7. GET '/food/add'
8. GET '/macros/add'
9. POST '/food/add'
10. GET '/food/new'
11. POST '/food/new'
12. GET '/food/<int:food_id>/edit'
13. POST '/food/<int:food_id>/edit'
14. POST '/food/<int:food_id>/delete'
15. POST '/macros/add'


Index '/'

- Takes user to login page if not logged in 
- return render_template('/pages/app_login.html')

- Takes user to app home page if user logged in and session['token'] is available 
- return render_template('/pages/app_home.html', user = session['user']))

Login '/login'

- Takes you to Auth0's login window
- Redirects to the callback URL after succesful login


Callback '/callback'

- Revieves the JWT from Auth0 and creates a session['user'] key from the username in the token
- Brings user to the home page and if the user is not currently in the database, adds them
- return render_template('pages/app_home.html', user = session['user'])


Logout '/logout'

- Clears the flask session which clears the session['user'] key
- Redirects user to login page
- return render_template('/pages/app_login.html')


GET '/food'

- Requires user permissions
- Gets all foods in food table as paginated
- Takes user to food page with a list of all foods
- return render_template('/pages/foods.html', foods = paged_foods)


GET '/macros'

- Requires user permissions
- Gets logged in users macros
- Takes user to macro page with the breakdown of each
- return render_template('pages/macro.html', user = user, username = username)


GET '/food/add'

- Requires user permissions
- Takes user to post food form page
- return render_template('forms/post_food.html', form=form)


GET '/macros/add'

- Requires user permissions
- Takes user to post macros form page
- return render_template('forms/post_macros.html', form=form)


POST '/food/add'

- Requires user permissions
- Post foods a user consumed 
- If food is in database it adds the foods macros to the users macros
- If food is not in database, promps user to add the food first
- return render_template('/pages/macro.html', user= user)


GET '/food/new'

- Requires user permissions
- Takes user to new food form page
- return render_template('forms/new_food.html', form=form)


POST '/food/new'

- Requires user permissions
- Post new foods to database
- If food is in database it promps user that it already exists
- return render_template('/pages/macro.html', user= user)
- returns to food page of listed foods
- return render_template('/pages/foods.html', foods = paged_foods)


GET '/food/<int:food_id>/edit'

- Requires admin permissions
- Takes user to edit food form page after clicking on edit button below food
- return render_template('forms/edit_food.html', form=form, food = food.food)


POST '/food/<int:food_id>/edit'

- Requires admin permissions
- Edits selected food via food_id and updates food in database
- Returns user to food page with updated list
- return render_template('/pages/foods.html', foods = paged_foods)


POST '/food/<int:food_id>/delete'

- Requires admin permissions
- Deletes selected food via food_id and updates food database
- Returns user to food page with updated list
- return render_template('/pages/foods.html', foods = paged_foods)



POST '/macros/add'

- Requires user permissions
- Adds entered macros to current session['user']'s macros and updates table
- Returns user to the macro page to view the updated data
- return render_template('/pages/macro.html', user= user)


```

**ERROR HANDLERS**
```

Error 422
Returns:
    {
      "success": False,
      "error": 422,
      "message": "unprocessable"
    } 422

Error 404
Returns:
    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    } 404

Error 400
Returns:
    {
        "success": False,
        "error": 400,
        "message": "Bad Request"
    } 400
    
Error AuthError
    {
        "success": False,
        "error": AuthError.status_code,
        "message": AuthError.error['description']
    }AuthError.status_code


```


# Testing
* Testing instructions
1. Create a new database for testing (choose and new name ex. _new_testing_db_)
``` 
    psql CREATE DATABASE new_testing_db;
```
        

2. In .env file, set the TEST_DATABASE_URL variable to the new_testing_db name

3. In the command line run
```
    python test_app.py
```
4. The tests will run and should all be completed sucessfully

