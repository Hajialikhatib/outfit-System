"""MySQL adapter setup."""

try:
	import pymysql
	pymysql.install_as_MySQLdb()
	# Django expects mysqlclient >= 2.2.1; set compatible version when using PyMySQL
	pymysql.version_info = (2, 2, 7, 'final', 0)
	pymysql.__version__ = '2.2.7'
except ImportError:
	# mysqlclient may be used instead of PyMySQL
	pass


