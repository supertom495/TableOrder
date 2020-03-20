import posOperation

def getAvtiveKeyboardItem(catIds, kbId):
	return posOperation.db_get("select cat_id, stock_id from KeyboardItem where cat_id in {} and kb_id = {};".format(catIds, kbId))