from django.contrib import admin
from .models import Expense, Category, Income, Source
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display=('amount','description','date','author','category')
    search_fields=('description','date','category')
admin.site.register(Expense,ExpenseAdmin)



admin.site.register(Category)
class IncomeAdmin(admin.ModelAdmin):
    list_display=('amount','description','date','author','source')
    search_fields=('description','date','category')
admin.site.register(Income, IncomeAdmin)
admin.site.register(Source)