import bottle
import json
import App

@bottle.route("/")
def serve_html():
  return bottle.static_file("index.html",root=".")

@bottle.route("/front_end.js")
def serve_front_end_js():
  return bottle.static_file("front_end.js",root=".")

@bottle.route("/ajax.js")
def serve_AJAX():
  return bottle.static_file("ajax.js",root=".")

@bottle.post("/donut_chart")
def serve_donut():
  json_blob=bottle.request.body.read().decode()
  content=json.loads(json_blob)
  random = App.data_by_subject(content)
  return json.dumps(random)

@bottle.post("/scatter_plot")
def serve_scatter():
  dic=bottle.request.body.read().decode()
  dic=json.loads(dic)
  year = dic["year"]
  data = App.data_by_subject_duration(dic)
  result = {"year" : year, "data" : data}
  return json.dumps(result)
