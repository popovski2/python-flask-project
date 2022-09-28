from marshmallow import Schema, fields


#=============PLAIN SCHEMAS ===================
class PlainItemSchema(Schema):
    #id e razlicno zatoa sto, toa pole sigurni sme deka go generirame nie sami na server-side, za razlika od drugite koi mozat da se generiraat
    #pri POST, primer create item(name,price,store_id)
    #zatoa  e dump_only i ne moze klientot da prati id na serverot vo JSON payload.
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


#=============== NORMAL SCHEMAS===============
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()




#koga ke ja koristime ovaa ItemSchema ke moze da go pustime store_id kako argument
#ova go pravime koga dobivame podatoci od klientot
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(),dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema),dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema),dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)