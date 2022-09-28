import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import ItemModel, StoreModel
from schemas import StoreSchema
#   blueprint in flask_smorest is  used to divide an API into multiple segments


blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

#   GET STORE BY ID
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

#   DELETE STORE BY ID
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Deleting a store is not implemented yet.")





@blp.route("/store")
class StoreList(MethodView):

#   GET ALL STORES
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return None
        #return stores.values()


#   CREATE NEW STORE
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            #uste ne e staveno vo baza ovde
            db.session.add(store)
            #tuka go zacuvuvat vo baza
            db.session.commit()
        except IntegrityError:
            abort(400,message="A store with that name already exists.")

        except SQLAlchemyError:
            abort(500,message="An error occured while inserting the store")

        return store
