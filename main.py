from flask import Flask, request, redirect, send_from_directory, Response
app = Flask('app')
jobs = []

load = lambda file: open(file).read()

@app.route('/<path:path>')
def static_(path):
  return send_from_directory('static', path)

@app.route('/')
def root():
  return load("static/index.html")

@app.route('/form.html', methods=["GET", "POST"])
def form():
  if request.method == "GET":
    return load("form.html")
  else:
    print(request.form)
    jobs.append(request.form)
    return load("form.html")

@app.route('/portal.html', methods=["GET", "POST"])
def form():
  if request.method == "GET":
    return load("portal_login.html")
  else:
    print(request.form)
    if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
      try:
        job_id = int(request.form["id"])
        jobs.pop(job_id)
      except:
        pass
      return load("portal.html").replace("USERNAME", USERNAME).replace("PASSWORD", PASSWORD)

app.run(host='0.0.0.0', port=8080)
