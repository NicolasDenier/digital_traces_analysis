from flask import Flask, url_for

app = Flask(__name__)

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

@app.route('/', methods=["GET"])
def hello_world():
    title="<h1>Hello</h1>"
    details="<p>You are analyzed by Google Analytics</p>"
    button=f"<a href='{url_for('click')}'>click here</a>"
    display=prefix_google+title+details+button
    return display

@app.route('/click', methods=["GET"])
def click():
    return prefix_google+"You have clicked"