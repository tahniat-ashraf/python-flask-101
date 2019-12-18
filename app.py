from flask import Flask, request, jsonify, render_template, escape, url_for
from validator import valid_login

app = Flask(__name__)

student_list = []


@app.route("/")
def root():
    return "Hello World"


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/hello/")
def hello_world_trailing_slash():
    return "Hello World with trailing slash"


@app.route("/hello/<username>")
def hello_username(username):
    return "Hello World Mr.{}, {}".format(escape(username), request.args.get("age"))


@app.route("/hello/int/<int:id>")
def hello_id(id):
    return "Hello id {}".format(escape(id))


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return render_template("login.html", message="Successfully logged in")
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', message=error)


@app.route("/student", methods=["POST"])
def add_student():
    student = request.json
    print("student {}", student)
    student_list.append(student)
    return print_student_list()


@app.route("/student/<int:student_id>", methods=["DELETE"])
def remove_student(student_id):
    for student in student_list:
        print(f"student['id'] {student['id']}, escape(student_id) {escape(student_id)}")
        if student["id"] == int(escape(student_id)):
            student_list.remove(student)
            return jsonify(student)
    return "{'errorMessage' : 'Student doesn\'t exit'}"


@app.route("/student/<int:student_id>", methods=["GET"])
def get_student(student_id):
    for student in student_list:
        print(f"student['id'] {student['id']}, escape(student_id) {escape(student_id)}")
        if student["id"] == int(escape(student_id)):
            return jsonify(student)
    return "{'errorMessage' : 'Student doesn\'t exit'}"


@app.route("/students")
def print_student_list():
    return jsonify(student_list)


@app.route("/students-html")
def print_student_list_in_html():
    return render_template("students.html", students=student_list)


with app.test_request_context():
    print(url_for('root'))
    print(url_for('hello_username', username="Priyam"))
    print(url_for('hello_username', username="Priyam", age=26))

if __name__ == "__main__":
    app.run(debug=True)
