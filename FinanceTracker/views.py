from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Category, Expense, Source, Income, Budget
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from Members.models import UserPreference
import datetime
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
from django.core.exceptions import ObjectDoesNotExist


def search_expenses(request):
   if request.method=='POST':
      search_str=json.loads(request.body).get('searchText')

      expenses=Expense.objects.filter(
          amount__istartswith=search_str, author=request.user) | Expense.objects.filter(date__istartswith=search_str, author=request.user)| Expense.objects.filter(description__icontains=search_str, author=request.user) | Expense.objects.filter(category__istartswith=search_str, author=request.user)
      data = expenses.values('amount', 'category', 'description', 'date')

      return JsonResponse(list(data), safe=False)
   
# Create your views here.
@login_required(login_url='/SignIn/')
def HomeView(request, *args, **kwargs):
    categories=Category.objects.all()
    expenses=Expense.objects.filter(author=request.user)
    paginator=Paginator(expenses,10)
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
         return render(request,'editexpense.html', context )
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
    paginator=Paginator(income,10)
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
   one_month_ago=todays_date-datetime.timedelta(days=31)
   expenses=Expense.objects.filter(author=request.user, date__gte=one_month_ago, date__lte=todays_date)
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
   one_month_ago=todays_date-datetime.timedelta(days=31)
   income=Income.objects.filter(author=request.user, date__gte=one_month_ago, date__lte=todays_date)
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


def DashboardView(request):
   total_income = calculate_total_income(request)
   total_expense = calculate_total_expense(request)  
   total_budget= calculate_total_budget(request)
   monthly_expense=display_monthly_expense(request)
   monthly_income=display_monthly_income(request)
   monthly_budget=display_monthly_budget(request)

 
   context = {
     'total_income': total_income,
     'total_expense':total_expense,
     'total_budget':total_budget,
     'monthly_expense':monthly_expense,
     'monthly_income':monthly_income,
     'monthly_budget':monthly_budget

    
   }

   return render(request,'dashboard.html', context)
def calculate_total_expense(request):
   user_expenses = Expense.objects.filter(author=request.user)
   total_expenses = sum(expense.amount for expense in user_expenses)
   context={
      'user_expenses': user_expenses, 
      'total_expenses': total_expenses
      }
   return total_expenses
def calculate_total_income(request):
   user_income = Income.objects.filter(author=request.user)
   total_income = sum(income.amount for income in user_income)
   context={
      'user_income': user_income, 
      'total_income': total_income
      }
   return total_income
def calculate_total_budget(request):
   user_budget = Budget.objects.filter(author=request.user)
   total_budget = sum(budget.amount for budget in user_budget)
   context={
      'user_budget': user_budget, 
      'total_budget': total_budget
      }
   return total_budget
def display_monthly_expense(request):
       author = request.user
       current_month = datetime.datetime.now().month
       user_expenses = Expense.objects.filter(author=request.user, date__month=current_month)
       monthly_expense = user_expenses.aggregate(total=Sum('amount'))
       return monthly_expense
def display_monthly_income(request):
       author = request.user
       current_month = datetime.datetime.now().month
       user_income = Income.objects.filter(author=request.user, date__month=current_month)
       monthly_income= user_income.aggregate(total=Sum('amount'))
       return monthly_income
def display_monthly_budget(request):
       author = request.user
       current_month = datetime.datetime.now().month
       user_budget = Budget.objects.filter(author=request.user, from_date__month=current_month)
       monthly_budget= user_budget.aggregate(total=Sum('amount'))
       return monthly_budget
@login_required(login_url='/SignIn/')
def BudgetView(request, *args, **kwargs):
    categories=Category.objects.all()
    budget=Budget.objects.filter(author=request.user)
    paginator=Paginator(budget,10)
    page_number=request.GET.get('page')    
    page_obj=Paginator.get_page(paginator,page_number)
    currency=UserPreference.objects.get(user=request.user).currency
    context={
       'budget':budget,
       'page_obj':page_obj,
       'currency':currency,
    }
    return render(request,'budget-index.html', context)

