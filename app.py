import os
from flask import Flask, request
from db import db
import models

from flask_smorest import abort
import uuid
from resources import item,store
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


#factory pattern t.e factory function for creating the app
def create_app(db_url=None):
    app = Flask(__name__)

    #ako se slucit nekoj exception vnatre  skrien vo nekoj modul primer item.py da go pokazit vo main
    app.config["PROPAGATE_EXCEPTIONS"] = True
    #naslovot kako ke e vo dokumentacijata
    app.config["API_TITLE"] = "Stores REST API"
    #verzijata nie si ja zadavame
    app.config["API_VERSION"] = "v1"
    #OpenApi_Version standard za dokumentacija so yaml
    app.config["OPENAPI_VERSION"] = "3.0.3"
    #OpenApi url prefix mu kazuva na flask-smorest kade e root na APIto
    app.config["OPENAPI_URL_PREFIX"] = "/"
    #documentation config mu kazuva na flasksmorest da go koristi swagger za dokumentacija na apito
    app.config["OPEN_API_SWAGGER_UI_PATH"] = "/swagger-ui"
    #go loadira swagger kodot od ovde
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    #connection to database (sega ja koristime sqlite posle postgre)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    #short config for sqlalchemy
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)

    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app




#probvam nesto
#from flask import render_template
#@app.route("/index")
#def index(name=None):
#    return render_template("index.html",name=name)

