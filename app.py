from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# In-memory task storage (for demonstration purposes)
tasks = []

@app.route('/')
def index():
    # Render the main page with the current tasks
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    # Check if the task is empty or just whitespace
    if not task or task.strip() == "":
        return 'Bad Request', 400  # Return 400 status code for empty task
    tasks.append(task)  # Add the task to the list
    return redirect('/')  # Redirect to the main page

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # Check if the task ID is valid
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)  # Remove the task if the ID is valid
    return redirect('/')  # Redirect to the main page

if __name__ == '__main__':
    app.run(debug=True)