from flask import render_template

def preference_to_human(preferences):
    if preferences is None:
        return

    pref_map = {
        "drive_mode": "You want to move using car",
        "walk_mode": "You prefer to walk to destination.",
        "prefer_few_people": "You prefer places that are not crowded.",
        "prefer_quiet": "You prefer prefer places with low noise.",
        "prefer_clean_air": "You prefer places with clean air."
    }

    result = []
    for preference in preferences:
        result.append(pref_map[preference])

    return result

def display_result(result, request):
    if type(result) is str:
        return render_template("page.html", err = result, request = request)

    return render_template("page.html", recommendations = result["recommendations"],
                           preferences = preference_to_human(result["preferences"]),
                           request = request) # Ugly hack to keep form data after submit.
