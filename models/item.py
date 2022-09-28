from db import db

#ORM mapping from a row in a table to a python class
class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2),unique=False, nullable=False)
    #One-to-many relationship (one store may have multiple items)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    #SQLAlchemy znajt deka stores tabelata e koristena od StoreModel klasata
    #Vekje koga go znaeme id-to na store, moze da definirame vrska so StoreModel klasata i avtomatski da ja popolnime ovaa store promenliva
    #so id = store_id
    store = db.relationship("StoreModel",back_populates="items")

    #go povrzuvame so tags
    tags = db.relationship("TagModel",back_populates="items",secondary="items_tags")

