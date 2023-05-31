from django.db import migrations
from django.db.models import Q


def insert_payment_services(apps, schema_editor):
    PaymentService = apps.get_model("packages", "PaymentService")
    db_alias = schema_editor.connection.alias
    PaymentService.objects.using(db_alias).bulk_create(
        [
            PaymentService(name="OpenpayService"),
            PaymentService(name="ManualService")
        ]
    )


def insert_mail_config(apps, schema_editor):
    MailConfig = apps.get_model("packages", "MailConfig")
    db_alias = schema_editor.connection.alias
    MailConfig.objects.using(db_alias).bulk_create(
        [
            MailConfig(mail_from="contact@testsystems.com", mail_cc="payments@testsystems.com", subject="Thanks for buying!",
                       message="Thanks for buying your plan in Test Systems", website="www.testsystems.com", image="https://s3-us-west-2.amazonaws.com/payment/img/test-logo.png")
        ]
    )


def insert_products(apps, schema_editor):
    MailConfig = apps.get_model("packages", "MailConfig")
    mail_config = MailConfig.objects.get(id=1)
    Product = apps.get_model("packages", "Product")
    db_alias = schema_editor.connection.alias
    Product.objects.using(db_alias).bulk_create(
        [
            Product(code="PRODUCT_A", name="Product A",
                    mail_config=mail_config),
            Product(code="PRODUCT_B", name="Product B",
                    mail_config=mail_config),
        ]
    )


def insert_addons(apps, schema_editor):
    Addon = apps.get_model("packages", "Addon")
    db_alias = schema_editor.connection.alias
    Addon.objects.using(db_alias).bulk_create(
        [
            Addon(code="ADDRFCS", name="Additional RFCs", display_name="Additional RFCs",
                  included=False, type="VAR", quantity=0, unit_of_measure="RFC", monthly_price=15, yearly_price=150),
            Addon(code="TAXMOD", name="Tax Module", display_name="Tax Module",
                  included=False, type="FIX", quantity=1, unit_of_measure="MOD", monthly_price=10, yearly_price=100),
            Addon(code="TRVMOD", name="Travel Module", display_name="Travel Module",
                  included=False, type="FIX", quantity=1, unit_of_measure="MOD", monthly_price=10, yearly_price=100),
            Addon(code="ASTMOD", name="Asset Module", display_name="Asset Module",
                  included=False, type="FIX", quantity=1, unit_of_measure="MOD", monthly_price=10, yearly_price=100),
            Addon(code="ADDSTMP", name="Additional Stamps", display_name="Additional Stamps",
                  included=False, type="VAR", quantity=0, unit_of_measure="STMP", monthly_price=1, yearly_price=10),
        ]
    )


def insert_plans(apps, schema_editor):
    Addon = apps.get_model("packages", "Addon")
    Plan = apps.get_model("packages", "Plan")
    Product = apps.get_model("packages", "Product")

    producta = Product.objects.get(id=1)
    productb = Product.objects.get(id=2)

    addons_producta = Addon.objects.filter(
        Q(unit_of_measure="RFC") | Q(unit_of_measure="MOD"))
    addons_productb = Addon.objects.filter(unit_of_measure="STMP")

    db_alias = schema_editor.connection.alias
    Plan.objects.using(db_alias).bulk_create(
        [
            Plan(code="PLAN1", name="Plan 1", display_name="Plan 1", quantity=1,
                 unit_of_measure="RFC", monthly_price=100, yearly_price=1000, status="A", product=producta),
            Plan(code="PLAN2", name="Plan 2", display_name="Plan 2", quantity=5,
                 unit_of_measure="RFC", monthly_price=150, yearly_price=1500, status="A", product=producta),
            Plan(code="PLAN3", name="Plan 3", display_name="Plan 3", quantity=15,
                 unit_of_measure="RFC", monthly_price=200, yearly_price=2000, status="A", product=producta),
            Plan(code="PLAN1", name="Plan 1", display_name="Plan 1", quantity=100,
                 unit_of_measure="STMP", monthly_price=50, yearly_price=500, status="A", product=productb),
            Plan(code="PLAN2", name="Plan 2", display_name="Plan 2", quantity=200,
                 unit_of_measure="STMP", monthly_price=75, yearly_price=750, status="A", product=productb),
            Plan(code="PLANPER", name="Plan personalizado", display_name="Plan personalizado", quantity=0,
                 unit_of_measure="STMP", monthly_price=100, yearly_price=1000, status="A", product=productb)
        ]
    )

    plans_producta = Plan.objects.filter(product=producta)
    for p in plans_producta:
        p.addons.set(addons_producta)

    custom_plan_productb = Plan.objects.get(code="PLANPER")
    custom_plan_productb.addons.set(addons_productb)


def insert_customers(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Customer = apps.get_model("packages", "Customer")

    Customer.objects.using(db_alias).create(
        email="hello@gmail.com",
        last_name="World",
        first_name="Hello",
        fiscal_name="ITS A HELLO",
        phone="5555 5555",
        postal_code="5436",
        state="CAL",
        city="LA",
        street="1 Ray",
        residence="1-65",
        country="US",
        internal_number="321321",
        external_number="123123")

    Customer.objects.using(db_alias).create(
        email="test@gmail.com",
        last_name="Test",
        first_name="Its",
        fiscal_name="ITS A TEST",
        phone="7777 7777",
        postal_code="3645",
        state="CAL",
        city="LA",
        street="1 Wins",
        residence="51-01",
        country="US",
        internal_number="456456",
        external_number="654654")


def insert_packages(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Customer = apps.get_model("packages", "Customer")
    # Product = apps.get_model("packages", "Product")
    Plan = apps.get_model("packages", "Plan")
    Addon = apps.get_model("packages", "Addon")
    Package = apps.get_model("packages", "Package")
    PackageAddon = apps.get_model("packages", "PackageAddon")

    plan1 = Plan.objects.get(pk=1)
    addons_producta = Addon.objects.filter(unit_of_measure="RFC")
    customer1 = Customer.objects.get(pk=1)

    package1 = Package.objects.using(db_alias).create(
        customer=customer1,
        frequency=1,
        plan=plan1,
        payment_method="CARD",
        start_date="2023-04-01",
        end_date="2023-05-01",
        status="A",
        order="1_20230401_051058",
        created_at="2022-04-01 05:10:58")

    for a in addons_producta:
        if a.type == "VAR":
            PackageAddon.objects.using(db_alias).create(
                package=package1, addon=a, quantity=5)
        else:
            PackageAddon.objects.using(db_alias).create(
                package=package1, addon=a, quantity=a.quantity)


def insert_service_identifiers(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Customer = apps.get_model("packages", "Customer")
    PaymentService = apps.get_model("packages", "PaymentService")
    ServiceIdentifier = apps.get_model("packages", "ServiceIdentifier")

    customer = Customer.objects.get(pk=1)
    payment_service = PaymentService.objects.get(pk=1)
    ServiceIdentifier.objects.using(db_alias).create(
        customer=customer,
        payment_service=payment_service,
        identifier="ajjnvx6yizzfyotpa7fn")


operations = [
    migrations.RunPython(insert_payment_services),
    migrations.RunPython(insert_mail_config),
    migrations.RunPython(insert_products),
    migrations.RunPython(insert_addons),
    migrations.RunPython(insert_plans),
    migrations.RunPython(insert_customers),
    migrations.RunPython(insert_packages),
    migrations.RunPython(insert_service_identifiers),
]
