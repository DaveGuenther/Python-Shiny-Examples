from shiny import ui, reactive, module

@module.ui
def module_ui(game_name):
    return ui.input_action_button(id='btn_song', label=game_name).add_class('green').add_style('width:100%;'),

@module.server
def module_server(input, output, session, game_id, selected_game):

    @reactive.effect
    @reactive.event(input.btn_song)
    def set_selected_song():
        selected_game.set(game_id)


