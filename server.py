# server.py

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def server_status():
    return "Server is on."


@app.route("/info", methods=["GET"])
def information():
    x = "This website will calculate blood chol.\n"
    x += "It is written by Ramana Balla"
    return x


@app.route("/hdl_check", methods=["POST"])
def hdl_check_from_internet():
    """
        incoming_json = {"name": <name_str>,
                         "hdl_value": <hdl_value_int>}
    """
    from blood_calculator import check_HDL
    in_data = request.get_json()
    hdl_value = in_data["hdl_value"]
    print("The received value was {}".format(hdl_value))
    answer = check_HDL(hdl_value)
    return answer


@app.route("/add_numbers", methods=["POST"])
def add_numbers():
    """
        incoming_json = {"a": <a_int>,
                         "b": <b_int>}
    """
    in_data = request.get_json()
    a = in_data["a"]
    b = in_data["b"]
    return jsonify(a+b)

if __name__ == "__main__":
    app.run()