from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from data.models import Company, Package, Customer, PackageDetails
from .forms import PurchasePackageForm
import datetime
from data.utilities import total_credits, update_context
from django.contrib import messages

# Create your views here.
@login_required
def purchase_package(request):
    customer = Customer.objects.get(user=request.user)
    packages = Package.objects.all().values()
    details = PackageDetails.objects.filter(customer = customer).values()
    message = ""
    if request.method == 'POST':
        form = PurchasePackageForm(request.POST, customer)
        if form.is_valid():
            id = int(form.cleaned_data["purchased_package"])
            package = Package.objects.get(id = id)
            if customer.purchase(package):
                packageDetails = PackageDetails(
                    customer = customer,
                    package = package,
                    credits = package.credits,
                    dueDate = datetime.date.today() + datetime.timedelta(days=package.duration)
                )
                packageDetails.save()
                messages.success(request, f"You had purchased package { package.name }.")
                return redirect(reverse('info'))
            else:
                messages.error(request, "Balance is not enought.")
        else:
            messages.error(request, "Invalid input.")
    else:
        form = PurchasePackageForm()    
        
    context = {
        'form' : form,
        'customer': customer,
        'packages': packages,
        'credits': total_credits(customer),
        'message': message,
    }
    return render(request, 'purchase_package.html', update_context(context))
