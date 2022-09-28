from db import db
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort

from models import TagModel,StoreModel,ItemModel, ItemTags
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags","tags", description="Operations on tags")

#   store/store_id/tag
@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):

    #   get all the tags from store with store_id1
    @blp.response(201,TagSchema(many=True))
    def get(self,store_id):
        #get tags from particular store
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    #   create a tag in store with store_id
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self,tag_data, store_id):

        tag = TagModel(**tag_data,store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


#   tag/tag_id
@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):

    #   get information about tag with tag_id
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag



    @blp.response(202,
                  description="Deletes a tag if no item is tagged with it.",
                  example={"message":"Tag deleted."}
                  )
    @blp.alt_response(404,
        description="Tag not found"
    )
    @blp.alt_response(400,
                description="Returned if the tag is assigned to one or more items. In this case the tag is not deleted."
    )
    def delete(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        #if the tag is not linked with items
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag deleted."}
        else:
            abort(400,message="Could not delete tag. Make sure tag is not associated with any items, then try do delete.")






# linking tags to items and unlinking
#   item/item_id/tag/tag_id
@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):

#add row to item_tags table to create connection between item and tag
    @blp.response(201, TagSchema)
    def post(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        try:
            item.tags.append(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the tag.")

        return tag


    @blp.response(200, TagAndItemSchema)
    def delete(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while unlinking the tag.")

        return {"message":"Item removed from tag","item":item,"tag":tag}

