# Flask Okta


## Hello World Flask App

The first step of developing a Flask App authenticating with Okta is to create
a little Flask App. The simplest to start with is the "Hello World" application.

I create the app in a file called `app.py` to which I copy the following code:

```python
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

```

In addition I create  file called `reqirements.txt` and add the following line:

```requirements.txt
flask==1.1.1
```

To start the app I can simply execute:

```
flask run -h localhost -p 8080
```

## Okta Developer Account

A developer account can be created 
at [https://developer.okta.com/](https://developer.okta.com/).

The next step is to create an Application in the Applications 
tab of the Okta developer page. 

I specified a host and a port when starting my flask application. 
This host and port is now used to create my application in the Developer Account.

```
Base URIs: http://localhost:8080/
Login redirect URIs: http://localhost:8080/login/okta/authorized
Logout redirect URIs: http://localhost:8080
Group Assignment: Everyone
Grant Type: Authorization Code
```

The following page can help to decide for a grant type: 
https://developer.okta.com/docs/concepts/auth-overview/

As a result a Client ID and Secret are generated. 


## Adding Okta to the Flask App

We have to set a few environment variables for the flask app to consume.
These can be found in .env.example.

Please create an env file based on .env.example and set your variable. 

- *FLASK_APP=app.py* 
- *FLASK_SECRET_KEY=* generated before deployment (see below)
- *OAUTH_CLIENT_ID=* provided by okta
- *OAUTH_CLIENT_SECRET=* provided by okta
- *OKTA_BASE_URL=* provided by okta e.g. dev-example.okta.com/oauth/default
- *OAUTHLIB_INSECURE_TRANSPORT=true* deactivates TSL for development, do not use this in production

The flask secret key is used for signing cookies cryptographically. 
https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions

I access the environment variables in `config.py` to later import them in `app.py`.

Then I go back to the application itself and modify it to use Okta.
The key lines are the following:

```
okta_blueprint = OAuth2ConsumerBlueprint(
    name='okta',
    import_name=__name__,
    client_id=OKTA_CLIENT_ID,
    client_secret=OKTA_CLIENT_SECRET,
    base_url=OKTA_BASE_URL,
    token_url=f'{OKTA_BASE_URL}/token',
    authorization_url=f'{OKTA_BASE_URL}/authorize',
    scope=['openid', 'email'],
    # by default a login redirects to the root page
)

app.register_blueprint(okta_blueprint, url_prefix='/login')
```

Then for any route to ensure authentication we need to add the follwoing lines:

```
    if not okta_blueprint.session.token:
        return redirect(url_for('okta.login'))
```

## Be Authenticated for Every Route

Instead of checking the token manually for every route, we can use flasks
`before_request` function. The only thing we need to do is excluding 
the endpoints 'okta.login' and 'okta.authorized' that are used during the login 
process from the redirect.