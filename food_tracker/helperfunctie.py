import datetime



"""
Calculates the nutritional values per x amount of a product
"""
def calc(nutrition: int, amount: int):
    return nutrition / 100 * amount

"""
Calculates the total nutritional values for the different meals of a day
"""
def meal_total(meal):
    calories = 0
    carbs = 0
    protein = 0
    fat = 0
    values = []

    for item in meal.items.all():
        calories += calc(item.product.calories, item.amount)
        carbs += calc(item.product.carbs, item.amount)
        protein += calc(item.product.protein, item.amount)
        fat += calc(item.product.fat, item.amount)

    values.append(calories)
    values.append(carbs)
    values.append(protein)
    values.append(fat)

    return values

"""
Calculates daily totals for the different nutrient classes
"""
def daily_totals(breakfast: list, lunch: list, dinner: list, snacks: list):
    totals = []

    total_calories = breakfast[0] + lunch[0] + dinner[0] + snacks[0]
    totals.append(f"Calorieën: {total_calories} kcal")

    total_carbs = breakfast[1] + lunch[1] + dinner[1] + snacks[1]
    totals.append(f"Koolhydraten: {total_carbs} gram")

    total_protein = breakfast[2] + lunch[2] + dinner[2] + snacks[2]
    totals.append(f"Eiwitten: {total_protein} gram")

    total_fat = breakfast[3] + lunch[3] + dinner[3] + snacks[3]
    totals.append(f"Vet: {total_fat} gram")   

    return totals

"""
Converts datetime object into YYYY-MM-DD string
"""
def date_converter(date_object):
    date=f"{date_object.year}-{date_object.month}-{date_object.day}"

    return date

"""
Converts date string (YYYY-MM-DD) into datetime object
"""
def datetime_converter(date):
    split = date.split("-")

    return datetime.date(int(split[0]), int(split[1]), int(split[2]))

"""
Gathers a user's favorite products and meals
"""
def favorites(favs):
    favorites = []

    for fav in favs:
        if fav.product != None:
            favorites.append(fav.product)
        else:
            favorites.append(fav.meal)
    return favorites


    