from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from .models import Campaign, Data, CustomTable
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
import pandas as pd
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


from .views import index

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
            csv_file = request.FILES['file']
            csv_pd = pd.read_csv(csv_file)
            csv_pd = csv_pd[campaign.fields.keys()]
            campaign.schedule = "Never"
            campaign.save()
            Data(campaign=campaign, data=json.loads(csv_pd.to_json(orient='records'))).save()

        campaign.save()

    return index(request)


@csrf_exempt
@login_required(login_url="/sign_in")
def create_custom_table(request):
    data = json.loads(request.POST.get("data"))
    name = data.pop("name")
    user = request.user

    cam1, cam2 = data
    col1, col2 = set(data[cam1]), set(data[cam2])
    if len(col1) != len(data[cam1]) or len(col2) != len(data[cam2]):
        raise Exception("Duplicate mapping in custom table definiton.")

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

        if fn != "pivot":
            try:
                df_col = tableDf[column].astype("float")
            except Exception as e:
                print("Invalid input in column.")
                print(e)
                return JsonResponse(
                    {
                        "result": "<span style='color: red;'>INVALID INPUT</span>",
                        "table": False,
                    }
                )

        if fn in ("sum", "mean", "median", "min", "max"):
            result = f"{fn.upper()}({column}) = {getattr(df_col, fn)()}"
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
            resultTable = tableDf.pivot_table(columns=column, aggfunc=np.sum)
            resultTable = resultTable.reset_index()

            # resultTable.columns = list(
            #     c[0] + "_" + c[1] for c in resultTable.columns
            # )
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


@csrf_exempt
@login_required(login_url="/sign_in")
def forecast(request):
    data = json.loads(request.POST.get("data"))

    customTable = CustomTable.objects.get(id=data.get("customTableId"))

    customTableDf = customTable.get_df()

    lr = LinearRegression()

    try:
        x = np.reshape(
            customTableDf[data.get("column1")].astype("float").tolist(), (-1, 1)
        )
        y = np.reshape(
            customTableDf[data.get("column2")].astype("float").tolist(), (-1, 1)
        )
        lr.fit(x, y)
        predictedVal = lr.predict(
            np.reshape([int(data.get("column1_x"))], (-1, 1))
        )
    except Exception as e:
        print("Error in input type - could not perform forecasting.")
        return JsonResponse(
            {
                "predictedVal": "<span style='color: red;'>ERROR IN FORECASTING</span>"
            }
        )
    return JsonResponse({"predictedVal": round(predictedVal[0][0], 2)})


@csrf_exempt
@login_required(login_url="/sign_in")
def export_csv(request, customTableId):
    customTable = CustomTable.objects.get(id=int(customTableId))
    customTableDf = customTable.get_df()
    # https://gist.github.com/jonperron/733c3ead188f72f0a8a6f39e3d89295d
    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = f"attachment; filename={customTable.name}.csv"
    customTableDf.to_csv(
        path_or_buf=response,
        sep=";",
        float_format="%.2f",
        index=False,
        decimal=",",
    )
    return response
