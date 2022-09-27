import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items,stores
from schemas import ItemSchema, ItemUpdateSchema

#   blueprint in flask_smorest is  used to divide an API into multiple segments


blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):

#   GET ITEM BY ID
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            return abort(404, message="Item not found.")


#   DELETE ITEM BY ID
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": f"Item with id {item_id} is deleted."}
        except KeyError:
            abort(404, message="Item not found")


#   UPDATE ITEM BY ID
    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        try:
            # mojt vaka
            # items[item_id]["name"] = item_data["name"]
            # items[item_id]["price"] = item_data["price"]
            # a mojt i vaka
            item = items[item_id]  # go zemam od db
            item |= item_data  # site values vo item_data gi zamenvet values vo item
            return item
        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):

#   GET ALL ITEMS
    def get(self):
        return {"items": list(items.values())}


#   CREATE NEW ITEM
    @blp.arguments(ItemSchema)
    def post(self, item_data):

        for item in items.values():
            if (item_data["name"] == item["name"]
                    and item_data["store_id"] == item["store_id"]):
                abort(404, message=f"Item already exists")

        if item_data["store_id"] not in stores:
            return abort(404, message="Store not found for this item.")

        item_id = uuid.uuid4().hex
        # vaka ako ne sakame da go prikazime negovoto id
        # new_item = {**item_data}

        new_item = {**item_data, "id": item_id}
        items[item_id] = new_item
        return new_item, 201

