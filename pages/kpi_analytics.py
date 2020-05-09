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
    fig1.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 単勝回収率
    fig2_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig2_df_diff = fig2_df[fig2_df["年月日"] != end_date]
    fig2 = wp.cp_add_steps_threshold_anda_delta_tansho_return(fig2_df, fig2_df_diff)
    fig2.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝回収率
    fig3_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig3_df_diff = fig3_df[fig3_df["年月日"] != end_date]
    fig3 = wp.cp_add_steps_threshold_anda_delta_fukusho_return(fig3_df, fig3_df_diff)
    fig3.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # １番人気
    fig4 = wp.cp_pie_chart_ninki_1(raceuma_df)
    fig4.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 単勝回収率
    fig5_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig5_df_diff = fig5_df[fig5_df["年月日"] != end_date]
    fig5 = wp.cp_add_steps_threshold_anda_delta_tansho_return(fig5_df, fig5_df_diff)
    fig5.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝回収率
    fig6_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig6_df_diff = fig6_df[fig6_df["年月日"] != end_date]
    fig6 = wp.cp_add_steps_threshold_anda_delta_fukusho_return(fig6_df, fig6_df_diff)
    fig6.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別単複回収率・的中率
    fig7 = wp.cp_multiple_line_and_bar_chart_place_tanpuku_return(race_df, raceuma_df)
    fig7.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別馬券回収率・的中率
    fig8 = wp.cp_multiple_line_and_bar_chart_place_bet_return(bet_df)
    fig8.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連的中1
    fig10 = wp.cp_basic_funnel_plot_umaren_1(race_df, raceuma_df, haraimodoshi_dict)
    fig10.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連的中2
    fig11 = wp.cp_basic_funnel_plot_umaren_2(race_df, raceuma_df, haraimodoshi_dict)
    fig11.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中1
    fig12 = wp.cp_basic_funnel_plot_umatan_1(race_df, raceuma_df, haraimodoshi_dict)
    fig12.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中2
    fig13 = wp.cp_basic_funnel_plot_umatan_2(race_df, raceuma_df, haraimodoshi_dict)
    fig13.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中3
    fig14 = wp.cp_basic_funnel_plot_umatan_3(race_df, raceuma_df, haraimodoshi_dict)
    fig14.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド的中1
    fig15 = wp.cp_basic_funnel_plot_wide_1(race_df, raceuma_df, haraimodoshi_dict)
    fig15.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})


    return dcc.Loading(id="kpi-analytics-lender-loading", children=[dbc.Row([
                wp.dbc_title("得点１位着順", 2),
                wp.dbc_title("単勝回収率", 2),
                wp.dbc_title("複勝回収率", 2),
                wp.dbc_title("１番人気", 2),
                wp.dbc_title("単勝回収率", 2),
                wp.dbc_title("複勝回収率", 2),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig1", 2, fig1),
                wp.dbc_graph("fig2", 2, fig2),
                wp.dbc_graph("fig3", 2, fig3),
                wp.dbc_graph("fig4", 2, fig4),
                wp.dbc_graph("fig5", 2, fig5),
                wp.dbc_graph("fig6", 2, fig6),
            ], className="h-20"),
            dbc.Row([
                wp.dbc_title("場所別単複回収率・的中率", 6),
                wp.dbc_title("場所別馬券回収率・的中率", 6),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig7", 6, fig7),
                wp.dbc_graph("fig8", 6, fig8),
            ], className="h-50"),
            dbc.Row([
                wp.dbc_title("馬連的中1", 2),
                wp.dbc_title("馬連的中2", 2),
                wp.dbc_title("馬単的中1", 2),
                wp.dbc_title("馬単的中2", 2),
                wp.dbc_title("馬単的中3", 2),
                wp.dbc_title("ワイド的中1", 2),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig10", 2, fig10),
                wp.dbc_graph("fig11", 2, fig11),
                wp.dbc_graph("fig12", 2, fig12),
                wp.dbc_graph("fig13", 2, fig13),
                wp.dbc_graph("fig14", 2, fig14),
                wp.dbc_graph("fig15", 2, fig15),
            ], className="h-50"),])
