from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("calender", views.calender, name="calender"),
    path("product/new_product", views.new_product, name="new_product"),
    path("product/<int:product_id>/faulty", views.faulty_product, name="faulty_product"),
    path("product/<int:product_id>/specify", views.product_specify_date, name="product_specify_date"),
    path("product/<int:product_id>/send", views.product_send_date, name="product_send_date"),
    path("product/<int:product_id>add_product/<str:date>", views.add_product, name="add_product"),
    path("meal/new_meal", views.new_meal, name="new_meal"),
    path("meal/my_meals", views.my_meals, name="my_meals"),
    path("meal/<int:meal_id>", views.meal, name="meal"),
    path("meal/<int:meal_id>/search", views.meal_search, name="meal_search"),
    path("meal/<int:meal_id>/results", views.meal_results, name="meal_results"),
    path("meal/<int:meal_id>/specify", views.meal_specify_date, name="meal_specify_date"),
    path("meal/<int:meal_id>/send", views.meal_send_date, name="meal_send_date"),
    path("meal/<int:meal_id>/add/<int:product_id>", views.meal_add_product, name="meal_add_product"),
    path("meal/<int:meal_id>/delete/<int:product_id>", views.meal_delete_product, name="meal_delete_product"),
    path("meal/<int:meal_id>/add_meal/<str:date>", views.add_meal, name="add_meal"),
    path("meal/<int:meal_id>/add_meal/<str:date>/default", views.default, name="default"),
    path("meal/<int:meal_id>/add_meal/<str:date>/set_default", views.set_default, name="set_default"),
    path("meal/<int:meal_id>/add_meal/<str:date>/get_default", views.get_default, name="get_default"),
    path("favorites", views.favorites, name="favorites"),
    path("favorites/product/<int:product_id>/delete", views.delete_product_favorite, name="delete_product_favorite"),
    path("favorites/product/<int:product_id>/add", views.add_product_favorite, name="add_product_favorite"),
    path("favorites/meal/<int:meal_id>/delete", views.delete_meal_favorite, name="delete_meal_favorite"),
    path("favorites/meal/<int:meal_id>/add", views.add_meal_favorite, name="add_meal_favorite"),
    path("<str:date>", views.index_alt, name="alt"),
    path("<str:date>/search", views.search, name="search"),
    path("<str:date>/results", views.results, name="results"),
    #path("<str:date>/add/snacks", views.add_snacks, name="add_snacks"),
]