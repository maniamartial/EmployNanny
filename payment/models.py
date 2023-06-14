from jobapp.models import ContractModel, DirectContract
from django.db import models
from django.contrib.auth.models import User
from users.models import NannyDetails


# This class create a table in the db called Payment that will store all details defined
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.PositiveIntegerField()
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    description = models.TextField()

    def __str__(self):
        return f"{self.user}'s Payment of {self.amount} ({self.status})"


class SalaryPayment(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    nanny = models.ForeignKey(NannyDetails, on_delete=models.CASCADE)
    #contract = models.ForeignKey(ContractModel, on_delete=models.CASCADE)
    contract = models.ForeignKey(
        ContractModel, on_delete=models.CASCADE, null=True)
    direct_contract = models.ForeignKey(
        DirectContract, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.amount


# Total deposit and total withdrawn(balance)


class EmployerTransactions(models.Model):
    employer = models.OneToOneField(User, on_delete=models.CASCADE)
    total_deposited = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_withdrawn = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Transactions for {self.employer.username}"

    def update_balance(self):
        deposits = self.employer.payment_set.filter(
            status='success').aggregate(models.Sum('amount'))
        withdrawals = self.employer.salarypayment_set.aggregate(
            models.Sum('amount'))

        total_deposited = deposits.get('amount__sum') or 0
        total_withdrawn = withdrawals.get('amount__sum') or 0

        self.total_deposited = total_deposited
        self.total_withdrawn = total_withdrawn
        self.balance = total_deposited - total_withdrawn
        self.save()
