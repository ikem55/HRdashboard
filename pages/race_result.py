import dash_bootstrap_components as dbc
import components.webparts as wp
import dash_core_components as dcc
import dash_html_components as html
import components.graph as gp
import pandas as pd
from datetime import datetime as dt
import datetime
import numpy as np

def race_result():
    return dbc.Container([
        dbc.Row([
            dcc.DatePickerSingle(
                id='raceresult-date-picker-single',
                min_date_allowed=dt(2019, 12, 1),
                initial_visible_month=dt.today(),
                date=datetime.date(dt.now().year, dt.now().month, dt.now().day)
            ),
            dcc.Dropdown(
                id="raceresult-dropdown-raceid",
                options=[],
                value="-----------------------------",
                style={"width": "300px"}
            ),
            wp.dbc_top_title("race result")
        ], className="h-30"),
        dcc.Loading(id="race-result-loading",
                    children=[html.Div(id="raceresult-race-detail")])
    ],
        style={"height": "90vh"},
        fluid=True
    )

def race_result_render(race_df, raceuma_df, bet_df, haraimodoshi_dict):
    race_sr = race_df.iloc[0]
    raceuma_df = raceuma_df.sort_values("タイム指数")
    raceuma_df.loc[:, "馬名"] = raceuma_df.apply(lambda x: x["馬名"] + "<br>(" + str(x["単勝人気"]) + "番人気 " + str(x["確定着順"]) + "着 " + str(x["馬券評価順位"]) + "位)", axis=1)
    haraimodoshi_df = pd.DataFrame()
    for key, val in haraimodoshi_dict.items():
        if len(val.index) != 0:
            val.loc[:, "式別"] = key
            haraimodoshi_df = haraimodoshi_df.append(val)

    # 得点
    fig1_df = raceuma_df[["馬名", "デフォルト得点", "得点V3", "WIN_RATE", "JIKU_RATE", "ANA_RATE"]].set_index("馬名")
    fig1_df.loc[:, "デフォルト得点"] = fig1_df["デフォルト得点"] / 3
    fig1_df.loc[:, "得点V3"] = fig1_df["得点V3"] / 3
    fig1_df.loc[:, "WIN_RATE"] = fig1_df["WIN_RATE"] * 0.55 / 3
    fig1_df.loc[:, "JIKU_RATE"] = fig1_df["JIKU_RATE"] * 0.20 / 3
    fig1_df.loc[:, "ANA_RATE"] = fig1_df["ANA_RATE"] * 0.25 / 3
    fig1_df = fig1_df.stack().reset_index()
    fig1_df.columns = ["name", "label", "value"]

    fig1 = gp.basic_horizontal_bar_chart(fig1_df)
    fig1.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 得点バブル
    fig3_df = raceuma_df[["確定着順", "デフォルト得点", "SCORE", "得点V3", "馬名"]].sort_values("確定着順")
    fig3_x_list = fig3_df["デフォルト得点"].tolist()
    fig3_y_list = fig3_df["SCORE"].tolist()
    fig3_z_list = fig3_df["得点V3"].tolist()
    fig3_name_list = fig3_df["馬名"].tolist()
    fig3_x_title = "デフォルト得点"
    fig3_y_title = "SCORE"
    fig3 = gp.buble_chart(fig3_x_list, fig3_y_list, fig3_z_list, fig3_name_list, fig3_x_title, fig3_y_title)
    fig3.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # テーブル
    fig4_df = raceuma_df[["馬番", "馬名", "性別コード", "予想タイム指数順位", "予想タイム指数", "デフォルト得点", "得点", "騎手名", "確定着順"]].sort_values("確定着順")

    # 払戻・投票
    if len(haraimodoshi_df.index) != 0:
        fig5_haraimodoshi_df = haraimodoshi_df[["式別", "馬番", "払戻"]]
    else:
        fig5_haraimodoshi_df = haraimodoshi_df
    fig5_bet_df = bet_df[["式別名", "番号", "金額", "結果", "合計"]]

    # タイム指数、予想タイム指数
    fig6_df = raceuma_df[["馬名", "タイム指数", "予想タイム指数"]]
    fig6_x = fig6_df["馬名"].to_list()
    fig6_y_value1 = fig6_df["タイム指数"].to_list()
    fig6_y_value2 = fig6_df["予想タイム指数"].to_list()
    fig6_y_title1 = "タイム指数"
    fig6_y_title2 = "予想タイム指数"
    fig6 = gp.basic_dot_plot(fig6_x, fig6_y_value1, fig6_y_value2, fig6_y_title1, fig6_y_title2)
    fig6.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # タイム指数、単勝オッズ
    fig10_df = raceuma_df[["馬名", "タイム指数", "単勝オッズ"]]
    fig10_x = fig10_df["馬名"].to_list()
    fig10_y_value1 = fig10_df["タイム指数"].to_list()
    fig10_y_value2 = fig10_df["単勝オッズ"].apply(lambda x: np.log(x)).to_list()
    fig10_y_title1 = "タイム指数"
    fig10_y_title2 = "単勝オッズ"
    fig10 = gp.bar_chart_with_line_plot(fig10_x, fig10_y_value1, fig10_y_value2, fig10_y_title1, fig10_y_title2)
    fig10.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # ラップ
    fig11_rap_text = race_sr["ラップタイム"]
    chunks, chunk_size = len(fig11_rap_text), 3
    rap_array = [fig11_rap_text[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
    rap_array = [i for i in rap_array if i != '000']
    if len(rap_array) != 0:
        fig11_df = pd.DataFrame({'value': rap_array, 'label': range(1, len(rap_array) + 1)})
        fig11 = gp.simple_line(fig11_df)
        fig11.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})
    else:
        print("rap empty")
        fig11 = ""

    # 単勝支持率
    fig12_labels = raceuma_df["馬名"].tolist()
    fig12_values = raceuma_df["単勝支持率"].tolist()
    fig12 = gp.pie_chart(fig12_labels, fig12_values)
    fig12.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})




    return dcc.Loading(id="race-result-render-loading", children=[dbc.Row([
                wp.dbc_race_info(race_sr),
                wp.dbc_race_result(race_sr),
            ], className="h-8"),

            dbc.Row([
                wp.dbc_title("単勝支持率", 3),
                wp.dbc_title("ラップ", 6),
                wp.dbc_title("払戻・投票", 3),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig12", 3, fig12),
                wp.dbc_graph("fig11", 6, fig11),
                dbc.Col([
                    dbc.Row(wp.dbc_table("fig5_1", 12, fig5_haraimodoshi_df)),
                    dbc.Row(wp.dbc_table("fig5_2", 12, fig5_bet_df)),
                ], width=3)
            ], className="h-50"),
            dbc.Row([
                wp.dbc_title("タイム指数、単勝オッズ", 6),
                wp.dbc_title("タイム指数、予想タイム指数", 6),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig10", 6, fig10),
                wp.dbc_graph("fig6", 6, fig6),
            ], className="h-50"),
            dbc.Row([
                wp.dbc_title("得点", 6),
                wp.dbc_title("得点バブル", 6),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig1", 6, fig1),
                wp.dbc_graph("fig3", 6, fig3),
            ], className="h-50"),
            wp.dbc_table("fig4", 16, fig4_df)
        ])

