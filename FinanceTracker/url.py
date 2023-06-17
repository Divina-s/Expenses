from django.urls import path
from .views import HomeView,addExpenseView, Editexpense, deleteexpense, search_expenses,IncomeView,addIncomeView, Editincome,deleteIncome, search_income,expense_category_summary,stats_View, income_source_summary, statsIncome_View
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
     path('',HomeView, name='home'),
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
]
