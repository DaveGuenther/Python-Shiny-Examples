# Shiny app for a custom "selectize" data viewer with selectable pills on the left and form data for the selected element on the right

# This shiny app demonstrated how to pass reactive values into shiny modules (buttons in a column in this case) and then update that reactive value 
# from within the module thereby kicking off the parent server function to use that data somehow.  In this case the app passes in a selected_game reactive value
# that represents a value from the 'id' column of the df_NES dataframe.  A button is created (as a shiny module) for each row in the df_NES['Name'] column.  
# Once a button is clicked, it's reactive effect/event updates the selected_item reactive value from the parent server function with the id value of that game.
# The parent server function then takes that selected_game reactive and pulls out the respective row of data as a series, rendering it's various column data
# in the red area on the right of the app window.

import pandas as pd
from shiny import App, ui, render, reactive
from pathlib import Path
import browser_tools # see get_browser_resolution example in this repository for reprex
import pill_module

# Data pulled from Wikipedia
df_NES = pd.DataFrame({
    'id':['0','1','2','3','4','5','6'],
    'Name':['Faxanadu','Metroid','Final Fantasy','Super Mario Bros. 3','The Legend of Zelda','Contra','Tetris'],
    'Genre':['Role-Playing','Action, Non-Linear','Role-Playing','Action','Role-Playing','Action, Arcade', 'Puzzle'],
    'Year':['1987','1986','1987','1988','1986','1987','1984'],
    'Description':[
        "Faxanadu is an action role-playing platform video game for the Nintendo Entertainment System. The name was licensed by computer game developer Nihon Falcom and was developed and released in Japan by Hudson Soft for the Famicom in 1987.",
        "Metroid is an action-adventure game franchise created by Nintendo. The player controls the bounty hunter Samus Aran, who protects the galaxy from Space Pirates and other malevolent forces and their attempts to harness the power of the parasitic Metroid creatures.",
        "Final Fantasy is a 1987 role-playing video game developed and published by Square. It is the first game in Square's Final Fantasy series, created by Hironobu Sakaguchi.",
        "Super Mario Bros. 3 is a 1988 platform game developed and published by Nintendo for the Nintendo Entertainment System. It was released for home consoles in Japan on October 23, 1988, in North America on February 12, 1990, and in Europe on August 29, 1991.",
        "The Legend of Zelda, originally released in Japan as The Hyrule Fantasy: Zelda no Densetsu, is an action-adventure game developed and published by Nintendo.",
        "Contra is a 1987 run and gun video game developed and published by Konami for arcades. A home version was released for the Nintendo Entertainment System in 1988, along with ports for various home computer formats, including the MSX2.",
        "Tetris is a puzzle video game created in 1985 by Alexey Pajitnov, a Soviet software engineer. It has been published by several companies on more than 65 platforms, setting a Guinness world record for the most ported game."
    ]
})

app_ui = ui.page_fluid(
    browser_tools.get_browser_res(),
    ui.tags.link(href='styles.css', rel="stylesheet"),
    ui.div(
        ui.row(
            ui.column(3,
                [pill_module.module_ui(id=game_id, song_name=game_name) for game_id, game_name in zip(df_NES['id'],df_NES['Name'])],  
                id="desktop-ui-placeholder"                
            ),
            ui.column(9,
                ui.div(
                    ui.h2("About This Game:"),
                    ui.div("Name:").add_class('main-content-title'),
                    ui.output_text(id='txtName').add_class('main-content-body'),
                    ui.div("Year:").add_class('main-content-title'),
                    ui.output_text(id='txtYear').add_class('main-content-body'),
                    ui.div("Genre:").add_class('main-content-title'),
                    ui.output_text(id='txtGenre').add_class('main-content-body'),            
                    ui.div("Description:").add_class('main-content-title'),
                    ui.output_text(id='txtDescription').add_class('main-content-body'),    
                ),        
            ).add_class('red'),
        ).add_class('blue'),
        id='wide-placeholder'
    ),
)


def server(input, output, session):
    # browser_resolution_stuff
    browser_res = reactive.value(None)
    @reactive.effect
    @reactive.event(input.dimension) # updates every time the browser dimensions change
    def set_browser_resolution():
        browser_res.set(input.dimension())

    # state info about what is currently selected
    selected_game=reactive.value(None)

    [pill_module.module_server(id=game_id, song_id=game_id, selected_game=selected_game) for game_id, game_name in zip(df_NES['id'],df_NES['Name'])]


    @reactive.effect
    @reactive.event(input.browser_res)
    def render_body():
        


    @reactive.calc
    def get_game_record_from_id():
        return df_NES[df_NES['id']==selected_game()].iloc[0]


    @render.text
    def txtName():
        ret_val = None
        if selected_game():
            ret_val = get_game_record_from_id()['Name']
        return ret_val

    @render.text
    def txtGenre():
        ret_val = None
        if selected_game():        
            ret_val = get_game_record_from_id()['Genre']
        return ret_val

    @render.text
    def txtYear():
        ret_val = None
        if selected_game():        
            ret_val = get_game_record_from_id()['Year']
        return ret_val

    @render.text
    def txtDescription():
        ret_val = None
        if selected_game():
            ret_val = get_game_record_from_id()['Description']
        return ret_val


app_dir = Path(__file__).parent
app = App(app_ui, server, debug=False, static_assets=app_dir / "www")