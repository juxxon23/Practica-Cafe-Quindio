from controllers.signin import Signin
from controllers.login import Login
from controllers.product import Product

client = {
    "signin": "/signin", "view_func_signin": Signin.as_view("api_signin"),
    "login": "/login", "view_func_login": Login.as_view("api_login")
}

product = {
    "product": "/product", "view_func_product": Product.as_view("api_product")
}