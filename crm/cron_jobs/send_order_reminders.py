from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Calculate date range (last 7 days)
seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()

# Define GraphQL query
query = gql("""
query GetRecentOrders($since: DateTime!) {
  orders(orderDate_Gte: $since) {
    id
    customer {
      email
    }
  }
}
""")

# Set up GraphQL client
transport = RequestsHTTPTransport(
    url=GRAPHQL_URL,
    verify=True,
    retries=3,
)

client = Client(
    transport=transport,
    fetch_schema_from_transport=False,
)

# Execute query
result = client.execute(query, variable_values={"since": seven_days_ago})

# Log results
log_file = "/tmp/order_reminders_log.txt"

with open(log_file, "a") as f:
    for order in result.get("orders", []):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(
            f"{timestamp} - Order ID: {order['id']}, "
            f"Customer Email: {order['customer']['email']}\n"
        )

print("Order reminders processed!")
