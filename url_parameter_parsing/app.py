# This app demonstrates how to pass and parse url parameters to Shiny apps.
# Once this app is loaded, pull it up in a browser and then add the following string after the url to demonstrate '?name=Bob&relation=Uncle&id=1337&answer=42'

from shiny import App, render, ui, reactive

app_ui = ui.page_fluid(
    ui.panel_title("URL Parameter Parsing App"),
    ui.input_text(id='txt_url_id', label="Enter an ID:"),
    ui.input_action_button(id='btn_submit', label='Submit'),
    ui.output_text_verbatim("submit_msg"),
)


def server(input, output, session):
   
    reactive_id = reactive.value(None) # This value is set automatically on app load to the id= value if one exists in the url string
    output_msg = reactive.value(None) # This contains the string message rendered by submit_msg()

    @reactive.effect # Run this reactive block once when application opens
    def getURL_Params():
        with reactive.isolate():
            # process url parameter string into dictionary
            url_param_string=session.input[".clientdata_url_search"]().replace('?','') ## start with string like 'id=1137&name=Bob&food=cake'
            url_param_list=url_param_string.split("&") # turn into list like ['id=1137','name=Bob','food=cake']
            key_value_pair_list = [parameter.split('=') for parameter in url_param_list] # turn into nested list like [['id','1137'],['name','Bob'],['food','cake']]
            if key_value_pair_list==[['']]:
                #no url parameters were provided at all
                param_dict={}
            else:
                # at least one parameter was identified
                param_dict = {param[0]:param[1] for param in key_value_pair_list} # finally get to dict like {'id':'1137','name':'Bob','food':'cake'}
            id_val = None if 'id' not in param_dict.keys() else param_dict['id']
            # set reactive_id to the id parameter of the URL
            reactive_id.set(id_val)
            # update ui text input element with URL parameter
            ui.update_text(id="txt_url_id", label="Enter an ID:", value=reactive_id())        
            print(session.input[".clientdata_url_search"]())

    @reactive.effect
    @reactive.event(input.btn_submit, ignore_init=True)
    def btn_submit_on_click():
        if input.txt_url_id()!=reactive_id():
            output_msg.set(input.txt_url_id())
        else:
            output_msg.set(reactive_id())
    
    @render.text
    def submit_msg():
        url_id = output_msg()
        ret_val = f"Your ID is: {url_id}" if url_id else ""           
        return ret_val


app = App(app_ui, server)
