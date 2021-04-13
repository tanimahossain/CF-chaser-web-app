from . import cfapi_handler, dataProcessor

dp = dataProcessor.DP()

def checkUser(cfHandle):
    profile = cfapi_handler.user_profile(cfHandle)

    if "name" not in profile:
        return False
    else:
        return True

def dataLoadCheck():
    if 'name' not in dp.my_profile:
        return False
    else:
        return True