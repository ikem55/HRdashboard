import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import components.webparts as wp
import components.graph as gp
from components.get_data import GetData
import components.calc_data as cd
import pandas as pd


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
    fig1.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 単勝回収率
    fig2_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig2_value = fig2_df["単勝配当"].mean()
    fig2_reference = 0
    fig2 = gp.add_steps_threshold_anda_delta(fig2_value, fig2_reference)
    fig2.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝回収率
    fig3_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig3_value = fig3_df["複勝配当"].mean()
    fig3_reference = 0
    fig3 = gp.add_steps_threshold_anda_delta(fig3_value, fig3_reference)
    fig3.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # １番人気
    fig4 = wp.cp_pie_chart_ninki_1(raceuma_df)
    fig4.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 単勝回収率
    fig5_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig5_value = fig5_df["単勝配当"].mean()
    fig5_reference = 0
    fig5 = gp.add_steps_threshold_anda_delta(fig5_value, fig5_reference)
    fig5.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝回収率
    fig6_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig6_value = fig6_df["複勝配当"].mean()
    fig6_reference = 0
    fig6 = gp.add_steps_threshold_anda_delta(fig6_value, fig6_reference)
    fig6.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別単複回収率・的中率
    fig7 = wp.cp_multiple_line_and_bar_chart_place_tanpuku_return(race_df, raceuma_df)
    fig7.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    if len(bet_df.index) != 0:
        # 場所別馬券回収率・的中率
        fig8 = wp.cp_multiple_line_and_bar_chart_place_bet_return(bet_df)
        fig8.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

        # 券種別結果
        summary_bet_df = cd.get_summary_bet_df(bet_df)
        fig9 = wp.cp_simple_waterfall_chart_balance_change(summary_bet_df)
        fig9.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})
    else:
        fig8 = ""
        fig9 = ""

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

    # 馬連的中1
    fig20 = wp.cp_basic_funnel_plot_umaren_1(race_df, raceuma_df, haraimodoshi_dict)
    fig20.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連的中2
    fig21 = wp.cp_basic_funnel_plot_umaren_2(race_df, raceuma_df, haraimodoshi_dict)
    fig21.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中1
    fig22 = wp.cp_basic_funnel_plot_umatan_1(race_df, raceuma_df, haraimodoshi_dict)
    fig22.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中2
    fig23 = wp.cp_basic_funnel_plot_umatan_2(race_df, raceuma_df, haraimodoshi_dict)
    fig23.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中3
    fig24 = wp.cp_basic_funnel_plot_umatan_3(race_df, raceuma_df, haraimodoshi_dict)
    fig24.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド的中1
    fig25 = wp.cp_basic_funnel_plot_wide_1(race_df, raceuma_df, haraimodoshi_dict)
    fig25.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})


    return dcc.Loading(id="racetrend-loading", children=[
        dbc.Container([
            dbc.Row([
                wp.dbc_top_title("todays race trend")
            ], className="h-30"),
            dbc.Row([
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
                wp.dbc_title("場所別単複回収率・的中率", 4),
                wp.dbc_title("場所別馬券回収率・的中率", 4),
                wp.dbc_title("券種別結果", 4),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig7", 4, fig7),
                wp.dbc_graph("fig8", 4, fig8),
                wp.dbc_graph("fig9", 4, fig9),
            ], className="h-30"),
            dbc.Row([
                wp.dbc_title("馬連的中1", 2),
                wp.dbc_title("馬連的中2", 2),
                wp.dbc_title("馬単的中1", 2),
                wp.dbc_title("馬単的中2", 2),
                wp.dbc_title("馬単的中3", 2),
                wp.dbc_title("ワイド的中1", 2),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig20", 2, fig20),
                wp.dbc_graph("fig21", 2, fig21),
                wp.dbc_graph("fig22", 2, fig22),
                wp.dbc_graph("fig23", 2, fig23),
                wp.dbc_graph("fig24", 2, fig24),
                wp.dbc_graph("fig25", 2, fig25),
            ], className="h-30"),
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
        ],
        style={"height": "90vh"},
        fluid=True
    )])