def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it'''

    global cur_hedons, cur_health
    global cur_time
    global last_activity, last_activity_duration
    global last_finished
    global bored_with_stars
    global last_star_time
    global tired
    global cur_star, cur_star_activity, star_offered_time, stars_offered
    global can_take_star
    global last_star_time
    global current_activity_duration

    current_activity_duration = 0
    star_offered_time = None
    stars_offered = 0
    cur_hedons = 0
    cur_health = 0
    cur_star = None
    cur_star_activity = None
    bored_with_stars = False
    last_activity = None
    last_activity_duration = 0
    cur_time = 0
    last_finished = -1000
    tired = False
    can_take_star = False
    last_star_time = 0


def star_can_be_taken(activity):
    '''Returns True if star can be taken for more hedons for activity activity'''

    global last_star_time, cur_time, can_take_star
    if (cur_time - last_star_time) >= 120: # Checks if stars were offered within 2 hours
        can_take_star = True
    else:
        can_take_star = False


def user_is_tired():
    '''Returns True if the user finished activity less than 2 hours ago'''

    global cur_time, last_finished
    return (cur_time - last_finished) < 120


def perform_activity(activity, duration):
    global cur_hedons, cur_health, cur_time, last_activity, last_activity_duration, current_activity_duration
    global last_finished
    if activity == last_activity:
        current_activity_duration += duration
    else:
        current_activity_duration = duration
    cur_health += estimate_health_delta(activity, duration, current_activity_duration)
    cur_hedons += estimate_hedons_delta(activity, duration)
    last_activity = activity
    last_activity_duration = duration
    cur_time += duration
    last_finished = cur_time


def get_cur_hedons():
    '''Returns the number of hedons accumulated.'''

    global cur_hedons
    return cur_hedons


def get_cur_health():
    '''Returns the number of health points accumulated.'''

    global cur_health
    return cur_health


def offer_star(activity):
    '''Simulates an offer of star for user for engaging in activity.'''

    global stars_offered, last_star_time, cur_time, bored_with_stars, cur_star_activity, can_take_star
    if not bored_with_stars: # Checks if the user is not bored with stars
        stars_offered += 1
        last_star_time = cur_time
        cur_star_activity = activity
        can_take_star = True
        if stars_offered >= 3 and (cur_time - last_star_time) < 120: # Checks if 3 stars were offered within 2 hours
            bored_with_stars = True


def most_fun_activity_minute():
    '''Returns the activity with most hedons.'''

    global cur_star_activity
    activities = ['running', 'textbooks', 'resting']
    hedons_per_minute = {}
    for activity in activities:
        hedons = estimate_hedons_delta(activity, 1)
        hedons_per_minute[activity] = hedons
    if cur_star_activity: # Checks if the star was offered to get additional hedons
        hedons_with_star = estimate_hedons_delta(cur_star_activity, 1)
        hedons_per_minute[cur_star_activity] = max(hedons_per_minute[cur_star_activity], hedons_with_star)
    most_fun_act = max(activities, key=hedons_per_minute.get)
    return most_fun_act


################################################################################
#These functions are not required, but we recommend that you use them anyway
#as helper functions

def get_effective_minutes_left_hedons(activity):
    '''Return the number of minutes during which the user will get the full
    amount of hedons for activity activity'''
    pass


def get_effective_minutes_left_health(activity):
    pass


def estimate_hedons_delta(activity, duration):
    '''Return the amount of hedon points the user would get for performing activity
    activity for duration minutes'''

    global cur_star_activity, bored_with_stars, can_take_star
    tired = user_is_tired()
    hedons = 0
    if activity == "running":
        if tired:
            hedons = (-2) * duration
        else:
            hedons = 2 * min(duration, 10) + (-2) * max(0,(duration - 10))
    elif activity == "textbooks":
        if tired:
            hedons = (-2) * duration
        else:
            hedons = 1 * min(duration, 20) + (-1) * max(0, (duration - 20))
    elif activity == "resting":
        hedons = 0
    star_used = False
    if (cur_star_activity == activity and not bored_with_stars and # Checks if can get more hedons due to stars
            not star_used and can_take_star):
        hedons += 3 * min(duration, 10)
        cur_star_activity = None
        star_used = True
    return hedons


def estimate_health_delta(activity, duration, current_activity_duration):
    '''Return the amount of health points the user would get for performing activity
    activity for duration minutes'''

    if activity == "running":
        return 3 * min(duration, 180 - (current_activity_duration - duration)) + max(0, duration - max(0, 180 - (current_activity_duration - duration)))
    elif activity == "textbooks":
        return 2 * duration
    elif activity == "resting":
        return 0
    else:
        return 0


################################################################################

if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons())            # -20 = 10 * 2 + 20 * (-2)             # Test 1
    print(get_cur_health())            # 90 = 30 * 3                          # Test 2
    print(most_fun_activity_minute())  # resting                              # Test 3
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute())  # running                              # Test 4
    perform_activity("textbooks", 30)
    print(get_cur_health())            # 150 = 90 + 30*2                      # Test 5
    print(get_cur_hedons())            # -80 = -20 + 30 * (-2)                # Test 6
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            # 210 = 150 + 20 * 3                   # Test 7
    print(get_cur_hedons())            # -90 = -80 + 10 * (3-2) + 10 * (-2)   # Test 8
    perform_activity("running", 170)
    print(get_cur_health())            # 700 = 210 + 160 * 3 + 10 * 1         # Test 9
    print(get_cur_hedons())            # -430 = -90 + 170 * (-2)              # Test 10