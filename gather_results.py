# main pipeline

import sys, glob, os
from flask import Flask, render_template
# from flask_restful import Resource, Api

import JobsDB as Jobs
import ResultsDB as Results

app = Flask(__name__)
# api = Api(app)

@app.template_filter()
def statusFormat(value):
    return value.lower()

def main(*args):
    print("Gather rersults from all jobs")
    print(" ".join(args))

    pdf_dir = args[0]

    print(f'PDF directory {pdf_dir}')
    ret = os.popen(f'mkdir -p export export/redlines export/artifacts')
    wat = ret.read()
    print(wat)

    for pdf_path in glob.iglob(f'{pdf_dir}/*.pdf'):
        job_id = pdf_path.split("/")[-1].split(".")[0]
        print(f'Job ID: {job_id}')

        with app.app_context():
            message = f"Jab {job_id}"
            job = Jobs.find(job_id)
            results = Results.find(job_id)
            images = sorted(glob.iglob(f'export/artifacts/{job_id}/*.png'))
            redline_path = pdf_path.replace("pdfs", "export/redlines").replace(".pdf", "_markup.pdf")
            html = render_template('job.html', message=message, job=job, results=results, images=images, pdf_path=redline_path)

            with open(f'export/{job_id}.html', 'w') as outfile:
                outfile.write(html)

    with app.app_context():
        message = "Jabs"
        jobs = Jobs.list_jobs()
        html = render_template('index.html', message=message, jobs=jobs)
        
        with open(f'export/index.html', 'w') as outfile:
            outfile.write(html)

if __name__ == '__main__':
    main(*sys.argv[1:])