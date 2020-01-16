from flask import Flask, redirect, url_for, request
from flask_dance.consumer import OAuth2ConsumerBlueprint

from config import FLASK_SECRET_KEY, OKTA_BASE_URL, OKTA_CLIENT_ID, OKTA_CLIENT_SECRET

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

okta_blueprint = OAuth2ConsumerBlueprint(
    name='okta',
    import_name=__name__,
    client_id=OKTA_CLIENT_ID,
    client_secret=OKTA_CLIENT_SECRET,
    base_url=OKTA_BASE_URL,
    token_url=f'{OKTA_BASE_URL}/token',
    authorization_url=f'{OKTA_BASE_URL}/authorize',
    scope=['openid', 'email', 'profile'],
    # by default a login redirects to the root page
)

app.register_blueprint(okta_blueprint, url_prefix='/login')


@app.before_request
def before_request_func():
    if not okta_blueprint.session.token and request.endpoint not in ['okta.login', 'okta.authorized']:
        return redirect(url_for('okta.login'))


@app.route('/')
@app.route('/user')
def index():
    resp = okta_blueprint.session.get(f'{OKTA_BASE_URL}/userinfo')
    email = resp.json()['email']
    return f'You are logged in as {email}'

