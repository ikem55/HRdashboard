import dash_bootstrap_components as dbc
import components.webparts as wp
import dash_core_components as dcc
import dash_html_components as html
import components.graph as gp
from datetime import datetime as dt
from components.get_data import GetData
import pandas as pd
import numpy as np
import datetime

def race_info():
    return dbc.Container([
        dbc.Row([
            dcc.DatePickerSingle(
                id='raceinfo-date-picker-single',
                min_date_allowed=dt(2019, 12, 1),
                initial_visible_month=dt.today(),
                date=datetime.date(dt.now().year, dt.now().month, dt.now().day)
            ),
            dcc.Dropdown(
                id="raceinfo-dropdown-keibajo",
                options=[],
                value=""
            ),
            dcc.Dropdown(
                id="raceinfo-dropdown-raceid",
                options=[],
                value=""
            ),
            wp.dbc_top_title("race info")
        ], className="h-30"),
        dcc.Loading(id="race-info-loading",
                    children=[html.Div(id="raceinfo-race-detail")])
    ],
        style={"height": "90vh"},
        fluid=True
    )

def raceuma_info_render(shap_df_win, shap_df_jiku, shap_df_are):
    # 勝ち根拠
    fig1 = wp.cp_controlling_text_fontsize_with_uniformtext_win_basis(shap_df_win)
    # 軸根拠
    fig2 = wp.cp_controlling_text_fontsize_with_uniformtext_jiku_basis(shap_df_jiku)
    # 荒れ根拠
    fig3 = wp.cp_controlling_text_fontsize_with_uniformtext_are_basis(shap_df_are)

    return [dbc.Row([
            wp.dbc_graph("fig1", 4, fig1, "勝ち根拠", 300, bottom=100),
            wp.dbc_graph("fig2", 4, fig2, "軸根拠", 300, bottom=100),
            wp.dbc_graph("fig3", 4, fig3, "荒れ根拠", 300, bottom=100),
        ], className="h-50"),
        ]

def race_info_render(race_df, raceuma_df, shap_df_umaren_are, shap_df_umatan_are, shap_df_sanrenpuku_are):
    race_sr = race_df.iloc[0]
    term_start_date = "2019-12-01"
    term_end_date = race_sr["月日"].strftime("%Y-%m-%d")
    ketto_toroku_bango_list = raceuma_df["血統登録番号"].tolist()
    raceuma_prev_df = GetData.get_raceuma_prev_df(term_start_date, term_end_date, ketto_toroku_bango_list)
    raceuma_prev_df = pd.merge(raceuma_df[["血統登録番号", "馬名"]], raceuma_prev_df, on="血統登録番号")
    raceuma_df = raceuma_df.sort_values("馬番", ascending=False)
    raceuma_prev_df = raceuma_prev_df.sort_values("馬名", ascending=False)

    # 得点
    fig1 = wp.cp_basic_horizontal_bar_chart_score(raceuma_df)
    # 最大得点分布
    #fig2 = wp.cp_basic_dot_plot_max_score(raceuma_df)
    # 得点バブル
    #fig3 = wp.cp_buble_chart_score(raceuma_df.sort_values("馬番"))
    # レーダーチャート
    fig4 = wp.cp_multiple_trace_rader_chart_score(raceuma_df.sort_values("馬番"))
    # 先行率
    fig5 = wp.cp_basic_horizontal_box_plot_senko_rate(raceuma_prev_df)
    # タイム指数
    fig6 = wp.cp_basic_horizontal_box_plot_time_score(raceuma_prev_df)

    # テーブルデータ
    fig7_df = raceuma_df[["枠番", "馬番", "馬名", "性別コード", "馬齢", "負担重量", "予想タイム指数順位", "予想タイム指数", "デフォルト得点", "得点", "馬券評価順位", "先行指数", "予想展開", "騎手名", "調教師名",
                          "所属", "得点V3", "WIN_RATE", "JIKU_RATE", "ANA_RATE", "WIN_RANK", "JIKU_RANK", "ANA_RANK", "SCORE", "SCORE_RANK", "CK1_RATE", "CK2_RATE", "CK3_RATE", "CK1_RANK", "CK2_RANK", "CK3_RANK"]].sort_values("馬番")

    # 馬連荒れ根拠
    #fig8 = wp.cp_controlling_text_fontsize_with_uniformtext_umaren_basis(shap_df_umaren_are)
    # 馬単荒れ根拠
    #fig9 = wp.cp_controlling_text_fontsize_with_uniformtext_umatan_basis(shap_df_umatan_are)
    # 三連複荒れ根拠
    #fig10 = wp.cp_controlling_text_fontsize_with_uniformtext_sanrenpuku_basis(shap_df_sanrenpuku_are)

    raceuma_dropdown_option = raceuma_df[["馬名", "馬番"]].rename(
        columns={"馬名": "label", "馬番": "value"}).to_dict(orient='record')
    return dcc.Loading(id="race-info-render-loading", children=[dbc.Row([
                wp.dbc_race_info(race_sr, 12),
            ], className="h-8"),
#            dbc.Row([
#                wp.dbc_graph("fig8", 4, fig8, "馬連荒れ根拠", 300, bottom=100),
#                wp.dbc_graph("fig9", 4, fig9, "馬単荒れ根拠", 300, bottom=100),
#                wp.dbc_graph("fig10", 4, fig10, "三連複荒れ根拠", 300, bottom=100),
#            ], className="h-30", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig1", 6, fig1, "得点", 500),
                wp.dbc_graph("fig4", 6, fig4, "レーダーチャート", 500),
            ], className="h-50", no_gutters=True),
#            dbc.Row([
#                wp.dbc_graph("fig2", 6, fig2, "最大得点分布", 500),
#                wp.dbc_graph("fig3", 6, fig3, "得点バブル", 500),
#            ], className="h-50", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig5", 6, fig5, "先行率", 500),
                wp.dbc_graph("fig6", 6, fig6, "タイム指数", 500),
            ], className="h-50", no_gutters=True),
            wp.dbc_race_info_table("fig7", 16, fig7_df),
            dbc.Row([
                wp.dbc_title("得点根拠", 6),
                dcc.Dropdown(
                    id="raceinfo-dropdown-raceuma",
                    options=raceuma_dropdown_option,
                    style={"width": "300px"}
                ),
            ], className="h-8"),
            dcc.Loading(id="raceuma-info-loading",
                        children=[html.Div(id="raceinfo-raceuma-detail")])
        ])

