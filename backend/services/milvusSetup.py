from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
connections.connect(alias="default")
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=1024),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=512) 
]

schema = CollectionSchema(fields, description="Hybrid search collection")
collection = Collection(name="documents", schema=schema)
collection.create_index("embedding", {"metric_type": "L2", "index_type": "IVF_FLAT", "params": {"nlist": 128}})

print("Milvus Lite setup completed!")
