import json
import sqlite3
import random

from flask import g, render_template, Flask, request

app = Flask(__name__)
DATABASE = 'database_secproj.db'


@app.route('/')
def index():
    results = query_db("select id, question, answer from catalog ORDER BY RANDOM() LIMIT 4")
    question = results[0]['question']
    db_id = results[0]['id']
    answers = list()
    for entry in results:
        answers.append(entry['answer'])
    random.shuffle(answers)
    return render_template("index.html", id=db_id, question=question, answers=answers)


@app.route('/check_answer', methods=['POST'])
def check_answer():
    if request.method == 'POST':
        data = request.form.to_dict()
        result = query_db("select id from catalog where id = ? AND answer like ?",
                          (data['question_id'], data['answer']), one=True)
        code = 404
        if result:
            code = 200
        return json.dumps({'correct': True}), code, {'ContentType': 'application/json'}

def query_db(query, args=(), one=False):
    con = get_db()
    con.row_factory = dict_factory
    cur = con.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


if __name__ == '__main__':
    app.run()
