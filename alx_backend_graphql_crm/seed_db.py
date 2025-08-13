import os
import django
import random

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")

# Initialize Django
django.setup()

# Import models
from crm.models import Customer, Product, Order

# ----------------- Seed Customers -----------------
customers_data = [
    {"name": "Alice Johnson", "email": "alice@example.com", "phone": "+1234567890"},
    {"name": "Bob Smith", "email": "bob@example.com", "phone": "+1987654321"},
    {"name": "Carol White", "email": "carol@example.com", "phone": None},
]

customers = []
for data in customers_data:
    customer, created = Customer.objects.get_or_create(
        email=data["email"],
        defaults={"name": data["name"], "phone": data["phone"]},
    )
    customers.append(customer)
print(f"Seeded {len(customers)} customers.")

# ----------------- Seed Products -----------------
products_data = [
    {"name": "Laptop", "price": 999.99, "stock": 10},
    {"name": "Smartphone", "price": 499.50, "stock": 20},
    {"name": "Headphones", "price": 79.99, "stock": 50},
]

products = []
for data in products_data:
    product, created = Product.objects.get_or_create(
        name=data["name"],
        defaults={"price": data["price"], "stock": data["stock"]},
    )
    products.append(product)
print(f"Seeded {len(products)} products.")

# ----------------- Seed Orders -----------------
for _ in range(5):
    customer = random.choice(customers)
    selected_products = random.sample(products, k=random.randint(1, len(products)))
    total_amount = sum(p.price for p in selected_products)

    order = Order.objects.create(customer=customer, total_amount=total_amount)
    order.products.set(selected_products)
    order.save()

print("Seeded 5 orders.")
print("Database seeding complete!")
