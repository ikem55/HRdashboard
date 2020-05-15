# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import components.webparts as wp
import components.graph as gp

from datetime import datetime as dt
import pandas as pd
import datetime

def kpi_analytics():
    return dbc.Container([
            dbc.Row([
                dcc.DatePickerRange(
                    id='kpi-analytics-date-picker-range',
                    min_date_allowed=dt(2019, 12, 1),
                    initial_visible_month=dt.today(),
                    start_date=datetime.date(2020, 4, 30),
                    end_date=datetime.date(dt.now().year, dt.now().month, dt.now().day)
                ),
                wp.dbc_top_title("kpi analytics")
            ], className="h-30"),
        dcc.Loading(id="kpi-analytics-loading",
                    children=[html.Div(id="kpi_analytics")])
        ],
        style={"height": "90vh"},
        fluid=True
    )

def kpi_analytics_render(race_df, raceuma_df, bet_df, haraimodoshi_dict, end_date):
    raceuma_df.loc[:, "競走馬コード"] = raceuma_df.apply(lambda x : str(x["競走コード"]) + str(x["馬番"]).zfill(2), axis=1)

    # 得点１位着順
    fig1 = wp.cp_pie_chart_score_1(raceuma_df)

    # 単勝回収率
    fig2_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig2_df_diff = fig2_df[fig2_df["年月日"] != end_date]
    fig2 = wp.cp_add_steps_threshold_anda_delta_tansho_return(fig2_df, fig2_df_diff)

    # 複勝回収率
    fig3_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig3_df_diff = fig3_df[fig3_df["年月日"] != end_date]
    fig3 = wp.cp_add_steps_threshold_anda_delta_fukusho_return(fig3_df, fig3_df_diff)

    # １番人気
    fig4 = wp.cp_pie_chart_ninki_1(raceuma_df)

    # 単勝回収率
    fig5_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig5_df_diff = fig5_df[fig5_df["年月日"] != end_date]
    fig5 = wp.cp_add_steps_threshold_anda_delta_tansho_return(fig5_df, fig5_df_diff)

    # 複勝回収率
    fig6_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig6_df_diff = fig6_df[fig6_df["年月日"] != end_date]
    fig6 = wp.cp_add_steps_threshold_anda_delta_fukusho_return(fig6_df, fig6_df_diff)

    # 場所別単複回収率・的中率
    fig7 = wp.cp_multiple_line_and_bar_chart_place_tanpuku_return(race_df, raceuma_df)
    # 場所別馬券回収率・的中率
    fig8 = wp.cp_multiple_line_and_bar_chart_place_bet_return(bet_df)
    # 馬連的中1
    fig10 = wp.cp_stacked_funnel_plot_umaren_1(race_df, raceuma_df, haraimodoshi_dict)
    # 馬連的中2
    fig11 = wp.cp_stacked_funnel_plot_umaren_2(race_df, raceuma_df, haraimodoshi_dict)
    # 馬単的中1
    fig12 = wp.cp_stacked_funnel_plot_umatan_1(race_df, raceuma_df, haraimodoshi_dict)
    # 馬単的中2
    fig13 = wp.cp_stacked_funnel_plot_umatan_2(race_df, raceuma_df, haraimodoshi_dict)
    # 馬単的中3
    fig14 = wp.cp_stacked_funnel_plot_umatan_3(race_df, raceuma_df, haraimodoshi_dict)
    # ワイド的中1
    fig15 = wp.cp_stacked_funnel_plot_wide_1(race_df, raceuma_df, haraimodoshi_dict)

    # 馬連的中1
    fig20 = wp.cp_parallel_categories_diagram_umaren_1(race_df, raceuma_df, haraimodoshi_dict)
    # 馬連的中2
    fig21 = wp.cp_parallel_categories_diagram_umaren_2(race_df, raceuma_df, haraimodoshi_dict)
    # 馬単的中1
    fig22 = wp.cp_parallel_categories_diagram_umatan_1(race_df, raceuma_df, haraimodoshi_dict)
    # 馬単的中2
    fig23 = wp.cp_parallel_categories_diagram_umatan_2(race_df, raceuma_df, haraimodoshi_dict)
    # 馬単的中3
    fig24 = wp.cp_parallel_categories_diagram_umatan_3(race_df, raceuma_df, haraimodoshi_dict)
    # ワイド的中1
    fig25 = wp.cp_parallel_categories_diagram_wide_1(race_df, raceuma_df, haraimodoshi_dict)

    return dcc.Loading(id="kpi-analytics-lender-loading", children=[
            dbc.Row([
                wp.dbc_graph("fig1", 2, fig1, "得点１位着順", 130),
                wp.dbc_graph("fig2", 2, fig2, "単勝回収率", 130),
                wp.dbc_graph("fig3", 2, fig3, "複勝回収率", 130),
                wp.dbc_graph("fig4", 2, fig4, "１番人気", 130),
                wp.dbc_graph("fig5", 2, fig5, "単勝回収率", 130),
                wp.dbc_graph("fig6", 2, fig6, "複勝回収率", 130),
            ], className="h-20", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig7", 6, fig7, "場所別単複回収率・的中率", 400),
                wp.dbc_graph("fig8", 6, fig8, "場所別馬券回収率・的中率", 400),
            ], className="h-50", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig10", 5, fig10, "馬連的中1", 400),
                wp.dbc_graph("fig20", 7, fig20, "", 400),
            ], className="h-50", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig11", 5, fig11, "馬連的中2", 400),
                wp.dbc_graph("fig21", 7, fig21, "", 400),
            ], className="h-50", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig12", 5, fig12, "馬単的中1", 400),
                wp.dbc_graph("fig22", 7, fig22, "", 400),
            ], className="h-50", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig13", 5, fig13, "馬単的中2", 400),
                wp.dbc_graph("fig23", 7, fig23, "", 400),
            ], className="h-50", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig14", 5, fig14, "馬単的中3", 400),
                wp.dbc_graph("fig24", 7, fig24, "", 400),
            ], className="h-50", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig15", 5, fig15, "ワイド的中1", 400),
                wp.dbc_graph("fig25", 7, fig25, "", 400),
            ], className="h-50", no_gutters=True),
    ])
