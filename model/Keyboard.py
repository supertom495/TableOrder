import posOperation

def getActiveKeyboard():
    return posOperation.db_get("select kb_id from Keyboard where kb_name2 = '{}'".format("online"))