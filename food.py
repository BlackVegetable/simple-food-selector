import json
import random
import sys

class Meal(object):
    '''
    Object representing a single meal or snack.
    The Meal object is agnositc to which kind of
    meal it is (e.g. Breakfast vs. Dinner).
    '''
    def __init__(self, name, ingredients, notes):
        self.name = name
        self.ingredients = ingredients
        self.notes = notes

    def __str__(self):
        s = "{}\n  ingredients = {}\n".format(self.name, self.ingredients)
        if self.notes:
            s += "  notes = {}\n".format(self.notes)
        s += "\n"
        return s

def meal_from_json(dictionary):
    '''
    Converter between a dictionary of meal elements and a Meal
    object. Translates from unicode strings to the simpler kind.
    '''
    return Meal(str(dictionary["name"]),
                str(map(str, dictionary["ingredients"])),
                str(dictionary["notes"]))

class DaysFood(object):
    '''
    Object representing a single day's worth of food.
    This includes one breakfast, one lunch, one dinner,
    and a variable number of snacks.
    '''
    def __init__(self, breakfast, lunch, dinner, snacks):
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner
        self.snacks = snacks

    def __str__(self):
        s = "Breakfast = {}Lunch = {}Dinner = {}".format(self.breakfast,
                                                         self.lunch,
                                                         self.dinner)

        for snack_number in xrange(len(self.snacks)):
            s += "Snack #{} = {}".format(snack_number + 1,
                                         self.snacks[snack_number])
        return s


def main(fname="food.json"):
    '''
    Randomly selects meals from the data file specified by the commandline
    or by the default name and arranges them into daily meals.
    '''
    with open(fname, "r") as f:
        food_data = json.load(f)
    meals = select_meals(food_data, food_data['days'], food_data['snacks_per_day'])
    write_out = ""
    for meal_number in xrange(len(meals)):
        write_out += "---- Day #{} ---- \n{}".format(meal_number + 1, str(meals[meal_number]))
    with open("meals.txt", "w") as f:
        f.write(write_out)
    print write_out

def select_meals(food_data, days, snacks_per_day=2):
    '''
    Select meals for 'days' days with a breakfast, lunch, dinner,
    and 'snacks_per_day' (default=two) snacks with no repeats.
    Returns a list of dictionaries of the form:
      {"breakfast": value, "lunch": value, "snacks": [value1, value2, ...]}
    Raises an Exception if insufficient meals exist for the given
    number of days.
    '''
    if min(len(food_data["breakfast"]), len(food_data["lunch"]),
           len(food_data["dinner"])) < days or \
       len(food_data["snacks"]) < (days * snacks_per_day):
       raise Exception("Not enough meals for this many days. Reduce"
                       " number of days or add more meals to food file.")

    breakfasts = map(meal_from_json, random.sample(food_data["breakfast"], days))
    lunches = map(meal_from_json, random.sample(food_data["lunch"], days))
    dinners = map(meal_from_json, random.sample(food_data["dinner"], days))
    snacks = map(meal_from_json, random.sample(food_data["snacks"], days * snacks_per_day))
    snack_lists = split_evenly(snacks, days)
    meals = map(lambda breakfast, lunch, dinner, daily_snacks:
                DaysFood(breakfast, lunch, dinner, daily_snacks),
                breakfasts, lunches, dinners, snack_lists)
    return meals
    
def split_evenly(lyst, num_output_lists):
    '''
    Splits a list with length evenly divisible by 'num_output_lists'
    into 'num_output_lists' lists.
    '''
    length_of_each = len(lyst) / num_output_lists
    output_lists = []
    for n in xrange(num_output_lists):
        start = n * length_of_each
        end = start + length_of_each
        output_lists.append(lyst[start:end])
    return output_lists

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()

    # Keep the console open on Windows.
    raw_input()

