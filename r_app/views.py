from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users, RoleActionMapping, Action, API, ApiUserMapping
from .serializers import UserSerializer, APISerializer, APIMappingSerializer
import json

# API For login the user and then generate the token


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Fetch the user from the database based on the username
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            user = None
        # Authenticate the user with the provided credentials
        if user is not None and user.password == password:
            # User credentials are valid, generate tokens
            user.generate_token()
            # Return tokens in the JSON response
            response_data = {"success": True,
                             "tokens": user.tokens}
            return JsonResponse(response_data)
        else:
            # User credentials are invalid
            response_data = {
                "success": False,
                "message": "Invalid username or password.",
            }
            return JsonResponse(response_data, status=401)
    # Return an empty JSON response for GET requests (or other methods)
    return JsonResponse({}, status=405)

# To render the login page


def login_page(request):
    return render(request, "loginpage.html")

# To render the main page


def main_page(request):
    return render(request, "main.html")

# To render user page


def users_page(request):
    return render(request, "user.html")

# To render the api page


def api_page(request):
    return render(request, "api.html")

# TO CREATE THE USER


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization')[7:]
        # print(token)
        request_body = json.loads(request.body)
        # print(request_body)
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        if found_user is None:
            return JsonResponse({"message": "Unauthorized"})
        user = Users.objects.get(id=found_user.id)  # type: ignore
        if user and user.role.role_name == "ADMIN":
            # Check if the Admin role has the permission to create a user
            create_user_action = Action.objects.get(action_name="ADD_USER")
            if RoleActionMapping.objects.filter(role=user.role, action=create_user_action).exists():
                # If the user has the required permission, allow them to create a new user
                serializer = UserSerializer(data=request_body)
                # print(serializer)
                if serializer.is_valid():
                    # Save the user
                    serializer.save()
                    return JsonResponse(
                        {"message": "User created successfully."}, status=201
                    )
                else:
                    return JsonResponse(serializer.errors, status=400)
        else:
            # If the user is not an admin, return a permission denied response
            return JsonResponse(
                {"message": "You do not have permission to create a user."}, status=403
            )
    else:
        return JsonResponse(
            {"message": "Use post method to create a user"}
        )

# TO UPDATE THE USER


@csrf_exempt
def update_user(request):
    if request.method == 'PUT':
        token = request.headers.get('Authorization')[7:]
        print(token)
        request_body = json.loads(request.body)
        print(request_body)
        update_body = {"username": request_body["username"],
                       "password": request_body["password"], "role": request_body['role']}
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        print(found_user)
        user = Users.objects.get(id=found_user.id)
        if found_user is None:
            return JsonResponse({"message": "Unauthorized"})
        if user.role.role_name == "ADMIN":
            # Check if the Admin role has the permission to update a user
            update_user_action = Action.objects.get(action_name="UPDATE_USER")
            if RoleActionMapping.objects.filter(role=1, action=update_user_action).exists():
                try:
                    user_to_update = Users.objects.get(id=request_body['id'])
                except Users.DoesNotExist:
                    return JsonResponse({"message": "User not found."}, status=404)
                serializer = UserSerializer(user_to_update, data=update_body)
                if serializer.is_valid():
                    # Save the updated user
                    serializer.save()
                    return JsonResponse(
                        {"message": "User updated successfully."}, status=200
                    )
                else:
                    return JsonResponse(serializer.errors, status=400)
        else:
            # If the user is not an admin, return a permission denied response
            return JsonResponse(
                {"message": "You do not have permission to update a user."}, status=401
            )
    else:
        return JsonResponse(
            {"message": "Use PUT method to update a user"}
        )

# TO DELETE USER


