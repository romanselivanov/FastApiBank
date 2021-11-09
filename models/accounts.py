from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, Boolean, sql, Float, DateTime
from .customers import customers_table
from .accounttype import accounttypes_table


metadata = MetaData()

accounts_table = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", ForeignKey(customers_table.c.id)),
    Column("created_at", DateTime()),
    Column("rate", Float()),
    Column("type", ForeignKey(accounttypes_table.c.id)),
    Column("is_active",
        Boolean(),
        server_default=sql.expression.true(),
        nullable=False,
    ),
)