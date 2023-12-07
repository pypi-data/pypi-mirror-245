# import requests
# import socketio

# class TieUiNameSpace(socketio.ClientNamespace):
#     def __init__(self, namespace, adk):
#         super().__init__(namespace)
#         self.adk = adk
#     def on_connect(self):
#         print('Connected to namespace:', self.namespace)

#     def on_disconnect(self):
#         print('Disconnected from namespace:', self.namespace)

#     def on_callBack(self, item):
#         print("CALLBACK RECEIVED:", item)
#         callback_id = item.get("componentId")
#         if callback_id and callback_id in self.adk.component_callbacks:
#             self.adk.component_callbacks[callback_id](item)
#         elif self.adk.execute_callback:  # default callback
#             self.adk.execute_callback(item)


# class TieUi:
#     def __init__(self, execute_callback=None):
#         self.components = []
#         self.sio = socketio.Client()
#         self.component_callbacks = {}
#         self.execute_callback = execute_callback

#         @self.sio.event
#         def connect():
#             print('Connected to Flask server.')

#         @self.sio.event
#         def disconnect():
#             print('Disconnected from Flask server.')

#         @self.sio.on('callBack')
#         def on_execute_callback(item):
#             print("executing callback")
#             callback_id = item["componentId"]
#             if callback_id and callback_id in self.component_callbacks:
#                 self.component_callbacks[callback_id](item)
#             elif self.execute_callback:  # default callback
#                 self.execute_callback(item)

#         # Connect to the Flask server upon initialization
#         self.sio.connect('http://localhost:8080')


#     def add(self, component):
#         self.components.append(component)
#         return self

#     def textBox(self, settings, callback=None):
#         # Translates Python settings to necessary JSON for React
#         component =  {"type": "textBox", "settings": settings}
#         if callback:
#             component_id = f"textBox_{len(self.components)}"
#             self.component_callbacks[component_id] = callback
#             component["callback_id"] = component_id
#         return component

#     def select(self, settings, callback=None):
#         component = {"type": "select", "settings": settings}
#         if callback:
#             component_id = f"select_{len(self.components)}"
#             self.component_callbacks[component_id] = callback
#             component["callback_id"] = component_id
#         return component

#     def button(self, settings, callback=None):
#         component = {"type": "button", "settings": settings}
#         if callback:
#             component_id = f"button_{len(self.components)}"
#             self.component_callbacks[component_id] = callback
#             component["callback_id"] = component_id
#         return component

#     def dataViz(self, chart):
#         return {"type": "dataViz", "settings": chart}
    
#     def publish(self):
#         response = requests.post("http://localhost:8080/publish", json=self.components)
#         self.wait_for_events()
#         return response.json()
    
#     def update(self):
#         self.publish()
    
#     def wait_for_events(self):
#         # To keep the script running and listening for events
#         try:
#             self.sio.wait()
#         except KeyboardInterrupt:
#             print("Interrupted by user.")
#             self.sio.disconnect()


import inspect
import os
import requests
import socketio
import time
import inspect
import json
import subprocess
import platform

url = 'http://172.105.148.14'
url = 'http://localhost:8080'
url = 'https://tieui-5c69a6002efd.herokuapp.com/'

class TieUiNameSpace(socketio.ClientNamespace):
    def __init__(self, namespace, adk):
        super().__init__(namespace)
        self.adk = adk
    def on_connect(self):
        print('Connected to namespace:', self.namespace)

    def on_disconnect(self):
        print('Disconnected from namespace:', self.namespace)

    def on_callBack(self, item):
        print("CALLBACK RECEIVED:", item)
        callback_id = item.get("componentId")
        if callback_id and callback_id in self.adk.component_callbacks:
            self.adk.component_callbacks[callback_id](item)
        elif self.adk.execute_callback:  # default callback
            self.adk.execute_callback(item)


