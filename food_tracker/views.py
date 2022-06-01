import datetime

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models.fields import CharField, IntegerField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import helperfunctie
from .models import (Breakfast, DefaultInstance, Lunch,
                     ProductInstance, User, Product, Meal,
                     Diary, DiaryEntry, Dinner, Snacks, Favs, Default, Faulty)


def index(request):
    """
    Directs verified user to the homepage of the current day
    """
    if request.user.is_authenticated:
        today = datetime.datetime.today()
        # Converts datetime object into string (YYYY-MM-DD)
        date = helperfunctie.date_converter(today)
        return HttpResponseRedirect(reverse("alt", args=(date,)))
    else:
        return HttpResponseRedirect(reverse("login"))


def index_alt(request, date):
    """
    Present the FoodTracker diary for any requested day
    """
    if request.user.is_authenticated:
        # Retrieves the user's FoodTrack diary
        diary = request.user.diary
        # Attempt to retrieve the date in question from the diary
        try:
            entry = diary.entries.get(date=date)

            breakfast = entry.breakfast
            lunch = entry.lunch
            dinner = entry.dinner
            snacks = entry.snacks

            # Calculates daily totals for the different nutrient classes
            totals = helperfunctie.daily_totals(breakfast.nutrition(),
                                                lunch.nutrition(),
                                                dinner.nutrition(),
                                                snacks.nutrition())

            # Converts date (YYYY-MM-DD) into datetime object
            date_object = helperfunctie.datetime_converter(date)

            yesterday_object = date_object - datetime.timedelta(1)
            yesterday = helperfunctie.date_converter(yesterday_object)

            tomorrow_object = date_object + datetime.timedelta(1)
            tomorrow = helperfunctie.date_converter(tomorrow_object)
            return render(request, "food_tracker/index.html", {
                "date_object": date_object,
                "date": date,
                "previous": yesterday,
                "next": tomorrow,
                "periods": [breakfast, lunch, dinner, snacks],
                "totals": totals,
            })
        except ObjectDoesNotExist:
            entry = DiaryEntry(date=date, diary=diary)
            entry.save()

            # Creates periods for a new date entry
            instant_periods(entry)
            return HttpResponseRedirect(reverse("alt", args=(date,)))
    else:
        return HttpResponseRedirect(reverse("index"))


def login_view(request):
    """
    Signs user into FoodTracker account
    """
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "food_tracker/login.html", {
                "message": "Ongeldige gebruikersnaam en/of wachtwoord."
            })
    else:
        return render(request, "food_tracker/login.html")


def logout_view(request):
    """
    Logs user out of FoodTracker account
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    Registers new FoodTracker account for user
    """
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "food_tracker/register.html", {
                "message": "Wachtwoorden moeten overeen komen."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password)
            user.save()

            diary = Diary(user=user)
            diary.save()
        except IntegrityError:
            return render(request, "food_tracker/register.html", {
                "message": "Gebruikersnaam is bezet."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "food_tracker/register.html")


def search(request, date):
    """
    Allows user to search for products and/or meals
    """
    return render(request, "food_tracker/search.html", {
        "date": helperfunctie.reverse_date(date),
    })


def results(request, date):
    """
    Collects all results that match the search query
    """
    query = request.POST["q"]

    products = Product.objects.filter(name__icontains=query)
    meals = Meal.objects.filter(name__icontains=query)
    favorites_objects = Favs.objects.filter(user=request.user).all()

    # Retrieves Product and Meal objects from Favs object
    favorites = helperfunctie.favorites(favorites_objects)
    return render(request, "food_tracker/results.html", {
        "date": date,
        "products": products,
        "meals": meals,
        "favorites": favorites,
        "query": query,
    })


def calender(request):
    """
    Allows user to select dates through a datepicker
    """
    date = request.POST["date"]

    # Error prevention because value element in datepicker is irresponsive
    if date == '':
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("alt", args=(date,)))


