from .models import PackageDetails, Company

def total_coupon(customer):
    coupon = 0
    records = PackageDetails.objects.filter(customer = customer)
    for record in records:
        coupon += record.coupon
    return coupon
   
def update_context(context):
    context['company'] = Company.objects.all()[0]
    return context
     
