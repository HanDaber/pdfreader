from flask import Flask, request, render_template
from flask_restful import Resource, Api
import JobsDB as Jobs

db_name = 'TEST_DB_1'
table_name = 'test_table_1'

app = Flask(__name__)
api = Api(app)

todos = {}

@app.template_filter()
def statusFormat(value):
    return value.lower()

@app.route("/")
def index():
    message = "Yobs"
    jobs = Jobs.list_jobs(db_name, table_name)
    # jobs = []
    # for job in Jobs.list_stocks():
        # jobs.append(dict(job))
    return render_template('index.html', message=message, jobs=jobs)

# class JobProcess(Resource):
    # def get(self, job_id):
    #     return {job_id: jobs[job_id]}

    # def put(self, job_id):
    #     jobs[job_id] = request.form['data']
    #     return {job_id: jobs[job_id]}

# JobList
# shows a list of all todos, and lets you POST to add new tasks
class JobList(Resource):
    def get(self):
        return Jobs.list_jobs(db_name, table_name)

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        todos[todo_id] = {'task': args['task']}
        return todos[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(JobList, '/jobs')
# api.add_resource(JobProcess, '/<string:job_id>')

if __name__ == '__main__':
    app.run(debug=True)