#!/usr/bin/env python3
# File: crm/cron_jobs/send_order_reminders.py
# Description: Queries GraphQL endpoint for pending orders in the last 7 days and logs reminders

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate last 7 days
today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)

# GraphQL query
query = gql(
    """
    query ($startDate: Date!) {
      orders(filter: {orderDate_Gte: $startDate}) {
        id
        customer {
          email
        }
      }
    }
    """
)

params = {"startDate": seven_days_ago.isoformat()}

try:
    result = client.execute(query, variable_values=params)
    orders = result.get("orders", [])

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("/tmp/order_reminders_log.txt", "a") as f:
        for order in orders:
            order_id = order["id"]
            email = order["customer"]["email"]
            f.write(f"{timestamp} - Order ID: {order_id}, Customer Email: {email}\n")

    print("Order reminders processed!")

except Exception as e:
    print(f"Error querying GraphQL endpoint: {e}")
