from controllers.signin import Signin
from controllers.login import Login

client = {
    "signin": "/signin", "view_func_signin":Signin.as_view("api_signin"),
    "login": "/login", "view_func_login":Login.as_view("api_login")
}