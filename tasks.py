from flask import Flask
import subprocess
app = Flask(__name__)
@app.route('/')
def home():
    # This runs the 'task' command and displays it in the browser
    output = subprocess.check_output(['task', 'list'], text=True)
    return f"<html><body><pre>{output}</pre></body></html>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5678)
