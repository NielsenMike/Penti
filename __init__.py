import json
import sqlite3
import random

from flask import g, render_template, Flask, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "database_secproj.db"


@app.route('/')
def index():
    main_result = query_db("select id, question, category, answer from catalog ORDER BY RANDOM() LIMIT 1", one=True)
    sub_result = query_db("select answer from catalog WHERE category like (?) ORDER BY RANDOM() LIMIT 3",
                          (main_result['category'],))
    question = main_result['question']
    db_id = main_result['id']
    answers = list()
    answers.append(main_result['answer'])
    for entry in sub_result:
        answers.append(entry['answer'])
    random.shuffle(answers)
    return render_template("index.html", id=db_id, question=question, answers=answers)


@app.route('/check_answer', methods=['POST'])
def check_answer():
    if request.method == 'POST':
        data = request.form.to_dict()
        result = query_db("select answer from catalog where id = ?",
                          (data['question_id'],), one=True)
        correct = (data['answer'] == result['answer'])
        return json.dumps({'correct': correct}), 200, {'ContentType': 'application/json'}


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
        db = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    return db


if __name__ == '__main__':
    app.run()
