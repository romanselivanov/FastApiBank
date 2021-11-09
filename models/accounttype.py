from sqlalchemy import Column, Integer, String, Float, MetaData, Table

metadata = MetaData()

accounttypes_table = Table(
    "accounttypes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("currency", String(40)),
    Column("value", Float()),
)