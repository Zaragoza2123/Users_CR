from flask import Flask, render_template, request, redirect
# import the class from user.py
from user import User
app = Flask(__name__)
@app.route("/")
def index():
    # call the get all classmethod to get all users
    users = User.get_all()
    print(users)
    return render_template("index.html", users = users)
            
# relevant code snippet from server.py

@app.route('/create')
def send():
    return render_template("create.html")


@app.route('/create_user', methods=["POST"])
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"]
        
    }
    # We pass the data dictionary into the save method from the User class.
    user_id = User.save(data)
    print("########")
    print(user_id)
    # Don't forget to redirect after saving to the database.
    return redirect(f'/user/{user_id}/show')

@app.route('/user/<int:user_id>/show')
def show_user(user_id):
    data = {
        "user_id": user_id
    }
    user = User.get_one(data)
    return render_template("read_one.html", user=user)

@app.route('/edit/<int:user_id>')
def send2(user_id):
    data = {
        "user_id": user_id
    }
    user = User.get_one(data)
    return render_template("edit_one.html", user = user)

@app.route('/user/<int:user_id>/update', methods =['POST'])
def update_user(user_id):

    data = {
        'id': user_id,
        'first_name': request.form['fname'],
        'last_name': request.form['lname'],
        'email': request.form['email']
    }

    User.update_user(data)
    return redirect(f'/user/{user_id}/show')

@app.route('/user/<int:user_id>/delete')
def delete_user(user_id):

    User.delete_user({'id':user_id})

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

