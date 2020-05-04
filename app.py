from __future__ import print_function
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import flask

import pandas as pd

import pages.toppage as p1
import pages.return_analytics as p2
import pages.kpi_analytics as p3
import pages.race_trend as p4
import pages.race_info as p5
import pages.graph_example as p6
import pages.graph_example2 as p7
import pages.race_result as p8
from components.get_data import GetData
import components.calc_data as cd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__) # define flask app.server
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("LocalHR Dashboard", className="display-4"),
        html.Hr(),
        html.P(
            "ダッシュボード", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("TOP", href="/page-1", id="page-1-link"),
                dbc.NavLink("回収率分析", href="/page-2", id="page-2-link"),
                dbc.NavLink("KPI分析", href="/page-3", id="page-3-link"),
                dbc.NavLink("レース傾向", href="/page-4", id="page-4-link"),
                dbc.NavLink("レース情報", href="/page-5", id="page-5-link"),
                dbc.NavLink("レース結果", href="/page-8", id="page-8-link"),
                dbc.NavLink("グラフ例", href="/page-6", id="page-6-link"),
                dbc.NavLink("グラフ例2", href="/page-7", id="page-7-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

## -------------------- toppage用コールバック -------------------------------##
@app.callback(
    Output('top_dashoboard', 'children'),
    [Input('toppage-date-picker-range', 'start_date'),
     Input('toppage-date-picker-range', 'end_date')]
)
def toppage_render_top_dashboard(start_date, end_date):
    print(f"---------toppage_render_top_dashboard callback: {start_date} {end_date}")
    if start_date != None and end_date != None:
        print("render_toppage: get_data")
        raceuma_df = GetData.get_raceuma_data(start_date, end_date)
        bet_df = GetData.get_bet_data(start_date, end_date)
        return p1.toppage_render(raceuma_df, bet_df)

## -------------------- return_analytics用コールバック -------------------------------##
@app.callback(
    Output('return_analytics', 'children'),
    [Input('return-analytics-date-picker-range', 'start_date'),
     Input('return-analytics-date-picker-range', 'end_date')]
)
def return_analytics_render_return_analytics(start_date, end_date):
    print(f"---------return_analytics_render_children callback: {start_date} {end_date}")
    if start_date != None and end_date != None:
        print("render_return_analytics: get_data")
        raceuma_df = GetData.get_raceuma_data(start_date, end_date)
        bet_df = GetData.get_bet_data(start_date, end_date)
        haraimodoshi_dict = GetData.get_haraimodoshi_dict(start_date, end_date)
        return p2.return_analytics_render(raceuma_df, bet_df, haraimodoshi_dict)


## -------------------- race_info用コールバック -------------------------------##
# 日付を指定、指定した場所をリストに表示させる
@app.callback(
    Output('raceinfo-dropdown-keibajo', 'options'),
    [Input('raceinfo-date-picker-single', 'date')]
)
def raceinfo_set_keibajo_list_option(date):
    print(f"---------raceinfo_set_keibajo_list_option callback: {date}")
    race_df = GetData.get_race_data(date, date)
    ba_list_df = race_df[race_df["月日"] == date][["場名"]].rename(columns={"場名": "label"})
    ba_list_df.loc[:, "value"] = ba_list_df["label"]
    ba_list = ba_list_df.drop_duplicates().to_dict(orient='record')
    return ba_list

# 場所を指定、指定した場所のレースIDをリストを表示させる
@app.callback(
    Output('raceinfo-dropdown-keibajo', 'value'),
    [Input('raceinfo-dropdown-keibajo', 'options')]
)
def raceinfo_set_keibajo_list_value(set_ba_list_option):
    print("---------raceinfo_set_keibajo_list_value callback)")
    return set_ba_list_option

# 場所を指定、指定した場所のレースIDをリストを表示させる
@app.callback(
    Output('raceinfo-dropdown-raceid', 'options'),
    [Input('raceinfo-dropdown-keibajo', 'value'),
     Input('raceinfo-date-picker-single', 'date')]
)
def raceinfo_set_raceid_list_option(ba_name, date):
    if type(ba_name) == str:
        print(f"---------raceinfo_set_raceid_list_option callback: {ba_name} {date}")
        race_df = GetData.get_race_data(date, date)
        race_list_df = race_df[race_df["場名"] == ba_name][["競走コード", "競走番号"]].rename(columns={"競走番号": "label", "競走コード": "value"})
        race_list = race_list_df.drop_duplicates().to_dict(orient='record')
    else:
        race_list = []
    return race_list

# 場所を指定、指定した場所のレースIDをリストを表示させる
@app.callback(
    Output('raceinfo-dropdown-raceid', 'value'),
    [Input('raceinfo-dropdown-raceid', 'options')]
)
def raceinfo_set_raceid_list_value(set_raceid_list_option):
    print("---------raceinfo_set_raceid_list_value callback)")
    return set_raceid_list_option


# レースIDを指定、指定したIDの情報を詳細ページに表示させる
@app.callback(
    Output('raceinfo-race-detail', 'children'),
    [Input('raceinfo-dropdown-raceid', 'value'),
     Input('raceinfo-date-picker-single', 'date')]
)
def raceinfo_render_race_detail(race_id, date):
    print(f"---------raceinfo_render_race_detail callback: {race_id} {date}")
    if type(race_id) == int:
        race_df = GetData.get_race_data(date, date)
        raceuma_df = GetData.get_raceuma_data(date, date)
        this_race_df = race_df[race_df["競走コード"] == race_id]
        this_raceuma_df = raceuma_df[raceuma_df["競走コード"] == race_id]
        return p5.race_info_render(this_race_df, this_raceuma_df)

# レースＩＤと馬番を指定して馬の詳細情報を表示させる
@app.callback(
    Output('raceinfo-raceuma-detail', 'children'),
    [Input('raceinfo-dropdown-raceid', 'value'),
     Input('raceinfo-dropdown-raceuma', 'value'),
     Input('raceinfo-date-picker-single', 'date')]
)
def raceinfo_render_raceuma_detail(race_id, umaban, date):
    print(f"---------raceinfo_render_raceuma_detail callback: {race_id} {umaban} {date}")
    if type(umaban) == int:
        raceuma_df = GetData.get_raceuma_data(date, date)
        this_raceuma_df = raceuma_df[raceuma_df["競走コード"] == race_id]
        shap_sr = cd.get_shap_sr(race_id, this_raceuma_df, umaban)
        return p5.raceuma_info_render(shap_sr)


## -------------------- race_result用コールバック -------------------------------##
# 日付を指定、指定したレース名をリストに表示させる
@app.callback(
    Output('raceresult-dropdown-raceid', 'options'),
    [Input('raceresult-date-picker-single', 'date')]
)
def raceresult_set_race_list_option(date):
    print(f"---------raceresult_set_race_list_option callback: {date}")
    race_df = GetData.get_race_data(date, date)
    ba_list_df = race_df[race_df["月日"] == date][["場名", "競走番号", "競走コード", "競走名略称"]]
    ba_list_df.loc[:, "競走名"] = ba_list_df["場名"] + "_" + ba_list_df["競走番号"].astype(str) + "R_" + ba_list_df["競走名略称"]
    ba_list_df = ba_list_df[["競走名", "競走コード"]].rename(columns={"競走名": "label", "競走コード": "value"})
    ba_list = ba_list_df.drop_duplicates().to_dict(orient='record')
    return ba_list

# を指定、指定した場所のレースIDをリストを表示させる
@app.callback(
    Output('raceresult-dropdown-raceid', 'value'),
    [Input('raceresult-dropdown-raceid', 'options')]
)
def raceresult_set_race_list_value(raceresult_set_race_list_option):
    print("---------raceresult_set_race_list_value callback)")
    return raceresult_set_race_list_option

# レースIDを指定、指定したIDの情報を詳細ページに表示させる
@app.callback(
    Output('raceresult-race-detail', 'children'),
    [Input('raceresult-dropdown-raceid', 'value'),
     Input('raceresult-date-picker-single', 'date')]
)
def raceresult_render_race_detail(race_id, date):
    print(f"---------raceinfo_render_race_detail callback: {race_id} {date}")
    if type(race_id) == int:
        race_df = GetData.get_race_data(date, date)
        raceuma_df = GetData.get_raceuma_data(date, date)
        haraimodoshi_dict = GetData.get_haraimodoshi_dict(date, date)
        bet_df = GetData.get_bet_data(date, date)
        this_tansho_df = haraimodoshi_dict["tansho_df"].query(f"競走コード == {race_id}")
        this_fukusho_df = haraimodoshi_dict["fukusho_df"].query(f"競走コード == {race_id}")
        this_umaren_df = haraimodoshi_dict["umaren_df"].query(f"競走コード == {race_id}")
        this_umatan_df = haraimodoshi_dict["umatan_df"].query(f"競走コード == {race_id}")
        this_wide_df = haraimodoshi_dict["wide_df"].query(f"競走コード == {race_id}")
        this_sanrenpuku_df = haraimodoshi_dict["sanrenpuku_df"].query(f"競走コード == {race_id}")
        this_race_df = race_df[race_df["競走コード"] == race_id]
        this_raceuma_df = raceuma_df[raceuma_df["競走コード"] == race_id]
        this_bet_df = bet_df.query(f"競走コード == {race_id}")
        this_haraimodoshi_dict = {"tansho_df": this_tansho_df, "fukusho_df": this_fukusho_df, "umaren_df": this_umaren_df,
                                  "umatan_df": this_umatan_df, "wide_df": this_wide_df, "sanrenpuku_df": this_sanrenpuku_df}
        return p8.race_result_render(this_race_df, this_raceuma_df, this_bet_df, this_haraimodoshi_dict)


## ルーティング用コールバック
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return p1.toppage()
    elif pathname == "/page-2":
        return p2.return_analytics()
    elif pathname == "/page-3":
        return p3.kpi_analytics()
    elif pathname == "/page-4":
        return p4.race_trend()
    elif pathname == "/page-5":
        return p5.race_info()
    elif pathname == "/page-8":
        return p8.race_result()
    elif pathname == "/page-6":
        return p6.graph_example()
    elif pathname == "/page-7":
        return p7.graph_example2()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == "__main__":
    print('on hello')
    app.run_server(host="127.0.0.1", port=8000)