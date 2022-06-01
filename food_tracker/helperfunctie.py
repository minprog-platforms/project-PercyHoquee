import datetime


def calc(nutrition: int, amount: int):
    """
    Calculates the nutritional values per x amount of a product
    """
    return nutrition / 100 * amount


def meal_total(meal):
    """
    Calculates the total nutritional values for the different meals of a day
    """
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


def daily_totals(breakfast: list, lunch: list, dinner: list, snacks: list):
    """
    Calculates daily totals for the different nutrient classes
    """
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


def date_converter(date_object):
    """
    Converts datetime object into YYYY-MM-DD string
    """
    date = f"{date_object.year}-{date_object.month}-{date_object.day}"

    return date


def datetime_converter(date):
    """
    Converts date string (YYYY-MM-DD) into datetime object
    """
    split = date.split("-")
    return datetime.date(int(split[0]), int(split[1]), int(split[2]))


def reverse_date(date):
    """
    Reverses YYYY-MM-DD date into DD-MM-YYYY date
    """
    split = date.split("-")
    reverse = f"{split[2]}-{split[1]}-{split[0]}"
    return reverse


def favorites(favs):
    """
    Gathers a user's favorite products and meals
    """
    favorites = []

    for fav in favs:
        if fav.product is not None:
            favorites.append(fav.product)
        else:
            favorites.append(fav.meal)
    return favorites
