import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as Table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import pandas as pd
import numpy
import math

external_stylesheets = ["assets/chrisP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Data
df = pd.read_csv("assets/athlete_events.csv")
official_countries = pd.read_csv("assets/countries.csv")

df = df.dropna(subset=["Medal"])
df_all = df
df = df[df["Team"].isin(official_countries["Country"])]
countries = numpy.unique(df["Team"])

sport_list = numpy.sort(numpy.unique(df["Sport"]))
sport_list = numpy.insert(sport_list, 0, "All Sports")
sport_options = [{"label": sport, "value": sport} for sport in sport_list]

app.layout = html.Div(
    [
        html.Div(
            # Graph Title and Olympic Rings
            className="Title",
            style={
                "text-align": "center",
                "width": "100%",
                "color": "#FBE4DE",
                "height": "10px",
            },
            children=[
                html.Div(
                    className="six columns offset-by-three columns",
                    children=[html.H1("All Time Olympic Medals")],
                ),
                html.Div(
                    style={"display": "inline-block", "margin-left": "13%"},
                    children=[
                        html.Img(
                            src="assets/olympic_rings.png",
                            alt="Olympic Rings",
                            width="140px",
                        )
                    ],
                ),
            ],
        ),
        html.Div(
            # Dropdown Titles
            className="row",
            children=[
                html.Div(
                    className="Title four columns offset-by-one column",
                    children=[html.H2("Sport")],
                ),
                html.Div(
                    className="Title four columns offset-by-two columns",
                    children=[html.H2("Event")],
                ),
            ],
        ),
        html.Div(
            className="row",
            style={"margin-bottom": "10px"},
            children=[
                # Sport
                html.Div(
                    className="four columns offset-by-one column",
                    style={"display": "inline-block"},
                    children=[
                        dcc.Dropdown(
                            id="sport_all_time", value="Canoeing", options=sport_options
                        )
                    ],
                ),
                # Event
                html.Div(
                    className="four columns offset-by-two columns",
                    style={"display": "inline-block"},
                    children=[dcc.Dropdown(id="event_all_time", value="All Events")],
                ),
            ],
        ),
        html.Div(
            # Country Comparison
            className="row",
            style={"margin-bottom": "10px"},
            children=[
                html.Div(
                    className="twelve columns",
                    children=[dcc.Graph(id="all_time_comparison")],
                )
            ],
        ),
        # Graph Titles
        html.Div(
            className="Title",
            style={
                "text-align": "center",
                "width": "100%",
                "color": "#FBE4DE",
                "height": "110px",
            },
            children=[
                html.Div(
                    className="six columns offset-by-three columns",
                    children=[html.H1("Olympic Medals by Country")],
                )
            ],
        ),
        html.Div(
            # Dropdown Titles
            className="row",
            children=[
                html.Div(
                    className="seven columns",
                    children=[
                        html.Div(
                            className="Title four columns",
                            style={"display": "inline-block"},
                            children=[html.H2("Country")],
                        ),
                        html.Div(
                            className="Title four columns",
                            style={"display": "inline-block"},
                            children=[html.H2("Sport")],
                        ),
                        html.Div(
                            className="Title four columns",
                            style={"display": "inline-block"},
                            children=[html.H2("Event")],
                        ),
                    ],
                ),
                html.Div(
                    className="five columns",
                    children=[
                        html.Div(
                            className="Title twelve columns",
                            style={"display": "inline-block"},
                            children=[html.H2("Year Range")],
                        )
                    ],
                ),
            ],
        ),
        html.Div(
            # Input Dropdowns
            className="row",
            children=[
                html.Div(
                    className="seven columns",
                    children=[
                        # Country
                        html.Div(
                            className="four columns",
                            style={"display": "inline-block"},
                            children=[
                                dcc.Dropdown(
                                    id="country",
                                    options=[
                                        {"label": country, "value": country}
                                        for country in countries
                                    ],
                                    value="Canada",
                                )
                            ],
                        ),
                        # Sport
                        html.Div(
                            className="four columns",
                            style={"display": "inline-block"},
                            children=[dcc.Dropdown(id="sport", value="All Sports")],
                        ),
                        # Event
                        html.Div(
                            className="four columns",
                            style={"display": "inline-block"},
                            children=[
                                dcc.Dropdown(id="event", value="All Events", style={})
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="five columns",
                    children=[
                        # Year selectors
                        html.Div(
                            style={
                                "margin-bottom": "45px",
                                "z-index": "1000",
                                "position": "relative",
                            },
                            id="year_select",
                            children=[
                                html.Div(dcc.Dropdown(id="start_year", value=0)),
                                html.Div(dcc.Dropdown(id="end_year", value=0)),
                                html.Div(dcc.RangeSlider(id="year", value=[])),
                            ],
                        )
                    ],
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                # Graph
                html.Div(
                    className="seven columns",
                    style={"background-color": "#D0E2ED"},
                    children=[dcc.Graph(id="country_stats")],
                ),
                html.Div(
                    className="five columns",
                    children=[
                        # Table
                        html.Div(
                            children=[
                                Table.DataTable(
                                    n_fixed_rows=1,
                                    id="medalists",
                                    style_cell={
                                        "minWidth": "0px",
                                        "maxWidth": "180px",
                                        "whiteSpace": "normal",
                                        "text-align": "center",
                                    },
                                    style_table={"maxHeight": "400px"},
                                    css=[
                                        {
                                            "selector": ".dash-cell div.dash-cell-value",
                                            "rule": "display: inline; white-space: inherit;\
                                             overflow: inherit; text-overflow: inherit;",
                                        }
                                    ],
                                    columns=[
                                        {"name": i, "id": i}
                                        for i in ["Name", "Year", "Event", "Medal"]
                                    ],
                                )
                            ]
                        )
                    ],
                ),
            ],
        ),
    ]
)


# Filter to show only country's statistics
def sort_country(country):
    return df[df["Team"] == country]


# Filter to show only country's statistics for a given sport
def sort_sport(country, sport):
    df_country = sort_country(country)
    return df_country[df_country["Sport"] == sport]


# Filter to show only country's statistics for a given event
def sort_event(country, sport, event):
    df_event = sort_sport(country, sport)
    return df_event[df_event["Event"] == event]


# Update sport options based on country
@app.callback(
    [Output("sport", "options"), Output("sport", "value")],
    [Input("country", "value")],
    [State("sport", "value")],
)
def find_sports(country, cur_sport):
    df_country = sort_country(country)
    df_sport = numpy.unique(df_country["Sport"])
    new_sport = "All Sports"
    if cur_sport in df_sport:
        new_sport = cur_sport
    df_sport = numpy.insert(df_sport, 0, "All Sports")
    return [{"label": sport, "value": sport} for sport in df_sport], new_sport


# Update event options based on country and sport
@app.callback(
    [Output("event", "options"), Output("event", "value")],
    [Input("sport", "value")],
    [State("country", "value"), State("event", "value")],
)
def find_event(sport, country, cur_event):
    df_sport = sort_sport(country, sport)
    df_event = numpy.unique(df_sport["Event"])
    new_event = "All Events"
    if cur_event in df_event:
        new_event = cur_event
    df_event = numpy.insert(df_event, 0, "All Events")
    return [{"label": event, "value": event} for event in df_event], new_event


# Update event_all_time options based on sport
@app.callback(
    [Output("event_all_time", "options"), Output("event_all_time", "value")],
    [Input("sport_all_time", "value")],
)
def find_event_all_time(sport):
    df_sport = df_all[df_all["Sport"] == sport]
    df_event = numpy.unique(df_sport["Event"])
    df_event = numpy.insert(df_event, 0, "All Events")
    return [{"label": event, "value": event} for event in df_event], "All Events"


# Determine type of input box for years
@app.callback(
    Output("year_select", "children"),
    [Input("event", "value")],
    [State("country", "value"), State("sport", "value")],
)
def find_years(event, country, sport):
    year_list = find_year_df(country, sport, event)[0]
    if len(year_list) < 10 and len(year_list) > 0:
        child = [
            html.Div(
                style={"margin-right": "10px"},
                children=[
                    dcc.RangeSlider(
                        id="year",
                        min=min(year_list),
                        max=max(year_list),
                        step=None,
                        marks={str(year): str(year) for year in year_list},
                        value=[min(year_list), max(year_list)],
                        allowCross=False,
                    )
                ],
            ),
            html.Div(
                style={"display": "none"},
                children=[
                    dcc.Dropdown(id="start_year", style={"display": "none"}, value=0)
                ],
            ),
            html.Div(
                style={"display": "none"},
                children=[
                    dcc.Dropdown(id="end_year", style={"display": "none"}, value=0)
                ],
            ),
        ]
    else:
        min_year = 1896
        max_year = 2016
        if year_list.size != 0:
            min_year = min(year_list)
            max_year = max(year_list)
        options = [{"label": str(year), "value": year} for year in year_list]
        child = [
            html.Div(
                className="six columns",
                children=[
                    dcc.Dropdown(id="start_year", value=min_year, options=options)
                ],
            ),
            html.Div(
                className="six columns",
                children=[dcc.Dropdown(id="end_year", value=max_year, options=options)],
            ),
            html.Div(
                style={"display": "none"},
                children=[dcc.RangeSlider(id="year", value=[])],
            ),
        ]
    return child


# Select df based on sport, event
def find_sport_year(sport, event):
    if sport == "All Sports":
        df_final = df_all
    elif event == "All Events":
        df_final = df_all[df_all["Sport"] == sport]
    else:
        df_sport = df_all[df_all["Sport"] == sport]
        df_final = df_all[df_all["Event"] == event]
    return df_final


# Determine years and select df based on those years
def find_year_df(country, sport, event):
    year_list = []
    if sport == "All Sports":
        df_final = sort_country(country)
        year_list = numpy.unique(df["Year"])
    elif event == "All Events":
        df_final = sort_sport(country, sport)
        df_sport = df[df["Sport"] == sport]
        year_list = numpy.unique(df_sport["Year"])
    else:
        df_final = sort_event(country, sport, event)
        df_sport = df[df["Sport"] == sport]
        df_event = df[df["Event"] == event]
        year_list = numpy.unique(df_event["Year"])
    year_list.sort()
    return [year_list, df_final]


# Update the all time graph based on sport,country
@app.callback(
    Output("all_time_comparison", "figure"),
    [Input("event_all_time", "value")],
    [State("sport_all_time", "value")],
)
def update_all_time_graph(event, sport):
    figure_data = []
    df_event = find_sport_year(sport, event)
    for i in df_event["Team"].unique():
        temp_df = df_event[df_event["Team"] == i]
        total_medals = len(temp_df)
        if total_medals < 1:
            continue
        years = numpy.unique(temp_df["Year"])
        medals = [len(temp_df[temp_df["Year"] == year]) for year in years]
        figure_data.append(
            go.Scatter(
                x=years,
                y=medals,
                mode="lines+markers",
                text="{}".format(i),
                name="{}".format(i),
            )
        )
    figure = {
        "data": figure_data,
        "layout": go.Layout(
            xaxis={"title": "Year", "type": "linear"},
            yaxis={
                "title": "# of medals for {} in {}".format(sport, event),
                "type": "linear",
            },
            plot_bgcolor="#CCE5E6",
            paper_bgcolor="#CCE5E6",
            margin={"l": 60, "b": 50, "t": 40, "r": 0},
            height=450,
        ),
    }
    return figure


# Update the by country graph based on the selections
@app.callback(
    [Output("country_stats", "figure"), Output("medalists", "data")],
    [
        Input("event", "value"),
        Input("year", "value"),
        Input("start_year", "value"),
        Input("end_year", "value"),
    ],
    [State("country", "value"), State("sport", "value")],
)
def update_graph(event, year, start_year, end_year, country, sport):
    df_vals = find_year_df(country, sport, event)
    filtered_df = df_vals[1]
    if len(year) != 0:
        start_year = year[0]
        end_year = year[1]
    x = [
        cur_year
        for cur_year in df_vals[0]
        if cur_year >= start_year and cur_year <= end_year
    ]

    y = [len(filtered_df[filtered_df["Year"] == year]) for year in x]
    # Line Graph
    figure1 = {
        "data": [go.Scatter(x=x, y=y, mode="lines+markers")],
        "layout": go.Layout(
            xaxis={"title": "Year", "type": "linear"},
            yaxis={
                "title": "# of medals for {} in {} ({})".format(sport, event, country),
                "type": "linear",
            },
            plot_bgcolor="#CCE5E6",
            paper_bgcolor="#CCE5E6",
            margin={"l": 40, "b": 30, "t": 10, "r": 0},
            height=450,
        ),
    }

    medalists = filtered_df[filtered_df.Medal.notnull()]
    medalists = medalists[["Name", "Year", "Event", "Medal"]]
    medalists = medalists[
        (medalists["Year"] >= start_year) & (medalists["Year"] <= end_year)
    ]
    medalists = medalists.sort_values("Year")
    table_data = medalists.to_dict("records")

    return figure1, table_data


if __name__ == "__main__":
    app.run_server(debug=True)
