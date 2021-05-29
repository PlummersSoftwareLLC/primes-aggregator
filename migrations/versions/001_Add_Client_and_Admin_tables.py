from sqlalchemy import MetaData, Table, Column, Integer, String
from migrate.changeset.constraint import ForeignKeyConstraint

meta = MetaData()


admin = Table(
    "administrators", meta,
    Column("id", Integer, index=True, primary_key=True),
    Column("username", String, index=True, unique=True),
    Column("password_hash", String(128)),
)


client = Table(
    "clients", meta,
    Column("id", Integer, primary_key=True, index=True),
    Column("token", String, unique=True, index=True),
    Column("owner_id", Integer, index=True),
)


client_admin_relation = ForeignKeyConstraint(("clients.owner_id", ), ("administrators.id", ))


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    admin.create()
    client.create()

    client_admin_relation.parent = client
    client_admin_relation.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    client_admin_relation.parent = client
    client_admin_relation.drop()

    client.drop()
    admin.drop()
