import requests
import json
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
			todos = response.json()
			return render_template("todos.html", todos=todos)
	return render_template("index.html")

@views.route('/todos/<int:id>', methods=["GET", "POST"])
def update(id):
	jwt_token = request.cookies.get("jwt_token")
	if jwt_token:
		headers = {"Authorization": "Bearer {}".format(jwt_token)}
		response = requests.get(f"http://localhost:8000/todos/{id}", headers=headers)
		if response.status_code == 200:
			todo = response.json()
			print(todo)
			
		
		if request.method == "POST":
			title = request.form.get("title")
			description = request.form.get("description")
			priority = request.form.get("priority")
			complete = bool(request.form.get("complete"))
			category_id = request.form.get("category_id")
			payload = json.dumps({"title": title, "description": description, "priority": priority, "complete": complete, "category_id": category_id})
			response = requests.put(f"http://localhost:8000/todos/{id}",headers=headers, data=payload)
			if response.status_code == 200:
				flash("Todo saved!", category="success")
				return redirect(url_for("views.todos"))

			else:
				flash("Error...", category="error")
	
	return render_template("update.html", todo=todo)

@views.route('/todos/create', methods=["GET", "POST"])
def create():
	jwt_token = request.cookies.get("jwt_token")
	if jwt_token:
		headers = {"Authorization": "Bearer {}".format(jwt_token)}
		if request.method == "POST":
			title = request.form.get("title")
			description = request.form.get("description")
			priority = request.form.get("priority")
			complete = bool(request.form.get("complete"))
			category_id = request.form.get("category_id")
			payload = json.dumps({"title": title, "description": description, "priority": priority, "complete": complete, "category_id": category_id})
			response = requests.post(f"http://localhost:8000/todos/",headers=headers, data=payload)
			if response.status_code == 200:
				flash("Todo created!", category="success")
				return redirect(url_for("views.todos"))

			else:
				flash("Error...", category="error")
	
	return render_template("create.html")


@views.route('/todos/delete/<int:id>')
def delete(id):
	jwt_token = request.cookies.get("jwt_token")
	if jwt_token:
		headers = {"Authorization": "Bearer {}".format(jwt_token)}
		response = requests.delete(f"http://localhost:8000/todos/{id}", headers=headers)
		if response.status_code == 200:
			flash("Todo deleted!", category="success")
			return redirect(url_for("views.todos"))
	return "Error"


@views.route("/logout")
def logout():
	jwt_token = request.cookies.get("jwt_token")
	if jwt_token:
		flash("Logged out!", category="success")
		response = make_response(render_template('index.html'))
		response.delete_cookie('jwt_token')
		return response
	flash("You were not logged in...", category="error")
	return render_template('index.html')



@views.route('/login', methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		response = requests.post("http://localhost:9000/users/token", data={"username": email, "password": password})
		
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
