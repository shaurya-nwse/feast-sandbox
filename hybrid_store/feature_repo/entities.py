from feast import Entity

driver = Entity(name="driver", join_keys=["driver_id"], description="Driver ID")

customer = Entity(name="customer", join_keys=["customer_id"], description="Customer ID")
