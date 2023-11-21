
from ninja import Router
# from stuff_manager_api.stuff_manager.authentication.clerk import ClerkBearerAuth
from stuff_manager.authentication.clerk import ClerkBearerAuth

test_auth_router = Router(auth=ClerkBearerAuth())
# @test_auth_router.get("/")

# @test_auth_router.get("/")
def auth(request):
    print(request)
    print(dir(request))
    print(request.user)
    print(type(request.user))
    print(request.auth)
    print(request.auth[0])
    print(type(request.auth[0]))
    return {"result": "hello"}

test_auth_router.add_api_operation("/", ['GET'], auth)
