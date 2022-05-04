from flask import Flask, request, send_from_directory
#import threading
#import json
#import time

USERNAME = "TechnoDot"
PASSWORD = "hwgSUX69420"

app = Flask('app')
jobs = []
feedback = []

load = lambda file: open(file).read()

#try:
#  jobs = json.loads(load("/home/TechDude/grassbandits/save.json"))
#  print("JSON save loaded")
#except:
#  jobs = []

#def save():
#  while True:
#    time.sleep(30)
#    file_h = open("save.json", "w")
#    file_h.write(json.dumps(jobs))
#    file_h.close()

#save_thread = threading.Thread(target=save)
#save_thread.start()

@app.route('/<path:path>')
def static_(path):
  try:
    return send_from_directory('/home/TechDude/grassbandits/static', path)
  except:
    return load('/home/TechDude/grassbandits/static/404.html')

@app.route('/')
def root():
  return load("/home/TechDude/grassbandits/static/index.html")

@app.route('/form.html', methods=["GET", "POST"])
def form():
  if request.method == "GET":
    return load("/home/TechDude/grassbandits/static/form.html")
  else:
    print(request.form)
    jobs.append(request.form)
    return load("/home/TechDude/grassbandits/static/thankyou.html")

@app.route('/portal.html', methods=["GET", "POST"])
def portal():
  if request.method == "GET":
    return load("/home/TechDude/grassbandits/dynamic/portal_login.html")
  else:
    print(request.form)
    if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
      try:
        print(request.form["id"])
        job_id = int(request.form["id"])
      except:
        print("Authenication successful")
      try:
        if job_id == 0:
          del job_id
        jobs.pop(job_id - 1)
      except:
        print("W@T D0 1 D31337???")
      html = load("/home/TechDude/grassbandits/dynamic/portal.html").replace("USERNAME", USERNAME).replace("PASSWORD", PASSWORD)
      insert = '<table id="customers"><th>ID</th><th>Email</th><th>Phone</th><th>Job Desc</th><th>Job Type</th><th>Address</th><th>Date & Time</th>'
      job_id = 1
      for job in jobs:
        insert += "<tr>"
        values = [job_id]
        values += job.values()
        for info in values:
          insert += "<td>" + str(info) + "</td>"
        insert += "</tr>"
        job_id += 1
      insert += "</table>"
      fdbk = '<table id="customers"><th>Email</th><th>Stars</th><th>Review</th>'
      for review in feedback:
        fdbk += "<tr>"
        for info in review:
          fdbk += "<td>" + str(info) + "</td>"
        fdbk += "</tr>"
      fdbk += "</table>"
      return html.replace("INSERT_LIST_HERE", insert).replace("FEEDBACK", fdbk)
    else:
      return load("/home/TechDude/grassbandits/dynamic/portal_login.html")

@app.route("/feedback.html", methods=["GET", "POST"])
def feedbk():
  if request.method == "GET":
    return load("/home/TechDude/grassbandits/static/feedback.html")
  if request.method == "POST":
    feedback.append(request.form)
    return load("/home/TechDude/grassbandits/static/thankyou.html")
