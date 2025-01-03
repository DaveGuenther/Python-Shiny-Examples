# Shiny app attempts to offer a responsive view that flips between a selectize view for wide desktops and
# an accordion view for mobile views (view where the window.innerWidth < 700px).  It builds upon previous 
# examples: get_browser_resolution, and pill_sidebar_layout.
#
# Essentially, this view creates a wide AND narrow version of the view (in two separate ways) and then 
# renders the content using ui.insert_ui/iu.remove_ui with a main placeholder 'dynamic-ui-placeholder'

import pandas as pd
from shiny import App, ui, render, reactive
from pathlib import Path
import browser_tools # see get_browser_resolution example in this repository for reprex
import shiny_modules

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
        ui.div(
            id='dynamic-ui-placeholder'
        ),
        id='horizontal-flex'
    )
)
def make_accordion_panels(game_id):
    ret_val = []
    for game_id in df_NES['id']:
        row = df_NES[df_NES['id']==game_id].iloc[0]
        ret_val.append(
            ui.accordion_panel(
                ui.div(
                    row['Name']
                ).add_class('green').add_style('width:100%;'),
                ui.div(
                    ui.h2("About This Game:"),
                    shiny_modules.game_details_ui(game_id,game_id),
                ).add_class('red'),  
                value=row['Name'],
            )
        )
    return ret_val

def server(input, output, session):
    # browser_resolution_stuff
    browser_res = reactive.value(None)
    @reactive.effect
    @reactive.event(input.dimension) # updates every time the browser dimensions change
    def set_browser_resolution():
        browser_res.set(input.dimension())

    # state info about what is currently selected
    selected_game=reactive.value(None)

    #set up server modules for wide-view server cards
    [shiny_modules.pill_server(id='wide_'+game_id, game_id=game_id, selected_game=selected_game) for game_id, game_name in zip(df_NES['id'],df_NES['Name'])]

    #set up server modules for game details sections
    [shiny_modules.game_details_server(id=game_id, game_id=game_id, df=df_NES) for game_id, in df_NES['id']]

    @reactive.effect
    @reactive.event(browser_res, selected_game)
    def render_body():
        if browser_res()[0]>=677:
            ui.remove_ui("#wide-ui-placeholder")
            ui.remove_ui("#narrow-ui-placeholder")
            ui.insert_ui(
                selector=f"#dynamic-ui-placeholder", 
                where="afterBegin", # nest inside 'dynamic-ui-placeholder' element
                ui= ui.div(
                    ui.row(
                        ui.column(5,
                            [shiny_modules.pill_ui(id='wide_'+game_id, game_name=game_name) for game_id, game_name in zip(df_NES['id'],df_NES['Name'])],                  
                        ),
                        ui.column(7,
                            ui.div(
                                ui.h2("About This Game:"),
                                shiny_modules.game_details_ui(selected_game(),selected_game()),
                            ),        
                        ).add_class('red'),
                    ).add_class('blue'),
                    id='wide-ui-placeholder'
                )
            )
        else:
            ui.remove_ui("#narrow-ui-placeholder")
            ui.remove_ui("#wide-ui-placeholder")
            ui.insert_ui(
                selector=f"#dynamic-ui-placeholder", 
                where="afterBegin", # nest inside 'dynamic-ui-placeholder' element
                ui= ui.div(
                    ui.accordion(*make_accordion_panels(selected_game()), id="acc_single", multiple=False).add_class('green'),
                    id='narrow-ui-placeholder'
                )
            )


app_dir = Path(__file__).parent
app = App(app_ui, server, debug=False, static_assets=app_dir / "www")