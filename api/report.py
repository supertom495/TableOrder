import xlwt
import requests
import json
import yaml

with open('./setting/flask.yaml') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

api_url_base = 'http://' + data['ServerName'] + ':5001/api/v1/report/report?date=20200630'

headers = {'Content-Type': 'application/json'}


def getReport():
	response = requests.get(api_url_base, headers=headers)

	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return None


reportDetail = getReport()

print(api_url_base)
print(reportDetail)


# 设置表格样式
def set_style(name, height, bold=False):
	style = xlwt.XFStyle()
	font = xlwt.Font()
	font.name = name
	font.bold = bold
	font.color_index = 4
	font.height = height
	style.font = font
	return style


# 写Excel
# def write_excel():
# 	f = xlwt.Workbook()
# 	sheet1 = f.add_sheet('学生',cell_overwrite_ok=True)
# 	row0 = ["姓名","年龄","出生日期","爱好"]
# 	colum0 = ["张三","李四","恋习Python","小明","小红","无名"]
# 	#写第一行
# 	for i in range(0,len(row0)):
# 		sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
# 	#写第一列
# 	for i in range(0,len(colum0)):
# 		sheet1.write(i+1,0,colum0[i],set_style('Times New Roman',220,True))
#
# 	sheet1.write(1,3,'2006/12/12')
# 	sheet1.write_merge(6,6,1,3,'未知')#合并行单元格
# 	sheet1.write_merge(1,2,3,3,'打游戏')#合并列单元格
# 	sheet1.write_merge(4,5,3,3,'打篮球')
#
# 	f.save('159sadf83' + '.xls')

def write_excel():
	f = xlwt.Workbook()
	sheet1 = f.add_sheet('report', cell_overwrite_ok=True)

	sheet1.write_merge(0, 0, 0, 10, 'report')
	sheet1.write_merge(1, 1, 0, 10, data['StoreName'] + '  ' + '20200630')

	sheet1.write_merge(2, 3, 0, 2, 'Summary Income')
	sheet1.write_merge(2, 3, 3, 4, 'Total')
	sheet1.write_merge(2, 3, 5, 10, 'Summary Details')

	summary = reportDetail['data']['summary']
	sheet1.write_merge(4, 4, 0, 2, 'Gross Income with Tax & Discount')
	sheet1.write_merge(4, 4, 3, 4, summary['totalInc'])
	sheet1.write_merge(5, 5, 0, 2, 'Net Income with Tax')
	sheet1.write_merge(5, 5, 3, 4, summary['totalInc'])
	sheet1.write_merge(6, 6, 0, 2, 'Net Income without Tax')
	sheet1.write_merge(6, 6, 3, 4, summary['totalEx'])

	# ---
	sheet1.write_merge(7, 9, 0, 1, 'Net Income with Tax')
	sheet1.write_merge(7, 7, 2, 2, 'Summary')
	sheet1.write_merge(7, 7, 3, 4, summary['totalInc'])
	sheet1.write_merge(8, 8, 2, 2, 'Take Away')
	sheet1.write_merge(8, 8, 3, 4, summary['takeAwayInc'])
	sheet1.write_merge(9, 9, 2, 2, 'Dine In')
	sheet1.write_merge(9, 9, 3, 4, summary['dineInInc'])

	# ---
	sheet1.write_merge(10, 12, 0, 1, 'Net Income without Tax')
	sheet1.write_merge(10, 10, 2, 2, 'Summary')
	sheet1.write_merge(10, 10, 3, 4, summary['totalEx'])
	sheet1.write_merge(11, 11, 2, 2, 'Take Away')
	sheet1.write_merge(11, 11, 3, 4, summary['takeAwayEx'])
	sheet1.write_merge(12, 12, 2, 2, 'Dine In')
	sheet1.write_merge(12, 12, 3, 4, summary['dineInEx'])\

	# ---
	payment = reportDetail['data']['payment']
	sheet1.write_merge(13, 13 + len(payment) -1, 0, 0, 'Income')
	count = 0
	for item in payment:
		sheet1.write_merge(13 + count, 13 + count, 1, 1, count + 1)
		sheet1.write_merge(13 + count, 13 + count, 2, 2, item)
		sheet1.write_merge(13 + count, 13 + count, 3, 3, payment[item])
		count += 1

	# ---
	table = reportDetail['data']['table']

	sheet1.write_merge(4, 9, 5, 6, 'No. of Covers / No. of Delivery')
	sheet1.write_merge(4, 4, 7, 7, 'Restaurant No. of Tables')
	sheet1.write_merge(4, 4, 8, 8, table['totalNumberOfTable'])
	sheet1.write_merge(4, 4, 9, 9, 'Restaurant Take Away')
	sheet1.write_merge(4, 4, 10, 10, table['takeAway'])

	sheet1.write_merge(5, 5, 7, 7, 'Covers Before 5pm')
	sheet1.write_merge(5, 5, 8, 8, table['coversBefore5'])
	sheet1.write_merge(6, 6, 7, 7, 'Covers After 5pm')
	sheet1.write_merge(6, 6, 8, 8, table['coversAfter5'])

	sheet1.write_merge(7, 7, 7, 7, 'Total Covers')
	sheet1.write_merge(7, 7, 8, 8, table['totalNumberOfCovers'])

	sheet1.write_merge(8, 8, 7, 7, 'Restaurant Average Check Per Person')
	sheet1.write_merge(8, 8, 8, 8, table['averageCheckPerPerson'])

	sheet1.write_merge(9, 9, 7, 7, 'Restaurant Covers Per Table')
	sheet1.write_merge(9, 9, 8, 8, table['averageCoverPerTable'])

	sheet1.write_merge(7, 8, 9, 9, 'Average Check Per Take Away')
	sheet1.write_merge(7, 8, 10, 10, table['averageCheckPerTakeAway'])


	# -------------------------------------
	sheet2 = f.add_sheet('discount', cell_overwrite_ok=True)
	discount = reportDetail['data']['discount']
	sheet2.write_merge(0, 0, 0, 0, 'discountPercentage')
	sheet2.write_merge(0, 0, 1, 1, 'original price')
	sheet2.write_merge(0, 0, 2, 2, 'price after discount')
	sheet2.write_merge(0, 0, 3, 3, 'datetime')
	sheet2.write_merge(0, 0, 4, 4, 'product')
	sheet2.write_merge(0, 0, 5, 5, 'quantity')
	sheet2.write_merge(0, 0, 6, 6, 'tablecode')

	count = 1
	for item in discount:
		sheet2.write_merge(count, count, 0, 0, str(float(item['discountPercentage']) * 100 ) + '%')
		sheet2.write_merge(count, count, 1, 1, item['originalPrice'])
		sheet2.write_merge(count, count, 2, 2, item['discountPrice'])
		sheet2.write_merge(count, count, 3, 3, item['discountDatetime'])
		sheet2.write_merge(count, count, 4, 4, item['discountProduct'])
		sheet2.write_merge(count, count, 5, 5, item['discountQuantity'])
		sheet2.write_merge(count, count, 6, 6, item['discountTableCode'])
		count += 1

	f.save('20200630' + '.xls')


if __name__ == '__main__':
	write_excel()
