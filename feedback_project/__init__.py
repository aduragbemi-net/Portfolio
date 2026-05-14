import os

# Only install PyMySQL as MySQLdb replacement when explicitly using MySQL.
# On Railway/Render, DATABASE_URL will point to PostgreSQL, so this is skipped.
if os.environ.get('USE_PYMYSQL', 'False') == 'True':
    import pymysql
    pymysql.install_as_MySQLdb()