@csrf_exempt
def delete_user(request):
    if request.method == 'DELETE':
        token = request.headers.get('Authorization')[7:]
        # print(token)
        request_body = json.loads(request.body)
        # print(request_body,type(request_body['id']))
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        if found_user is None:
            return JsonResponse({"message": "Unauthorized"})
        user = Users.objects.get(id=found_user.id)
        if user.role.role_name == "ADMIN":
            # Check if the Admin role has the permission to update a user
            update_user_action = Action.objects.get(action_name="REMOVE_USER")
            if RoleActionMapping.objects.filter(role=1, action=update_user_action).exists():
                try:
                    user_to_update = Users.objects.get(id=request_body['id'])
                except Users.DoesNotExist:
                    return JsonResponse({"message": "User not found."}, status=404)
                user_to_update.delete()
                return JsonResponse({"message": "User deleted successfully."}, status=200)
        else:
            # If the user is not an admin, return a permission denied response
            return JsonResponse(
                {"message": "You do not have permission to delete a user."}, status=401
            )
    else:
        return JsonResponse(
            {"message": "Use DELETE method to delete a user"}
        )

# TO CRETAE API


@csrf_exempt
def create_api(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization')[7:]
        print(token)
        request_body = json.loads(request.body)
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        # print(found_user)
        if found_user is None:
            return JsonResponse({"message": "Unauthorized"})
        user = Users.objects.get(id=found_user.id)
        # Check if the user is an admin or a regular user
        add_api_action = Action.objects.get(action_name="ADD_API")
        if RoleActionMapping.objects.filter(
                role=user.role, action=add_api_action).exists():
            # If the user has the required permission to create an API, proceed with creation
            serializer = APISerializer(
                data=request_body, context={"request": request})
            if serializer.is_valid():
                # Save the new API object with the authenticated user in the allowed_users field
                serializer.save()
                return JsonResponse(
                    {"message": "API object created successfully."}, status=201
                )
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            # If the user doesn't have the required permission, return a permission denied response
            return JsonResponse(
                {"message": "You do not have permission to create an API object."},
                status=403,
            )
    else:
        return JsonResponse(
            {"message": "Use Post method to create a api"}
        )

# TO UPDATE THE API


@csrf_exempt
def update_api(request):
    if request.method == 'PUT':
        token = request.headers.get('Authorization')[7:]
        request_body = json.loads(request.body)
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        user = Users.objects.get(id=found_user.id)
        if found_user is None:
            return JsonResponse({"message": "Unauthorized"})
        update_api = Action.objects.get(action_name="UPDATE_API")
        if RoleActionMapping.objects.filter(role=user.role, action=update_api).exists():
            try:
                api_to_update = API.objects.get(id=request_body['id'])
            except API.DoesNotExist:
                return JsonResponse({"message": "API not found."}, status=404)
            serializer = APISerializer(api_to_update, data=request_body)
            if serializer.is_valid():
                # Save the updated user
                serializer.save()
                return JsonResponse(
                    {"message": "API updated successfully."}, status=200
                )
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse(
                {"message": "You do not have permission to update a API."}, status=401
            )
    else:
        return JsonResponse(
            {"message": "Use DELETE method to UPDATE a API"}
        )

# TO DELETE API


@csrf_exempt
def delete_api(request):
    if request.method == 'DELETE':
        token = request.headers.get('Authorization')[7:]
        # print(token)
        request_body = json.loads(request.body)
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        # print(found_user)
        user = Users.objects.get(id=found_user.id)
        if found_user is None:
            return JsonResponse({"message": "Unauthorized"})
        update_user_action = Action.objects.get(action_name="REMOVE_API")
        if RoleActionMapping.objects.filter(role=user.role, action=update_user_action).exists():
            try:
                user_to_update = API.objects.get(id=request_body['id'])
            except API.DoesNotExist:
                return JsonResponse({"message": "API not found."}, status=404)
            if not ApiUserMapping.objects.filter(api_id=request_body['id']):
                user_to_update.delete()
            else:
                return JsonResponse({"message": "You cannot delete the api"}, status=403)
            return JsonResponse({"message": "API deleted successfully."}, status=200)
        else:
            # If the user is not an admin, return a permission denied response
            return JsonResponse(
                {"message": "You do not have permission to delete a api."}, status=401
            )
    else:
        return JsonResponse(
            {"message": "Use DELETE method to delete a API"}
        )

# VIEW API


@csrf_exempt
def view_api(request):
    if request.method == 'GET':
        token = request.headers.get('Authorization')[7:]
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        if found_user is None:
            return JsonResponse({"message": "Unauthorized"})
        all_api = API.objects.all()
        serializer = APISerializer(all_api, many=True)
        serialized_data = serializer.data
        for api_data in serialized_data:
            api_id = api_data['id']
            users_mapped = ApiUserMapping.objects.filter(
                api_id=api_id).values_list('user__username', 'user__role')
            if len(users_mapped) > 0:
                api_data['users_mapped'] = list(users_mapped)
            else:
                api_data['users_mapped'] = None
        # print(serialized_data)
        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse(
            {"message": "Use GET method to GET a API"}
        )

# VIEW USERS


@csrf_exempt
def view_user(request):
    if request.method == 'GET':
        token = request.headers.get('Authorization')[7:]
        print(token)
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        print(found_user)
        user = Users.objects.get(id=found_user.id)
        if user and user.role.role_name == "ADMIN":
            all_user = Users.objects.all()
            serializer = UserSerializer(all_user, many=True)
            # Sort the serialized data based on the 'id' attribute in descending order
            sorted_serializer_data = sorted(
                serializer.data, key=lambda x: x['id'], reverse=False)

            return JsonResponse(sorted_serializer_data, safe=False)
        else:
            return JsonResponse(
                {"message": "You do not have permission to view users"}, status=401
            )
    else:
        return JsonResponse(
            {"message": "Use GET method to GET a API"}
        )

# POST TO Fetch USERS BY ID


@csrf_exempt
def get_userById(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization')[7:]
        # print(token)
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        # print(found_user)
        # print(request.body)
        request_body = json.loads(request.body)
        user = Users.objects.get(id=found_user.id)
        if user and user.role.role_name == "ADMIN":
            all_user = Users.objects.get(id=request_body['id'])
            serializer = UserSerializer(all_user)
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(
                {"message": "You do not have permission to view users"}, status=401
            )
    else:
        return JsonResponse(
            {"message": "Use GET method to GET a API"}
        )

# Post to Fetch API BY ID


@csrf_exempt
def get_apiById(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization')[7:]
        # print(token)
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        # print(found_user)
        # print(request.body)
        request_body = json.loads(request.body)
        user = Users.objects.get(id=found_user.id)
        if user and user.role.role_name == "ADMIN" or user.role.role_name == "USER":
            all_api = API.objects.get(id=request_body['id'])
            serializer = APISerializer(all_api)
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(
                {"message": "You do not have permission to view api"}, status=401
            )
    else:
        return JsonResponse(
            {"message": "Use Post  method to GET a API"}
        )

# Mapping the api with the user


@csrf_exempt
def mappingAPI_User(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization')[7:]
        found_user = Users.objects.filter(
            tokens__contains={"access": token}).first()
        user = Users.objects.get(id=found_user.id)
        if found_user is None:
            return JsonResponse({"message": "Unauthorized"})
        if user.role.role_name == "ADMIN":
            update_user_action = Action.objects.get(action_name="MAP_API")
            if RoleActionMapping.objects.filter(role=user.role, action=update_user_action).exists():
                try:
                    data = json.loads(request.body)
                    api_id = data.get("api_id")
                    user_ids = data.get("user_id")
                    print(user_ids)
                    api = API.objects.get(id=api_id)
                    users = Users.objects.filter(id__in=user_ids)
                    print(users)
                    # Create or update the ApiUserMapping entry using the serializer
                    # Pass the queryset directly
                    mapping_data = [{'api': api.id, 'user': user.id}
                                    for user in users]
                    for entry in mapping_data:
                        print(entry)
                        serializer = APIMappingSerializer(data=entry)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            return JsonResponse(serializer.errors, status=400)
                    return JsonResponse({"message": "Mapped Successfully!!!"})
                except (json.JSONDecodeError, API.DoesNotExist, Users.DoesNotExist) as e:
                    return JsonResponse({"message": "Invalid data or API/User not found"}, status=400)
        else:
            return JsonResponse({"message": "Unauthorized"}, status=401)
        return JsonResponse({"message": "Mapped Successfully!!!"})
    else:
        return JsonResponse({"message": "Use Post method to Map API"})
