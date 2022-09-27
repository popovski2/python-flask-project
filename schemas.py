from marshmallow import Schema, fields

class ItemSchema(Schema):
    #id e razlicno zatoa sto, toa pole sigurni sme deka go generirame nie sami na server-side, za razlika od drugite koi mozat da se generiraat
    #pri POST, primer create item(name,price,store_id)
    #zatoa  e dump_only i ne moze klientot da prati id na serverot vo JSON payload.
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