class TieUi:
    def __init__(self, app_name=None, og_app_name=None, execute_callback=None, isLocal=None):
        self.components = []
        if app_name is None:
            self.app_name = 'local'
        else:
            print('is not None')
            self.app_name = app_name        
        if isLocal: 
            aName = 'local'
            global url
            url = 'http://localhost:8080'

            os_name = platform.system()
            module_dir = os.path.dirname(os.path.realpath(__file__))
            # if os_name == 'Windows':
            local_version_path = os.path.join(module_dir, 'local-version')
            server_py_path = os.path.join(local_version_path, 'server.py')
            http_server_path = os.path.join(local_version_path, 'out')
            electron_app_path = os.path.join(local_version_path, 'main.js')
            node_modules_path = os.path.join(local_version_path, 'node_modules')


            shell_option = True
            # else:  # macOS and Linux
            #     local_version_path = os.path.join(module_dir, 'local-version')
            #     server_py_path = './local-version/server.py'
            #     http_server_path = './local-version/out/'
            #     electron_app_path = './local-version/main.js'
            #     npm_path = './local-version'

            #     shell_option = False if os_name == 'Linux' else True

            # Check if node_modules directory exists
            if not os.path.exists(node_modules_path):
                # Run npm install if node_modules does not exist
                npm_install_command = f'npm install'
                subprocess.run(npm_install_command, shell=True, cwd=local_version_path)


            # Maybe pip install before the server 
            subprocess.Popen(["python3", server_py_path], stdout=subprocess.PIPE, text=True)

            response = requests.post(f"{url}/register-app/{aName}", json=self.components)
            server_process = subprocess.Popen(["python3", "-m", "http.server", "3000", "--directory", http_server_path], stdout=subprocess.PIPE, text=True)
            # electron_app_path = '.\\local-version\\main.js'
            command = f'electron {electron_app_path}'
            subprocess.Popen(command, shell=True)
            time.sleep(5)  # 3-second delay

        self.og_app_name=og_app_name
        self.sio = socketio.Client()
        self.component_callbacks = {}
        self.execute_callback = execute_callback
        self.layout_data = self._load_layout_data()
        self.tabLayout_data = self._load_tabLayout_data()


        # Create and register custom namespace
        self.namespace = TieUiNameSpace('/' + self.app_name, self)
        self.sio.register_namespace(self.namespace)

        # Connect to the Flask server upon initialization
        self.sio.connect(url, namespaces=['/' + self.app_name])

    def _load_tabLayout_data(self):
        layout_file_path = f'./{self.app_name}_tabLayout.json'
        print(layout_file_path)
        try:
            with open(layout_file_path, 'r') as layout_file:
                return json.load(layout_file)
        except FileNotFoundError:
            # return {}
            try:
                layout_file_path = f'./{self.og_app_name}_layout.json'
                with open(layout_file_path, 'r') as layout_file:
                    return json.load(layout_file)
            except FileNotFoundError:
                return {}  # return an empty dict if the layout file doesn't exist


    def _load_layout_data(self):
        print("inside layout data")
        # print(location)
        # print(self.components)
        """
        Load layout data from the saved JSON file.
        """
        layout_file_path = f'./{self.app_name}_layout.json'
        print(layout_file_path)

        try:
            with open(layout_file_path, 'r') as layout_file:
                return json.load(layout_file)
        except FileNotFoundError:
            # return {}
            try:
                layout_file_path = f'./{self.og_app_name}_layout.json'
                with open(layout_file_path, 'r') as layout_file:
                    return json.load(layout_file)
            except FileNotFoundError:
                return {}  # return an empty dict if the layout file doesn't exist

    # ------------------- COMPONENTS ------------------

    def textBox(self, settings, callback=None):
        # Translates Python settings to necessary JSON for React
        component =  {"type": "textBox", "settings": settings}
        if callback:
            component_id = f"textBox_{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component

    def select(self, settings, callback=None):
        component = {"type": "select", "settings": settings}
        if callback:
            component_id = f"select_{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component

    def button(self, settings, callback=None):
        component = {"type": "button", "settings": settings}
        if callback:
            component_id = f"button_{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component

    def dataViz(self, chart):
        return {"type": "dataViz", "settings": chart}
    
    def barChart(self, settings):
        component = {"type": "barChart", "settings": settings}
        return component

    def lineChart(self, settings):
        component = {"type": "lineChart", "settings": settings}
        return component
    
    def label(self, settings):
        component = {"type": "label", "settings": settings}
        return component
    
    def checkbox(self, settings, callback=None):
        component = {"type": "checkbox", "settings": settings}
        if callback:
            component_id = f"checkbox{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component
    
    def slider(self, settings, callback=None):
        component = {"type": "slider", "settings": settings}
        if callback:
            component_id = f"slider{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component
    
    def switch(self, settings, callback=None):
        component = {"type": "switch", "settings": settings}
        if callback:
            component_id = f"switch{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component
    def chip(self, settings, callback=None):
        component = {"type": "chip", "settings": settings}
        if callback:
            component_id = f"chip{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component
    def progress(self, settings, callback=None):
        component = {"type": "progress", "settings": settings}
        if callback:
            component_id = f"progress{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component
    def tabs(self, settings, callback=None):
        component = {"type": "tabs", "settings": settings}
        if callback:
            component_id = f"tabs{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component
    def links(self, settings, callback=None):
        component = {"type": "links", "settings": settings}
        if callback:
            component_id = f"links{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component
    def alerts(self, settings, callback=None):
        component = {"type": "alerts", "settings": settings}
        if callback:
            component_id = f"alerts{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component
    def imageList(self, settings, callback=None):
        component = {"type": "imageList", "settings": settings}
        if callback:
            component_id = f"imageList{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component

    def dataGrid(self, settings, callback=None):
        component = {"type": "dataGrid", "settings": settings}
        if callback:
            component_id = f"dataGrid_{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component
    # ----------------- FUNCTIONS -------------------

    def add(self, component):
        self.components.append(component)
        return self
    
    def publish(self, script_code=None):
        styling = self._load_layout_data()
        tabStyling = self._load_tabLayout_data()
        
        print(url)
        print(script_code)
        if script_code is not None:
            # If script_code is provided, use it
            response = requests.post(f"{url}/publish/{self.app_name}", json={"components": self.components, "code": script_code, "styling": styling, "tab_styling": tabStyling})
        else:
            # If script_code is not provided, try to retrieve it from __main__
            try:
                import __main__
                script_code = open(__main__.__file__).read()
                response = requests.post(f"{url}/publish/{self.app_name}", json={"components": self.components, "code": script_code, "styling": styling, "tab_styling": tabStyling})
                print('response', response)
            except AttributeError:
                response = requests.post(f"{url}/publish/{self.app_name}", json={"components": self.components, "code": 'N/A', "styling": styling, "tab_styling": tabStyling})
                print('another one', response)

                # raise Exception("script_code is not provided, and __main__ module has no __file__ attribute.")

        self.wait_for_events()
        return response.json()
    
    def publishLocal(self, script_code=None):
        # start the server, start the front end, run electron
        global url
        url = 'http://localhost:8080'
        subprocess.Popen(["python3", '.\\local-version\\server.py'])
        subprocess.Popen(["npx", "serve", '.\\local-version\\out\\'])


        local_version_directory = '.\\local-version'
        os.chdir(local_version_directory)
        # Run the "npm run" command to execute Electron
        subprocess.Popen(['npm', 'start'])

    
    def publishFromAi(self, script_code=None):
        print("punlishing from AIs")
        print(self.app_name)
        print(self.components)         
        response = requests.post(f"{url}/publish/{self.app_name}", json={"components": self.components, "code": ""})
        self.wait_for_events()
        return response.json()
    
    def update(self):
        self.publish()
    
    def liveUpdate(self, script_code=None):
        if script_code is None:
            # If script_code is not provided, get the code of the current module
            script_code = inspect.getsource(self.__class__)

        import __main__
        script_code = open(__main__.__file__).read()
        
        styling = self._load_layout_data()
        tabStyling = self._load_tabLayout_data()
        print(styling)
        response = requests.post(f"{url}/publish/{self.app_name}", json={"components": self.components, "code": script_code, "styling": styling, "tab_styling": tabStyling})
        # self.wait_for_events()
        return response.json()

    def registerApp(self):
        print('register')
        print(self.app_name)
        response = requests.post(f"{url}/register-app/{self.app_name}", json=self.components)
        time.sleep(5)
        return response.json()
    
    def wait_for_events(self):
        # To keep the script running and listening for events
        try:
            self.sio.wait()
        except KeyboardInterrupt:
            print("Interrupted by user.")
            self.sio.disconnect()


    # ----------------- HELPER -----------------
    @staticmethod
    def _get_calling_script_code():
        # Get the frame of the caller (the script that imports and uses the TieUi class)
        caller_frame = inspect.currentframe().f_back

        # Get the filename of the calling script
        calling_script_file = caller_frame.f_globals['__file__']

        # Get the absolute path of the calling script
        calling_script_path = os.path.abspath(calling_script_file)

        # Read the contents of the calling script
        with open(calling_script_path, 'r') as script_file:
            script_code = script_file.read()

        return script_code