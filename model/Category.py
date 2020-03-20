import posOperation

def getCategoryName(catCode):
	return posOperation.db_get("select cat_name, cat_name2 from Category where cat_code = {};".format(catCode))