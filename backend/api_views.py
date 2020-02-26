from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from .models import Campaign, Data
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

    campaign1, campaign2 = data
    fields1, fields2 = data[campaign1], data[campaign2]

    df1_fields_map = {}
    df2_fields_map = {}

    for fIdx in range(len(fields1)):
        if fields1[fIdx] != fields2[fIdx]:
            df1_fields_map[fields1[fIdx]] = f"{fields1[fIdx]}__{fields2[fIdx]}"
            df2_fields_map[fields2[fIdx]] = f"{fields1[fIdx]}__{fields2[fIdx]}"
        else:
            df1_fields_map[fields1[fIdx]] = fields1[fIdx]
            df2_fields_map[fields2[fIdx]] = fields2[fIdx]

    # finalDf = pd.DataFrame(columns=df)

    df1 = Data.objects.filter(campaign__id=campaign1).order_by("-created_at")[0]
    df1 = pd.DataFrame(df1.data)
    df2 = Data.objects.filter(campaign__id=campaign2).order_by("-created_at")[0]
    df2 = pd.DataFrame(df2.data)

    finalDf = pd.concat(
        [
            df1.rename(columns=df1_fields_map),
            df2.rename(columns=df2_fields_map),
        ],
        ignore_index=True,
    )

    print(finalDf)

    return JsonResponse({"success": True})
