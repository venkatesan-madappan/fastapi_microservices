
'''
https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-working-with-transactions
https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1
'''
#SQL Alchemy Imports
from sqlalchemy import create_engine, text, URL
from sqlalchemy import text, Column, Integer

#central source of connections to a particular database
url_object = URL.create("postgresql+psycopg2",username="venkatesan",
    password="Sriviviji@101",host="localhost",port="5432", database="fcms")
db_engine = create_engine(url_object, echo=True)

'''
with the Core directly, the Connection object is how all interaction with the database is done. 
Textual SQL is created with a construct called text() 

when the connection is released, a ROLLBACK is emitted to end the transaction. 
The transaction is not committed automatically; 
'''
with db_engine.connect() as conn:
    trans = conn.begin()
    try:
        # conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        trans.commit()  # commit using the transaction
    except:
        trans.rollback()
        raise

# with db_engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table"))
#     # for row in result:
#     for row in result.mappings():
#         # print(f"x: {row.x}  y: {row.y}") # Using Attribute names
#         # print(f"x: {row[0]}  y: {row[1]}") # Using Index
#         print(f" X : {row["x"]}, Y : {row["y"]}") # using mappings

'''
Sending Parameters to execute
'''
# with db_engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
#     for row in result:
#         print(f"x: {row.x}  y: {row.y}")

'''
Sending Multiple Parameters
'''
# with db_engine.connect() as conn:
#     conn.execute(
#         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
#     )
#     conn.commit()
'''
ORM - Session Basics

the Session establishes all conversations with the database and represents a “holding zone” 
for all the objects which you’ve loaded or associated with it during its lifespan.

It provides the interface where SELECT and other queries are made that will return and modify ORM-mapped objects. 

The ORM objects themselves are maintained inside the Session, inside a structure called the identity map - a 
data structure that maintains unique copies of each object, where “unique” means “only one object with a 
particular primary key”.

The ORM objects maintained by a Session are instrumented such that whenever an attribute or a collection is modified in the 
Python program, a change event is generated which is recorded by the Session. Whenever the database is about to be queried, 
or when the transaction is about to be committed, the Session first flushes all pending changes stored in memory to the 
database. This is known as the unit of work pattern.
'''

'''
Opening and Closing a Session
'''

from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()

class MyModel(Base):
    __tablename__ = "sess_table"
    id = Column(Integer, primary_key=True) 
    x = Column(Integer)
    y = Column(Integer)

Base.metadata.create_all(db_engine)

'''
with Session(db_engine) as session:
    session.add(MyModel(id=1, x=55, y=56))
    session.add(MyModel(id=2, x=65, y=66))
    session.commit()
'''
'''
Session.commit() is optional, and is only needed if the work we’ve done with the Session includes new data to be 
persisted to the database. 
'''
'''
Framing out a begin / commit / rollback block
'''

'''
# verbose version of what a context manager will do
with Session(db_engine) as session:
    session.begin()
    try:
        session.add(MyModel(id=3, x=15, y=16))
        session.add(MyModel(id=4, x=25, y=26))
    except:
        session.rollback()
        raise
    else:
        session.commit()

# create session and add objects
with Session(db_engine) as session:
    with session.begin():
        session.add(MyModel(id=5, x=35, y=36))
        session.add(MyModel(id=6, x=45, y=46))
    # inner context calls session.commit(), if there were no exceptions
# outer context calls session.close()

# create session and add objects
with Session(db_engine) as session, session.begin():
    session.add(MyModel(id=7, x=85, y=86))
    session.add(MyModel(id=8, x=95, y=96))
# inner context calls session.commit(), if there were no exceptions
# outer context calls session.close()
'''
'''
Using a sessionmaker
sessionmaker is to provide a factory for Session objects with a fixed configuration. 
'''

from sqlalchemy.orm import sessionmaker

# a sessionmaker(), also in the same scope as the engine
Session = sessionmaker(bind=db_engine)

'''
# we can now construct a Session() without needing to pass the
# engine each time
with Session() as session:
    session.add(MyModel(id=11, x=11, y=111))
    session.add(MyModel(id=12, x=12, y=122))
    session.commit()
# closes the session
'''

'''
When you write your application, the sessionmaker factory should be scoped the same as the Engine object 
created by create_engine(), which is typically at module-level or global scope. As these objects are 
both factories, they can be used by any number of functions and threads simultaneously.
'''
'''
# we can now construct a Session() and include begin()/commit()/rollback()
# at once
with Session.begin() as session:
    session.add(MyModel(id=13, x=11, y=111))
    session.add(MyModel(id=14, x=11, y=111))
# commits the transaction, closes the session
'''
'''
Querying
 select() construct to create a Select object, which is then executed to return a result using methods such as 
 Session.execute() and Session.scalars()
 https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html
'''

from sqlalchemy import select

with Session() as session:
    # query for ``User`` objects
    statement = select(MyModel).filter_by(id=12)

    # list of ``User`` objects
    # user_obj = session.scalars(statement).all()
    user_obj = session.execute(statement).all()

    print("==================================")
    print(user_obj)
    print("==================================")
    # query for individual columns
    statement = select(MyModel.x, MyModel.y)

    # list of Row objects
    rows = session.execute(statement).all()
    print("==================================")
    print(rows)
    print("==================================")

model = MyModel(id=33, x=11, y=111)
model_1 = MyModel(id=34, x=11, y=111)
model_2 = MyModel(id=35, x=11, y=111)
model_3 = MyModel(id=36, x=11, y=111)

session.add(model)
session.add_all([model_1, model_2, model_3])
'''
Delete is a tricky one, we need to take care of the relationship
'''
session.delete(model_1)

'''
session.flush()	Sends SQL to the DB (e.g., INSERT/UPDATE) but doesn't commit
session.commit()	Flushes and commits (ends transaction)
session.rollback()	Undoes uncommitted changes
'''
# Flushing
session.flush() 

#Get by Primary Key
my_user = session.get(MyModel, 5)


'''
The concurrency model for SQLAlchemy’s Session and AsyncSession is therefore Session per thread, 
AsyncSession per task. An application that uses multiple threads, or multiple tasks in asyncio such as 
when using an API like asyncio.gather() would want to ensure that each thread has its own Session, each 
asyncio task has its own AsyncSession.
'''


