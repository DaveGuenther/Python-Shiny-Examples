# This shiny app 

from shiny import App, ui, render, reactive
from pathlib import Path

app_ui = ui.page_fluid(
    ui.row(
        ui.column(

        ).add_style('width:200px;'),
        ui.column("Main Content")
    )
    )

def server(input, output, session):
    pass    

app_dir = Path(__file__).parent
app = App(app_ui, server, debug=False, static_assets=app_dir / "www")