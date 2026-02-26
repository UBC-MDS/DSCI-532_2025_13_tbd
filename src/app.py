from shiny import App, ui, reactive, render
import pandas as pd
import altair as alt
from shinywidgets import output_widget, render_altair

# Load raw data
df_raw = pd.read_csv("data/raw/crime_rate_data_raw.csv")
selected_cities = sorted(df_raw["department_name"].dropna().unique().tolist())

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
        ui.input_selectize(
            "cities",
            "City / Department",
            choices=["All"] + selected_cities,
            selected=["All"],
            multiple=True,
            options={
                "plugins": ["remove_button"],
                "placeholder": "All (default) or search cities...",
                "maxOptions": 150,
                "closeAfterSelect": True
            },
        ),
        ui.p("Population slider"),

        ui.hr(),

        ui.h5("Crime Details"),
        ui.p("Crime category filter"),
        # Aggregated crime filter
        ui.input_slider(
            "violent_range",
            "Violent Crime Range",
            min=int(df_raw["violent_crime"].min()),
            max=int(df_raw["violent_crime"].max()),
            value=(int(df_raw["violent_crime"].min()),int(df_raw["violent_crime"].max()))
        ),
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

    # Aggregated Crime Line Plot
    ui.card(
        ui.h5("Violent crime over time"),
        output_widget("line_plot"),
    ),

    ui.hr(),

    # Full Data Table
    ui.card(
        ui.h5("Data Table"),
        ui.p("Interactive data table placeholder")
    )
)

def server(input, output, session):
    @reactive.calc
    def filtered_df():
        df = df_raw.copy()

        vmin, vmax = input.violent_range()
        df = df[(df["violent_crime"] >= vmin) & (df["violent_crime"] <= vmax)]

        selected = list(input.cities())
        if selected and "All" not in selected:
            df = df[df["department_name"].isin(selected)]

        return df

    @render.text
    def debug_line_plot():
        df = filtered_df()
        return (
            f"rows: {len(df)}\n"
            f"cities: {list(input.cities())}\n"
            f"violent_range: {input.violent_range()}\n"
        )

    @render_altair
    def line_plot():
        df = filtered_df().copy()

        df["year"] = pd.to_numeric(df["year"], errors="coerce")
        df["violent_crime"] = pd.to_numeric(df["violent_crime"], errors="coerce")
        df = df.dropna(subset=["year", "violent_crime"])

        if df.empty:
            return alt.Chart(pd.DataFrame({"msg": ["No data after filtering"]})).mark_text(size=16).encode(text="msg:N")

        selected = list(input.cities())
        multi = selected and ("All" not in selected)

        if multi:
            plot_df = df.groupby(["year", "department_name"], as_index=False)["violent_crime"].sum()
            return (
                alt.Chart(plot_df)
                .mark_line()
                .encode(
                    x=alt.X("year:Q", title="Year"),
                    y=alt.Y("violent_crime:Q", title="Violent crime (count)"),
                    color=alt.Color("department_name:N", title="City/Dept"),
                    tooltip=["year:Q", "department_name:N", "violent_crime:Q"],
                )
                .properties(width="container", height=340)
            )

        plot_df = df.groupby("year", as_index=False)["violent_crime"].sum()
        return (
            alt.Chart(plot_df)
            .mark_line()
            .encode(
                x=alt.X("year:Q", title="Year"),
                y=alt.Y("violent_crime:Q", title="Violent crime"),
                tooltip=["year:Q", "violent_crime:Q"],
            )
            .properties(width="container", height=340)
        )

app = App(app_ui, server)
