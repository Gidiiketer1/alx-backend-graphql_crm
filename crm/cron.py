from datetime import datetime
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message to confirm the CRM app is alive.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(message)

def update_low_stock():
    """
    Runs a GraphQL mutation to update low-stock products.
    """

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    mutation = gql("""
        mutation {
            updateLowStockProducts {
                success
                products {
                    name
                    stock
                }
            }
        }
    """)

    result = client.execute(mutation)

    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
        for product in result["updateLowStockProducts"]["products"]:
            log_file.write(
                f"{timestamp} {product['name']} restocked to {product['stock']}\n"
            )