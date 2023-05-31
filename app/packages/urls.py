from django.urls import path
from packages.views.plan import PlanView
from packages.views.addon import AddonView
from packages.views.package import PackageView
from packages.views.order import OrderView
from packages.views.payment import PaymentView
from packages.views.webhook import WebhookView


urlpatterns = [
    path('product/<int:product_id>/plan', PlanView.as_view()),
    path('product/<int:product_id>/plan/<int:plan_id>/addon', AddonView.as_view()),
    path('customer/<int:customer_id>/product/<int:product_id>/package',
         PackageView.as_view()),
    path('customer/<int:customer_id>/product/<int:product_id>/order',
         OrderView.as_view()),
    path('customer/<int:customer_id>/product/<int:product_id>/order/pay',
         PaymentView.as_view()),
    path('webhook', WebhookView.as_view())
]
