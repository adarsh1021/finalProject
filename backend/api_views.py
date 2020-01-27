from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt


"""
Always follow the below response format
{
    status: <status_code>,
    message: <message>,
    redirect_flag: <true/false>,
    redirect: <relative url>,
}
If confused about which status code to use refer https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

Example for a successful api call
{
    status: 200,
    message: "success",
    redirect_flag: True,
    redirect: "/index",
}
"""


@csrf_exempt
def sign_up(request):
    """
    This endpoint is used for creating new users
    method: POST
    POST format
    {
        username*: <username>,
        password*: <password>,
        email*: <email>,
    }
    """

    if request.method == "POST":
        data = request.POST
        if User.objects.filter(email=data["email"]):
            return JsonResponse(
                {"message": "User already exists", "redirect_flag": False},
                status=409,
            )

        user = User.objects.create_user(
            username=data.get("username"),
            password=data.get("password"),
            email=data.get("email"),
        )
        request.session["user"] = user.id
        return JsonResponse(
            {"message": "Success", "redirect_flag": True, "redirect": "/index"},
            status=200,
        )

    else:
        return JsonResponse(
            {"message": "Method not allowed", "redirect_flag": False},
            status=405,
        )


@csrf_exempt
def sign_in(request):
    """
    This endpoint is used for authenticating with the user
    method: POST
    POST format
    {
        username: <username>,
        password: <password>,
    }
    """

    if request.method == "POST":
        data = request.POST
        user = User.objects.get(email=data.get("email"))
        username = user.username
        user = authenticate(username=username, password=data.get("password"))
        if user:
            request.session["user"] = user.id
            return JsonResponse(
                {
                    "message": "Success",
                    "redirect_flag": True,
                    "redirect": "/index",
                },
                status=200,
            )

        else:
            return JsonResponse(
                {"message": "Authentication failed", "redirect_flag": False},
                status=401,
            )

    else:
        return JsonResponse(
            {"message": "Method not allowed", "redirect_flag": False},
            status=405,
        )

