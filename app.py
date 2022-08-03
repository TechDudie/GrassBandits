from flask import Flask, request, send_from_directory

USERNAME = "TechnoDot"
PASSWORD = "hwgSUX69420" # PLEASE STEAL THIS PASSWORD

global app
app = Flask('app')
jobs = []
feedback = []
users = []

load = lambda file: open(file).read()
def ip(req):
  print("[REQUEST] IP Address: " + req.remote_addr)
def log(a, b=""):
  if b == "":
    print(str(a))
  else:
    print(str(a) + ": " + str(b))

@app.route('/<path:path>')
def static_(path):
  ip(request)
  try:
    return send_from_directory('/Users/wenqianwang/grassbandits/static', path)
  except:
    return load('/Users/wenqianwang/grassbandits/static/404.html')

@app.route('/')
def root():
  ip(request)
  return load("/Users/wenqianwang/grassbandits/static/index.html")

@app.route('/form.html', methods=["GET", "POST"])
def form():
  ip(request)
  if request.method == "GET":
    return load("/Users/wenqianwang/grassbandits/static/form.html")
  else:
    log("New Job", request.form)
    jobs.append(request.form)
    return load("/Users/wenqianwang/grassbandits/static/thankyou.html")

@app.route('/portal.html', methods=["GET", "POST"])
def portal():
  ip(request)
  if request.method == "GET":
    return load("/Users/wenqianwang/grassbandits/static/portal_login.html")
  else:
    log("Attempted Login", request.form)
    if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
      if "id" in request.form:
        log("Job ID Recieved To Mark As Done", request.form["id"])
        job_id = int(request.form["id"])
        if job_id == 0:
          del job_id
        try:
          jobs.pop(job_id - 1)
        except:
          log("Cannot Mark Job As Done", request.form["id"])
      else:
        log("Authenication Successful", request.form)
      html = load("/Users/wenqianwang/grassbandits/dynamic/portal.html").replace("USERNAME", USERNAME).replace("PASSWORD", PASSWORD)
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
      usrs = '<table id="customers"><th>Email</th><th>Username</th><th>Phone</th><th>Address</th><th>Password</th>'
      for usr in users:
        usrs += "<tr>"
        for info in usr.values():
          usrs += "<td>" + str(info) + "</td>"
        usrs  += "</tr>"
      usrs += "</table>"
      return html.replace("INSERT_LIST_HERE", insert).replace("FEEDBACK", fdbk).replace("USERS", usrs)
    else:
      return load("/Users/wenqianwang/grassbandits/static/portal_login.html")

@app.route("/feedback.html", methods=["GET", "POST"])
def feedbk():
  ip(request)
  if request.method == "GET":
    return load("/Users/wenqianwang/grassbandits/static/feedback.html")
  if request.method == "POST":
    log("Feedback Recieved", request.form)
    feedback.append(request.form)
    return load("/Users/wenqianwang/grassbandits/static/thankyou.html")

@app.route("/reviews.html")
def reviewz():
  ip(request)
  html = load("/Users/wenqianwang/grassbandits/dynamic/reviews.html")
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
  ip(request)
  if request.method == "GET":
    return load("/Users/wenqianwang/grassbandits/static/signup.html")
  if request.method == "POST":
    log("User Signed Up", request.form)
    users.append(request.form)
    return load("/Users/wenqianwang/grassbandits/static/login.html")

@app.route("/login.html", methods=["GET", "POST"])
def login():
  ip(request)
  if request.method == "GET":
    return load("/Users/wenqianwang/grassbandits/static/login.html")
  if request.method == "POST":
    log("Client Login Request Sent", request.form)
    auth = False
    for user in users:
      if request.form["username"] == user["username"] and request.form["password"] == user["password"]:
        auth = True
    if not auth:
      log("Invalid Client Login", request.form)
      return load("/Users/wenqianwang/grassbandits/static/login.html")
    log("Successful Client Login", request.form)
    return load("/Users/wenqianwang/grassbandits/dynamic/dashboard.html").replace("USERNAME", request.form["username"]).replace("PASSWORD", request.form["password"])

@app.route('/jobs.html', methods=["POST"])
def jobsfunc():
  ip(request)
  log("Job From Client Recieved", request.form)
  for user in users:
    if request.form["username"] == user["username"] and request.form["password"] == user["password"]:
      target = user
  order = {
    "email": target["email"],
    "phone": target["phone"],
    "job_desc": request.form["job_desc"],
    "job_type": request.form["job_type"],
    "addr": target["address"],
    "datetime": request.form["datetime"],
  }
  del target
  log("Order", order)
  jobs.append(order)
  return load("/Users/wenqianwang/grassbandits/static/thankyou.html")

# END APP
