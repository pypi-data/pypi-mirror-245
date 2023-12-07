from sqlalchemy.dialects import registry


registry.register("mobio", "mobio.libs.olap.mining_warehouse.dialect", "MobioDialect")
