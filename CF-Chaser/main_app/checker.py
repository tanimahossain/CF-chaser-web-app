from . import cfapi_handler

def checkUser(cfHandle):
    profile = cfapi_handler.user_profile(cfHandle)

    if "name" not in profile:
        return False
    else:
        return True

def profile(username):
    details = cfapi_handler.user_profile(username)
    details['cur_rank']=details['cur_rank'][0].upper()+details['cur_rank'][1:]
    details['max_rank'] = details['max_rank'][0].upper() + details['max_rank'][1:]

    return details