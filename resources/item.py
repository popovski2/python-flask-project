import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel,StoreModel
from schemas import ItemSchema, ItemUpdateSchema

#   blueprint in flask_smorest is  used to divide an API into multiple segments


blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):

#   GET ITEM BY ID
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

#   DELETE ITEM BY ID
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item deleted"}


#   UPDATE ITEM BY ID
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id,**item_data)

        db.session.add(item)
        db.session.commit()

#==========================================ITEM LIST================================
@blp.route("/item")
class ItemList(MethodView):

#   GET ALL ITEMS
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()


#   CREATE NEW ITEM
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema(many=True))
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            #uste ne e staveno vo baza ovde
            db.session.add(item)
            #tuka go zacuvuvat vo baza
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occured while inserting the item")

        return item