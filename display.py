from flask import render_template

def display_result(result, request):
    return render_template("page.html", responses=result["responses"],
                           request=request) # Ugly hack to keep form data after submit.
