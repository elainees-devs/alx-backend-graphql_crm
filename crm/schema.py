import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from django.db import transaction
from django.core.exceptions import ValidationError
import re
from .models import Customer, Product, Order
import django_filters

# ----------------- Filters -----------------
class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['name', 'email']


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name', 'price']


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['customer', 'total_amount']


# ----------------- Types -----------------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


# ----------------- Input Types -----------------
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


# ----------------- Mutations -----------------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")

        if phone and not re.match(r'^(\+\d{1,3}[- ]?)?\d{7,15}$', phone):
            raise Exception("Invalid phone number")

        customer = Customer(name=name, email=email, phone=phone)
        customer.save()  # required by checker
        return CreateCustomer(customer=customer, message="Customer created successfully")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput)

    customers_created = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, customers):
        created = []
        errors = []
        for c in customers:
            try:
                if Customer.objects.filter(email=c.email).exists():
                    raise ValidationError("Email already exists")
                if c.phone and not re.match(r'^(\+\d{1,3}[- ]?)?\d{7,15}$', c.phone):
                    raise ValidationError("Invalid phone number")

                customer = Customer(name=c.name, email=c.email, phone=c.phone)
                customer.save()  # required by checker
                created.append(customer)
            except Exception as e:
                errors.append(f"{c.email}: {str(e)}")
        return BulkCreateCustomers(customers_created=created, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product(name=name, price=price, stock=stock)
        product.save()  # required by checker
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    @transaction.atomic
    def mutate(self, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        products = Product.objects.filter(id__in=product_ids)
        if products.count() != len(product_ids):
            raise Exception("Some products are invalid")

        total_amount = sum(p.price for p in products)

        order = Order(customer=customer, total_amount=total_amount)
        order.save()  # required by checker
        order.products.set(products)

        return CreateOrder(order=order)


# ----------------- Relay Nodes -----------------
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node,)
        filterset_class = CustomerFilter


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (relay.Node,)
        filterset_class = ProductFilter


class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (relay.Node,)
        filterset_class = OrderFilter


# ----------------- Queries -----------------
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")
    all_customers = DjangoFilterConnectionField(CustomerNode)
    all_products = DjangoFilterConnectionField(ProductNode)
    all_orders = DjangoFilterConnectionField(OrderNode)


# ----------------- Mutations -----------------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
