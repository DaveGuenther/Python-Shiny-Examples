from shiny import App, ui, reactive, render

# main ui object for the app
app_ui = ui.page_fluid(
    ui.div(
        (   "Welcome Screen",
            ui.input_text(id='str_val', label='Type in something'),
            ui.input_action_button(id="btn_welcome", label="Proceed!"),
        ),
        id="welcome_screen",
    ),
    ui.div(id="main_page")
)

# main server function for the app
def server(input, output, session):
    @reactive.effect
    @reactive.event(input.btn_welcome, ignore_init=True, ignore_none=True)
    def _():
        ui.remove_ui("#welcome_screen")
        
        ui.insert_ui(
            selector=f"#main_page", 
            where="beforeBegin",
            ui= ui.page_navbar(
                
                ui.nav_panel("Tab 1", "Tab 1 content",ui.output_text('str_val')),
                ui.nav_panel("Tab 2", "Tab 2 content"),
                ui.nav_panel("Tab 3", "Tab 3 content"),
                title="Main Page",
                id="page",
            ),
        )
        
    @render.text
    def str_val():
        return input.str_val()

app = App(app_ui, server)
