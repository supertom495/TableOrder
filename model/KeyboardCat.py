import posOperation

def getActiveKeyboardCat(kbId):
    return posOperation.db_get("select cat_id, cat_code from KeyboardCat where kb_id = {};".format(kbId))