from django.shortcuts import render, HttpResponse, redirect
# Controller
# Create your views here. all the urls need to be added here
def index(request):
    return HttpResponse("Hello world!")

def move_back_home(request):
    print("I am hotting the move back home")
    return redirect("/")

def first_html(request):
    return render(request, "index.html")