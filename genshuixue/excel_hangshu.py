#ecoding:utf-8
import sys
import xlrd
reload(sys)
sys.setdefaultencoding("utf-8")

data = xlrd.open_workbook('爱站自动外链数据.xls')
table = data.sheets()[0]
nrows = table.nrows #行数
print nrows
