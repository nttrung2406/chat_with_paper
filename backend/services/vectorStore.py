from pymilvus import connections, Collection

connections.connect("default", host="127.0.0.1", port="19530")
milvus_collection = Collection("documents")

def search_documents(query: str):
    results = milvus_collection.search([query], "embedding", params={"metric_type": "L2"}, limit=5)
    return results