from flask import Flask, request,redirect,url_for,session,flash,jsonify,send_from_directory
from flask import render_template
from flask import current_app as app
from application.database import db
from flask_sqlalchemy import SQLAlchemy
from application.models import *
from flask_bcrypt import Bcrypt
import os
bcrypt=Bcrypt(app)



@app.route("/",methods=["GET","POST"])
def index():
    if "username" not in session:
       return redirect(url_for('login'))
    else:
        current_user = User.query.filter_by(email=session['user_email']).first()
        if current_user:
            tasks = current_user.tasks  # Fetch all tasks for the logged-in user
            #print("tasks",tasks)
            return render_template('index.html', tasks=tasks)
        else:
            return redirect(url_for('login'))  # Redirect to login if user is not found'''



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
      if "username" in session:
         return(redirect(url_for("index")))
      error_message=request.args.get("error")  
      return (render_template("login.html",error_message=error_message))
    else:
     if request.method=="POST":
        user=User.query.filter_by(email=request.form["email"]).first()
   
        if user:
            if bcrypt.check_password_hash(user.password,request.form["password"]):
                session["username"]= user.username
                session["user_email"]=user.email
                return redirect(url_for('index'))
            else:
              error_message = "Invalid email or password."
              return render_template('login.html', error_message=error_message)
            
        else:
           return(redirect(url_for('register')))
      



@app.route("/register",methods=["GET","POST"])
def register():
    if "username" in session:
         return(redirect(url_for("index")))
    if request.method=='GET':
     return (render_template("register_user.html"))
    elif request.method=='POST':
        username=request.form["username"]
        email = request.form["email"]
        if "@" in email:
            user=User.query.filter_by(email=request.form["email"]).first()
            password=request.form["password"]
            if user:
               error="Email already registered"
               return (render_template("register_user.html", error=error))
            else:
               if(password!=request.form["confirm_password"]):
                  error="Password does not match with Confirm Password"
                  return(render_template("register_user.html",error=error))
               password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
              
               
               user=User(username=username,email=email,password=password_hash)
               #user.products=[]
               
               db.session.add(user)
               db.session.commit()
              
               session["username"]=username  #maintaining cookie
           
               session["user_email"]=user.email
               return redirect(url_for("login"))
        else:
           error = "Enter a valid email"
           return render_template("register_user.html", error = error)
        
@app.route("/logout")
def logout():
    if "username" in session:
     
        session.pop("username")
        session.pop("user_email")
    return redirect("/")
 


@app.route("/add_task",methods=["GET","POST"])
def add_task():
   if "username" not in session:
      return redirect(url_for('index'))
   else:
      if request.method=='GET':
         return render_template("add_task.html")
      elif request.method=='POST':
         task_name=request.form["task_name"]
         task_description=request.form["task_description"]
         new_task=Task(name=task_name,description=task_description)
         db.session.add(new_task)
         db.session.commit()
         task_id = new_task.task_id
         user=User.query.filter_by(email=session['user_email']).first()
         
         if user:
            user.tasks.append(new_task)
            db.session.commit()
         return redirect(url_for('index'))

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    if "username" not in session:
        return redirect(url_for('login'))
    else:
        task = Task.query.get(task_id)
        current_user = User.query.filter_by(email=session['user_email']).first()
        if task and task in current_user.tasks:
                return render_template("task_detail.html", task=task)
        elif task and task not in current_user.tasks:
                 error_message = "You do not have access to this task."
                 # Redirect with an error message
                 return redirect(url_for('index', error=error_message))
        else:
            error_message = "Task not found."
            # Redirect with an error message
            return redirect(url_for('index', error=error_message))



@app.route("/tasks/update/<int:task_id>", methods=["GET", "POST"])
def update_task(task_id):
    if "username" not in session:
        return redirect(url_for('login'))
    
    task = Task.query.get(task_id)
    if task is None:
        return "Task not found", 404

    current_user = User.query.filter_by(email=session['user_email']).first()
    if task not in current_user.tasks:
        return "Access denied: You do not own this task", 403

    if request.method == "POST":
        task.name = request.form.get('name', task.name)
        task.description = request.form.get('description', task.description)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('update_task.html', task=task)

