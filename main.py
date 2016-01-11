import jenkinsapi
import pprint
from flask import Flask
from flask import render_template
import datetime
from nocache import nocache
app = Flask(__name__)


class jenkins_builds(object):
    build_id = job = timestamp = status = ''

    def __init__(self, job, build_id, timestamp, status):
        self.build_id = build_id
        self.job = job
        self.timestamp = timestamp
        self.status = status


def initiate_connection():
    server = jenkinsapi.jenkins.Jenkins('http://192.168.0.200:8080/')
    return server


def get_builds():
    builds = []
    jenkins = initiate_connection()
    job = jenkins.get_job('test-job')
    for build_id in job.get_build_ids():
        build = job.get_build(build_id)
        j = jenkins_builds(job, build_id, str(
            build.get_timestamp()), build.get_status())
        builds.append(j)

    return builds


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fadi')
def fadi():
    return render_template('heatmap2.html')


@app.route('/heatmap')
def heatmap():
    return render_template('heatmap.html')


@app.route('/foo')
def foo():
    return str(datetime.datetime.now())

if __name__ == '__main__':
    app.run(port=9090, debug=True)
    for i in get_builds():
        print i.build_id
# Number of projects in the pipeline
# Most Active Project:
# Succsessful / Failed Promotions:
# Most Aactive Day:
# Most Active hour:
# Promotions Today:
# Last Promoted Project:
