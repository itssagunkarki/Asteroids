from flask import Flask, render_template, request, redirect, url_for
import json
from flask_caching import Cache

from asteroids.asteroid_data import AsteroidData
from asteroids.graphs import AsteroidGraph

app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "simple"})


@app.route("/")
def home():
    return render_template("index.html")

@app.errorhandler(404)
def error(e):
    return render_template("404.html")

@app.route("/asteroids/", methods=["GET", "POST"])
def asteroids():
    if request.method == "GET":
        if all(key in request.args for key in ["start_date", "end_date"]):
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")

            data = {
                "start_date": start_date,
                "end_date": end_date
            }

            cached_result = cache.get(f"{start_date}_{end_date}")
            if cached_result:
                data['asteroids_data'] = cached_result['asteroids_data']
            else:
                asteroids = AsteroidData(start_date, end_date)
                data['asteroids_data'] = asteroids.get_data_from_nasa()
                cache.set(f"{start_date}_{end_date}", data, timeout=3600)  # Cache the result for 1 hour
            
            graphs = AsteroidGraph(data['asteroids_data']).get_graph()

            

    return render_template("asteroids.html", title="Asteroids", graphs=graphs)


# @app.route("/asteroids/asteroid_table")
# def asteroid_table():
#     if request.method == "GET":
#         if all(key in request.args for key in ["start_date", "end_date"]):
#             start_date = request.args.get("start_date")
#             end_date = request.args.get("end_date")

#             data = {
#                 "start_date": start_date,
#                 "end_date": end_date
#             }

#             cached_result = cache.get(f"{start_date}_{end_date}")
#             if cached_result:
#                 data['asteroid_count'] = cached_result['asteroid_count']
#                 data['asteroids'] = cached_result['asteroids']
#                 return render_template("asteroids.html", title=f"Asteroids from {start_date} to {end_date}", data=data)

#             asteroids = AsteroidData(start_date, end_date)
#             data['asteroids'] = asteroids.get_list_all_asteroids()
#             data['asteroid_count'] = asteroids.get_num_asteroids()

#             cache.set(f"{start_date}_{end_date}", data, timeout=3600)  # Cache the result for 1 hour

#             return render_template("asteroid_table.html", title=f"Asteroids from {start_date} to {end_date}", data=data)



if __name__ == "__main__":
    app.run(debug=True)
