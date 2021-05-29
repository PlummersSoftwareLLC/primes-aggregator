from sqlalchemy import MetaData, Table, Column, String
from migrate.changeset import create_column, drop_column

meta = MetaData()

os = Column("os", String)
arch = Column("arch", String)
cpuname = Column("cpuname", String)

client = Table("clients", meta)


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    create_column(os, client)
    create_column(arch, client)
    create_column(cpuname, client)


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    drop_column(cpuname, client)
    drop_column(arch, client)
    drop_column(os, client)
