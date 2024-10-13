# Core
import os
from dotenv import load_dotenv

# Web/Visual frameworks
from shiny import App, ui, reactive

# pull database location and credential information from env variables
load_dotenv("variables.env")

app_ui = ui.page_fluid(

    ui.div(
        
        ui.h3("Please Enter Your Credentials:").add_style("text-align: center;"),
        ui.input_text(id='user',label="User Name:"),
        ui.input_password(id='password', label="Password:"),
        ui.input_action_button(id='btn_login',label='Login'),
        id="credentials_input",
    ),
    ui.div(id=f"rest_of_app"),

)

def server(input, output, session):
    
    @reactive.effect
    @reactive.event(input.btn_login, ignore_none=True, ignore_init=True)
    def btnLogin():
             
        with reactive.isolate():
            user_name=input.user()
            pw=input.password()
            if ((user_name == os.getenv('user_name'))&(pw == os.getenv('secret_pw'))):
                # remove user/pw screen
                ui.remove_ui(selector="#credentials_input")

                # Insert the main tabs
                ui.insert_ui(
                    selector=f"#rest_of_app", 
                    where="beforeBegin",
                    ui= ui.page_navbar(
                        # Rest of your app goes here
                        ui.nav_panel("First Tab", 
                            "Here is a tab",
                        ), 
                        ui.nav_panel("Songs",
                            "Here is another tab"
                        ),
                        title="My Awesome App",
                        id="page",
                    ),
                )


app = App(app_ui, server, debug=True)
