from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt


'''
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
'''
@csrf_exempt
def sign_up(request):
    '''
    This endpoint is used for creating new users
    method: POST
    POST format
    {
        username*: <user_name>,
        password*: <password>,
        email*: <email>,
        first_name: <first_name>,
        last_name: <last_name>,
    }
    '''

    if(request.method == "POST"):
        print(request.GET)
        data = request.POST
        print(data)
        if(User.objects.get(email=data['email'])):
            return JsonResponse({"message": "User already exists", "redirect_flag": False }, status=409)
        User.objects.create_user(
            username=data['user_name'],
            password=data['password'],
            email=data['email'],
        )
        return JsonResponse({"message": "Success", "redirect_flag": True, "redirect": "/index" }, status=200)
    
    else:
        return JsonResponse({"message": "Method not allowed", "redirect_flag": False }, status=405)


@csrf_exempt
def sign_in(request):
    '''
    This endpoint is used for authenticating with the user
    method: POST
    POST format
    {
        username: <user_name>,
        password: <password>,
    }
    '''

    if(request.method == "POST"):
        data = requst.POST
        user = authenticate(username=data['username'], password=data['password'])
        if(user):
            print(user)
            return JsonResponse({"message": "Success", "redirect_flag": True, "redirect": "/index"}, status=200)

        else:
            return JsonResponse({"message": "Authentication failed", "redirect_flag": False}, status=401)

    else:
        return JsonResponse({"message": "Method not allowed", "redirect_flag": False }, status=405)
