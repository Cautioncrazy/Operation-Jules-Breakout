from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/api/v1/debug')
def debug():
    # CRITICAL VULNERABILITY: This endpoint executes shell commands 
    # passed via the 'cmd' parameter to "test system latency."
    command = request.args.get('cmd')
    if not command:
        return "No command provided.", 400
    
    try:
        # Executes as the user running the script (root)
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Listen only on localhost so it's "internal only"
    app.run(host='127.0.0.1', port=8080)
