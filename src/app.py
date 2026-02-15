from shiny import App, ui

app_ui = ui.page_sidebar(

    # Filter Section
    ui.sidebar(
        ui.h4("Filters"),

        ui.hr(),

        ui.h5("Date Range"),
        ui.p("Date Range filter"),

        ui.hr(),

        ui.h5("Geography"),
        ui.p("State dropdown"),
        ui.p("City dropdown"),
        ui.p("Population slider"),

        ui.hr(),

        ui.h5("Crime Details"),
        ui.p("Crime category filter"),
        ui.p("Metric type selector"),
    ),

    # Visualization and Summary Section
    ui.h1("USA Crime Dashboard"),

    # KPI and Summary 
    ui.layout_columns(
        ui.card("Total Crimes"),
        ui.card("Crime Rate (per 100k)"),
        ui.card("Population (millions)"),
        ui.card("Most Common Crime"),
        ui.card("Change in Crime Rate"),
    ),

    ui.hr(),

    # Map and Top X Visuals
    ui.layout_columns(
        ui.card(
            ui.h5("Total Crime by State"),
            ui.p("Map placeholder")
        ),
        ui.card(
            ui.h5("Top 10 Crime Rates"),
            ui.p("Ranking placeholder")
        ),
    ),

    ui.hr(),

    # Time Series Charts
    ui.card(
        ui.h5("Total Number of Crimes Per Year"),
        ui.p("Stacked area chart placeholder")
    ),

    ui.hr(),

    # Full Data Table
    ui.card(
        ui.h5("Data Table"),
        ui.p("Interactive data table placeholder")
    )
)

def server(input, output, session):
    pass

app = App(app_ui, server)
