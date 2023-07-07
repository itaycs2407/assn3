import requests
import sys
from Ninja_key import NINJA_API_KEY


def get_food_info(food):
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(food)
        try:
            response = requests.get(api_url, headers={'X-Api-Key': NINJA_API_KEY})
        except:
            print("Error from api.api-ninjas.com/v1/nutrition.  response code = ", response.status_code)
            print("response text = ", response.text)
            print("raising SomeAPIError")
            sys.stdout.flush()
            raise Exception #SomeAPIError
        else:
            if response.status_code == requests.codes.ok:
                try:
                    # the response might include multiple items.  E.g., if the query to Ninja is for "cereal and eggs", it
                    # will return one item for cereal and one for eggs.  However, "cereal and eggs" is treated as one dish,
                    # so the calories, sodium, etc. of the dish is the sum of the calories, sodium, etc. of the items in the
                    # response.
                    resp = response.json()
                    if not resp:  # response.json() is empty
                        raise Exception
                    calories = 0
                    serving_size = 0
                    sodium = 0
                    sugar = 0
                    for val in resp:
                        calories += val.get("calories")
                        sodium += val.get("sodium_mg")
                        sugar += val.get("sugar_g")
                    return calories, sodium, sugar
                except:  # if API returns empty text, then this dish is not found.   Raise DishNotDefined exception
                    print("Response Error from api.api-ninjas.com/v1/nutrition.  response code = ",
                          response.status_code)
                    print("response text = ", response.text)
                    # print("if empty text then API did not recognize dish called ", name)
                    print("raising DishNotDefined")
                    sys.stdout.flush()
                    raise Exception #DishNotDefined
            else:  # bad response code from api.api-ninjas.com/v1/nutrition.   Probably "502" Internal Server error.  Need
                # to retry
                print("Bad response code from api.api-ninjas.com/v1/nutrition.  response code = ", response.status_code)
                print("response text = ", response.text)
                print("raising APINotReachable")
                sys.stdout.flush()
                raise Exception # APINotReachable  # need to add custom exception class to handle the different exceptions


if __name__ == '__main__':
    fh_query = open("query.txt", 'r')
    lines = fh_query.readlines()
    fh_query.close()
    fh_resp = open("/tmp/response.txt",'w')
    for line in lines:
        food = line.strip()
        cal, sod, sug = get_food_info(food)
        s = food + " contains " + '{:1f}'.format(cal) + " calories, " + '{:1f}'.format(sod) + " mgs of sodium, and " + \
            '{:1f}'.format(sug) + " grams of sugar\n"
        fh_resp.write(s)
    fh_resp.close()


