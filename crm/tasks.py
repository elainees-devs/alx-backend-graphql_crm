# crm/tasks.py
import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query {
            allCustomers: allCustomers {
                totalCount
            }
            allOrders: allOrders {
                totalCount
                edges {
                    node {
                        totalAmount
                    }
                }
            }
        }
        """
    )

    try:
        result = client.execute(query)
        total_customers = result["allCustomers"]["totalCount"]
        total_orders = result["allOrders"]["totalCount"]
        total_revenue = sum(edge["node"]["totalAmount"] for edge in result["allOrders"]["edges"])

        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n")
    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{timestamp} - Error generating CRM report: {e}\n")
