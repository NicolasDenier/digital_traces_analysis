from flask import Flask, redirect, url_for, render_template, url_for, request
from markupsafe import escape # to escape user inputs and so avoid injection attacks
import requests
import json
import subprocess
#subprocess.run(["pip", "install", "pandas"]) # bypass the requirements size limit
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from pytrends.request import TrendReq
import time
from string import punctuation
from collections import Counter
from apscheduler.schedulers.background import BackgroundScheduler

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

def timer_log(function):
    def wrapper(*args):
        start_time = time.time()
        function(*args)
        execution_time = round(time.time()-start_time, 2)
        return execution_time 
    return wrapper

counts_dict = dict()
counter = Counter()

def word_count_using_dict(words):
    global counts_dict
    for word in words:
        if word in counts_dict:
            counts_dict[word] += 1
        else:
            counts_dict[word] = 1

def word_count_using_counter(words):
    global counter
    counter.update(words)

@timer_log # Monitor execution time for this function
def count_occurences(link, count_function):
    # Stream data from link and call a count function for each line
    r = requests.get(link, stream=True)
    for line in r.iter_lines(decode_unicode=True):
        if line:
            # set line to lower case, remove punctuation and split words
            words = line.lower().translate(str.maketrans('', '', punctuation)).split()
            count_function(words)

# Transform a python dict to an HTML table (as string)
def dict_to_table(d):
    table="<table>"
    table+="<tr><th>Word</th><th>Occurences</th></tr>"
    d = dict(sorted(d.items(), key=lambda item: item[1], reverse=True)) # sort by values
    for key, value in d.items():
        table+=f'<tr><td>{key}</td><td>{value}</td></tr>'
    table +="</table>"
    return table

execution_times = [[],[]]
def long_calculations(k):
    global execution_times
    shakespeare_artwork = 'https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt'
    for i in range(k):
        execution_times[0].append(count_occurences(shakespeare_artwork, word_count_using_dict))
        execution_times[1].append(count_occurences(shakespeare_artwork, word_count_using_counter))
        if k != 1:
            counts_dict = dict() # reset dict
            counter = Counter() # reset counter


@app.route('/process_result', methods=["GET"])
def process_result():
    long_calculations(1)
    distribution_0 = dict(Counter(execution_times[0]))
    distribution_1 = dict(Counter(execution_times[1]))
    
    # get values from 2 dicts to a single dataframe to lists
    df0 = pd.DataFrame.from_dict(distribution_0, orient='index', columns=['distribution_0']).reset_index()
    df1 = pd.DataFrame.from_dict(distribution_1, orient='index', columns=['distribution_1']).reset_index()
    df = pd.concat([df0, df1], ignore_index=True, sort=False).groupby(['index']).sum().reset_index()
    labels=df['index'].values.tolist() # list of unique labels in both distributions
    values0=df['distribution_0'].astype('int').values.tolist()
    values1=df['distribution_1'].astype('int').values.tolist()

    return render_template('exec_time_distribution.html', labels=labels, values0=values0, values1=values1)

@app.route('/timer', methods=["GET"])
def timer():
    global execution_times
    execution_times = [[],[]] # reset execution_times on page reload
    long_calculations(1)
    mean_times = list(map(lambda x: round(sum(x)/len(x),2), execution_times))
    return prefix_google+render_template('timer.html', execution_times=mean_times, table=dict_to_table(counts_dict))

if __name__ == "__main__":
    '''scheduler = BackgroundScheduler()
    scheduler.add_job(random_num, "interval", seconds=10)
    scheduler.start()
    '''
    app.run()