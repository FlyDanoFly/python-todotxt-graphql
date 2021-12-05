from pathlib import Path

from ariadne import (
    QueryType, gql, make_executable_schema, load_schema_from_path,
    ObjectType, snake_case_fallback_resolvers
)
# from ariadne.asgi import GraphQL
from ariadne.wsgi import GraphQL, GraphQLMiddleware
from extensions import QueryExecutionTimeExtension
from scalars import datetime_scalar
from queries import(
    get_modified_at_resolver,
    listTasks_resolver,
    getTask_resolver
)
from mutations import (
    commit_all_tasks_resolver, create_task_resolver, update_task_resolver, delete_task_resolver
)
from auth import authenticate_and_get_context

# Create type instance for Query type defined in our schema...
query = QueryType()

query = ObjectType("Query")
query.set_field("getModifiedAt", get_modified_at_resolver)
query.set_field("listTasks", listTasks_resolver)
query.set_field("getTask", getTask_resolver)

mutation = ObjectType("Mutation")
mutation.set_field("commitAllTasks", commit_all_tasks_resolver)
mutation.set_field("createTask", create_task_resolver)
mutation.set_field("updateTask", update_task_resolver)
mutation.set_field("deleteTask", delete_task_resolver)

# ...and assign our resolver function to its "hello" field.
# @query.field("hello")
# def resolve_hello(_, info):
#     request = info.context["request"]
#     user_agent = request.headers.get("user-agent", "guest")
#     return "Hello2, %s!" % user_agent

this_dir = Path(__file__).resolve().parent
type_defs = load_schema_from_path(this_dir / "schema.graphql")
schema = make_executable_schema(
    type_defs, query,
    mutation,
    datetime_scalar, snake_case_fallback_resolvers
)


# schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, context_value=authenticate_and_get_context, debug=True)
