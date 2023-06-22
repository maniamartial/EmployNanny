from django.contrib import admin
from .models import Payment, SalaryPayment, EmployerTransactions, AdvancePayment
# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'amount')


class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ('employer', 'nanny', 'amount')


class EmployerTransactionAdmin(admin.ModelAdmin):
    list_display = ('employer', 'total_deposited',
                    'total_withdrawn', 'balance')


class AdvancePaymentAdmin(admin.ModelAdmin):
    list_display = ('nanny', 'employer', 'amount', 'timestamp')


admin.site.register(Payment, PaymentAdmin)


admin.site.register(SalaryPayment, SalaryPaymentAdmin)

admin.site.register(EmployerTransactions, EmployerTransactionAdmin)

admin.site.register(AdvancePayment, AdvancePaymentAdmin)
