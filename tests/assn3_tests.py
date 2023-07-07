import sys

import connectionController
# from assertions import *
global orange_ID, spaghetti_ID, apple_pie_ID, meal_ID


# test 1:  Execute three POST /dishes requests using the dishes, “orange”, “spaghetti”, and “apple pie”.   The test is
# successful if (i) all 3 requests return unique IDs (none of the IDs are the same), and (ii) the return status code
# from each POST request is 201.
def test1():
    orange = {"name": "orange"}
    global orange_ID, spaghetti_ID, apple_pie_ID
    orange_response = connectionController.http_post("dishes", orange)
    assert orange_response.status_code == 201
    orange_ID = orange_response.json()

    spaghetti = {"name": "spaghetti"}
    spaghetti_response = connectionController.http_post("dishes", spaghetti)
    assert spaghetti_response.status_code == 201
    spaghetti_ID = spaghetti_response.json()

    apple_pie = {"name": "apple pie"}
    apple_pie_response = connectionController.http_post("dishes", apple_pie)
    assert apple_pie_response.status_code == 201
    apple_pie_ID = apple_pie_response.json()

    assert orange_ID != spaghetti_ID
    assert orange_ID != apple_pie_ID
    assert spaghetti_ID != apple_pie_ID


# test 2: Execute a GET dishes/<orange-ID> request, using the ID of the orange dish.  The test is successful if (i) the
# sodium field of the return JSON object is between 1 and 5 and (ii) the return status code from the request is 200.
def test2():
    response = connectionController.http_get(f"dishes/{orange_ID}")
    sodium = response.json()["sodium"]
    assert response.status_code == 200
    assert sodium >= .9 and sodium <= 1.1
    print("sodium of orange = ", sodium)
    sys.stdout.flush()


# test 3: Execute a GET /dishes request.  The test is successful if (i) the returned JSON object has 3 embedded JSON
# objects (dishes), and (ii) the return status code from the GET request is 200.
def test3():
    response = connectionController.http_get("dishes")
    # get number of objects returned
    json_obj = response.json()
    length = len(json_obj)
    assert response.status_code == 200
    assert length == 3


# test 4:  Execute a POST /dishes request supplying the dish name “blah”. The test is successful if (i) the return
# value is -3, and (ii) the return code is 404 or 400.
def test4():
    blah = {"name": "blah"}
    blah_response = connectionController.http_post("dishes", blah)
    assert blah_response.json() == -3
    assert blah_response.status_code == 400 or blah_response.status_code == 422 or blah_response.status_code == 404


# Perform a POST dishes request with the dish name “orange”.   The test is successful if (i) the return value is -2, and
# (ii) the return status code is 400 or 404 or 422.
def test5():
    orange = {"name": "orange"}
    orange_response = connectionController.http_post("dishes", orange)
    assert orange_response.status_code == 400 or orange_response.status_code == 422 or orange_response.status_code == 404
    resp = orange_response.json()
    assert resp == -2


# Perform a POST /meals request specifying that the meal contains an “orange” for the appetizer, “spaghetti” for the
# main, and “apple pie” for the dessert (note you will need to use their dish IDs). The test is successful if
# (i) the returned ID > 0 and (ii) the return status code is 201.
def test6():
    global meal_ID
    meal = {
        "name": "delicious",
        "appetizer": orange_ID,
        "main": spaghetti_ID,
        "dessert": apple_pie_ID
    }
    response = connectionController.http_post("meals", meal)
    meal_ID = response.json()
    assert meal_ID > 0
    assert response.status_code == 201


# Perform a GET /meals request. The test is successful if (i) the returned JSON object has 1 meal, (ii) the calories of
# that meal is between X and Y, and (iii) the return status code from the GET request is 200.
def test7():
    response = connectionController.http_get("meals")
    meals = response.json()
    # get number of objects returned
    length = len(meals)
    assert length == 1

    print(meals)
    print("meal_ID = ", str(meal_ID))
    sys.stdout.flush()

    meal_obj = meals[str(meal_ID)]  # get meal with ID meal_ID
    calories = meal_obj["cal"]
    assert calories > 300 and calories < 700

    assert response.status_code == 200


# Perform a POST /meals request as in test 6 with the same meal name (and courses can be the same or different).
# The test is successful if (i) the code is -2 (same meal name as existing meal) and, and
# (ii) the return status code from the request is 400 or 422.
def test8():
    global meal_ID
    meal = {
        "name": "delicious",
        "appetizer": orange_ID,
        "main": spaghetti_ID,
        "dessert": apple_pie_ID
    }
    response = connectionController.http_post("meals", meal)
    meal_ID = response.json()
    assert meal_ID == -2
    assert response.status_code == 400 or response.status_code == 422
