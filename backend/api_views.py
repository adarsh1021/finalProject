from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from .models import Campaign, Data, CustomTable
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
import pandas as pd


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
        login(request, user)
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
            login(request, user)
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


@csrf_exempt
@login_required(login_url="/sign_in")
def create_campaign(request):
    """
    To create a new campaign
    method: POST
    POST format:
    {
        fields: [],
        crawlInterval: <daily, weekly, monthly>
    }
    """
    if request.method == "POST":
        campaign = Campaign(
            user=request.user,
            name=request.POST.get("campaignName"),
            sourceType=request.POST.get("sourceType"),
            fields={
                field: "char" for field in request.POST.get("fields").split(",")
            },
            crawlInterval=getattr(Campaign, request.POST.get("schedule")),
        )
        if campaign.sourceType == "sm":
            campaign.source = request.POST.get("socialMedia")
        elif campaign.sourceType == "api":
            campaign.source = request.POST.get("api")
        elif campaign.sourceType == "csv":
            campaign.sourceType = "csvFile"

        campaign.save()

    return JsonResponse({"success": True})


@csrf_exempt
@login_required(login_url="/sign_in")
def create_custom_table(request):
    data = json.loads(request.POST.get("data"))
    name = data.pop("name")
    user = request.user

    CustomTable.objects.create(user=user, name=name, structure=data)

    return JsonResponse({"success": True})


@csrf_exempt
@login_required(login_url="/sign_in")
def analytics(request):

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Use a POST request."}
        )
    # TODO: Cache the dataframe later
    data = json.loads(request.POST.get("data"))
    customTableId = data.get("customTableId")
    functions = data.get("functions")

    customTable = CustomTable.objects.get(id=customTableId)

    if functions == {}:
        tableJson = customTable.get_json()
        return JsonResponse(
            {"table": {"name": customTable.name, "data": tableJson}}
        )
    else:
        tableDf = customTable.get_df()
        fn = list(functions.keys())[0]
        column = functions[fn]

        if fn in ("sum", "mean", "median", "min", "max"):
            result = (
                f"{fn.upper()}({column}) = {getattr(tableDf[column], fn)()}"
            )
            return JsonResponse({"result": result, "table": False})
        elif fn in ("groupby"):
            resultTable = tableDf.groupby(column).sum()
            resultTable = resultTable.reset_index()
            return JsonResponse(
                {
                    "table": {
                        "data": resultTable.to_json(),
                        "name": f"{customTable.name}.GROUPBY({column})",
                    }
                }
            )
        elif fn in ("pivot"):
            resultTable = tableDf.pivot(columns=column)
            resultTable = resultTable.reset_index()
            resultTable.columns = list(
                c[0] + "_" + c[1] for c in resultTable.columns
            )
            return JsonResponse(
                {
                    "table": {
                        "data": resultTable.to_json(),
                        "name": f"{customTable.name}.PIVOT({column})",
                    }
                }
            )
        elif fn in ("T"):
            resultTable = tableDf.T
            resultTable = resultTable.reset_index()
            return JsonResponse(
                {
                    "table": {
                        "data": resultTable.to_json(),
                        "name": f"{customTable.name}.PIVOT({column})",
                    }
                }
            )

    # if(cache.get('table')):
    #     table = cache.get('table')
    # else:
    #     table =

    # df["fieldnmae"].sum()

