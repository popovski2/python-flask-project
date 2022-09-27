from flask import Flask, request
from db import items, stores
from flask_smorest import abort
import uuid
from resources import item,store
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from flask import g, current_app

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


api = Api(app)
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)



#probvam nesto
from flask import render_template
@app.route("/index")
def index(name=None):
    return render_template("index.html",name=name)