@login_required(login_url='/SignIn/')
def addBudgetView(request):
   categories=Category.objects.all()
   context={
       'categories': categories,
       'values':request.POST,
    }




   if request.method=='GET':
       
       return render(request,'add-budget.html', context )
   if request.method =='POST':
      amount=request.POST['amount']
    
      if not amount:
         messages.error(request,'Amount is required')
         return render(request,'add-budget.html', context )
      Name=request.POST['name']
      category= request.POST['category']
      from_date=request.POST['from_date']
      to_date=request.POST['to_date']
       
      Budget.objects.create(author=request.user,amount=amount, from_date=from_date, to_date=to_date, category=category,Name=Name ) 
      messages.success(request,'Budget added Successfully!')
      return redirect('budget-index')
@login_required(login_url='/SignIn/')   
def EditBudget(request,id):
    budget=Budget.objects.get(pk=id)
    categories=Category.objects.all()
    context={
         'budget':budget,
         'values':budget,
         'categories': categories,
         
      }
    if request.method=="GET":
        return render(request,'edit-budget.html', context)
   
    if request.method=="POST":
       amount=request.POST['amount']
    
       if not amount:
         messages.error(request,'Amount is required')
         return render(request,'edit-budget.html', context )
       Name=request.POST['name']
       category= request.POST['category']
       from_date=request.POST['from_date']
       to_date=request.POST['to_date']
    
       budget.author=request.user
       budget.amount=amount
       budget.from_date=from_date
       budget.to_date=to_date
       budget.category=category
       budget.name=Name 
       budget.save()
       messages.success(request,'Budget Updated Successfully!')
       return redirect('budget-index')

@login_required(login_url='/SignIn/')
def deletebudget(request, id):
   budget=Budget.objects.get(pk=id)
   budget.delete()
   messages.success(request, 'Budget Removed')
   return redirect('home')
       
  
def search_budget(request):
   if request.method=='POST':
      search_str=json.loads(request.body).get('searchdata')

      budget=Budget.objects.filter(
          amount__istartswith=search_str, author=request.user) | Budget.objects.filter(from_date__istartswith=search_str, author=request.user)|Budget.objects.filter(to_date__istartswith=search_str, author=request.user)| Budget.objects.filter(name__icontains=search_str, author=request.user) | Budget.objects.filter(category__istartswith=search_str, author=request.user)
      data=budget.values()
      return JsonResponse(list(data), safe=False)
