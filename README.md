# Task Manager Web Application

This is a Flask-based web application for managing tasks. Users can register, login, add, update, delete tasks, and view task details.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SJ-1407/Task.git

2. **Create and Activate Virtual Environment:**

     To create a virtual environment, you can use the following commands:

    ```bash
    python3 -m venv venv


3. **Install Dependencies:**
    ```bash
    pip install -r reqs.txt





5. **Environment Variables:**
Create a `.env` file in the root directory and add the following environment variables:
 
       SECRET_KEY=<your_secret_key>

6. **Run the Application:**



# Routes Documentation

## Authentication Routes

### Index

- **URL:** `/`
- **Method:** GET, POST
- **Description:** Displays the dashboard if the user is logged in, otherwise redirects to the login page.
- **Behavior:**
  - If the user is logged in, fetches all tasks for the logged-in user and displays them on the dashboard.
  - If the user is not logged in, redirects to the login page.

### Login

- **URL:** `/login`
- **Method:** GET, POST
- **Description:** Allows users to log in with their email and password.
- **Behavior:**
  - GET: Displays the login form.
  - POST: Authenticates the user and redirects to the dashboard on success, or displays an error message on failure.

### Register

- **URL:** `/register`
- **Method:** GET, POST
- **Description:** Allows new users to register with a username, email, and password.
- **Behavior:**
  - GET: Displays the registration form.
  - POST: Registers the user and redirects to the login page on success, or displays an error message on failure.

### Logout

- **URL:** `/logout`
- **Method:** GET
- **Description:** Logs out the current user and clears the session.
- **Behavior:** Redirects to the login page after logout.

## Task Routes

### Add Task

- **URL:** `/add_task`
- **Method:** GET, POST
- **Description:** Allows users to add a new task.
- **Behavior:**
  - GET: Displays the form to add a new task.
  - POST: Adds the new task to the database and redirects to the dashboard.

### View Task Details

- **URL:** `/tasks/<task_id>`
- **Method:** GET
- **Description:** Displays details of a specific task.
- **Behavior:**
  - Displays the details of the task if the user has access to it.
  - Redirects to the dashboard with an error message if the task is not found or the user does not have access to it.

### Update Task

- **URL:** `/tasks/update/<task_id>`
- **Method:** GET, POST
- **Description:** Allows users to update details of a specific task.
- **Behavior:**
  - GET: Displays the form to update the task details.
  - POST: Updates the task details in the database and redirects to the dashboard.

### Delete Task

- **URL:** `/tasks/delete/<task_id>`
- **Method:** GET, POST
- **Description:** Allows users to delete a specific task.
- **Behavior:**
  - GET: Displays the confirmation page to delete the task.
  - POST: Deletes the task from the database and redirects to the dashboard.



