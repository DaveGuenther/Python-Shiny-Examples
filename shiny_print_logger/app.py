## This example demonstrates how to use a simple logger to understand the flow of your shiny app
## use as follows:
##
## import logger
## Logger = logger.FunctionLogger
##
## Then inside a server function or server module:
## Logger(session.ns)
##
## You can also use outside a server function in a regular program with
## Logger()
##
## The logger will print to the console at the point you run Logger() and again when that function 
## from which it was called goes out of scope.

from shiny import App, ui, render, reactive, module

import logger

Logger = logger.FunctionLogger

# Uncomment to turn off the logger
#Logger.setLogger(False) 


@module.ui
def module_ui():
    return ui.output_text("server_msg"),

@module.server
def module_server(input, output, session):    
    @reactive.calc
    def get_id():
        Logger(session.ns, show_line_numbers=False)
        return session.ns
    
    @render.text
    def server_msg():
        Logger(session.ns, show_line_numbers=False)
        return f"This module's namespace ID is {get_id()}"

def run_ui_modules():
    return [module_ui('module_'+str(i)) for i in range(5)]

app_ui = ui.page_fluid(
    run_ui_modules()
)

def server(input, output, session):
    Logger(session.ns, show_line_numbers=False)
    for i in range(5):
        module_server('module_'+str(i))

app = App(app_ui, server, debug=False)
