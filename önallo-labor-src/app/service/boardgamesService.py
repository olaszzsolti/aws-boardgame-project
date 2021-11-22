from flask import Flask, jsonify, json, Response, request
from flask_cors import CORS
import boardgamesTableClient

app = Flask(__name__)
CORS(app)


@app.route("/")
def healthCheckResponse():
    return jsonify({"message" : "Nothing here, used for health check. Try /boardgames instead."})


# Lekéri a boardgames a DYnamoDb-ből a megfelő filter szerint, 
# ha nincs filter az összeset.
@app.route("/boardgames", methods=['GET'])
def getBoardgames():

    filterCategory = request.args.get('filter')
    if filterCategory:
        filterValue = request.args.get('value')
        queryParam = {
            'filter': filterCategory,
            'value': filterValue
        }
        serviceResponse = boardgamesTableClient.queryBoardgames(queryParam)
    else:
        serviceResponse = boardgamesTableClient.getAllBoardgames()

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse


# lekérdezi az adatokat egy adott boardgame-hez 
@app.route("/boardgames/<boardgamesId>", methods=['GET'])
def getBoardgame(boardgamesId):
    serviceResponse = boardgamesTableClient.getBoardgame(boardgamesId)

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse


# megnöveli a like számlálót 1-el adott boardgame-nél
@app.route("/boardgames/<boardgamesId>/like", methods=['POST'])
def likeBoardgame(boardgamesId):
    serviceResponse = boardgamesTableClient.likeBoardgame(boardgamesId)

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse



# a service azon a serveren fut, ahova telepítve van a 8080 porton hallgat.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
