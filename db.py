# fake database

#ova e nested dictionary
#explained:

#accessing
# items[1] = { "name": "Chair", "price": 17.99, "store_id":"44213ihjhjk"}
# items[1]["name"] = Chair
# items[2]["name"] = Table

#deleting
# del items[1] = go brisit cel dictionary so id 1
# del items[1]["name"] = go brisit samo key value parot so key "name", a to e "name":"chair"

#adding another dictionary e simple
# items[3] = {"name": "newItem", "price": 23.55, "store_id":"22232dfdfd"}

#iterating
#items.items() -> vrakjat lista od tuples koj sho se (key, dictionary) ili (1, {}) vo slucajov
# item_id e key t.e 1, a item_info e celiot sleden dictionary vnatre {}
# for item_id, item_info in items.items():
#   print(f"item id is {item_id}")
#       for key in item_info:
#           print(key + ":" + item_info[key])

items = {
    # 1 i 2 se id
    1: {
        "name": "Chair",
        "price": 17.99,
        "store_id":"44213ihjhjk"
    },
    2: {
        "name": "Table",
        "price": 145.99,
        "store_id":"223123jh12"
    }
}
print(items.items())
stores = {

    'some_store_id':{
        "name": "First Store"
    }

}
print(stores.items())