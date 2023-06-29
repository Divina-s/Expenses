from django.urls import path
from .views import HomeView,addExpenseView, Editexpense, deleteexpense, search_expenses,IncomeView,addIncomeView, Editincome,deleteIncome, search_income,expense_category_summary,stats_View, income_source_summary, statsIncome_View, DashboardView,BudgetView,addBudgetView,EditBudget,deletebudget,search_budget, export_csv, exportincome_csv,exportbudget_csv,export_excel,exportincome_excel,exportbudget_excel,export_pdf,exportincome_pdf, exportbudget_pdf
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
     path('',DashboardView, name='dashboard'),
     path('expense-index/',HomeView, name='home'),
     path('add-expenses/', addExpenseView, name='add-expense'),
     path('edit-expenses/<int:id>', Editexpense, name='edit-expense'),
     path('delete-expenses/<int:id>', deleteexpense, name='delete-expense'),
     path('searchexpenses/', csrf_exempt(search_expenses) , name='search-expenses'),
     path('income-index',IncomeView, name='income-index'),
     path('add-income/', addIncomeView, name='add-income'),
     path('edit-income/<int:id>', Editincome, name='edit-income'),
     path('delete-income/<int:id>', deleteIncome, name='delete-income'),
     path('searchincome/', csrf_exempt(search_income) , name='search-income'),
     path('expense_category_summary',expense_category_summary, name="expense_category_summary"),
     path('stats',stats_View, name="stats"),
     path('income_source_summary',income_source_summary, name="income_category_summary"),
     path('statsincome',statsIncome_View, name="stats-income"),
     path('budget-index/',BudgetView, name='budget-index'),
     path('add-budget/', addBudgetView, name='add-budget'),
     path('edit-budget/<int:id>', EditBudget, name='edit-budget'),
     path('delete-budget/<int:id>', deletebudget, name='delete-budget'),
     path('searchbudget/', csrf_exempt(search_budget) , name='search-budget'), 
     path('export_csv',export_csv, name="export-csv"),
     path('exportincome_csv',exportincome_csv, name="exportincome-csv"),
     path('exportbudget_csv',exportbudget_csv, name="exportbudget-csv"),
     path('export_excel',export_excel, name="export-excel"),
     path('exportincome_excel',exportincome_excel, name="exportincome-excel"),
     path('exportbudget_excel',exportbudget_excel, name="exportbudget-excel"),
     path('export_pdf',export_pdf, name="export-pdf"),
     path('exportincome_pdf',exportincome_pdf, name="exportincome-pdf"),
     path('exportbudget_pdf',exportbudget_pdf, name="exportbudget-pdf"),
  
  
     
]
