from flask import Flask, request, redirect, url_for, render_template, flash

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Required for flash messages
    tasks = []
    MAX_LENGTH = 50  # Define a maximum length for tasks

    @app.route('/')
    def index():
        return render_template('index.html', tasks=tasks)

    @app.route('/add', methods=['POST'])
    def add_task():
        task = request.form.get('task')
        
        # Input validation
        if not task or task.strip() == '':
            flash('Invalid task. Please enter a valid task.', 'error')
            return 'Invalid task', 400  # Return 400 Bad Request
        if len(task) > MAX_LENGTH:
            flash('Task is too long. Please limit to {} characters.'.format(MAX_LENGTH), 'error')
            return 'Task is too long', 400  # Return 400 Bad Request
        
        # Add task to the list
        tasks.append(task)
        return redirect(url_for('index'))  # Redirect after successful addition

    @app.route('/delete/<int:task_id>', methods=['POST'])
    def delete_task(task_id):
        # Check if the task ID is valid
        if 0 <= task_id < len(tasks):
            tasks.pop(task_id)  # Remove the task by ID
        return redirect(url_for('index'))  # Redirect after deletion

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
