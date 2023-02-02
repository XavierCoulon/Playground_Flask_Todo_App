import requests
from flask import Blueprint, render_template, request, redirect, flash, url_for, make_response
views = Blueprint('views', __name__)

@views.route('/')
def home():
	return render_template("index.html")

@views.route('/todos')
def todos():
	jwt_token = request.cookies.get("jwt_token")
	if jwt_token:
		headers = {"Authorization": "Bearer {}".format(jwt_token)}
		response = requests.get("http://localhost:8000/todos", headers=headers)
		if response.status_code == 200:
			print(response.json())
			todos = response.json()
	
	return render_template("todos.html", todos=todos)


@views.route('/login', methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		response = requests.post("http://localhost:9000/users/token", data={"username": email, "password": password})
		response_data = response.json()
		
		if response.status_code == 200:
			flash("Logged in!", category="success")
			jwt_token = response.json()['token']
			resp = make_response(redirect(url_for("views.home")))
			resp.set_cookie('jwt_token', jwt_token)
			return resp
		flash("Credentials incorrect...", category="error")
	
	return render_template("login.html")

@views.route('/signup', methods=["GET", "POST"])
def signup():
	if request.method == 'POST':
		email = request.form.get('email')
		password1 = request.form.get('password1')

		response = requests.post("http://localhost:9000/users/", data={"email": email, "password": password1})
		response_data = response.json()
		print(response_data)
		flash("Account created!", category="success")
		return redirect(url_for("views.home"))
		
	return render_template("signup.html")
