import sqlite3
from top2vec import Top2Vec
conn = sqlite3.connect('database.db')
print("Opened database successfully")

#conn.execute('CREATE TABLE topics (id INT, label TEXT, relevant TEXT)')

model = Top2Vec.load("models/fulltext_pubmed_large")
topic_words = model.topic_words
cursor = conn.cursor()
for i, row in enumerate(topic_words):
    conn.execute("INSERT INTO topics (id, label, relevant)"
                 "VALUES ('"+str(i)+"', '', '')")
    conn.commit()
print("Table created successfully")
conn.close()