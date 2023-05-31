import json
from django.db import models
from packages.models import Customer, Plan, Product


class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment = models.FloatField()
    subscription = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    package_data = models.JSONField()
    hash = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def get_package_data(self):
        plan_data = self.package_data["plan"]
        addon_data = self.package_data["addon"]
        frequency: int = self.package_data["frequency"]
        plan_json = json.loads(plan_data)
        addon_json = json.loads(addon_data)
        addons = [{"id": a["id"], "quantity": a["quantity"]}
                  for a in addon_json]
        plan = Plan.objects.get(pk=plan_json["id"])
        return plan, addons, frequency
