def search_breakfast(request, date):
    return render(request, "food_tracker/search.html", {
        "date": date,
        "breakfast": True
    })


def search_lunch(request, date):
    return render(request, "food_tracker/search.html", {
        "date": date,
        "lunch": True
    })


def search_dinner(request, date):
    return render(request, "food_tracker/search.html", {
        "date": date,
        "dinner": True
    })


def search_snacks(request, date):
    return render(request, "food_tracker/search.html", {
        "date": date,
        "snacks": True
    })


def add_breakfast(request, date):
    diary = request.user.diary

    entry = diary.entries.get(date=date)

    breakfast = entry.breakfast

    name = request.POST["name"]

    product = Product.objects.get(name=name)

    amount = request.POST["amount"]

    addition = ProductInstance(breakfast_item=breakfast, product=product, amount=amount)

    return HttpResponseRedirect(reverse(f"{date}"))


def add_lunch(request, date):
    diary = request.user.diary

    entry = diary.entries.get(date=date)

    lunch = entry.lunch

    name = request.POST["name"]

    product = Product.objects.get(name=name)

    amount = request.POST["amount"]

    addition = ProductInstance(lunch_item=lunch, product=product, amount=amount)

    return HttpResponseRedirect(reverse(f"{date}"))


def add_dinner(request, date):
    diary = request.user.diary

    entry = diary.entries.get(date=date)

    dinner = entry.dinner

    name = request.POST["name"]

    product = Product.objects.get(name=name)

    amount = request.POST["amount"]

    addition = ProductInstance(breakfast_item=dinner, product=product, amount=amount)

    return HttpResponseRedirect(reverse(f"{date}"))


def add_snacks(request, date):
    diary = request.user.diary

    entry = diary.entries.get(date=date)

    snacks = entry.snacks

    name = request.POST["name"]

    product = Product.objects.get(name=name)

    amount = request.POST["amount"]

    addition = ProductInstance(breakfast_item=snacks, product=product, amount=amount)

    return HttpResponseRedirect(reverse(f"{date}"))