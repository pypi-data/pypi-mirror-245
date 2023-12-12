def firestore_save(db, doc_collection, data):
    """Basic save new doc and get back new ref"""
    #ToDo: 
    # - Add firebase client as parameter
    # - Add error management
    val, doc_ref = db.collection(doc_collection).add(data)
    if doc_ref:
        return True, doc_ref 
    else:
        return False, None