from tieui_module import TieUi

tie = TieUi(isLocal=True)


text_input_value = 0.0
text_input_value2 = 0
text_input_value3 = 0

def calculate_u(r, p, n):
    u_values = [p]
    
    for i in range (0 , n):
        u_i = r * u_values[i] * (1 - u_values[i]) #Logistic Map formula
        u_values.append(u_i)
        
    return u_values

def custom_button_callback_handler(item):
    print("CUSTOM")
    try:
        r = float(text_input_value)
        p = float(text_input_value2)
        n = int(text_input_value3)
        result = calculate_u(r, p, n)
        tie.components[4]['settings']['label'] = "Result: " + str(result[-1])  # I assume you want the last value, change this as needed
    except ValueError:
        tie.components[4]['settings']['label'] = "Invalid input"
    except TypeError:
        tie.components[4]['settings']['label'] = "Error in calculation"
    tie.update()

def handle_text_input_change(item):
    global text_input_value
    new_value = item.get("value", "")
    text_input_value = new_value

def handle_text_input_change2(item):
    global text_input_value2
    new_value = item.get("value", "")
    text_input_value2 = new_value

def handle_text_input_change3(item):
    global text_input_value3
    new_value = item.get("value", "")
    text_input_value3 = new_value

def handle_checkbox_change(item):
    print(item)
def handle_slider_change(item):
    print(item)
def handle_switch_change(item):
    print(item)
def handle_chip_clicked(item):
    val = item.get("value", "")
    if (val == "delete"):
        print("chip deleted")
    else:
        print("chip Clicked")
def handle_select_change(item):
    print(item)
    tie.components[11]['settings']['value'] = item.get("value", '')
    tie.update()

def handle_update(item):
    print("PUTO")
tie.add(tie.textBox({"id": "unique-id-1","label": "A Float R", "variant": "outlined"},handle_text_input_change))
tie.add(tie.textBox({"id": "unique-id-2","label": "Initial Value P", "variant": "outlined"},handle_text_input_change2))
tie.add(tie.textBox({"id": "unique-id-2","label": "Non Negative Integer", "variant": "outlined"},handle_text_input_change3))

tie.add(tie.button({"id": "unique-id-3", "label": "Add Numbers", "variant": "outlined"}, custom_button_callback_handler))
tie.add(tie.label({"label": "Result: ", "variant": "h6", "color": "black"}))
tie.add(tie.checkbox({"label": "Result: "}, handle_checkbox_change))
tie.add(tie.checkbox({"label": "Result: ", "labelPlacement": "bottom"}, handle_checkbox_change))
tie.add(tie.slider({"min": 5, "max": 30, "step": 1}, handle_slider_change))
tie.add(tie.switch({"label": "Result: "}, handle_switch_change))
tie.add(tie.chip({"label": "Result: "}, handle_chip_clicked))
tie.add(tie.chip({"label": "Result: ", "variant": "outlined"}, handle_chip_clicked))
tie.add(tie.progress({"color": "success"}))
options = [
    {"label": "Option 1", "value": "option1"},
    {"label": "Option 2", "value": "option2"},
    {"label": "Option 3", "value": "option3"},
]
# Add a select component to your TieUi application
tie.add(tie.select({
    "id": "unique-id-3",  # Replace with a unique identifier
    "options": options,  # List of selectable options
    "label": "Select label",
    "variant": "outlined",  # Variant of the select component
    "value": "option1"  # Provide a default value that matches one of the available options
}, handle_select_change))

data_grid_component = tie.dataGrid(
    {
        "rows": [
            {
                "id": 1,
                "column1": "Value 1",
            }
        ],
        "columns": [
            {
                "field": "column1",
                "headerName": "Column 1",
                "width": 150,
            }
        ],
        "options": {},  # Add any options you need for the DataGrid
    }
)
tie.add(data_grid_component)

tab1_components = [
    tie.label({"label": "Content for Tab 1", "variant": "body1"}),
    tie.chip({"label": "Result: "}, handle_chip_clicked),
    tie.select({
        "id": "unique-id-3",  # Replace with a unique identifier
        "options": [
    {"label": "Option 1", "value": "option1"},
    {"label": "Option 2", "value": "option2"},
    {"label": "Option 3", "value": "option3"},
],  # List of selectable options
        "label": "Select label",
        "variant": "outlined",  # Variant of the select component
        "value": "option1"  # Provide a default value that matches one of the available options
    }, handle_select_change)
]

tab2_components = [
    tie.label({"label": "Content for Tab 2", "variant": "body1"}),
    tie.button({"id": "unique-id-qw3", "label": "Add Numbers", "variant": "outlined"}, handle_update)
]

tabs_settings = {
    "value": 0,  # default active tab index
    "tab": [
        {"label": "Tab 1", "value": "tab1", "components": tab1_components},
        {"label": "Tab 2", "value": "tab2", "components": tab2_components},
        # ... more tabs if needed
    ]
}

tie.add(tie.links({"href": "https://tieui.app", "underline":"hover", "label": "underline hover"}))

tie.add(tie.tabs(tabs_settings))
tie.add(tie.alerts({"severity": "error", "label": "This is an error alert — check it out!"}))

# tie.registerApp()
tie.publish()