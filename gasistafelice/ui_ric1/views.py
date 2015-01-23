from django.shortcuts import render_to_response

def index(request):
    context = {}
    return render_to_response("ui_ric1/index.html", context)
