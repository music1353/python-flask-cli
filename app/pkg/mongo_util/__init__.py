def get_next_seq_id(collection):
    seq_id = int()

    curs = collection.find().sort( [("id", -1)] ).limit(1)
    if curs == None:
        seq_id = 0
    else:
        for document in curs:
            seq_id = int(document['id']) + 1

    return seq_id