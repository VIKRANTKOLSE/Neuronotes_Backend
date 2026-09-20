from psycopg_pool import AsyncConnectionPool

pool=AsyncConnectionPool(
    "postgresql://ravik:vicky%409999@localhost:5432/neuronotes_testing"
)

