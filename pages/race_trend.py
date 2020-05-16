import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import components.webparts as wp
import components.graph as gp
from components.get_data import GetData
import components.calc_data as cd


def race_trend():
    race_df = GetData.get_race_data_real().query("データ区分 == '7'")
    raceuma_df = GetData.get_raceuma_data_real().query("データ区分 == '7'")

    raceuma_df.loc[:, "競走馬コード"] = raceuma_df.apply(lambda x : str(x["競走コード"]) + str(x["馬番"]).zfill(2), axis=1)
    bet_df = GetData.get_bet_data_real()
    haraimodoshi_dict = GetData.get_haraimodoshi_dict_real()
    if len(race_df.index) == 0 or len(raceuma_df.index) == 0:
        return html.P("no data")

    # 得点１位着順
    fig1 = wp.cp_pie_chart_score_1(raceuma_df)

    # 単勝回収率
    fig2_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig2_value = fig2_df["単勝配当"].mean()
    fig2_reference = 0
    fig2 = gp.add_steps_threshold_anda_delta(fig2_value, fig2_reference)

    # 複勝回収率
    fig3_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig3_value = fig3_df["複勝配当"].mean()
    fig3_reference = 0
    fig3 = gp.add_steps_threshold_anda_delta(fig3_value, fig3_reference)

    # １番人気
    fig4 = wp.cp_pie_chart_ninki_1(raceuma_df)

    # 単勝回収率
    fig5_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig5_value = fig5_df["単勝配当"].mean()
    fig5_reference = 0
    fig5 = gp.add_steps_threshold_anda_delta(fig5_value, fig5_reference)

    # 複勝回収率
    fig6_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig6_value = fig6_df["複勝配当"].mean()
    fig6_reference = 0
    fig6 = gp.add_steps_threshold_anda_delta(fig6_value, fig6_reference)

    # 場所別単複回収率・的中率
    fig7 = wp.cp_multiple_line_and_bar_chart_place_tanpuku_return(race_df, raceuma_df)

    if len(bet_df.index) != 0:
        # 場所別馬券回収率・的中率
        fig8 = wp.cp_multiple_line_and_bar_chart_place_bet_return(bet_df)
        # 券種別結果
        summary_bet_df = cd.get_summary_bet_df(bet_df)
        fig9 = wp.cp_simple_waterfall_chart_balance_change(summary_bet_df)
    else:
        fig8 = ""
        fig9 = ""

    # 単勝配当分布
    #fig10 = wp.cp_pie_chart_tansho_dist(haraimodoshi_dict)
    # 複勝配当分布
    #fig11 = wp.cp_pie_chart_fukusho_dist(haraimodoshi_dict)
    # 馬連配当分布
    #fig12 = wp.cp_pie_chart_umaren_dist(haraimodoshi_dict)
    # 馬単配当分布
    #fig13 = wp.cp_pie_chart_umatan_dist(haraimodoshi_dict)
    # ワイド配当分布
    #fig14 = wp.cp_pie_chart_wide_dist(haraimodoshi_dict)
    # 三連複配当分布
    #fig15 = wp.cp_pie_chart_sanrenpuku_dist(haraimodoshi_dict)
    # 馬連的中1
    fig20 = wp.cp_stacked_funnel_plot_umaren_1(race_df, raceuma_df, haraimodoshi_dict)
    # 馬連的中2
    fig21 = wp.cp_stacked_funnel_plot_umaren_2(race_df, raceuma_df, haraimodoshi_dict)
    # 馬単的中1
    fig22 = wp.cp_stacked_funnel_plot_umatan_1(race_df, raceuma_df, haraimodoshi_dict)
    # 馬単的中2
    fig23 = wp.cp_stacked_funnel_plot_umatan_2(race_df, raceuma_df, haraimodoshi_dict)
    # 馬単的中3
    fig24 = wp.cp_stacked_funnel_plot_umatan_3(race_df, raceuma_df, haraimodoshi_dict)
    # ワイド的中1
    fig25 = wp.cp_stacked_funnel_plot_wide_1(race_df, raceuma_df, haraimodoshi_dict)

    return dcc.Loading(id="racetrend-loading", children=[
        dbc.Container([
            dbc.Row([
                wp.dbc_top_title("todays race trend")
            ], className="h-30"),
            dbc.Row([
                wp.dbc_graph("fig1", 2, fig1, "得点１位着順", 130),
                wp.dbc_graph("fig2", 2, fig2, "単勝回収率", 130),
                wp.dbc_graph("fig3", 2, fig3, "複勝回収率", 130),
                wp.dbc_graph("fig4", 2, fig4, "１番人気", 130),
                wp.dbc_graph("fig5", 2, fig5, "単勝回収率", 130),
                wp.dbc_graph("fig6", 2, fig6, "複勝回収率", 130),
            ], className="h-20", no_gutters=True),
#            dbc.Row([
#                wp.dbc_graph("fig10", 2, fig10, "単勝配当分布", 200),
#                wp.dbc_graph("fig11", 2, fig11, "複勝配当分布", 200),
#                wp.dbc_graph("fig12", 2, fig12, "馬連配当分布", 200),
#                wp.dbc_graph("fig13", 2, fig13, "馬単配当分布", 200),
#                wp.dbc_graph("fig14", 2, fig14, "ワイド配当分布", 200),
#                wp.dbc_graph("fig15", 2, fig15, "三連複配当分布", 200),
#            ], className="h-20", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig7", 4, fig7, "場所別単複回収率・的中率", 300),
                wp.dbc_graph("fig8", 4, fig8, "場所別馬券回収率・的中率", 300),
                wp.dbc_graph("fig9", 4, fig9, "券種別結果", 300),
            ], className="h-30", no_gutters=True),
            dbc.Row([
                wp.dbc_graph("fig20", 2, fig20, "馬連的中1", 400),
                wp.dbc_graph("fig21", 2, fig21, "馬連的中2", 400),
                wp.dbc_graph("fig22", 2, fig22, "馬単的中1", 400),
                wp.dbc_graph("fig23", 2, fig23, "馬単的中2", 400),
                wp.dbc_graph("fig24", 2, fig24, "馬単的中3", 400),
                wp.dbc_graph("fig25", 2, fig25, "ワイド的中1", 400),
            ], className="h-30", no_gutters=True),
        ],
        style={"height": "90vh"},
        fluid=True
    )])