def export_csv(request):   
   response= HttpResponse(content_type='text/csv')
   response['Content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.now())+'.csv'

   writer=csv.writer(response)
   writer.writerow(['Amount','Description','Category','Date'])

   expenses=Expense.objects.filter(author=request.user)

   for expense in expenses:
      writer.writerow([expense.amount,expense.description,expense.category,expense.date])
   return response   
def exportincome_csv(request):   
   response= HttpResponse(content_type='text/csv')
   response['Content-Disposition']='attachment; filename=Income'+str(datetime.datetime.now())+'.csv'

   writer=csv.writer(response)
   writer.writerow(['Amount','Description','Source','Date'])

   incomes=Income.objects.filter(author=request.user)

   for income in incomes:
      writer.writerow([income.amount,income.description,income.source,income.date])
   return response   
def exportbudget_csv(request):   
   response= HttpResponse(content_type='text/csv')
   response['Content-Disposition']='attachment; filename=Budget'+str(datetime.datetime.now())+'.csv'

   writer=csv.writer(response)
   writer.writerow(['Amount','from_date','to_date','Category','Name','period'])

   budgets=Budget.objects.filter(author=request.user)

   for budget in budgets:
      writer.writerow([budget.amount,budget.from_date,budget.to_date,budget.category,budget.Name,budget.period])
   return response   
def export_excel(request):
   response=HttpResponse(content_type='application/ms-excel')
   response['Content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.now())+'.xls'
   wb=xlwt.Workbook(encoding='utf-8')
   ws=wb.add_sheet('Expenses')
   row_num= 0
   font_style=xlwt.XFStyle()
   font_style.font.bold=True

   columns=['Amount','Description','Category','Date']

   for col_num in range(len(columns)):
      ws.write(row_num,col_num,columns[col_num],font_style)

   font_style=xlwt.XFStyle()

   rows= Expense.objects.filter(author=request.user).values_list('amount','description','category','date')
   for row in rows:
      row_num+=1
      
      for col_num in range(len(row)):
          ws.write(row_num,col_num, str(row[col_num]),font_style)
   wb.save(response)
   return response       
def exportincome_excel(request):
   response=HttpResponse(content_type='application/ms-excel')
   response['Content-Disposition']='attachment; filename=Income'+str(datetime.datetime.now())+'.xls'
   wb=xlwt.Workbook(encoding='utf-8')
   ws=wb.add_sheet('Income')
   row_num= 0
   font_style=xlwt.XFStyle()
   font_style.font.bold=True

   columns=['Amount','Description','Source','Date']

   for col_num in range(len(columns)):
      ws.write(row_num,col_num,columns[col_num],font_style)

   font_style=xlwt.XFStyle()

   rows= Income.objects.filter(author=request.user).values_list('amount','description','source','date')
   for row in rows:
      row_num+=1
      
      for col_num in range(len(row)):
          ws.write(row_num,col_num, str(row[col_num]),font_style)
   wb.save(response)
   return response       
def exportbudget_excel(request):
   response=HttpResponse(content_type='application/ms-excel')
   response['Content-Disposition']='attachment; filename=Budget'+str(datetime.datetime.now())+'.xls'
   wb=xlwt.Workbook(encoding='utf-8')
   ws=wb.add_sheet('Income')
   row_num= 0
   font_style=xlwt.XFStyle()
   font_style.font.bold=True

   columns=['Amount','from_date','to_date','Category','Name','period']

   for col_num in range(len(columns)):
      ws.write(row_num,col_num,columns[col_num],font_style)

   font_style=xlwt.XFStyle()

   rows= Budget.objects.filter(author=request.user).values_list('amount','from_date','to_date','category','Name','period')
   for row in rows:
      row_num+=1
      
      for col_num in range(len(row)):
          ws.write(row_num,col_num, str(row[col_num]),font_style)
   wb.save(response)
   return response       
def export_pdf(request):
   response=HttpResponse(content_type='application/pdf')
   response['Content-Disposition']='inline; attachment; filename=Expenses'+str(datetime.datetime.now())+'.pdf'
   response['Content-Transfer-Encoding']="binary"

   expenses= Expense.objects.filter(author=request.user)
   sum=expenses.aggregate(Sum('amount'))
   html_string=render_to_string('expenseoutput.html',{'expenses':expenses,'total':sum['amount__sum']})
   html=HTML(string=html_string)
   result= html.write_pdf()

   with tempfile.NamedTemporaryFile(delete=True) as output:
       output.write(result)
       output.flush()
       output=open(output.name,'rb')
       response.write(output.read())
   return response
def exportincome_pdf(request):
   response=HttpResponse(content_type='application/pdf')
   response['Content-Disposition']='inline; attachment; filename=Income'+str(datetime.datetime.now())+'.pdf'
   response['Content-Transfer-Encoding']="binary"

   incomes= Income.objects.filter(author=request.user)
   sum=incomes.aggregate(Sum('amount'))
   html_string=render_to_string('incomeoutput.html',{'incomes':incomes,'total':sum['amount__sum']})
   html=HTML(string=html_string)
   result= html.write_pdf()

   with tempfile.NamedTemporaryFile(delete=True) as output:
       output.write(result)
       output.flush()
       output=open(output.name,'rb')
       response.write(output.read())
   return response
def exportbudget_pdf(request):
   response=HttpResponse(content_type='application/pdf')
   response['Content-Disposition']='inline; attachment; filename=Budget'+str(datetime.datetime.now())+'.pdf'
   response['Content-Transfer-Encoding']="binary"

   budgets= Budget.objects.filter(author=request.user)
   sum=budgets.aggregate(Sum('amount'))
   html_string=render_to_string('budgetoutput.html',{'budgets':budgets,'total':sum['amount__sum']})
   html=HTML(string=html_string)
   result= html.write_pdf()

   with tempfile.NamedTemporaryFile(delete=True) as output:
       output.write(result)
       output.flush()
       output=open(output.name,'rb')
       response.write(output.read())
   return response
