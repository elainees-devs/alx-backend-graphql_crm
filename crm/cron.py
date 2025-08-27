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
