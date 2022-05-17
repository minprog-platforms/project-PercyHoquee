from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField, IntegerField, DateField, PositiveIntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from . import helperfunctie


# Create your models here.
class User(AbstractUser):
    pass


class Product(models.Model):
    name = CharField(max_length=100)
    UNIT_CHOICES = (
        ('ml.', 'ml.'),
        ('gr.', 'gr.'),
    )
    unit = CharField(max_length=3, choices=UNIT_CHOICES)
    calories = PositiveIntegerField()
    carbs = PositiveIntegerField()
    protein = PositiveIntegerField()
    fat = PositiveIntegerField()
    creator = ForeignKey(User, on_delete=models.PROTECT, related_name='created_products')


class Meal(models.Model):
    name = CharField(max_length=100)
    product = ManyToManyField(Product)
    creator = ForeignKey(User, on_delete=models.PROTECT, related_name='created_meals')


class Diary(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, related_name='diary')


class DiaryEntry(models.Model):
    date = DateField(null=True)
    diary = ForeignKey(Diary, on_delete=models.CASCADE, related_name='entries')


class Breakfast(models.Model):
    entry = OneToOneField(DiaryEntry, on_delete=models.CASCADE, related_name='breakfast')
    name = "Ontbijt"

    def nutrition(self):
        return helperfunctie.meal_total(self)


class Lunch(models.Model):
    entry = OneToOneField(DiaryEntry, on_delete=models.CASCADE, related_name='lunch')
    name = "Lunch"

    def nutrition(self):
        return helperfunctie.meal_total(self)


class Dinner(models.Model):
    entry = OneToOneField(DiaryEntry, on_delete=models.CASCADE, related_name='dinner')
    name = "Avondeten"

    def nutrition(self):
        return helperfunctie.meal_total(self)


class Snacks(models.Model):
    entry = OneToOneField(DiaryEntry, on_delete=models.CASCADE, related_name='snacks')
    name = "Snacks"

    def nutrition(self):
        return helperfunctie.meal_total(self)


class ProductInstance(models.Model):
    breakfast_item = ForeignKey(Breakfast, blank=True, null=True, on_delete=models.CASCADE, related_name='items')
    lunch_item = ForeignKey(Lunch, blank=True, null=True, on_delete=models.CASCADE, related_name='items')
    dinner_item = ForeignKey(Dinner, blank=True, null=True, on_delete=models.CASCADE, related_name='items')
    snack_item = ForeignKey(Snacks, blank=True, null=True, on_delete=models.CASCADE, related_name='items')
    product = ForeignKey(Product, on_delete=models.CASCADE, null=True)
    amount = IntegerField()

    def calories(self):
        return helperfunctie.calc(self.product.calories, self.amount)

    def carbs(self):
        return helperfunctie.calc(self.product.carbs, self.amount)

    def protein(self):
        return helperfunctie.calc(self.product.protein, self.amount)

    def fat(self):
        return helperfunctie.calc(self.product.fat, self.amount)


class Favs(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    meal = ForeignKey(Meal, blank=True, null=True, on_delete=models.CASCADE)


class Default(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='defaults')
    meal = ForeignKey(Meal, on_delete=models.CASCADE)


class DefaultInstance(models.Model):
    default = ForeignKey(Default, on_delete=models.CASCADE, related_name='instances')
    product = ForeignKey(Product, null=True, on_delete=models.CASCADE)
    amount = PositiveIntegerField(null=True)


class Faulty(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    product = ForeignKey(Product, on_delete=models.CASCADE)









