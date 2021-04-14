from flask import Flask, request, render_template
from flask_restful import Resource, Api

import JobsDB as Jobs
import ResultsDB as Results

app = Flask(__name__)
api = Api(app)



@app.template_filter()
def statusFormat(value):
    return value.lower()

@app.route("/")
def index():
    message = "Yabs"
    jobs = Jobs.list_jobs()
    return render_template('index.html', message=message, jobs=jobs)

@app.route("/job/<string:job_id>")
def job(job_id):
    message = f"Yab {job_id}"
    job = Jobs.find(job_id)
    results = Results.find(job_id)
    return render_template('job.html', message=message, job=job, results=results)



class JobProcess(Resource):
    def get(self, job_id):
        found_job = Jobs.find(job_id)
        found_job['results'] = Results.find(job_id)
        return found_job

    # def put(self, job_id):
    #     jobs[job_id] = request.form['data']
    #     return {job_id: jobs[job_id]}

class JobProcessResults(Resource):
    def get(self, job_id):
        results = Results.find(job_id)
        return results

class JobList(Resource):
    def get(self):
        return Jobs.list_jobs()

    # def post(self):
    #     args = parser.parse_args()
    #     todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
    #     todo_id = 'todo%i' % todo_id
    #     todos[todo_id] = {'task': args['task']}
    #     return todos[todo_id], 201



##
## Actually setup the Api resource routing here
##
api.add_resource(JobList, '/jobs')
api.add_resource(JobProcess, '/jobs/<string:job_id>')
api.add_resource(JobProcessResults, '/jobs/<string:job_id>/results')

if __name__ == '__main__':
    app.run(debug=True)