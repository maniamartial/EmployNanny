from import_export import resources
from payment.models import Payment
from import_export import fields


class PaymentResource(resources.ModelResource):
    user = fields.Field(column_name='Employer name',
                        attribute='user__username')
    amount = fields.Field(column_name='Amount deposited', attribute='amount')
    company_commission = fields.Field(column_name='Company commission')
    salary = fields.Field(column_name='Salary for job')

    class Meta:
        model = Payment
        fields = ('user', 'amount', 'company_commission', 'salary')
        export_order = ('user', 'amount', 'salary', 'company_commission')

    def dehydrate_company_commission(self, payment):
        return round(payment.amount * 0.1, 2)

    def dehydrate_salary(self, payment):
        return round(payment.amount - (payment.amount * 0.1), 2)