def add_product(request, date, product_id):
    """
    Adds product to the user's FoodTracker diary
    """
    if request.method == "POST":
        amount = request.POST["amount"]
        if amount == '':
            return HttpResponseRedirect(reverse("add_product",
                                                args=(product_id, date,)))

        diary = request.user.diary
        try:
            entry = diary.entries.get(date=date)
        except ObjectDoesNotExist:
            entry = DiaryEntry(date=date, diary=diary)
            entry.save()

            instant_periods(entry)
        product = Product.objects.get(id=product_id)

        # Add product to the requested period of the day
        if request.POST["period"] == "breakfast":
            new = ProductInstance(breakfast_item=entry.breakfast,
                                  product=product, amount=amount)
            new.save()
        elif request.POST["period"] == "lunch":
            new = ProductInstance(lunch_item=entry.lunch,
                                  product=product, amount=amount)
            new.save()
        elif request.POST["period"] == "dinner":
            new = ProductInstance(dinner_item=entry.dinner,
                                  product=product, amount=amount)
            new.save()
        else:
            new = ProductInstance(snack_item=entry.snacks,
                                  product=product, amount=amount)
            new.save()
        return HttpResponseRedirect(reverse("alt", args=(date,)))
    else:
        return render(request, "food_tracker/add_product.html", {
            "product": Product.objects.get(id=product_id),
        })


def add_meal(request, meal_id, date):
    """
    Adds all products in a meal to the user's FoodTracker diary
    """
    if request.method == "POST":
        diary = request.user.diary
        try:
            entry = diary.entries.get(date=date)
        except ObjectDoesNotExist:
            entry = DiaryEntry(date=date, diary=diary)
            entry.save()

            instant_periods(entry)
        meal = Meal.objects.get(id=meal_id)

        # Adds each product to the requested period of the day
        for product in meal.product.all():
            amount = request.POST[f"{product.id}"]
            if amount == '':
                return HttpResponseRedirect(reverse("add_meal",
                                                    args=(meal_id, date,)))
            if request.POST["period"] == "breakfast":
                new = ProductInstance(breakfast_item=entry.breakfast,
                                      product=product, amount=amount)
                new.save()
            elif request.POST["period"] == "lunch":
                new = ProductInstance(lunch_item=entry.lunch,
                                      product=product, amount=amount)
                new.save()
            elif request.POST["period"] == "dinner":
                new = ProductInstance(dinner_item=entry.dinner,
                                      product=product, amount=amount)
                new.save()
            else:
                new = ProductInstance(snack_item=entry.snacks,
                                      product=product, amount=amount)
                new.save()
        return HttpResponseRedirect(reverse("alt", args=(date,)))
    else:
        return render(request, "food_tracker/add_meal.html", {
            "meal": Meal.objects.get(id=meal_id),
            "date": date,
        })


def new_product(request):
    """
    Creates new product in FoodTracker database
    """
    if request.method == "POST":
        name = request.POST["name"]
        unit = request.POST["unit"]
        calories = request.POST["calories"]
        carbs = request.POST["carbs"]
        protein = request.POST["protein"]
        fat = request.POST["fat"]
        if '' in {calories, carbs, protein, fat}:
            return HttpResponseRedirect(reverse("new_product"))

        new_product = Product(name=name, unit=unit, calories=calories,
                              carbs=carbs, protein=protein,
                              fat=fat, creator=request.user)
        new_product.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "food_tracker/new_product.html")


def new_meal(request):
    """
    Creates new meal in FoodTracker database
    """
    if request.method == "POST":
        name = request.POST["name"]
        meal = Meal(name=name, creator=request.user)
        meal.save()
        return HttpResponseRedirect(reverse("meal", args=(meal.id,)))
    else:
        return render(request, "food_tracker/new_meal.html")


def meal(request, meal_id):
    """
    Shows the overview page for an user created meal
    """
    meal = Meal.objects.get(id=meal_id)
    return render(request, "food_tracker/meal.html", {
        "meal": meal
    })


