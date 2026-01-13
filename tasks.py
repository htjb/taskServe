from flask import Flask, request, redirect, url_for
import subprocess
import json

app = Flask(__name__)

def render_task_row(task):
    project = task.get('project', '')
    due = task.get('due', '')
    if due:
        due = due[:4] + '-' + due[4:6] + '-' + due[6:8]
    tags = " ".join(task.get('tags', []))
    urgency = task.get('urgency', 0)

    return f"""
    <tr>
        <td>{task['id']}</td>
        <td>{task['description']}</td>
        <td>{tags}</td>
        <td>{project}</td>
        <td>{due}</td>
        <td>{urgency}</td>
        <td>
            <form method="POST" action="/delete" onsubmit="return confirm('Delete this task?');">
                <input type="hidden" name="id" value="{task['id']}">
                <button type="submit">Delete</button>
            </form>
        </td>
    </tr>
    """

@app.route('/')
def home():

    pending = subprocess.check_output(['task', 
                'status:pending', 'export'], text=True)
    waiting = subprocess.check_output(['task', 
                'status:waiting', 'export'], text=True)

    tasks = json.loads(pending) + json.loads(waiting)

    tasks.sort(key=lambda t: t.get('urgency', ''), reverse=True)
    
    rows = "".join([render_task_row(task) for task in tasks])

    return f"""
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='style.css')}">
      </head>
      <body>
        <form method="POST" action="/add">
          <input name="desc" placeholder="New task description" />
          <input name="tags" placeholder="Enter tags as +tag" />
          <input name="project" placeholder="Enter project" />
          <button type="submit">Add</button>
        </form>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Description</th>
                    <th>Tags</th>
                    <th>Project</th>
                    <th>Due</th>
                    <th>Urgency</th>
                    <th>Delete</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
      </body>
    </html>
    """

@app.route('/add', methods=["POST"])
def add():
    desc = request.form.get("desc", "")
    tags = request.form.get("tags", "")
    project = request.form.get("project", "")
    if desc.strip():
        subprocess.run(["task", "add", desc, 
                        tags, f"pro:{project}"])
    return redirect("/")

@app.route('/delete', methods=["POST"])
def delete():
    identity = request.form.get("id", "")
    if identity.strip():
        subprocess.run(["task", "rc.confirmation=no", identity, "del"])
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5678)
