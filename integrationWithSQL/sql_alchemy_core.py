""" Módulo para uso de SQLAlchemy """

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import text
from sqlalchemy.orm import Session

engine = create_engine("sqlite://")

metadata_obj = MetaData()
user = Table(
    "users",
    metadata_obj,
    Column("user_id", Integer, primary_key=True, nullable=False),
    Column("email", String(50), nullable=False),
    Column("EnderecoEmail_id", String(60)),
    Column("nickname", String(50), nullable=False),
)

user_prefs = Table(
    "user_pref",
    metadata_obj,
    Column("pref_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user_pref.user_id"), nullable=False),
    Column("pref_name", String(40), nullable=False),
    Column("pref_value", String(100)),
)

for table in metadata_obj.sorted_tables:
    print(table)


metadata_obj.create_all(engine)

metadata_db_obj = MetaData()
financial_info = Table(
    "financial_info",
    metadata_db_obj,
    Column("id", Integer, primary_key=True),
    Column("value", String(100), nullable=False),
)


print("\nInfo da tabela Users")
print(user.primary_key)
print(user_prefs.c)

print("\nInfo da tabela Financial Info")
print(financial_info.primary_key)
print(financial_info.c)


print("\n\nExecutando uma consulta SQL")
with Session(engine) as session:
    # Executar uma consulta SQL diretamente no objeto Session
    sql = text("select * from users")
    result = session.execute(sql)
    for row in result:
        print(row)


# Inserindo info na tabela users
# sql_insert = text("insert into users values(4, 'joe', 'jo@gmail.com', 'joebloggs')")
# session.execute(sql_insert)
