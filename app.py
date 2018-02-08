from wpvulscan import wpscan
import requests
from rq import Queue
from rq.job import Job
from worker import conn
from flask import Flask, render_template, request, jsonify



app = Flask(__name__)
q = Queue(connection=conn)


def githubify(text):
    text = '```console\n' + text + '```\n'    
    r = requests.post('https://api.github.com/markdown/raw', data=text, headers={'Content-Type': 'text/x-markdown'})
    return r.text


@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')


@app.route('/enqueue', methods=['POST'])
def enqueue():
    task = q.enqueue_call(func=wpscan, args=(request.form['url'],), result_ttl=5000, timeout=3600)
    response = {
        'status': 'success',
        'data': {
            'task_id': task.get_id()
        }
    }
    return jsonify(response), 202


@app.route('/tasks/<task_id>', methods=['GET'])
def get_status(task_id):
    task = q.fetch_job(task_id)

    if task:
        response = {
            'status': 'success',
            'data': {
                'task_id': task.get_id(),
                'task_status': task.get_status(),
            }
        }
    else:
        response = {'status': 'error'}

    return jsonify(response)




@app.route('/results/<task_id>', methods=['GET'])
def result(task_id):
    task = q.fetch_job(task_id)
    url = task.result.splitlines()[0][9:]
    return render_template('result.html', results=[{'url': url, 'content': githubify(task.result)}])



if __name__=='__main__':
    app.run()
