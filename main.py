from flask import Flask, request, send_from_directory

USERNAME = "TechnoDot"
PASSWORD = "hwgSUX69420" # PLEASE STEAL THIS PASSWORD

global app
app = Flask('app')
jobs = []
feedback = []
users = []

load = lambda file: open(file).read()

@app.route('/<path:path>')
def static_(path):
  try:
    return send_from_directory('static', path)
  except:
    return load('static/404.html')

@app.route('/')
def root():
  return load("static/index.html")

@app.route('/form.html', methods=["GET", "POST"])
def form():
  if request.method == "GET":
    return load("static/form.html")
  else:
    print(request.form)
    jobs.append(request.form)
    return load("static/thankyou.html")

@app.route('/portal.html', methods=["GET", "POST"])
def portal():
  if request.method == "GET":
    return load("static/portal_login.html")
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
      html = load("dynamic/portal.html").replace("USERNAME", USERNAME).replace("PASSWORD", PASSWORD)
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
        for info in review.values():
          fdbk += "<td>" + str(info) + "</td>"
        fdbk += "</tr>"
      fdbk += "</table>"
      return html.replace("INSERT_LIST_HERE", insert).replace("FEEDBACK", fdbk)
    else:
      return load("static/portal_login.html")

@app.route("/feedback.html", methods=["GET", "POST"])
def feedbk():
  if request.method == "GET":
    return load("static/feedback.html")
  if request.method == "POST":
    print(request.form)
    feedback.append(request.form)
    return load("static/thankyou.html")

@app.route("/reviews.html")
def reviewz():
  html = load("dynamic/reviews.html")
  insert = ""
  for view in feedback[-4:]:
    try:
      stars = '<span>&bigstar;</span>' * int(view["stars"])
    except:
      stars = '<span>&bigstar;</span>' * 5
    insert += '<div class="mySlides w3-container w3-xlarge w3-white w3-card-4">' + stars + '<p>' + view["review"] + '</p></div>'
  return html.replace("REVIEW", insert)

@app.route("/signup.html", methods=["GET", "POST"])
def signup():
  if request.method == "GET":
    return load("static/signup.html")
  if request.method == "POST":
    print(request.form)
    users.append(request.form)
    return load("static/login.html")

@app.route("/login.html", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    return load("static/login.html")
  if request.method == "POST":
    print(request.form)
    auth = False
    for user in users:
      if request.form["username"] == user["username"] and request.form["password"] == user["password"]:
        auth = True
    if not auth:
      return load("static/login.html")
    return load("dynamic/dashboard.html").replace("USERNAME", request.form["username"]).replace("PASSWORD", request.form["password"])

@app.route('/jobs.html', methods=["POST"])
def jobsfunc():
  print(request.form)
  for user in users:
    if request.form["username"] == user["username"] and request.form["password"] == user["password"]:
      target = user
  order = {
    "email": target["email"],
    "phone": target["email"],
    "job_desc": request.form["job_desc"],
    "job_type": request.form["job_type"],
    "addr": target["email"],
    "datetime": request.form["datetime"],
  }
  jobs.append(order)
  return load("static/thankyou.html")

app.run(host='0.0.0.0', port=8080)