from pymilvus import connections, Collection
import numpy as np
connections.connect(alias="default")

collection = Collection("documents")
query_embedding = np.random.rand(1, 512).tolist()

search_results = collection.search(
    data=query_embedding,
    anns_field="embedding",
    param={"metric_type": "L2"},
    limit=3
)

for result in search_results[0]:
    print(f"Matched ID: {result.id}, Distance: {result.distance}")
