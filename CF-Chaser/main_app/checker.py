from . import cfapi_handler

def checkUser(cfHandle):
    profile = cfapi_handler.user_profile(cfHandle)

    if "name" not in profile:
        return False
    else:
        return True
