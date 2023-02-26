from .models import User

def create_new_user(data):
    user = User.objects.create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        first_name=data.get("firstName", ""),
        last_name=data.get("lastName", ""),
        gender=data.get("gender", ""),
        address=data.get("address", ""),
        mobile=data.get("mobile", ""),
        telephone=data.get("telephone", ""),
        facebook=data.get("facebook", ""),
    )
    return user