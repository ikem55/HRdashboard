import dash_bootstrap_components as dbc
import components.webparts as wp
import components.graph as gp
import components.calc_data as cd
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt
import pandas as pd
import datetime

def toppage():
    return dbc.Container([
            dbc.Row([
                dcc.DatePickerRange(
                    id='toppage-date-picker-range',
                    min_date_allowed=dt(2020, 4, 30),
                    initial_visible_month=dt.today(),
                    start_date=datetime.date(2020, 4, 30),
                    end_date=datetime.date(dt.now().year, dt.now().month, dt.now().day)
                ),
                wp.dbc_top_title("Dashboard top")
            ], className="h-30"),
            dcc.Loading(id="top-loading",
                        children=[html.Div(id="top_dashoboard")])
        ],
        style={"height": "90vh"},
        fluid=True
    )

def toppage_render(race_df, raceuma_df, bet_df, haraimodoshi_dict):
    print("toppage_render")

    daily_bet_df = cd.get_daily_bet_df(bet_df)
    daily_rank1_raceuma_df = cd.get_daily_rank1_raceuma_df(raceuma_df)
    summary_bet_df = cd.get_summary_bet_df(bet_df)
    place_bet_df = cd.get_place_bet_df(bet_df)

    prev_daily_bet_df = daily_bet_df.drop(daily_bet_df.tail(1).index)
    prev_daily_rank1_raceuma_df = daily_rank1_raceuma_df.drop(daily_bet_df.tail(1).index)
    place_bet_df = place_bet_df[place_bet_df["金額"] != 0].copy()
    raceuma_df.loc[:, "競走馬コード"] = raceuma_df.apply(lambda x : str(x["競走コード"]) + str(x["馬番"]).zfill(2), axis=1)

    # 回収
    fig1 = wp.cp_data_cards_return(daily_bet_df, prev_daily_bet_df)
    fig1.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 回収率
    fig2 = wp.cp_showing_information_above_return_rate(daily_bet_df, prev_daily_bet_df)
    fig2.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 単勝回収率
    fig3 = wp.cp_add_steps_threshold_anda_delta_tansho_return(daily_rank1_raceuma_df, prev_daily_rank1_raceuma_df)
    fig3.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝回収率
    fig4 = wp.cp_add_steps_threshold_anda_delta_fukusho_return(daily_rank1_raceuma_df, prev_daily_rank1_raceuma_df)
    fig4.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 残高推移1
    fig5 = wp.cp_time_series_with_range_selector_buttions_balance_change(daily_bet_df)
    fig5.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    # 残高推移2
    fig6 = wp.cp_simple_waterfall_chart_balance_change(summary_bet_df)
    fig6.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別回収率的中率払戻
    fig7 = wp.cp_buble_chart_place_return_hit(place_bet_df)
    fig7.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 券種毎回収率
    fig8 = wp.cp_multi_bullet(summary_bet_df)
    fig8.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 得点１位着順
    fig9 = wp.cp_pie_chart_score_1(raceuma_df)
    fig9.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別単複回収率・的中率
    fig10 = wp.cp_multiple_line_and_bar_chart_place_tanpuku_return(race_df, raceuma_df)
    fig10.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別馬券回収率・的中率
    fig11 = wp.cp_multiple_line_and_bar_chart_place_bet_return(bet_df)
    fig11.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連的中1
    fig12 = wp.cp_basic_funnel_plot_umaren_1(race_df, raceuma_df, haraimodoshi_dict)
    fig12.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連的中2
    fig13 = wp.cp_basic_funnel_plot_umaren_2(race_df, raceuma_df, haraimodoshi_dict)
    fig13.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中1
    fig14 = wp.cp_basic_funnel_plot_umatan_1(race_df, raceuma_df, haraimodoshi_dict)
    fig14.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中2
    fig15 = wp.cp_basic_funnel_plot_umatan_2(race_df, raceuma_df, haraimodoshi_dict)
    fig15.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中3
    fig16 = wp.cp_basic_funnel_plot_umatan_3(race_df, raceuma_df, haraimodoshi_dict)
    fig16.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド的中1
    fig17 = wp.cp_basic_funnel_plot_wide_1(race_df, raceuma_df, haraimodoshi_dict)
    fig17.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連配当分布
    fig18 = wp.cp_choosing_the_algorithm_umaren_dist(race_df, haraimodoshi_dict)
    fig18.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単配当分布
    fig19 = wp.cp_choosing_the_algorithm_umatan_dist(race_df, haraimodoshi_dict)
    fig19.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド配当分布
    fig20 = wp.cp_choosing_the_algorithm_wide_dist(race_df, haraimodoshi_dict)
    fig20.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    # 三連複配当分布
    fig21 = wp.cp_choosing_the_algorithm_sanrenpuku_dist(race_df, haraimodoshi_dict)
    fig21.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    print("start rendering")
    return dcc.Loading(id="top-detail-loading", children=[
        dbc.Row([
                wp.dbc_title("回収", 2),
                wp.dbc_title("回収率", 4),
                wp.dbc_title("得点１位着順", 2),
                wp.dbc_title("単勝回収率", 2),
                wp.dbc_title("複勝回収率", 2),
            ], className="h-8"),
        dbc.Row([
            wp.dbc_graph("fig1", 2, fig1),
            wp.dbc_graph("fig2", 4, fig2),
            wp.dbc_graph("fig9", 2, fig9),
            wp.dbc_graph("fig3", 2, fig3),
            wp.dbc_graph("fig4", 2, fig4),
        ], className="h-20"),
        dbc.Row([
            wp.dbc_title("券種毎回収率", 3),
            wp.dbc_title("残高推移", 4),
            wp.dbc_title("場所別回収率的中率払戻", 5),
        ], className="h-8"),
        dbc.Row([
            wp.dbc_graph("fig8", 3, fig8),
            dbc.Col([
                dbc.Row(
                    wp.dbc_graph("fig5", 12, fig5),
                ),
                dbc.Row(
                    wp.dbc_graph("fig6", 12, fig6),
                )], width=4),
            wp.dbc_graph("fig7", 5, fig7),
        ], className="h-50",),
        dbc.Row([
            wp.dbc_title("場所別単複回収率・的中率", 6),
            wp.dbc_title("場所別馬券回収率・的中率", 6),
        ], className="h-8"),
        dbc.Row([
            wp.dbc_graph("fig10", 6, fig10),
            wp.dbc_graph("fig11", 6, fig11),
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
            wp.dbc_graph("fig12", 2, fig12),
            wp.dbc_graph("fig13", 2, fig13),
            wp.dbc_graph("fig14", 2, fig14),
            wp.dbc_graph("fig15", 2, fig15),
            wp.dbc_graph("fig16", 2, fig16),
            wp.dbc_graph("fig17", 2, fig17),
        ], className="h-50"),
        dbc.Row([
            wp.dbc_title("馬連配当分布", 6),
            wp.dbc_title("馬単配当分布", 6),
        ], className="h-8"),
        dbc.Row([
            wp.dbc_graph("fig18", 6, fig18),
            wp.dbc_graph("fig19", 6, fig19),
        ], className="h-50"),
        dbc.Row([
            wp.dbc_title("ワイド配当分布", 6),
            wp.dbc_title("三連複配当分布", 6),
        ], className="h-8"),
        dbc.Row([
            wp.dbc_graph("fig20", 6, fig20),
            wp.dbc_graph("fig21", 6, fig21),
        ], className="h-50"),
        ])
