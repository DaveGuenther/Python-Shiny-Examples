from shiny import ui, reactive, module, render

@module.ui
def game_details_ui(song_id):
    ret_val=None
    if song_id:
        ret_val = ui.div(
            ui.div("Name:").add_class('main-content-title'),
            ui.output_text(id='txtName').add_class('main-content-body'),
            ui.div("Year:").add_class('main-content-title'),
            ui.output_text(id='txtYear').add_class('main-content-body'),
            ui.div("Genre:").add_class('main-content-title'),
            ui.output_text(id='txtGenre').add_class('main-content-body'),            
            ui.div("Description:").add_class('main-content-title'),
            ui.output_text(id='txtDescription').add_class('main-content-body'),  
        )
    return ret_val

@module.server
def game_details_server(input, output, session, game_id, df):

    def get_game_record_from_id():
        return df[df['id']==game_id].iloc[0]


    @render.text
    def txtName():
        ret_val = None
        if game_id:
            ret_val = get_game_record_from_id()['Name']
        return ret_val

    @render.text
    def txtGenre():
        ret_val = None
        if game_id:        
            ret_val = get_game_record_from_id()['Genre']
        return ret_val

    @render.text
    def txtYear():
        ret_val = None
        if game_id:        
            ret_val = get_game_record_from_id()['Year']
        return ret_val

    @render.text
    def txtDescription():
        ret_val = None
        if game_id:
            ret_val = get_game_record_from_id()['Description']
        return ret_val


@module.ui
def pill_ui(game_name):
    return ui.input_action_button(id='btn_game', label=game_name).add_class('green').add_style('width:100%;'),

@module.server
def pill_server(input, output, session, game_id, selected_game):

    @reactive.effect
    @reactive.event(input.btn_game)
    def set_selected_game():
        selected_game.set(game_id)


