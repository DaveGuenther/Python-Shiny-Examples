# This shiny example demonstrates how to conditionally style parts of dataframe cells by 
# combining ui.HTML() and pandas.apply().

from shiny import App, ui, render, reactive
import pandas as pd
df = pd.DataFrame(
    {'Base Text':['are red,','are blue,','is sweet,','and so is data!'],
     'Special Text':['Roses','Violets', 'Sugar',''],
     'Color':['red','#0000ff', '#00ff00',''],
     }
)

app_ui = ui.page_fluid(
    ui.h3("Using Raw HTML in Cell"),
    ui.output_data_frame('styled_dataframe_HTML'),
    ui.br(),
    ui.h3("Using Shiny tags attributes in Cell"),
    ui.output_data_frame('styled_dataframe_tags'),
)


def server(input, output, session):

    @render.data_frame
    def styled_dataframe_HTML():    

        def style_dataframe_cell_w_HTML(row):
            special_text=row['Special Text']
            base_text=row['Base Text']
            color=row['Color']
            rendered_html = ui.HTML(f'<div><span style="color:{color}">{special_text} </span> <span>{base_text}</span></div>')
            return rendered_html

        df['HTML Output'] = df.apply(lambda row: style_dataframe_cell_w_HTML(row), axis=1)
        return render.DataGrid(df[['Base Text','Special Text','Color','HTML Output']])

    @render.data_frame
    def styled_dataframe_tags():  

        def style_dataframe_cell_w_tags(row):
            special_text=row['Special Text']
            base_text=row['Base Text']
            color=row['Color']
            rendered_html = ui.div(
                ui.span(row['Special Text']).add_style('color:'+row['Color']+';'),
                ui.span(' ',row['Base Text']),
            )
            return rendered_html        

        df['tags Output'] = df.apply(lambda row: style_dataframe_cell_w_tags(row), axis=1)
        return render.DataGrid(df[['Base Text','Special Text','Color','tags Output']])
    

app = App(app_ui, server, debug=False)
