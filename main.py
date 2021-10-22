import pandas as pd
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from top2vec import Top2Vec
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from functions import *

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
Bootstrap(app)



global topic_words
#lobal topic_labels
#global conn
model = Top2Vec.load("models/fulltext_pubmed_large")
topic_words = model.topic_words
topic_ids = [*range(0, len(topic_words))]

#topic_labels = {x:"Unlabeled" for x in topic_ids}

data = pd.read_csv("data/pubmed_fulltext_meshonly.tsv", sep="\t", usecols=["title", "mesh_terms"])
data = filter_mesh_terms(data)
data = data.fillna("")
@app.route("/")
def mainpage():
    topic_words_enum = enumerate(topic_words)
    conn = sqlite3.connect('database.db', check_same_thread=False)
    topic_labels = [i[0] for i in conn.execute("SELECT label from topics").fetchall()]
    relevant = [i[0] for i in conn.execute("SELECT relevant from topics").fetchall()]
    conn.close()
    return render_template('main.html', topic_words = topic_words_enum, topic_labels=topic_labels, relevant = relevant)#,

@app.route("/subpage/<int:topic_id>", methods=['GET', 'POST'])
def labelpage(topic_id):
    topic_docs = get_topic_document(topic_id,  model, data, num_docs=20)
    ## TODO ADD KEYWORDS
    titles = topic_docs["title"].tolist()
    keywords = topic_docs["mesh_terms"].tolist()
    keywords = [ast.literal_eval(x) for x in keywords]
    _keywords = []
    for doc in keywords:
        list_to_add = []
        for k,v in doc.items():
            list_to_add.append(v["category"])
        _keywords.append(", ".join(list_to_add))
    keywords = _keywords
    global topic_words
    words = topic_words

    return render_template("labelpage.html", topic_id=topic_id, topic_words=topic_words, titles=enumerate(titles), keywords=keywords)

@app.route("/addrec/<int:topic_id>", methods=["POST", "GET"])
def addrec(topic_id):
    if request.method == "POST":
        form_data = request.form
        label = form_data["topic_label"]
        relevant = form_data["relevant"]
        conn = sqlite3.connect('database.db', check_same_thread=False)
        conn.execute("UPDATE topics SET label = '"+str(label)+"', relevant = '"+str(relevant)+"' WHERE id = "+str(topic_id)+"")
        conn.commit()
        conn.close()
        return redirect(url_for("mainpage"))
if __name__ == "__main__":
    app.run()