@app.route("/tasks/delete/<int:task_id>", methods=["GET", "POST"])
def delete_task(task_id):
    if "username" not in session:
        return redirect(url_for('login'))

    task = Task.query.get(task_id)
    if task is None:
        return "Task not found", 404

    current_user = User.query.filter_by(email=session['user_email']).first()
    if task not in current_user.tasks:
        return "Access denied: You do not own this task", 403

    if request.method == "POST":

        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('confirm_delete.html', task_id=task_id)

 
'''@app.route("/tasks", methods=["GET"])
def get_tasks():
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    current_user = User.query.filter_by(email=session['user_email']).first()
    tasks = [{'task_id': task.task_id, 'name': task.name, 'description': task.description} for task in current_user.tasks]
    return jsonify(tasks)

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    task = Task.query.get(task_id)
    current_user = User.query.filter_by(email=session['user_email']).first()
    if task and task in current_user.tasks:
        return jsonify({'task_id': task.task_id, 'name': task.name, 'description': task.description})
    return jsonify({'error': 'Task not found or access denied'}), 404

@app.route("/tasks", methods=["POST"])
def add_task():
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    task_name = request.json['name']
    task_description = request.json['description']
    new_task = Task(name=task_name, description=task_description)
    db.session.add(new_task)
    db.session.commit()
    user = User.query.filter_by(email=session['user_email']).first()
    if user:
        user.tasks.append(new_task)
        db.session.commit()
    return jsonify({'task_id': new_task.task_id}), 201

@app.route("/tasks/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    if request.json:
        task.name = request.json.get('name', task.name)
        task.description = request.json.get('description', task.description)
        db.session.commit()
        return jsonify({'message': 'Task updated'}), 200
    return jsonify({'error': 'Update failed'}), 400

@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200'''

'''
@app.route("/api/login", methods=["GET", "POST"])
def api_login():
    if request.method == "GET":
        if 'user_email' in session:
            return jsonify({"message": "User is already logged in", "user": session['user_email']}), 200
        return jsonify({"error": "No user is currently logged in"}), 401
    
    # POST request: Handle login
    email = request.json.get("email")
    password = request.json.get("password")
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session["username"] = user.username
        session["user_email"] = user.email
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid email or password"}), 401

@app.route("/api/register", methods=["POST"])
def api_register():
    if User.query.filter_by(email=request.json["email"]).first():
        return jsonify({"error": "Email already registered"}), 409
    if request.json["password"] != request.json["confirm_password"]:
        return jsonify({"error": "Passwords do not match"}), 400
    hashed_password = bcrypt.generate_password_hash(request.json["password"]).decode('utf-8')
    user = User(username=request.json["username"], email=request.json["email"], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registration successful"}), 201

@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.pop('username', None)
    session.pop('user_email', None)
    return jsonify({"message": "Logged out"}), 200


# API Routes for interacting with React frontend
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.filter_by(email=session['user_email']).first()
    tasks = [{'task_id': task.task_id, 'name': task.name, 'description': task.description} for task in user.tasks]
    return jsonify(tasks)

@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    task = Task.query.get(task_id)
    if task and any(t.task_id == task_id for t in User.query.filter_by(email=session['user_email']).first().tasks):
        return jsonify({'task_id': task.task_id, 'name': task.name, 'description': task.description})
    return jsonify({'error': 'Task not found or access denied'}), 404

@app.route("/api/tasks", methods=["POST"])
def add_task():
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    task_name = request.json['name']
    task_description = request.json['description']
    new_task = Task(name=task_name, description=task_description)
    db.session.add(new_task)
    db.session.commit()
    user = User.query.filter_by(email=session['user_email']).first()
    user.tasks.append(new_task)
    db.session.commit()
    return jsonify({'task_id': new_task.task_id}), 201

@app.route("/api/tasks/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    task.name = request.json.get('name', task.name)
    task.description = request.json.get('description', task.description)
    db.session.commit()
    return jsonify({'message': 'Task updated'}), 200

@app.route("/api/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200

# Serving React Build
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

'''