from django.contrib import admin
from .models import Payment, SalaryPayment, EmployerTransactions
# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'amount')


class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ('employer', 'nanny', 'amount')


class EmployerTransactionAdmin(admin.ModelAdmin):
    list_display = ('employer', 'total_deposited',
                    'total_withdrawn', 'balance')


admin.site.register(Payment, PaymentAdmin)


admin.site.register(SalaryPayment, SalaryPaymentAdmin)

admin.site.register(EmployerTransactions, EmployerTransactionAdmin)
