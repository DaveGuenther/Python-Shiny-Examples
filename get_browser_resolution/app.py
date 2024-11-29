# This shiny example demonstrates how to store the browser resolution 
# into a reactive value to assist with responsive desktop/mobile shiny 
# designs.

from shiny import App, ui, render, reactive

import browser_tools

app_ui = ui.page_fluid(
    "Hello World",
    browser_tools.get_browser_res(),
    ui.output_text("browser_resolution_from_input"), # demonstrates how to just echo back the ui directly from its input element
    ui.output_text("browser_resolution_from_reactive_value"), # demonstrates how to store the input.dimension() into a reactive value that you could pass down to nested shiny modules
)

def server(input, output, session):
    
    browser_res = reactive.value(None)

    @reactive.effect
    @reactive.event(input.dimension) # updates every time the browser dimensions change
    def set_browser_resolution():
        browser_res.set(input.dimension())


    @render.text
    def browser_resolution_from_input():
        resolution = input.dimension()
        return f"input.dimension() is {resolution} pixels."

    @render.text
    def browser_resolution_from_reactive_value():
        resolution = browser_res()
        return f"reactive.value browser_res() is {resolution} pixels."

app = App(app_ui, server, debug=False)
