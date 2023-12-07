from flask_cors import CORS
from flask_socketio import SocketIO, Namespace
from flask import Flask, request, jsonify
import subprocess
import threading
import json
import os
import signal
import re
import tempfile
import requests


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
CORS(app)


class CustomNamespace(Namespace):
    def __init__(self, namespace, app_name):
        super().__init__(namespace)
        self.app_name = app_name

    def on_connect(self):
        print('Client connected to {self.app_name}')

    def on_disconnect(self):
        print('Client disconnected from {self.app_name}', self.app_name)
        stop_subprocess(self.app_name)

    def on_message(self, message):
        print('received message on {self.app_name}:', message)

    def on_publish_event(self):
        self.emit('update', {'data': 'New data from {self.app_name}.adk.publish()'})

    def on_executeCallback(self, item):
        socketio.emit('callBack', item)
        self.emit('callBack', item)



@app.route('/send-contact-email', methods=['POST'])
def sendEmailContact():
    toEmail = request.json.get('to')
    phone = request.json.get('phone')
    msg = request.json.get('msg')
    name = request.json.get('name')

    # The URL of the endpoint
    url = "https://tieui-5c69a6002efd.herokuapp.com/send-contact-email"

    # Data to be sent in the POST request
    data = {
        "to": toEmail,
        "phone": phone,
        "msg": msg,
        "name": name
    }

    # Making the POST request
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)


@app.route('/publish/<appName>', methods=['POST'])
def publish(appName):
    print('puto')
    # print(request)
    data = request.json  # Get the entire JSON object
    # print('started publish', data)
    pythonCode = data.get('code')
    components = data.get('components')
    styling = data.get('styling')
    tabStyling = data.get('tab_styling')
    namespace =f'/{appName}'
    socketio.emit('update', {'data': components, 'code': pythonCode, 'styling': styling, 'tab_styling': tabStyling}, namespace=namespace)
    return {'status': 'success'}

@app.route('/test_emit/<appName>')
def test_emit(appName):
    namespace =f'/{appName}'
    socketio.emit('update', {'data': 'Test data from /test_emit'}, namespace=namespace)
    return {'status': 'Test emit success'}

running_subprocesses = {}

