import MySQLdb
from DBUtils.PooledDB import PooledDB
self.pool = PooledDB(MySQLdb, 5, host=writer['host'], user=writer['user'], passwd=writer['passwd'], db=writer['db'], port=writer['port'],charset='utf8')