def meal_search(request, meal_id):
    """
    Searches for products to add to a meal
    """
    meal = Meal.objects.get(id=meal_id)
    return render(request, "food_tracker/search.html", {
        "meal": meal
    })


def meal_results(request, meal_id):
    """
    Collects all the products that match the search query
    """
    meal = Meal.objects.get(id=meal_id)
    query = request.POST["q"]
    products = Product.objects.filter(name__icontains=query)
    return render(request, "food_tracker/results_meal.html", {
        "products": products,
        "meal": meal,
        "query": query,
    })


def meal_add_product(request, meal_id, product_id):
    """
    Adds a product to a meal
    """
    meal = Meal.objects.get(id=meal_id)
    product = Product.objects.get(id=product_id)
    meal.product.add(product)
    meal.save()
    return HttpResponseRedirect(reverse("meal", args=(meal_id,)))


def meal_delete_product(request, meal_id, product_id):
    """
    Removes a product from a meal
    """
    meal = Meal.objects.get(id=meal_id)
    product = Product.objects.get(id=product_id)
    meal.product.remove(product)
    meal.save()
    return HttpResponseRedirect(reverse("meal", args=(meal_id,)))


def my_meals(request):
    """
    Collects all meals created by the user
    """
    meals = request.user.created_meals.all()
    fav_objects = Favs.objects.filter(user=request.user).all()
    favorites = helperfunctie.favorites(fav_objects)
    return render(request, "food_tracker/results_my_meals.html", {
        "meals": meals,
        "favorites": favorites,
    })


def favorites(request):
    """
    Collects all products and meals marked as a favorite by the user
    """
    favs = Favs.objects.filter(user=request.user).all()
    products = []
    meals = []

    # Seperates products and meals for layout purposes
    for fav in favs:
        if fav.product is not None:
            products.append(fav.product)
        else:
            meals.append(fav.meal)
    return render(request, "food_tracker/results_favorites.html", {
        "products": products,
        "meals": meals,
        "favorites": products + meals,
    })


def add_product_favorite(request, product_id):
    """
    Marks a product as a favorite
    """
    product = Product.objects.get(id=product_id)
    fav = Favs(user=request.user, product=product, meal=None)
    fav.save()
    return HttpResponseRedirect(reverse("favorites"))


def delete_product_favorite(request, product_id):
    """
    Unmarks a product as a favorite
    """
    product = Product.objects.get(id=product_id)
    fav = Favs.objects.get(user=request.user, product=product)
    fav.delete()
    return HttpResponseRedirect(reverse("favorites"))


def add_meal_favorite(request, meal_id):
    """
    Marks a meal as a favorite
    """
    meal = Meal.objects.get(id=meal_id)
    fav = Favs(user=request.user, product=None, meal=meal)
    fav.save()
    return HttpResponseRedirect(reverse("favorites"))


def delete_meal_favorite(request, meal_id):
    """
    Unmarks a meal as a favorite
    """
    meal = Meal.objects.get(id=meal_id)
    fav = Favs.objects.get(user=request.user, meal=meal)
    fav.delete()
    return HttpResponseRedirect(reverse("favorites"))


def product_specify_date(request, product_id):
    """
    Specifies date on which product should be added
    """
    return render(request, "food_tracker/specify_date_product.html", {
        "product": Product.objects.get(id=product_id),
    })


def product_send_date(request, product_id):
    """
    Directs user to page to specify amount and period
    """
    date = request.POST["date"]

    # Error prevention because value element in datepicker is irresponsive
    if date == '':
        return HttpResponseRedirect(reverse("product_specify_date",
                                            args=(product_id,)))
    else:
        return HttpResponseRedirect(reverse("add_product",
                                            args=(product_id, date,)))


def meal_specify_date(request, meal_id):
    """
    Specifies date on which meal should be added
    """
    return render(request, "food_tracker/specify_date_meal.html", {
        "meal": Meal.objects.get(id=meal_id),
    })


