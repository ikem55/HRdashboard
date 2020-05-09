import dash_bootstrap_components as dbc
import components.webparts as wp
import components.graph as gp

import components.calc_data as cd
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
from datetime import datetime as dt
import datetime

def return_analytics():
    return dbc.Container([
            dbc.Row([
                dcc.DatePickerRange(
                    id='return-analytics-date-picker-range',
                    min_date_allowed=dt(2019, 12, 1),
                    initial_visible_month=dt.today(),
                    start_date=datetime.date(2020, 4, 30),
                    end_date=datetime.date(dt.now().year, dt.now().month, dt.now().day)
                ),
                wp.dbc_top_title("return analytics")
            ], className="h-30"),
            dcc.Loading(id="return-analytics-loading",
                        children=[html.Div(id="return_analytics")])
        ],
        style={"height": "90vh"},
        fluid=True
    )

def return_analytics_render(raceuma_df, bet_df, haraimodoshi_dict):
    daily_summary_bet_df = cd.get_daily_summary_bet_df(bet_df)

    # 単勝
    fig1 = wp.cp_add_steps_threshold_anda_delta_tansho(daily_summary_bet_df)
    fig1.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝
    fig2 = wp.cp_add_steps_threshold_anda_delta_fukusho(daily_summary_bet_df)
    fig2.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連
    fig3 = wp.cp_add_steps_threshold_anda_delta_umaren(daily_summary_bet_df)
    fig3.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単
    fig4 = wp.cp_add_steps_threshold_anda_delta_umatan(daily_summary_bet_df)
    fig4.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド
    fig5 = wp.cp_add_steps_threshold_anda_delta_wide(daily_summary_bet_df)
    fig5.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 三連複
    fig6 = wp.cp_add_steps_threshold_anda_delta_sanrenpuku(daily_summary_bet_df)
    fig6.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 月別券種別回収率推移
    fig7 = wp.cp_label_lines_with_annotations_bet_return_balance(bet_df)
    fig7.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 券種別配当分布
    fig8 = wp.cp_visualizing_the_distribution_haraimodoshi_dist(haraimodoshi_dict)
    fig8.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別回収的中率
    fig9 = wp.cp_bar_chart_with_line_plot_place_bet_return(bet_df)
    fig9.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 単勝配当分布
    fig10 = wp.cp_pie_chart_tansho_dist(haraimodoshi_dict)
    fig10.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝配当分布
    fig11 = wp.cp_pie_chart_fukusho_dist(haraimodoshi_dict)
    fig11.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連配当分布
    fig12 = wp.cp_pie_chart_umaren_dist(haraimodoshi_dict)
    fig12.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単配当分布
    fig13 = wp.cp_pie_chart_umatan_dist(haraimodoshi_dict)
    fig13.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド配当分布
    fig14 = wp.cp_pie_chart_wide_dist(haraimodoshi_dict)
    fig14.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # 三連複配当分布
    fig15 = wp.cp_pie_chart_sanrenpuku_dist(haraimodoshi_dict)
    fig15.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # 券種別配当分布比較
    fig16 = wp.cp_choosing_the_algorithm_haraimodoshi_dist(haraimodoshi_dict)
    fig16.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 券種別配当中央値比較
    fig17 = wp.cp_styled_categorical_dot_plot_haraimodoshi_median(haraimodoshi_dict)
    fig17.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    return dcc.Loading(id="return-analytics-render-loading", children=[dbc.Row([
                wp.dbc_title("単勝", 2),
                wp.dbc_title("複勝", 2),
                wp.dbc_title("馬連", 2),
                wp.dbc_title("馬単", 2),
                wp.dbc_title("ワイド", 2),
                wp.dbc_title("三連複", 2),
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
                wp.dbc_title("単勝配当分布", 2),
                wp.dbc_title("複勝配当分布", 2),
                wp.dbc_title("馬連配当分布", 2),
                wp.dbc_title("馬単配当分布", 2),
                wp.dbc_title("ワイド配当分布", 2),
                wp.dbc_title("三連複配当分布", 2),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig10", 2, fig10),
                wp.dbc_graph("fig11", 2, fig11),
                wp.dbc_graph("fig12", 2, fig12),
                wp.dbc_graph("fig13", 2, fig13),
                wp.dbc_graph("fig14", 2, fig14),
                wp.dbc_graph("fig15", 2, fig15),
            ], className="h-20"),
            dbc.Row([
                wp.dbc_title("月別券種別回収率推移", 4),
                wp.dbc_title("券種別配当分布", 4),
                wp.dbc_title("場所別回収的中率", 4),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig7", 4, fig7),
                wp.dbc_graph("fig8", 4, fig8),
                wp.dbc_graph("fig9", 4, fig9),
            ], className="h-50",),
            dbc.Row([
                wp.dbc_title("券種別配当分布比較", 7),
                wp.dbc_title("券種別配当中央値比較", 5),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig16", 7, fig16),
                wp.dbc_graph("fig17", 5, fig17),
            ], className="h-50", ),])
