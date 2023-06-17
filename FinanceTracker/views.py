from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Category, Expense, Source, Income
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from Members.models import UserPreference
import datetime

def search_expenses(request):
   if request.method=='POST':
      search_str=json.loads(request.body).get('searchText')

      expenses=Expense.objects.filter(
          amount__istartswith=search_str, author=request.user) | Expense.objects.filter(date__istartswith=search_str, author=request.user)| Expense.objects.filter(description__icontains=search_str, author=request.user) | Expense.objects.filter(category__istartswith=search_str, author=request.user)
      data=expenses.values()
      return JsonResponse(list(data), safe=False)
   
# Create your views here.
@login_required(login_url='/SignIn/')
def HomeView(request, *args, **kwargs):
    categories=Category.objects.all()
    expenses=Expense.objects.filter(author=request.user)
    paginator=Paginator(expenses,2)
    page_number=request.GET.get('page')    
    page_obj=Paginator.get_page(paginator,page_number)
    currency=UserPreference.objects.get(user=request.user).currency
    context={
       'expenses':expenses,
       'page_obj':page_obj,
       'currency':currency,
    }
    return render(request,'home.html', context)


@login_required(login_url='/SignIn/')
def addExpenseView(request):
   categories=Category.objects.all()
   context={
       'categories': categories,
       'values':request.POST,
    }




   if request.method=='GET':
       
       return render(request,'add-expense.html', context )
   if request.method =='POST':
      amount=request.POST['amount']
    
      if not amount:
         messages.error(request,'Amount is required')
         return render(request,'add-expense.html', context )
      description=request.POST['description']
      category= request.POST['category']
      date=request.POST['date_expense']
       
      Expense.objects.create(author=request.user,amount=amount, date=date, category=category,description=description ) 
      messages.success(request,'Expense added Successfully!')
      return redirect('home')
@login_required(login_url='/SignIn/')   
def Editexpense(request,id):
    expense=Expense.objects.get(pk=id)
    categories=Category.objects.all()
    context={
         'expense':expense,
         'values':expense,
         'categories': categories,
         
      }
    if request.method=="GET":
        return render(request,'editexpense.html', context)
   
    if request.method=="POST":
       amount=request.POST['amount']
    
       if not amount:
         messages.error(request,'Amount is required')
         return render(request,'edit-expense.html', context )
       description=request.POST['description']
       category= request.POST['category']
       date=request.POST['date_expense']
      
       expense.author=request.user
       expense.amount=amount
       expense.date=date
       expense.category=category
       expense.description=description 
       expense.save()
       messages.success(request,'Expense Updated Successfully!')
       return redirect('home')

@login_required(login_url='/SignIn/')
def deleteexpense(request, id):
   expense=Expense.objects.get(pk=id)
   expense.delete()
   messages.success(request, 'Expense Removed')
   return redirect('home')
       
  
@login_required(login_url='/SignIn/')
def IncomeView(request, *args, **kwargs):
    sources=Source.objects.all()
    income=Income.objects.filter(author=request.user)
    paginator=Paginator(income,2)
    page_number=request.GET.get('page')    
    page_obj=Paginator.get_page(paginator,page_number)
    currency=UserPreference.objects.get(user=request.user).currency
    context={
       'income':income,
       'page_obj':page_obj,
       'currency':currency,
    }
    return render(request,'income-index.html', context)


@login_required(login_url='/SignIn/')
def addIncomeView(request):
   sources=Source.objects.all()
   context={
       'sources': sources,
       'values':request.POST,
    }




   if request.method=='GET':
       
       return render(request,'add-income.html', context )
   if request.method =='POST':
      amount=request.POST['amount']
    
      if not amount:
         messages.error(request,'Amount is required')
         return render(request,'add-income.html', context )
      description=request.POST['description']
      source= request.POST['source']
      date=request.POST['date_income']
       
      Income.objects.create(author=request.user,amount=amount, date=date, source=source,description=description ) 
      messages.success(request,'Income added Successfully!')
      return redirect('income-index')       
   
@login_required(login_url='/SignIn/')   
def Editincome(request,id):
    income=Income.objects.get(pk=id)
    sources=Source.objects.all()
    context={
         'income':income,
         'values':income,
         'sources': sources,
         
      }
    if request.method=="GET":
        return render(request,'edit-income.html', context)
   
    if request.method=="POST":
       amount=request.POST['amount']
    
       if not amount:
         messages.error(request,'Amount is required')
         return render(request,'edit-income.html', context )
       description=request.POST['description']
       source= request.POST['source']
       date=request.POST['date_income']
      
       income.author=request.user
       income.amount=amount
       income.date=date
       income.source=source
       income.description=description 
       income.save()
       messages.success(request,'Income Updated Successfully!')
       return redirect('income-index')

@login_required(login_url='/SignIn/')
def deleteIncome(request, id):
   income=Income.objects.get(pk=id)
   income.delete()
   messages.success(request, 'Income Removed')
   return redirect('income-index')


def search_income(request):
   if request.method=='POST':
      search_str=json.loads(request.body).get('searchText')

      income=Income.objects.filter(
          amount__istartswith=search_str, author=request.user) | Income.objects.filter(date__istartswith=search_str, author=request.user)| Income.objects.filter(description__icontains=search_str, author=request.user) | Income.objects.filter(source__istartswith=search_str, author=request.user)
      data=income.values()
      return JsonResponse(list(data), safe=False)
def expense_category_summary(request):
   todays_date=datetime.date.today()
   six_months_ago=todays_date-datetime.timedelta(days=30*6)
   expenses=Expense.objects.filter(author=request.user, date__gte=six_months_ago, date__lte=todays_date)
   finalrep={}

   def get_category(expense):
      return expense.category
   
   category_list=list(set(map(get_category, expenses)))
   

   def get_expense_category_amount(category):
      amount=0
      filtered_by_category=expenses.filter(category=category)

      for item in filtered_by_category:
         amount+=item.amount

      return amount
   for x in expenses:
       for y in category_list:
          finalrep[y]=get_expense_category_amount(y)


   return JsonResponse({'expense_category_data':finalrep}, safe=False)      
def stats_View(request):
   return render(request,'stats.html', {})
def statsIncome_View(request):
   return render(request,'statsincome.html', {})

def income_source_summary(request):
   todays_date=datetime.date.today()
   six_months_ago=todays_date-datetime.timedelta(days=30*6)
   income=Income.objects.filter(author=request.user, date__gte=six_months_ago, date__lte=todays_date)
   finalrep={}

   def get_source(income):
      return income.source
   
   source_list=list(set(map(get_source, income)))
   

   def get_income_source_amount(source):
      amount=0
      filtered_by_source=income.filter(source=source)

      for item in filtered_by_source:
         amount+=item.amount

      return amount
   for x in income:
       for y in source_list:
          finalrep[y]=get_income_source_amount(y)


   return JsonResponse({'income_source_data':finalrep}, safe=False)      