@app.route('/execute_python_code/<appName>', methods=['POST'])
def execute_python_code(appName):
    try:
        # Get the Python code from the request
        python_code = request.json.get('pythonCode', '')

        print('the python code')
        print(python_code)
        python_code = re.sub(r'from tieui import TieUi', f'from tieui_module import TieUi', python_code)
        print(python_code)
        # Execute the Python code and capture the output
        def execute_code():
            result = execute_remote_code_async(python_code, appName)
            return result
        
        process = subprocess.Popen(['python3', '-c', python_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setpgrp)
        running_subprocesses[appName] = process

        # result = threading.Thread(target=execute_code).start()

        return jsonify({'result': 0})
    except Exception as e:
        print({'error': str(e)})
        return jsonify({'error': str(e)})

def execute_remote_code_async(command, appName):
    try:
        # Create a temporary Python script file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(command)
            temp_file_path = temp_file.name

        # Run the Python script using subprocess, and create a process group
        process = subprocess.Popen(['python3', temp_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setpgrp)

        # Store the process object in the dictionary indexed by app name
        running_subprocesses[appName] = process

        # Wait for the subprocess to finish and capture the output
        stdout, stderr = process.communicate()

        # Print and return the result
        result = {'stdout': stdout.decode('utf-8'), 'stderr': stderr.decode('utf-8')}
        return result
    except subprocess.CalledProcessError as e:
        return {'error_code': e.returncode, 'error_output': e.stderr.decode('utf-8')}
    except Exception as e:
        return {'error': str(e)}
    finally:
        # Remove the temporary file after execution
        os.remove(temp_file_path)

@app.route('/run-published-code', methods=['POST'])
def run_code_from_route():
    print('running published code')
    data = request.get_json()
    file_location = data.get('location')
    independent = data.get('isIndependent')
    new_app_name = data.get('newAppName')
    app_n = data.get('appName')
    og_app_n = data.get('ogAppName')

    print(app_n)
    print(og_app_n)

    if file_location is None:
        return jsonify(error="No Location Provided")
    
    try:
        if independent:
            with open(file_location, 'r') as file:
                content = file.read()

            # Use a regular expression to find and replace the app_name value
            print(file_location)
            file_name = file_location.split('/')[-1].rsplit('.', 1)[0]
            print("THIS IS THE NAME: ", file_name)
            # content = re.sub(r'app_name\s*=\s*".*?"', f'app_name="{new_app_name}"', content)

            content = re.sub(r'app_name\s*=\s*".*?"', f'app_name="{new_app_name}", og_app_name="{file_name}"', content)
            print(content)

            # Run the Python script using subprocess and store the process object
            print('the content')
            print(content)
            process = subprocess.Popen(['python3', '-c', content], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setpgrp)
            running_subprocesses[new_app_name] = process
        else:
            # Run the Python script using subprocess and store the process object
            process = subprocess.Popen(['python3', file_location], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setpgrp)
            running_subprocesses[new_app_name] = process

        return jsonify(stdout="", stderr=""), 200
    except subprocess.CalledProcessError as e:
        return jsonify(error=str(e), stderr=e.stderr), 400
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/stop_subprocess/<appName>', methods=['POST'])
def stop_subprocess(appName):
    try:
        # Check if the subprocess is running for the given app name
        if appName in running_subprocesses:
            # Terminate the subprocess and its process group
            os.killpg(os.getpgid(running_subprocesses[appName].pid), signal.SIGTERM)
            del running_subprocesses[appName]
            return jsonify(message=f'Subprocess for {appName} stopped successfully')
        else:
            return jsonify(error=f'No subprocess found for {appName}'), 404
    except Exception as e:
        return jsonify(error=str(e)), 500
@app.route('/publish-code/<appName>', methods=['POST'])
def publish_code(appName):
    data = request.get_json()
    code = data.get('code')
    app_name = data.get('app_name')
    layout = data.get('layout')
    tabLayout = data.get('tabLayouts')
    # save_directory = f'./{appName}-'  # Replace with your desired directory
    save_directory = ''  
    # Construct the file path with app_name as the filename
    file_path = save_directory + app_name + '.py'
    layout_file_path = save_directory + app_name + '_layout.json'
    tabLayout_file_path = save_directory + app_name + '_tabLayout.json'
    print("THIS IS THE CODE: ", code)
    try:
        # Open the file for writing and save the code
        with open(file_path, 'w') as file:
            file.write(code)

        with open(layout_file_path, 'w') as layout_file:
            json.dump(layout, layout_file, indent=4)
        
        with open(tabLayout_file_path, 'w') as tabLayout_file:
            json.dump(tabLayout, tabLayout_file, indent=4)
            
        return jsonify({'message': 'Code saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/execute_ai_prompt', methods=['POST'])
def execute_ai_prompt():
    # Get the prompt from the request
    prompt = request.json.get('prompt', '')
    newAppName = request.json.get('appName', '')
    # The URL of the endpoint
    url = "https://tieui-5c69a6002efd.herokuapp.com/execute_ai_prompt"

    # Data to be sent in the POST request
    data = {
        "prompt": prompt,
        "newAppName": newAppName,
    }

    # Making the POST request
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)

custom_namespaces = {}

def register_custom_namespace(app_name):
    namespace = f'/{app_name}'
    custom_namespace = CustomNamespace(namespace, app_name)
    socketio.on_namespace(custom_namespace)
    # Store the custom_namespace object itself, not a 'sid'
    custom_namespaces[app_name] = custom_namespace
    print(socketio.server.manager.rooms.keys())
    print(socketio.server.namespace_handlers.keys())

def unregister_all_routes_and_namespaces():
    global custom_namespaces
    namespace_copy = dict(socketio.server.namespace_handlers)
    
    for namespace in namespace_copy.keys():
        # Disconnect clients from the namespace
        socketio.server.namespace_handlers.pop(namespace)
        socketio.server.disconnect(namespace)
    print(socketio.server.namespace_handlers.keys())
    custom_namespaces.clear()  # Clear the dictionary

@app.route('/register-app/<appName>', methods=['POST'])
def register_app(appName):
    print('registering')
    register_custom_namespace(appName)
    return {'status': 'app registered'}

@app.route('/unregister-all', methods=['POST'])
def unregister_all():
    unregister_all_routes_and_namespaces()
    
    return jsonify({'status': 'All routes and namespaces unregistered.'})

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  userId = request.json.get('userId', '')
  price = request.json.get('price', '')
  units = request.json.get('units', '')

  # The URL of the endpoint
  url = "https://https://tieui-5c69a6002efd.herokuapp.com/create-checkout-session"

  # Data to be sent in the POST request
  data = {
    "userId": userId,
    "price": price,
    "units": units
  }

  # Making the POST request
  response = requests.post(url, json=data)

  # Check if the request was successful
  if response.status_code == 200:
    return response.json()
  else:
    print("Error:", response.status_code, response.text)

@app.route('/create-subscription', methods=['POST'])
def create_subscription():
    userId = request.json.get('userId', '')
    priceId = request.json.get('priceId', '')  # The ID of the Stripe Price object
    customer_email = request.json.get('customer_email', '')  # The customer's email
    quantity = request.json.get('quantity', 1)  # Default to 1 if quantity is not provided
    new_payment_id = request.json.get('new_payment_id', False)
    # The URL of the endpoint
    url = "https://tieui-5c69a6002efd.herokuapp.com/create-subscription"

    # Data to be sent in the POST request
    data = {
        "userId": userId,
        "priceId": priceId,
        "customer_email": customer_email,
        "quantity": quantity,
        "new_payment_id": new_payment_id
    }

    # Making the POST request
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)

@app.route('/health-check', methods=['GET'])
def health_check():
    print('checking health')
    return {'status': 300}
if __name__ == '__main__':
    print('server started')
    port = int(os.environ.get('PORT', 8080))
    socketio.run(app, host='0.0.0.0', port=port)
