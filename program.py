from flask import Flask, redirect, url_for, render_template, request
import Task3
from Task3 import change_map, write_to_file
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("domain")
    token = request.form.get("tocken")
    return f"{name} {token}"
    
@app.route("/register/map", methods=["POST"])
def take_elements():
    elements = register().split()
    name = elements[0]
    tocker = elements[1]
    file_with_friends = write_to_file(name, tocker)
    your_map = change_map("friends.json")
    return your_map.get_root().render()

if __name__ == "__main__":
    app.run(debug=True)