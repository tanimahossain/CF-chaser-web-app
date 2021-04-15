# color determination
def getColor(rating):
    if rating < 1200:
        return [128, 128, 128, 128, 128, 128]
    elif rating < 1400:
        return [12, 115, 12, 12, 115, 12]
    elif rating < 1600:
        return [15, 222, 222, 0, 222, 222]
    elif rating < 1900:
        return [0, 0, 255, 0, 0, 255]
    elif rating < 2200:
        return [214, 56, 214, 214, 56, 214]
    elif rating < 2400:
        return [255, 165, 0, 255, 165, 0]
    elif rating < 3000:
        return [255, 0, 0, 255, 0, 0]
    else:
        return [0, 0, 0, 255, 0, 0]

def profileColoring(userProfile):
    profile = userProfile

    profile['handle1'] = profile['handle'][0]
    profile['handle2'] = profile['handle'][1:]

    color = getColor(profile['cur_rating'])
    handle_color1 = color[0:3]
    handle_color2 = color[3:]
    cur_rating_color = color[3:]

    color = getColor(profile['max_rating'])
    max_rating_color = color[3:]

    profile['r1'] = handle_color1[0]
    profile['g1'] = handle_color1[1]
    profile['b1'] = handle_color1[2]

    profile['r2'] = handle_color2[0]
    profile['g2'] = handle_color2[1]
    profile['b2'] = handle_color2[2]

    profile['crr'] = cur_rating_color[0]
    profile['crg'] = cur_rating_color[1]
    profile['crb'] = cur_rating_color[2]

    profile['mrr'] = max_rating_color[0]
    profile['mrg'] = max_rating_color[1]
    profile['mrb'] = max_rating_color[2]

    return profile