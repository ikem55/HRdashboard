import dash_bootstrap_components as dbc
import components.webparts as wp
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt
import datetime

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
    raceuma_df.loc[:, "馬名表用"] = raceuma_df["馬名"]
    raceuma_df.loc[:, "馬名"] = raceuma_df.apply(lambda x: x["馬名"] + "<br>(" + str(x["単勝人気"]) + "番人気 " + str(x["確定着順"]) + "着 " + str(x["馬券評価順位"]) + "位)", axis=1)
    haraimodoshi_df = pd.DataFrame()
    for key, val in haraimodoshi_dict.items():
        if len(val.index) != 0:
            val.loc[:, "式別"] = key
            haraimodoshi_df = haraimodoshi_df.append(val)

    # 得点
    fig1 = wp.cp_basic_horizontal_bar_chart_score(raceuma_df)
    # 得点バブル
    #fig3_df = raceuma_df[["確定着順", "デフォルト得点", "SCORE", "得点V3", "馬名"]].sort_values("確定着順")
    #fig3 = wp.cp_buble_chart_score(fig3_df)

    # テーブル
    fig4_df = raceuma_df[["枠番", "馬番", "馬名表用", "性別コード", "タイム", "タイム指数", "デフォルト得点", "得点", "馬券評価順位", "単勝オッズ",
                          "単勝人気", "複勝オッズ1", "複勝オッズ2", "展開コード", "騎手名", "馬齢", "調教師名", "負担重量", "馬体重", "確定着順",
                          "コーナー順位1", "コーナー順位2", "コーナー順位3", "コーナー順位4", "上がりタイム", "所属", "得点V3", "WIN_RATE",
                          "JIKU_RATE", "ANA_RATE", "WIN_RANK", "JIKU_RANK", "ANA_RANK", "SCORE", "SCORE_RANK", "CK1_RATE",
                          "CK2_RATE", "CK3_RATE", "CK1_RANK", "CK2_RANK", "CK3_RANK"]].sort_values("タイム指数", ascending=False)

    # 払戻・投票
    if len(haraimodoshi_df.index) != 0:
        fig5_haraimodoshi_df = haraimodoshi_df[["式別", "馬番", "払戻"]]
    else:
        fig5_haraimodoshi_df = haraimodoshi_df
    fig5_bet_df = bet_df[["式別名", "番号", "金額", "結果", "合計"]]

    # タイム指数、予想タイム指数
    fig6 = wp. cp_basic_dot_plot_time_record(raceuma_df)
    # タイム指数、単勝オッズ
    fig10 = wp.cp_bar_chart_with_line_plot_time_record_tansho(raceuma_df)
    # ラップ
    #fig11 = wp.cp_simple_line_rap(race_sr, 500)
    # 単勝支持率
    fig12 = wp.cp_pie_chart_tansho_approval_rate(raceuma_df)


    return dcc.Loading(id="race-result-render-loading", children=[dbc.Row([
                wp.dbc_race_info(race_sr, 8),
                wp.dbc_race_result(race_sr, haraimodoshi_df, 4),
            ], className="h-8", no_gutters=True),

            dbc.Row([
                wp.dbc_graph("fig12", 4, fig12, "単勝支持率", 400),
                wp.dbc_graph("fig10", 4, fig10, "タイム指数、単勝オッズ", 500),
                wp.dbc_haraimodoshi_table("fig5_1", 2, fig5_haraimodoshi_df),
                wp.dbc_bet_table("fig5_2", 2, fig5_bet_df),
            ], className="h-50", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig1", 6, fig1, "得点", 400),
                wp.dbc_graph("fig6", 6, fig6, "タイム指数、予想タイム指数", 500),
            ], className="h-50", no_gutters=True),
#            dbc.Row([
#                wp.dbc_graph("fig3", 6, fig3, "得点バブル", 500),
#                wp.dbc_graph("fig11", 4, fig11, "ラップ", 400),
#            ], className="h-50", no_gutters=True),
            wp.dbc_race_result_table("fig4", 16, fig4_df)
        ])

