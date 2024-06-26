from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_msearch import Search
from config import Config
from dotenv import load_dotenv

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

search = Search(db=db)
search.init_app(app)
search.create_index(update=True)

load_dotenv()

from app import routes, models
