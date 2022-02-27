from django.shortcuts import render,redirect
from .models import Expense, User
from django.contrib import messages
import bcrypt
def index(request):
    return render(request,"index.html")

def process_registration(request):
    validation_messages = User.objects.user_validator(request.POST)
    if len(validation_messages) > 0:
        for key, msg in validation_messages.items():
            messages.error(request, msg)
        return redirect('/')
    password = request.POST['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        fname  = request.POST['fname'],
        lname = request.POST['lname'],
        email = request.POST['email'],
        password = hashed
    )
    request.session['logged_in_user'] = new_user.id
    return redirect('/')

def process_login(request):
    validation_messages = User.objects.login_validator(request.POST) 
    if len(validation_messages) > 0:
        for key, msg in validation_messages.items():
            messages.error(request, msg)
        return redirect('/')
    email_user = User.objects.filter(email = request.POST['email'])
    if len(email_user) < 1:
        messages.error(request, 'No emails!')
        return redirect('/')
    user_to_verify = email_user[0]
    password = request.POST['password']
    if bcrypt.checkpw(password.encode(), user_to_verify.password.encode()):
        request.session['logged_in_user'] = user_to_verify.id
        request.session['logged_user_name'] = user_to_verify.fname
        return redirect('/summary')
    messages.error(request, "Password don't match!")

    return redirect('/')

def summary(request):
    if 'logged_in_user' not in request.session:
        return redirect('/')
    my_user = User.objects.get(id=request.session['logged_in_user'])    
    context={
        'logged_in_user':my_user,
        'all_expenses':Expense.objects.all(),
        "username":request.session['logged_user_name']
    }
    return render(request,"success.html",context)
def addexpense(request):
    return render(request,'addexpense.html')

def process_expense(request):
    my_user=User.objects.get(id=request.session['logged_in_user'])
    new_expense = Expense.objects.create(
    expenseTitle=request.POST['expenseTitle'],
    amount=request.POST['amount'],
    category=request.POST['category'],
    description=request.POST['description'],
    submitter=my_user 
    )
    return redirect(f'/expenses/{new_expense.id}')

def one_expense(request,expense_id):
    context={
        'one_expense':Expense.objects.get(id=expense_id),
    }
    return render(request,"one_expense.html",context)

def delete(request,expense_id):
    to_delete = Expense.objects.get(id=expense_id)
    to_delete.delete()
    return redirect('/summary')

def editexpense(request,expense_id):
    context={
        "expense":Expense.objects.get(id=expense_id)
    }
    return render(request, "editexpense.html",context)


def logout(request):
    request.session.flush()
    return redirect('/')