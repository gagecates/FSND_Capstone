# Udacity Full Stack Capstone Project

https://gage-heroku-app.herokuapp.com/
 
This app is a nutritional macro counter. A logged in user can post consumed foods if the food exists in the databse or 
add a food if it does not. Macros can be manually individually posted as well. Once logged in, the user is added to the database and their
macros are tracked and viewable.


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
                    email: usertestmacroapp@gmail.com
                    password: usertestmacroapp
                    
**Admin** (User permissions + edit and delete foods)

Login credentials:
                    email: admintestmacroapp@gmail.com
                    password: admintestmacroapp


Once logged in, you will be redirected to the apps home page. Feel free to check it out from here. 


# Run app locally

Install the necessary requirmenets by running:

```
  pip install -r requirements.txt
```

1. Open a terminal and cd to the project directory and install requirements:
``` 
    cd ~/{ProjectDirectory}
    # Then
    pip install -r requirements.txt
```
2. Create capstone database in psql
'''
    login to psql 
    CREATE DATABASE capstone;
    
''''


3. Set up your DATABASE_URL variable depending on OS:

```
    export DATABASE_URL="{DATABASE_URL}"
```

3. Run ALL three migration commands **ONLY** on you first set up:

``` 
# Run the init command once
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade

# Run the last 2 commands if/when you make changes to database structure
```

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
7. GETj '/food/add'
8. GET '/macros/add'
9. POST '/food/add'
10. GET '/food/new'
11. POST '/food/new'
12. GET '/food/<int:food_id>/edit'
13. POST '/food/<int:food_id>/edit'
14. POST '/food/<int:food_id>/delete'
15. POST '/macros/add'


Index '/'

- Takes user to login page if not logged in.
  render_template('/pages/app_login.html')

- Takes user to app home page if user logged in and session['token'] is available. 
  render_template('/pages/app_home.html', user = session['user'])


Login '/login'

- Gets all the info from a selected restaurant
- <int:id> relpaces the ID of the restaurant you want
- Returns:
    {
        'success': True,
        'restaurants': [{
            "id": self.id,
            "name": self.name,
            "address": self.address
            }]
    }

GET '/restaurants/<int:id>/menu'
- No Authorization required
- Gets the menu items that belong to a restaurnt, could be more than one
- <int:id> replaces the ID of restaurant you want to see the menu items 
- Returns:
    {
        'success': True,
        "items": [{
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "restaurant_name": self.restaurnt_menu_item.name
            }, ...]
    }

POST '/restaurants/<int:id>/reservation'
- Requred Authorization with 'Customer' role
- Posts a reservation for the restaurant with id in <int:id>
- Required input (data type listed inside brackets):
    {
        "time_of_res": (datetime),
        "num_of_people": (int),
        "name_for_res": (string)
    }
- Returns all upcoming reservation for the customer making the reservation:
    {   
        'success': True,
        'upcoming_reservations': [{
            "time_of_res": self.time_of_res,
            "num_of_people": self.num_of_people,
            "restaurant_name": self.restaurant_name,
        }, ...]
        
    }

POST '/restaurants'
- Requred Authorization with 'Restaurant Manager' role
- Restaurant Manager can post their restaurant
- Required input (data type listed inside brackets):
    {
        "name": (string),
        "address": (string)
    }
- Returns all the restaurants that the user owns:
    {
        "success": True,
        "owned_restaurants": [{
            "id": self.id,
            "name": self.name,
            "address": self.address
        }, ...]
    }

PATCH '/restaurants/<int:id>'
- Requred Authorization with 'Restaurant Manager' role, and the Restaurant manager can only PATCH his/her own restaurnat
- Restaurant manager can edit their restaurants. They can edit the name, the address, or both
- Required input (data type listed inside brackets):
    {
        "name": (string),
        "address": (string)
    }
- Returns the the newly updated restaurant with the new information:
    {
        "name": 'NEW NAME',
        "address": 'NEW ADDRESS'
    }


DELETE '/restaurants/<int:id>'
- Requred Authorization with 'Restaurant Manager' role, and the Restaurant manager can only DELETE his/her own restaurnat
- Deletes the restaurant with id replaced by <int:id>
- Returns Response if deletes succesfully:
    {
        "success": True
    }
```

**ERROR HANDLERS**
```bash

Error 422 (Unprocessable)
Returns:
    {
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }

Error 404 (Bad Request)
Returns:
    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

Error 401 (Resource Not Found)
Returns:
    {
        "success": False,
        "error": 401,
        "message": "Unauthorized Error"
    }

Error 400 (Unauthorized Error)
Returns:
    {
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }


```

# Authentication 
 * This app can be run at https://fsnd-happyhour.herokuapp.com/

 * You can securly Sign Up or Log In through Auth0: https://fsnd-happyhour.auth0.com/authorize?audience=fsndcapstone&response_type=token&client_id=rY3ee6xjoWocXP7PkCUouHS48vX9YAoo&redirect_uri=https://fsnd-happyhour.herokuapp.com/login-results


# Testing
* Testing instructions
1. Create a new database for testing (choose and new name ex. _new_testing_db_)
``` bash
    createdb new_testing_db
```
        

2. In **test_app.py** set _database_name_ and _database_path_ from your local machine

3. In the command line run
``` bash
    python test_app.py
```
4. The tests will run and should all be completed sucessfully

# Deployment
This app is deployed on Heroku. For deployment, you need to:

1. Install Heroku CLI and login to Heroku on the terminal

2. create a [setup.sh](setup.sh) file and declare all your variables in the file

3. Install gunicorn
``` bash
    pip install gunicorn
```

4. Create a [Procfile](Procfile) and add the line below. The Procfile instructs Heroku on what to do. Make sure that **your app** is housed in **[app.py](app.py)**
``` bash
    web: gunicorn app:app
```

5. Install the following requirements
``` bash
    pip install flask_script
    pip install flask_migrate
    pip install psycopg2-binary
```       

6. Freeze your requirements in the [requirements.txt](requirements.txt) file
``` bash
    pip freeze > requirements.txt
```   

7. Create Heroku app
``` bash
    heroku create name_of_your_app
```
        
8. Add git remote for Heroku to local repository
``` bash
    git remote add heroku heroku_git_url
``` 

9. Add postgresql add on for our database
``` bash
    heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
```
10. Add all the Variables in Heroku under settings
``` bash
    # This should already exist from the last step
    DATABASE_URL
    # Get these from Auth0
    AUTH0_DOMAIN
    ALGORITHMS
    API_AUDIENCE
```
        
10. Push any changes to your GitHub Repository

11. Push to Heroku
``` bash
    git push heroku master
```      

12. Run Migrations to the Heroku database
``` bash
    heroku run python manage.py db upgrade --app name_of_your_application
```

Visit your Heroku app on the hosted URL!

# Authors
* **Viktor Dojnov** - https://github.com/vdojnov

# Acknowledgments
Special thanks to:
* Kurt Galvin - https://github.com/kurtgalvin
* The Udacity Team!
