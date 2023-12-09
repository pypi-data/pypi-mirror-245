from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Define the GraphQL query
query = gql('''
  query {
    retrieveQID
  }
''')

# Set up the GraphQL client
transport = RequestsHTTPTransport(
    url='http://localhost:5000/api/graphql-server',  # Replace with the actual server URL
)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Send the query and receive the response
response = client.execute(query)

# Process the response
print(response)