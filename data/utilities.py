from .models import PackageDetails, Company, CleanUp, Customer
from datetime import date

def save_customer(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2' or backend.name == 'github':
        customer = Customer.objects.filter(user=user)
        if len(customer) == 0:
            customer = Customer(user = user)
            customer.save()
        
def total_credits(customer):
    credits = 0
    records = PackageDetails.objects.filter(customer = customer)
    for record in records:
        credits += record.credits
    return credits
   
def update_context(context):
    cleanUpDate = CleanUp.objects.all()[0]
    if cleanUpDate.date < date.today():
        total = 0
        packageDetails = PackageDetails.objects.filter(dueDate__lt=date.today(), credits__gt=0)
        for packageDetail in packageDetails:
            total += packageDetail.credits
            packageDetail.credits = 0
            packageDetail.save()
        cleanUpDate = CleanUp(date=date.today(), credits=total)
        cleanUpDate.save()
    context['company'] = Company.objects.all()[0]
    return context
     
