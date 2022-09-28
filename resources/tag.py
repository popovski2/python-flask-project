from db import db
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort

from models import TagModel,StoreModel,ItemModel
from schemas import TagSchema

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

