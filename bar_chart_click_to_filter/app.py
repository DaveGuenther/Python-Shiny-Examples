# Load data and compute static values
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_widget
import plotly.graph_objects as go
import pandas as pd
import palmerpenguins
import numpy as np

df_penguins = palmerpenguins.load_penguins()

app_ui = ui.page_fluid(
    ui.h1("Palmer Penguins Analysis"),
    # Main Panel
    ui.row(
        ui.column( 
            6,
            # Plot
            ui.card_header(ui.output_text('chart_title')),
            output_widget('penguin_plot'),
            ui.span("on_hover Data: "),
            ui.output_text_verbatim('hover_info_output'),
            ui.span("on_click Data: "),
            ui.output_text_verbatim('click_info_output'),
        ),
        ui.column( 
            6,
            # Table
            ui.card_header(ui.output_text('total_rows')),
            ui.column(
                12, #width
                ui.output_table('table_view'),
                style="height:300px; overflow-y: scroll"
            ),
            ui.input_action_button('reset','Reset Chart')
        )
    )
)

def server (input, output, session):
    click_filter=reactive.value({})
    hover_info=reactive.value({})

    def setHoverValues(trace, points, selector):
        if not points.point_inds:
            return
        hover_info.set(points)


    def setClickedValues(trace, points, selector):
        inds = np.array(points.point_inds)
        if not points.point_inds:
            return
        click_filter.set({'year':points.xs,'species':points.trace_name})

    # Dynamic Chart Title
    @render.text
    def chart_title():
        return "Number of Palmer Penguins by Year, colored by Species"

    @reactive.calc
    def df_filter():
        df_filtered = df_penguins
        if click_filter.get() == {}:
            return df_filtered
        # Add additional filters on dataset from segments selected on the visual
        df_filtered = df_filtered[
            (df_filtered['year'].isin(click_filter.get()['year'])) &
            (df_filtered['species'].isin([click_filter.get()['species']]))
        ]

        return df_filtered 
    
    @reactive.calc
    def df_summarized():
        return df_penguins.groupby(['year','species'], as_index=False).count().rename({'body_mass_g':"count"},axis=1)[['year','species','count']]

    @render_widget
    def penguin_plot():
        df_plot = df_summarized()
        bar_columns = list(df_plot['year'].unique()) # x axis column labels
        bar_segments = list(df_plot['species'].unique()) # bar segment category labels
        data = [go.Bar(name=segment, x=bar_columns,y=list(df_plot[df_plot['species']==segment]['count'].values), customdata=['species']) for segment in bar_segments]
        fig = go.Figure(data)
        fig.update_layout(barmode="stack")
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        figWidget = go.FigureWidget(fig)


        for trace in figWidget.data:
            trace.on_hover(setHoverValues)
            trace.on_click(setClickedValues)

        return figWidget
    
    @render.text
    def hover_info_output():
        return hover_info.get()

    @render.text
    def click_info_output():
        return click_filter.get()

    @render.text
    def total_rows():
        return "Total Rows: "+str(df_filter().shape[0])

    @render.table
    def table_view():
        return df_filter()

    @reactive.effect
    @reactive.event(input.reset)
    def reset_filters():
        click_filter.set({})

app = App(app_ui, server)