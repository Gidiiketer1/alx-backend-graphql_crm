from datetime import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql',
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql("""
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """)

    result = client.execute(query)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = (
        f"{timestamp} - Report: "
        f"{result['totalCustomers']} customers, "
        f"{result['totalOrders']} orders, "
        f"{result['totalRevenue']} revenue\n"
    )

    with open("/tmp/crm_report_log.txt", "a") as log_file:
        log_file.write(log_line)
