
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def dbc_top_title(title):
    return \
        dbc.Col(
            html.H1(title),
            style={
                "size": "30px",
                "background-color": "#1b1935",
                "color": "white",
                "textAlign": "center",
            },
        )

def dbc_title(title, width):
    return \
        dbc.Col(
            html.H4(title),
            width=width,
            style={
                "height": "100%",
                "background-color": "white",
                "textAlign": "left",
                "padding": "10px"
            },
        )

def dbc_graph(graph_id, width, fig):
    if fig != "":
        return \
        dbc.Col(
            dcc.Graph(
                id=graph_id,
                figure=fig
            ),
            width=width,
            style={
                "height": "100%",
                "background-color": "white",
                "border-color": "white",
                "border-width": "10px"
            },
        )
    else:
        return dbc.Col(html.P("no data"), width=width)

def dbc_graph_with_click(graph_id, width, fig, selected_data):
    return \
        dbc.Col(
            dcc.Graph(
                id=graph_id,
                selectedData=selected_data,
                figure=fig
            ),
            width=width,
            style={
                "height": "100%",
                "background-color": "white",
                "border-color": "white",
                "border-width": "10px"
            },
        )

def dbc_table(table_id, width, df):
    return \
        dbc.Col(
            generate_table(df),
            width=width,
            style={"height": "100%"}
        )

def dbc_race_info(race_sr):
    return \
        dbc.Col(
            html.H4(race_sr["場名"] + " " + str(race_sr["競走番号"]) + "R " + str(race_sr["距離"]) + "m " + race_sr["競走条件名称"]
                    + " 馬連荒れ：" + str(race_sr["UMAREN_ARE_RATE"]) + " 馬単荒れ：" + str(race_sr["UMATAN_ARE_RATE"]) + " 三連複荒れ：" + str(race_sr["SANRENPUKU_ARE_RATE"])),
            style={
                "height": "100%",
                "background-color": "white",
                "textAlign": "left",
                "padding": "10px"
            },
        )


def dbc_race_result(race_sr):
    return \
        dbc.Col(
            html.H4(str(race_sr["天候コード"]) + " " + str(race_sr["馬場状態コード"]) + " " + race_sr["ペース"]),
            style={
                "height": "100%",
                "background-color": "white",
                "textAlign": "left",
                "padding": "10px"
            },
        )