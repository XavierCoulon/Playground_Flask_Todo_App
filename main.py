import os
from flask import Flask
from dotenv import load_dotenv
from views import views

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.register_blueprint(views, url_prefix='/')

if __name__ == "__main__":
	app.run(debug=True)
