import requests
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from algorithm.image import image_data

from cruddy.query import *

from pathlib import \
    Path  # https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and
# -linux-11a072b58d5f

app_starter = Blueprint('starter', __name__,
                        url_prefix='/starter',
                        template_folder='templates/starter/',
                        static_folder='static',
                        static_url_path='static/assets')


@app_starter.route('/')
def binary():
    return render_template("binary_conversion.html")


@app_starter.route('/greet', methods=['GET', 'POST'])
def greet():
    # submit button has been pushed
    if request.form:
        name = request.form.get("name")
        if len(name) != 0:  # input field has content
            return render_template("greet.html", name=name)
    # starting and empty input default
    return render_template("greet.html", name="World")


@app_starter.route('/binary_login', methods=["GET", "POST"])
def binary_login():
    # obtains form inputs and fulfills login requirements
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password):       # zero index [0] used as email is a tuple
            return redirect(url_for('starter.binary'))

    # if not logged in, show the login page
    return render_template("binary_login.html")


@app_starter.route('/rgb/')
def rgb():
    path = Path(app_starter.root_path) / "static" / "img"
    return render_template('rgb.html', images=image_data(path))


@app_starter.route('/joke', methods=['GET', 'POST'])
def joke():
    """
    # use this url to test on and make modification on you own machine
    url = "http://127.0.0.1:5222/api/joke"
    """
    url = "https://csp.nighthawkcodingsociety.com/api/joke"
    response = requests.request("GET", url)
    return render_template("joke.html", joke=response.json())


@app_starter.route('/jokes', methods=['GET', 'POST'])
def jokes():
    """
    # use this url to test on and make modification on you own machine
    url = "http://127.0.0.1:5222/api/jokes"
    """
    url = "https://csp.nighthawkcodingsociety.com/api/jokes"

    response = requests.request("GET", url)
    return render_template("jokes.html", jokes=response.json())


@app_starter.route('/covid19', methods=['GET', 'POST'])
def covid19():
    url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api"
    headers = {
        'x-rapidapi-key': "dec069b877msh0d9d0827664078cp1a18fajsn2afac35ae063",
        'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    stats = response.json()

    """
    # uncomment this code to test from terminal
    world = response.json().get('world_total')
    countries = response.json().get('countries_stat')
    print(world['total_cases'])
    for country in countries:
        print(country["country_name"])
    """
    return render_template("covid19.html", stats=stats)

@app_starter.route('/life')
def life():
    return render_template("../frontend/templates/frontend/life.html")
