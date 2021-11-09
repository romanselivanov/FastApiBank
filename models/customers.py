from sqlalchemy import Column, Integer, String, Boolean, sql, MetaData, Table

metadata = MetaData()

customers_table = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(40), unique=True, index=True),
    Column("phone", String(40), unique=True, index=True),
    Column("first_name", String(100)),
    Column("last_name", String(100)),
    Column("patronymic", String(100)),
    Column("hashed_password", String()),
    Column("is_active",
        Boolean(),
        server_default=sql.expression.false(),
        nullable=False,
    ),
)