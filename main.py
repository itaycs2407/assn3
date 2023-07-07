from flask import Flask, request
import requests
import json
app = Flask(__name__)
ERR_STATUS, OK_STATUS = 409, 200

X_Api_key = '7+4oMBnrMSKOOU1Ck62Pvg==2O3G4LxAIbnXo8Ms'
counter = 1
counter_meal = 1
dishes = {}
meals = {}


@app.route('/dishes', methods=['POST'])
def post_dish_from_user():
    global counter
    try:
        json_string = json.dumps(request.get_json(), indent=4)
    except:
        return str(0), 415
    # print(json_string)
    data = json.loads(json_string)
    try:
        name = data['name']
    except:
        return str(-1), 400
    dish_data = get_ninja_api(name)
    if dish_data == "Error":
        return str(-4), 400
    if dish_data == "empty":
        return str(-3), 400
    for i in dishes.values():
        if name == i["name"]:
            return str(-2), 400
    dishes[counter] = {"name": name, "ID": counter, "cal": dish_data["calories"],
                       "size": dish_data["serving_size_g"], "sodium": dish_data["sodium_mg"], "sugar": dish_data["sugar_g"]}
    tmp_counter = counter
    # Get the "arguments" array from the data
    counter += 1

    return str(tmp_counter), 201


@app.route('/dishes/<int:id>', methods=['GET'])
def get_dish_by_id(id):

    if id not in dishes.keys():
        return str(-5), 404
    return json.dumps(dishes[id], indent=4), OK_STATUS


@app.route('/dishes/<string:name>', methods=['GET'])
def get_dish_by_name(name):

    for i in dishes.values():
        if name == i["name"]:
            return json.dumps(i, indent=4), OK_STATUS
    return str(-5), 404


@app.route('/dishes', methods=['DELETE'])
def err_delete():
    return str(-5), 404


@app.route('/dishes', methods=['GET'])
def get_all_dishes():
    return json.dumps(dishes, indent=4), 200


@app.route('/dishes/<string:name>', methods=['DELETE'])
def delete_dish_by_name(name):
    for i in dishes.values():
        if name == i["name"]:
            id = i["ID"]
            print(dishes)
            del dishes[id]
            print("after______")
            print(dishes)
            return str(id), OK_STATUS
    return str(-5), 404


@app.route('/dishes/<int:id>', methods=['DELETE'])
def delete_dish_by_id(id):
    print(dishes)
    print("after")
    if id not in dishes.keys():
        return str(-5), 404
    del dishes[id]
    print(dishes)
    return str(id), OK_STATUS


def is_dish_already_exist(name):
    for i in dishes.values():
        if name == i["name"]:
            return -2
    return 0
#query = '1lb brisket and fries'


def get_ninja_api(query):
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': X_Api_key})
    if response.status_code == requests.codes.ok:
        print(response.text)
        if response.text == "[]":
            return "empty"
        return make_deash(json.loads(response.text))
    else:
        print("Error:", response.status_code, response.text)
        return "Error"


def make_deash(dishes_arrary):
    res_dish = {"calories": 0, "serving_size_g": 0,
                "sodium_mg": 0, "sugar_g": 0}
    for dish in dishes_arrary:
        res_dish["calories"] += dish["calories"]
        res_dish["serving_size_g"] += dish["serving_size_g"]
        res_dish["sodium_mg"] += dish["sodium_mg"]
        res_dish["sugar_g"] += dish["sugar_g"]

    return res_dish


@app.route('/meals', methods=['POST'])
def post_meal_from_user():
    global counter_meal
    try:
        json_string = json.dumps(request.get_json(), indent=4)
    except:
        return str(0), 415

    data = json.loads(json_string)
    try:
        meal_name = data["name"]
        appetizer = int(data["appetizer"])
        main = int(data["main"])
        dessert = int(data["dessert"])
    except:
        return str(-1), 400
    for meal in meals.values():
        if meal_name == meal["name"]:
            return str(-2), 400

    meal_id = {appetizer, main, dessert}
    for i in meal_id:
        if i not in dishes.keys():
            return str(-5), 400

    meal = {"name": meal_name, "ID": counter_meal, "appetizer": appetizer, "main": main, "dessert": dessert,
            "cal": dishes[appetizer]["cal"] + dishes[main]["cal"] + dishes[dessert]["cal"],
            "size": dishes[appetizer]["size"] + dishes[main]["size"] + dishes[dessert]["size"],
            "sodium": dishes[appetizer]["sodium"] + dishes[main]["sodium"] + dishes[dessert]["sodium"],
            "sugar": dishes[appetizer]["sugar"] + dishes[main]["sugar"] + dishes[dessert]["sugar"]}
    meals[counter_meal] = meal
    return str(counter_meal), 201


@app.route('/meals', methods=['GET'])
def get_meals():
    return json.dumps(meals, indent=4), OK_STATUS


@app.route('/meals/<int:id>', methods=['GET'])
def get_meal_by_id(id):
    if id not in meals.keys():
        return str(-5), 404
    return json.dumps(meals[id], indent=4), OK_STATUS


@app.route('/meals/<int:id>', methods=['DELETE'])
def delete_meal_by_id(id):
    if id not in meals.keys():
        return str(-5), 404
    print(meals)
    print("after")
    del meals[id]
    print(dishes)
    return str(id), OK_STATUS


@app.route('/meals/<int:id>', methods=['PUT'])
def put_meal_by_id(id):
    json_string = json.dumps(request.get_json(), indent=4)
    # print(json_string)
    data = json.loads(json_string)
    meal_name = data["name"]
    appetizer = int(data["appetizer"])
    main = int(data["main"])
    dessert = int(data["dessert"])
    meal_id = {appetizer, main, dessert}
    for i in meal_id:
        if i not in dishes.keys():
            return str(-5), 400

    meal = {"name": meal_name, "ID": id, "appetizer": appetizer, "main": main, "dessert": dessert,
            "cal": dishes[appetizer]["cal"] + dishes[main]["cal"] + dishes[dessert]["cal"],
            "size": dishes[appetizer]["size"] + dishes[main]["size"] + dishes[dessert]["size"],
            "sodium": dishes[appetizer]["sodium"] + dishes[main]["sodium"] + dishes[dessert]["sodium"],
            "sugar": dishes[appetizer]["sugar"] + dishes[main]["sugar"] + dishes[dessert]["sugar"]}
    meals[id] = meal
    return str(id), 200


@app.route('/meals/<string:name>', methods=['GET'])
def get_meal_by_name(name):
    for i in meals.values():
        if name == i["name"]:
            return json.dumps(i, indent=4), OK_STATUS
    return str(-5), 404


@app.route('/meals/<string:name>', methods=['DELETE'])
def delete_meal_by_name(name):
    for i in meals.values():
        if name == i["name"]:
            id = i["ID"]
            print(meals)
            del meals[id]
            print("after______")
            print(meals)
            return str(id), OK_STATUS
    return str(-5), 404


@app.route('/meals', methods=['DELETE'])
def delete_meals():
    return str(-5), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
