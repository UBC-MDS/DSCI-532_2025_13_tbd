from shiny import App, ui, reactive, render
import pandas as pd
import altair as alt
from shinywidgets import output_widget, render_altair
from vega_datasets import data

# Load and Clean Raw Crime Data
df_raw = pd.read_csv("data/raw/crime_rate_data_raw.csv").drop(columns=["source", "url"])
df_raw = df_raw.rename(columns={"department_name": "city", "ORI": "state_id"})
df_raw["city"] = df_raw["city"].str.partition(",")[0]
df_raw["state_id"] = df_raw["state_id"].str[:2]

# Load and Clean US Cities Data
cities = pd.read_csv("data/uscities_raw.csv")
cities = cities[cities["state_name"] != "Puerto Rico"]
cities = cities[["city", "state_id", "lat", "lng"]]

# Merge Crime and City Data for Map Plot
df_merged = pd.merge(df_raw, cities, how="inner", on=["city", "state_id"])

# Get all cities
selected_cities = sorted(df_merged["city"].dropna().unique().tolist())

# Geographic data for the background map
states = alt.topo_feature(data.us_10m.url, feature="states")

# Get the State Names as a map to ids in states data
state_id_map = {
    0: "All",
    1: "Alabama (AL)",
    2: "Alaska (AK)",
    4: "Arizona (AZ)",
    5: "Arkansas (AR)",
    6: "California (CA)",
    8: "Colorado (CO)",
    9: "Connecticut (CT)",
    10: "Delaware (DE)",
    11: "District of Columbia (DC)",
    12: "Florida (FL)",
    13: "Georgia (GA)",
    15: "Hawaii (HI)",
    16: "Idaho (ID)",
    17: "Illinois (IL)",
    18: "Indiana (IN)",
    19: "Iowa (IA)",
    20: "Kansas (KS)",
    21: "Kentucky (KY)",
    22: "Louisiana (LA)",
    23: "Maine (ME)",
    24: "Maryland (MD)",
    25: "Massachusetts (MA)",
    26: "Michigan (MI)",
    27: "Minnesota (MN)",
    28: "Mississippi (MS)",
    29: "Missouri (MO)",
    30: "Montana (MT)",
    31: "Nebraska (NE)",
    32: "Nevada (NV)",
    33: "New Hampshire (NH)",
    34: "New Jersey (NJ)",
    35: "New Mexico (NM)",
    36: "New York (NY)",
    37: "North Carolina (NC)",
    38: "North Dakota (ND)",
    39: "Ohio (OH)",
    40: "Oklahoma (OK)",
    41: "Oregon (OR)",
    42: "Pennsylvania (PA)",
    44: "Rhode Island (RI)",
    45: "South Carolina (SC)",
    46: "South Dakota (SD)",
    47: "Tennessee (TN)",
    48: "Texas (TX)",
    49: "Utah (UT)",
    50: "Vermont (VT)",
    51: "Virginia (VA)",
    53: "Washington (WA)",
    54: "West Virginia (WV)",
    55: "Wisconsin (WI)",
    56: "Wyoming (WY)",
}

# Convert Mapping id's to a data frame
mapping_df = pd.DataFrame(list(state_id_map.items()), columns=["id", "state_name"])

# Configure plot settings for bubbles in map_plot
CRIME_CONFIG = {
    "violent": {
        "color": "#800000",
        "column": "violent_crime",
        "title": "Violent Crime",
    },
    "homs": {"color": "#191970", "column": "homs_sum", "title": "Homicides"},
    "rape": {"color": "#006064", "column": "rape_sum", "title": "Rapes"},
    "rob": {"color": "#A0522D", "column": "rob_sum", "title": "Robberies"},
    "agg_ass": {
        "color": "#2F4F4F",
        "column": "agg_ass_sum",
        "title": "Aggravated Assault",
    },
}


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
                "closeAfterSelect": True,
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
            value=(
                int(df_raw["violent_crime"].min()),
                int(df_raw["violent_crime"].max()),
            ),
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
        ui.card(ui.h5("Total Crime by State"), ui.p("Map placeholder")),
        ui.card(ui.h5("Top 10 Crime Rates"), ui.p("Ranking placeholder")),
    ),
    ui.hr(),
    # Aggregated Crime Line Plot
    ui.card(
        ui.h5("Violent crime over time"),
        output_widget("line_plot"),
    ),
    ui.hr(),
    # Full Data Table
    ui.card(ui.h5("Data Table"), ui.p("Interactive data table placeholder")),
)


def server(input, output, session):
    @reactive.calc
    def filtered_df():
        df = df_raw.copy()

        vmin, vmax = input.violent_range()
        df = df[(df["violent_crime"] >= vmin) & (df["violent_crime"] <= vmax)]

        selected = list(input.cities())
        if selected and "All" not in selected:
            df = df[df["city"].isin(selected)]

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
            return (
                alt.Chart(pd.DataFrame({"msg": ["No data after filtering"]}))
                .mark_text(size=16)
                .encode(text="msg:N")
            )

        selected = list(input.cities())
        multi = selected and ("All" not in selected)

        if multi:
            plot_df = df.groupby(["year", "city"], as_index=False)[
                "violent_crime"
            ].sum()
            return (
                alt.Chart(plot_df)
                .mark_line()
                .encode(
                    x=alt.X("year:Q", title="Year"),
                    y=alt.Y("violent_crime:Q", title="Violent crime (count)"),
                    color=alt.Color("city:N", title="City/Dept"),
                    tooltip=["year:Q", "city:N", "violent_crime:Q"],
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
