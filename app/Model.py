from peewee import *
from Globals import WORK_DIR
from datetime import datetime

from datetime import datetime
db   = SqliteDatabase(WORK_DIR + '/data/database/datahtml.db')
# db = SqliteDatabase("/home/repente/prog/python/kwork/selenium/betcsgo/DockerApp/app/datahtml.db") # html


class HtmlData(Model):
    m_time   = IntegerField()
    html     = BlobField()

    @staticmethod
    def auto_clear_db():
        cursor = db.execute_sql( 'SELECT count(*) FROM HtmlData' )
        quantity_rows = cursor.fetchone()[0]
        cursor = db.execute_sql( 'SELECT rowid FROM HtmlData ORDER BY rowid LIMIT 1' )
        first_row_id = cursor.fetchone()[0]
        "38888 - 18000"
        if quantity_rows > 200:
            for x in range(first_row_id, first_row_id + 101):
                HtmlData.delete().where(HtmlData.id == x).execute()

        return None

    class Meta:
        database = db


HtmlData.create_table()
if __name__ == '__main__':
    query = HtmlData.select()
    print(len(query))
# docker run --name selenium -v csbet:/usr/src/app/data --network=mynet selenium_docker
# docker run -d --name selenium -v csbet:/usr/src/app/data --network=mynet selenium_docker