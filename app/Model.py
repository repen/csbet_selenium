from peewee import *
from Globals import WORK_DIR, BASE_DIR
import os


with open(os.path.join( BASE_DIR, "data", "task.txt" ), "w", encoding="utf-8") as f:
    f.write("")

db  = SqliteDatabase( os.path.join( BASE_DIR, "data", "datahtml.db" ) )
db2 = SqliteDatabase( os.path.join( BASE_DIR, "data", "result_page.db" ) )


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

class ResultPage(Model):
    m_time   = IntegerField()
    m_id = IntegerField()
    data = BlobField()


    class Meta:
        database = db2

HtmlData.create_table()
ResultPage.create_table()

if __name__ == '__main__':
    query = HtmlData.select()
    print(len(query))
