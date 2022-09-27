import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

#   blueprint in flask_smorest is  used to divide an API into multiple segments

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

#   GET STORE BY ID
    def get(self,store_id):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404, message="Store not found.")

#   DELETE STORE BY ID
    def delete(self,store_id):
        try:
            del stores[store_id]
            return {"message": f"Store with id {store_id} is deleted."}
        except KeyError:
            abort(404, message="Store not found")




@blp.route("/store")
class StoreList(MethodView):

#   GET ALL STORES
    def get(self):
        return {"stores": list(stores.values())}


#   CREATE NEW STORE
    def post(self):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(400, message="Bad Request. Ensure 'name' is included in the JSON payload.")
        for store in stores.values():
            if (store_data["name"] == store["name"]):
                abort(400, message="Bad Request. Store already exists.")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        print(stores)
        return new_store, 201
