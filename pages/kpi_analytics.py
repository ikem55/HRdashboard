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
    fig1_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig1_df.loc[:, "確定着順"] = fig1_df["確定着順"].apply(lambda x: str(x) + "着" if x in (1,2,3) else "着外")
    fig1_gp = fig1_df[["確定着順", "競走コード"]].groupby("確定着順").count().reset_index()
    fig1_gp.columns = ["labels", "values"]
    fig1_labels = fig1_gp["labels"].tolist()
    fig1_values = fig1_gp["values"].tolist()
    fig1 = gp.pie_chart(fig1_labels, fig1_values)
    fig1.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 単勝回収率
    fig2_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig2_df_diff = fig2_df[fig2_df["年月日"] != end_date]
    fig2_value = fig2_df["単勝配当"].mean()
    fig2_reference = fig2_df_diff["単勝配当"].mean()
    fig2 = gp.add_steps_threshold_anda_delta(fig2_value, fig2_reference)
    fig2.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝回収率
    fig3_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig3_df_diff = fig3_df[fig3_df["年月日"] != end_date]
    fig3_value = fig3_df["複勝配当"].mean()
    fig3_reference = fig3_df_diff["複勝配当"].mean()
    fig3 = gp.add_steps_threshold_anda_delta(fig3_value, fig3_reference)
    fig3.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # １番人気
    fig4_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig4_df.loc[:, "確定着順"] = fig4_df["確定着順"].apply(lambda x: str(x) + "着" if x in (1,2,3) else "着外")
    fig4_gp = fig4_df[["確定着順", "競走コード"]].groupby("確定着順").count().reset_index()
    fig4_gp.columns = ["labels", "values"]
    fig4_labels = fig4_gp["labels"].tolist()
    fig4_values = fig4_gp["values"].tolist()
    fig4 = gp.pie_chart(fig4_labels, fig4_values)
    fig4.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 単勝回収率
    fig5_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig5_df_diff = fig5_df[fig5_df["年月日"] != end_date]
    fig5_value = fig5_df["単勝配当"].mean()
    fig5_reference = fig5_df_diff["単勝配当"].mean()
    fig5 = gp.add_steps_threshold_anda_delta(fig5_value, fig5_reference)
    fig5.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝回収率
    fig6_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig6_df_diff = fig6_df[fig6_df["年月日"] != end_date]
    fig6_value = fig6_df["複勝配当"].mean()
    fig6_reference = fig6_df_diff["複勝配当"].mean()
    fig6 = gp.add_steps_threshold_anda_delta(fig6_value, fig6_reference)
    fig6.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別単複回収率・的中率
    fig7_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig7_df = pd.merge(race_df[["競走コード", "場名"]], fig7_df[["競走コード", "単勝配当", "複勝配当", "確定着順"]], on="競走コード" )
    fig7_df.loc[:, "単勝"] = fig7_df["確定着順"].apply(lambda x: 1 if x == 1 else 0)
    fig7_df.loc[:, "複勝"] = fig7_df["確定着順"].apply(lambda x: 1 if x in (1,2,3) else 0)
    fig7_gp = fig7_df.groupby("場名")[["単勝配当", "複勝配当", "単勝", "複勝"]].mean().reset_index()
    fig7_gp["単勝"] = fig7_gp["単勝"] * 100
    fig7_gp["複勝"] = fig7_gp["複勝"] * 100
    fig7_x_name = fig7_gp["場名"].tolist()
    fig7_bar_y_list = [fig7_gp["単勝配当"].tolist(), fig7_gp["複勝配当"].tolist()]
    fig7_bar_y_name = ["単勝回収率", "複勝回収率"]
    fig7_line_y_list = [fig7_gp["単勝"].tolist(), fig7_gp["複勝"].tolist()]
    fig7_line_y_name = ["単勝的中率", "複勝的中率"]
    fig7 = gp.multiple_line_and_bar_chart(fig7_x_name, fig7_line_y_list,fig7_line_y_name, fig7_bar_y_list, fig7_bar_y_name)
    fig7.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別馬券回収率・的中率
    fig8_df = bet_df.copy()
    fig8_df["レース"] = 1
    fig8_df.loc[:, "的中"] = fig8_df["結果"].apply(lambda x: 1 if x > 0 else 0)
    fig8_gp = fig8_df.groupby("場名")[["金額", "結果", "的中", "レース"]].sum().reset_index()
    fig8_gp.loc[:, "回収率"] = fig8_gp.apply(lambda x: x["結果"] / x["金額"] * 100, axis=1)
    fig8_gp.loc[:, "的中率"] = fig8_gp.apply(lambda x: x["的中"] / x["レース"] * 100, axis=1)
    fig8_x_name = fig8_gp["場名"].tolist()
    fig8_line_y_list = [fig8_gp["回収率"].tolist(), fig8_gp["的中率"].tolist()]
    fig8_line_y_name = ["回収率", "的中率"]
    fig8_bar_y_list = [fig8_gp["金額"].tolist(), fig8_gp["結果"].tolist()]
    fig8_bar_y_name = ["金額", "結果"]
    fig8 = gp.multiple_line_and_bar_chart(fig8_x_name, fig8_line_y_list, fig8_line_y_name, fig8_bar_y_list, fig8_bar_y_name)
    fig8.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # "馬連的中1
    fig10_base = race_df.query("UMAREN_ARE >= 50 and 場名 in ('園田','笠松','高知','水沢','盛岡','川崎','船橋','大井','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig10_base_set = set(fig10_base)
    fig10_jiku1 = raceuma_df.query("馬券評価順位 <= 2 and 得点 >= 51 and JIKU_RATE >= 47 and WIN_RATE >= 57 and 確定着順 in (1,2)")["競走馬コード"]
    fig10_jiku1_temp_set = set(fig10_jiku1)
    fig10_jiku1_set =set(map(lambda x: x[:11], list(fig10_jiku1_temp_set)))
    fig10_jiku2 = raceuma_df.query(f"得点 >= 40 and 確定着順 in (1,2)")["競走馬コード"]
    fig10_jiku2_temp_set = set(fig10_jiku2) - set(fig10_jiku1_temp_set)
    fig10_jiku2_set =set(map(lambda x: x[:11], list(fig10_jiku2_temp_set)))
    fig10_odds = haraimodoshi_dict["umaren_df"].query(f"払戻 >= 3000 and 払戻 <= 9000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig10_odds_set = set(fig10_odds) & fig10_base_set
    fig10_level1 = fig10_base_set
    fig10_level2 = fig10_base_set.intersection(fig10_jiku1_set)
    fig10_level3 = fig10_level2.intersection(fig10_jiku2_set)
    fig10_level4 = fig10_level3.intersection(fig10_odds_set)
    fig10_number = [len(fig10_level1), len(fig10_level2) , len(fig10_level3), len(fig10_level4)]
    fig10_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig10_data = dict(number=fig10_number, stage=fig10_stage)
    fig10 = gp.basic_funnel_plot(fig10_data)
    fig10.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連的中2
    fig11_base = race_df.query("UMAREN_ARE < 50 and 場名 in ('園田','笠松','高知','佐賀','水沢','盛岡','川崎','名古屋','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig11_base_set = set(fig11_base)
    fig11_jiku1 = raceuma_df.query("馬券評価順位 <= 2 and 得点 >= 53 and 予想人気 <= 5 and デフォルト得点 >= 51 and JIKU_RATE >= 54 and JIKU_RANK <= 3 and WIN_RATE >= 57 and WIN_RANK <= 2 and 確定着順 in (1,2)")["競走馬コード"]
    fig11_jiku1_temp_set = set(fig11_jiku1)
    fig11_jiku1_set =set(map(lambda x: x[:11], list(fig11_jiku1_temp_set)))
    fig11_jiku2 = raceuma_df.query(f"得点 >= 43 and 馬券評価順位 <= 8 and JIKU_RANK <= 9 and 予想人気 >= 4 and 確定着順 in (1,2)")["競走馬コード"]
    fig11_jiku2_temp_set = set(fig11_jiku2) - set(fig11_jiku1_temp_set)
    fig11_jiku2_set =set(map(lambda x: x[:11], list(fig11_jiku2_temp_set)))
    fig11_odds = haraimodoshi_dict["umaren_df"].query(f"払戻 >= 2000 and 払戻 <= 5000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig11_odds_set = set(fig11_odds) & fig11_base_set
    fig11_level1 = fig11_base_set
    fig11_level2 = fig11_base_set.intersection(fig11_jiku1_set)
    fig11_level3 = fig11_level2.intersection(fig11_jiku2_set)
    fig11_level4 = fig11_level3.intersection(fig11_odds_set)
    fig11_number = [len(fig11_level1), len(fig11_level2) , len(fig11_level3), len(fig11_level4)]
    fig11_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig11_data = dict(number=fig11_number, stage=fig11_stage)
    fig11 = gp.basic_funnel_plot(fig11_data)
    fig11.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中1
    fig12_base = race_df.query("場名 in ('園田','笠松','金沢','高知','水沢','川崎','船橋','名古屋','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig12_base_set = set(fig12_base)
    fig12_jiku1 = raceuma_df.query("得点 >= 48 and 馬券評価順位 <= 5 and JIKU_RATE >= 50 and WIN_RATE >= 45 and 確定着順 == 1")["競走馬コード"]
    fig12_jiku1_temp_set = set(fig12_jiku1)
    fig12_jiku1_set =set(map(lambda x: x[:11], list(fig12_jiku1_temp_set)))
    fig12_jiku2 = raceuma_df.query(f"得点 >= 43 and 馬券評価順位 <= 6 and デフォルト得点 >= 45 and JIKU_RATE >= 42 and 確定着順 == 2")["競走馬コード"]
    fig12_jiku2_temp_set = set(fig12_jiku2) - set(fig12_jiku1_temp_set)
    fig12_jiku2_set =set(map(lambda x: x[:11], list(fig12_jiku2_temp_set)))
    fig12_odds = haraimodoshi_dict["umatan_df"].query(f"払戻 >= 5000 and 払戻 <= 14000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig12_odds_set = set(fig12_odds) & fig12_base_set
    fig12_level1 = fig12_base_set
    fig12_level2 = fig12_base_set.intersection(fig12_jiku1_set)
    fig12_level3 = fig12_level2.intersection(fig12_jiku2_set)
    fig12_level4 = fig12_level3.intersection(fig12_odds_set)
    fig12_number = [len(fig12_level1), len(fig12_level2) , len(fig12_level3), len(fig12_level4)]
    fig12_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig12_data = dict(number=fig12_number, stage=fig12_stage)
    fig12 = gp.basic_funnel_plot(fig12_data)
    fig12.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中2
    fig13_base = race_df.query("場名 in ('浦和','園田','笠松','高知','佐賀','水沢','盛岡','川崎','船橋','大井','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig13_base_set = set(fig13_base)
    fig13_jiku1 = raceuma_df.query("得点 >= 54 and 馬券評価順位 == 1 and デフォルト得点 >= 53 and JIKU_RATE >= 55 and WIN_RANK <= 2 and 確定着順 == 1")["競走馬コード"]
    fig13_jiku1_temp_set = set(fig13_jiku1)
    fig13_jiku1_set =set(map(lambda x: x[:11], list(fig13_jiku1_temp_set)))
    fig13_jiku2 = raceuma_df.query(f"得点 >= 43 and 馬券評価順位 <= 8 and 確定着順 == 2")["競走馬コード"]
    fig13_jiku2_temp_set = set(fig13_jiku2) - set(fig13_jiku1_temp_set)
    fig13_jiku2_set =set(map(lambda x: x[:11], list(fig13_jiku2_temp_set)))
    fig13_odds = haraimodoshi_dict["umatan_df"].query(f"払戻 >= 2000 and 払戻 <= 6000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig13_odds_set = set(fig13_odds) & fig13_base_set
    fig13_level1 = fig13_base_set
    fig13_level2 = fig13_base_set.intersection(fig13_jiku1_set)
    fig13_level3 = fig13_level2.intersection(fig13_jiku2_set)
    fig13_level4 = fig13_level3.intersection(fig13_odds_set)
    fig13_number = [len(fig13_level1), len(fig13_level2) , len(fig13_level3), len(fig13_level4)]
    fig13_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig13_data = dict(number=fig13_number, stage=fig13_stage)
    fig13 = gp.basic_funnel_plot(fig13_data)
    fig13.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中3
    fig14_base = race_df.query("場名 in ('浦和','園田','笠松','高知','水沢','盛岡','川崎','大井')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig14_base_set = set(fig14_base)
    fig14_jiku1 = raceuma_df.query("得点 >= 43 and 馬券評価順位 <= 8 and WIN_RATE >= 47 and ANA_RANK <= 7 and 確定着順 == 1")["競走馬コード"]
    fig14_jiku1_temp_set = set(fig14_jiku1)
    fig14_jiku1_set =set(map(lambda x: x[:11], list(fig14_jiku1_temp_set)))
    fig14_jiku2 = raceuma_df.query(f"得点 >= 51 and JIKU_RANK <= 4 and 確定着順 == 2")["競走馬コード"]
    fig14_jiku2_temp_set = set(fig14_jiku2) - set(fig14_jiku1_temp_set)
    fig14_jiku2_set =set(map(lambda x: x[:11], list(fig14_jiku2_temp_set)))
    fig14_odds = haraimodoshi_dict["umatan_df"].query(f"払戻 >= 9000 and 払戻 <= 20000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig14_odds_set = set(fig14_odds) & fig14_base_set
    fig14_level1 = fig14_base_set
    fig14_level2 = fig14_base_set.intersection(fig14_jiku1_set)
    fig14_level3 = fig14_level2.intersection(fig14_jiku2_set)
    fig14_level4 = fig14_level3.intersection(fig14_odds_set)
    fig14_number = [len(fig14_level1), len(fig14_level2) , len(fig14_level3), len(fig14_level4)]
    fig14_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig14_data = dict(number=fig14_number, stage=fig14_stage)
    fig14 = gp.basic_funnel_plot(fig14_data)
    fig14.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド的中1
    fig15_base = race_df.query("場名 in ('笠松','佐賀','水沢','盛岡','川崎','大井','姫路','名古屋','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig15_base_set = set(fig15_base)
    fig15_jiku1 = raceuma_df.query("得点 >= 51 and デフォルト得点 <= 55 and JIKU_RANK <= 6 and WIN_RANK <= 4 and 確定着順 in (1,2,3)")["競走馬コード"]
    fig15_jiku1_temp_set = set(fig15_jiku1)
    fig15_jiku1_set =set(map(lambda x: x[:11], list(fig15_jiku1_temp_set)))
    fig15_jiku2 = raceuma_df.query(f"得点 >= 42 and JIKU_RANK <= 10 and 確定着順 in (1,2,3)")["競走馬コード"]
    fig15_jiku2_temp_set = set(fig15_jiku2) - set(fig15_jiku1_temp_set)
    fig15_jiku2_set =set(map(lambda x: x[:11], list(fig15_jiku2_temp_set)))
    fig15_odds = haraimodoshi_dict["wide_df"].query(f"払戻 >= 3000 and 払戻 <= 6000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig15_odds_set = set(fig15_odds) & fig15_base_set
    fig15_level1 = fig15_base_set
    fig15_level2 = fig15_base_set.intersection(fig15_jiku1_set)
    fig15_level3 = fig15_level2.intersection(fig15_jiku2_set)
    fig15_level4 = fig15_level3.intersection(fig15_odds_set)
    fig15_number = [len(fig15_level1), len(fig15_level2) , len(fig15_level3), len(fig15_level4)]
    fig15_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig15_data = dict(number=fig15_number, stage=fig15_stage)
    fig15 = gp.basic_funnel_plot(fig15_data)
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
