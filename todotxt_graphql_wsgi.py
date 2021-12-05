#!/usr/bin/env python3

import os

from ariadne import make_executable_schema
from ariadne.wsgi import GraphQL
from todotxt_graphql import type_defs, resolvers

schema = make_executable_schema(type_defs, resolvers)
application = GraphQL(schema)
