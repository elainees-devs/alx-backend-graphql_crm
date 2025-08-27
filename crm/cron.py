# File: crm/cron.py
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """Logs CRM heartbeat every 5 minutes"""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    # Append heartbeat to log file
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_message)

    # Optional: Verify GraphQL endpoint
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("{ hello }")  # Assuming you have a hello field in schema
        client.execute(query)
    except Exception:
        pass  # Do not fail cron if GraphQL is unresponsive

def update_low_stock():
    """Runs every 12 hours, executes UpdateLowStockProducts mutation, logs updates."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql(
        """
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                success
            }
        }
        """
    )

    try:
        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["updatedProducts"]

        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            for product in updated_products:
                f.write(f"{timestamp} - Product: {product['name']}, Stock: {product['stock']}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp} - Error updating low stock products: {e}\n")
