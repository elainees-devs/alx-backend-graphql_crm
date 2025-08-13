# Main GraphQL schema for the CRM application.
import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

# Combine CRM queries
class Query(CRMQuery, graphene.ObjectType):
    # You can still keep a hello field for testing if you want
    hello = graphene.String(default_value="Hello, GraphQL!")

# Combine CRM mutations
class Mutation(CRMMutation, graphene.ObjectType):
    pass

# Create the main schema
schema = graphene.Schema(query=Query, mutation=Mutation)
