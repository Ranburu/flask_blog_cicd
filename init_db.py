import os
import psycopg2

connection = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])


# with open('schema.sql') as f:
#     connection.executescript(f.read())

cur = connection.cursor()

cur.execute('DROP TABLE IF EXISTS posts;')
cur.execute('CREATE TABLE posts (id serial PRIMARY KEY,'
                                'created date DEFAULT CURRENT_TIMESTAMP,'
                                'title text NOT NULL,'
                                'content text NOT NULL);'
            )

cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)",
            ('Second Post', 'Content for the second post')
            )

cur.close()
connection.commit()
connection.close()
