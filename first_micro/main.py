from flask import Flask, redirect, url_for, render_template, url_for, request
from markupsafe import escape # to escape user inputs and so avoid injection attacks
import requests
import json
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from pytrends.request import TrendReq

app = Flask(__name__)
app.config.from_pyfile('settings.py')

flow = None

def create_keyfile_dict():
    variables_keys = {
        "web":{
        "client_id": app.config.get("CLIENT_ID"),
        "project_id": app.config.get("PROJECT_ID"),
        "auth_uri": app.config.get("AUTH_URI"),
        "token_uri": app.config.get("TOKEN_URI"),
        "auth_provider_x509_cert_url": app.config.get("AUTH_PROVIDER_X509_CERT_URL"),
        "client_secret": app.config.get("CLIENT_SECRET")
        }
    }
    return variables_keys


def ga_auth(scopes):
    global flow
    auth_url="/"
    try:
        flow = InstalledAppFlow.from_client_config(create_keyfile_dict(), scopes)
        flow.redirect_uri = 'https://lhkxlc.deta.dev/cookies'
        auth_url, _ = flow.authorization_url(prompt='consent')
        print('Please go to this URL: {}'.format(auth_url))
    except Exception as e:
        print('exception')
        print(e)

    return '{}'.format(auth_url)


prefix_google="""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-250950402-1"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'UA-250950402-1');
    </script>

    """
user_input=""

@app.route('/', methods=["GET"])
def home():
    display=prefix_google+render_template('home.html')
    return display

@app.route('/click', methods=["GET"])
def click():
    return prefix_google+"You have clicked"

@app.route('/logger', methods=["GET", "POST"])
def logger():
    global user_input
    print('This is a log from python')
    if request.method == 'POST':
        user_input=escape(request.form.get("user_input")) + '\n' + user_input
    return prefix_google+render_template('logger.html', text=user_input)


@app.route('/cookies/auth', methods=["GET"])
def auth():
    scopes = ['https://www.googleapis.com/auth/analytics.readonly']
    auth_url = ga_auth(scopes)
    return redirect(auth_url)


@app.route('/cookies/', methods=["GET"])
def cookies():
    code = escape(request.args.get('code', None))
    #state  = request.args.get('state', None)
    flow.fetch_token(code=code)
    return redirect(url_for('visitors'))


@app.route('/cookies/visitors', methods=["GET"])
def visitors():
    google_cookies = "Unable to get cookies"
    try:
        req = requests.get("https://www.google.com/")
        google_cookies = req.cookies.get_dict()
        google_cookies = str(json.dumps(google_cookies, indent=2))

        service = build('analytics', 'v3', credentials=flow.credentials)
        results = service.data().ga().get(
            ids='ga:' + app.config.get("VIEW_ID"),
            start_date='30daysAgo',
            end_date='today',
            metrics='ga:users'
            ).execute()
        number_users = results['totalsForAllResults']['ga:users']
    except Exception as e:
        print('exception')
        print(e)
    display=prefix_google+render_template('cookies.html', google_cookies=google_cookies, number_users=str(number_users))
    return display


@app.route('/trends/', methods=["GET"])
def trends():
    pytrends = TrendReq(hl='fr-FR') # french language
    #suggestions = pd.DataFrame(pytrends.suggestions(keyword='Cookie'))
    kw_list = ["/m/021mn","/m/0d18sk"] # Cookie (food), Cookie (web)
    cat = '0' 
    timeframe ='today 3-m'
    geo = '' # worldwide
    gprop = '' # websearch
    pytrends.build_payload(kw_list,cat,timeframe,geo,gprop)
    data = pd.DataFrame(pytrends.interest_over_time()).reset_index()
    data = data.rename(columns={"/m/021mn": "food", "/m/0d18sk": "web"})

    return prefix_google+render_template('trends.html', labels=data["date"], values1=data["food"], values2=data["web"])