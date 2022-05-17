breakfast = entry.breakfast
breakfast_nutrition = breakfast.nutrition()

lunch = entry.lunch
lunch_nutrition = lunch.nutrition()

dinner = entry.dinner
dinner_nutrition = dinner.nutrition()

snacks = entry.snacks
snacks_nutrition = snacks.nutrition()

# vervangen voor javascript of functie?
total_calories = breakfast_nutrition[0] + lunch_nutrition[0] + dinner_nutrition[0] + snacks_nutrition[0]
total_carbs = breakfast_nutrition[1] + lunch_nutrition[1] + dinner_nutrition[1] + snacks_nutrition[1]
total_protein = breakfast_nutrition[2] + lunch_nutrition[2] + dinner_nutrition[2] + snacks_nutrition[2]
total_fat = breakfast_nutrition[3] + lunch_nutrition[3] + dinner_nutrition[3] + snacks_nutrition[3]

favs = Favs.objects.filter(user=request.user).all()
favorites = []  
for fav in favs:
    if fav.product != None:
        product = fav.product

        favorites.append(product)
    else:
        meal = fav.meal

        favorites.append(meal)


if request.POST["period"] == "breakfast":
breakfast = entry.breakfast

new = ProductInstance(breakfast_item=breakfast, product=product, amount=amount)
new.save()
elif request.POST["period"] == "lunch":
lunch = entry.lunch

new = ProductInstance(lunch_item=lunch, product=product, amount=amount)
new.save()
elif request.POST["period"] == "dinner":
dinner = entry.dinner

new = ProductInstance(dinner_item=dinner, product=product, amount=amount)
new.save()
else:
snacks = entry.snacks

new = ProductInstance(snack_item=snacks, product=product, amount=amount)
new.save()