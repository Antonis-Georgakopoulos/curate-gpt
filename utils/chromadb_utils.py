import chromadb

def get_collections(path_of_db, collection_name):
    """
    Get the collections of the chromaDB
    """
    client = chromadb.PersistentClient(path=path_of_db)

    if client.get_or_create_collection(name=collection_name).count() > 0:
        collection = client.get_or_create_collection(name=collection_name)
        print(collection)


if __name__ == "__main__":
    # get_collections('stagedb', 'elsst')

    client = chromadb.PersistentClient(path = 'db')
    collection = client.get_collection(name='elsst')
    # results = collection.query(
    #     query_texts=['mesenchymal cell'],
    #     n_results=1
    # )
    items = collection.peek()
    print(items)