def meal_send_date(request, meal_id):
    """
    Directs user to page to specify amount and period
    """
    date = request.POST["date"]

    # Error prevention because value element in datepicker is irresponsive
    if date == '':
        return HttpResponseRedirect(reverse("meal_specify_date",
                                            args=(meal_id,)))
    else:
        return HttpResponseRedirect(reverse("add_meal", args=(meal_id, date,)))


def default(request, meal_id, date):
    """
    Updates or creates preference amounts for meals
    """
    meal = Meal.objects.get(id=meal_id)

    # Check for any existing preferences
    try:
        default = Default.objects.get(user=request.user, meal=meal)
        instances = default.instances.all()

        products = []
        for instance in instances:
            products.append(instance.product)
        return render(request, "food_tracker/default.html", {
            "meal": meal,
            "date": date,
            "defaults": instances,
            "products": products,
        })
    except ObjectDoesNotExist:
        return render(request, "food_tracker/default.html", {
            "meal": meal,
            "date": date,
        })


def set_default(request, meal_id, date):
    """
    Attempts to update preferences for a meal
    """
    meal = Meal.objects.get(id=meal_id)

    # Attempt to update existing preferences
    try:
        default = Default.objects.get(user=request.user, meal=meal)

        # Attempt to set preferences for each product in meal
        for product in meal.product.all():
            try:
                instance = DefaultInstance.objects.get(default=default,
                                                       product=product)
                amount = request.POST[f"{product.id}"]

                # Error prevention
                if amount == "":
                    return HttpResponseRedirect(reverse("default",
                                                        args=(meal_id, date,)))
                instance.amount = amount
                instance.save()
            except ObjectDoesNotExist:
                amount = request.POST[f"{product.id}"]
                if amount == "":
                    return HttpResponseRedirect(reverse("default",
                                                        args=(meal_id, date,)))
                instance = DefaultInstance(default=default,
                                           product=product, amount=amount)
                instance.save()
        return HttpResponseRedirect(reverse("add_meal", args=(meal_id, date,)))

    # Create new preferences
    except ObjectDoesNotExist:
        default = Default(user=request.user, meal=meal)
        default.save()
        for product in meal.product.all():
            amount = request.POST[f"{product.id}"]
            if amount == "":
                return HttpResponseRedirect(reverse("default",
                                                    args=(meal_id, date,)))
            instance = DefaultInstance(default=default,
                                       product=product, amount=amount)
            instance.save()
        return HttpResponseRedirect(reverse("add_meal", args=(meal_id, date,)))


def get_default(request, meal_id, date):
    """
    Retrieves preferences at user request
    """
    meal = Meal.objects.get(id=meal_id)

    # Attempt to retrieve preferences for a meal
    try:
        default = Default.objects.get(user=request.user, meal=meal)
        instances = default.instances.all()
        products = []
        for instance in instances:
            products.append(instance.product)
        return render(request, "food_tracker/add_meal.html", {
                "meal": Meal.objects.get(id=meal_id),
                "date": date,
                "defaults": instances,
                "products": products,
                })
    except ObjectDoesNotExist:
        return render(request, "food_tracker/add_meal.html", {
            "meal": Meal.objects.get(id=meal_id),
            "date": date,
            "message": "Er Zijn Nog Geen Voorkeuren Ingesteld Voor Dit Product"
        })


def faulty_product(request, product_id):
    """
    Allows users to report faulty products (requires administrator)
    """
    product = Product.objects.get(id=product_id)
    faulty_product = Faulty(user=request.user, product=product)
    faulty_product.save()
    return HttpResponseRedirect(reverse("index"))


def instant_periods(entry):
    """
    Creates periods for a diary entry
    """
    breakfast = Breakfast(entry=entry)
    breakfast.save()

    lunch = Lunch(entry=entry)
    lunch.save()

    dinner = Dinner(entry=entry)
    dinner.save()

    snacks = Snacks(entry=entry)
    snacks.save()
