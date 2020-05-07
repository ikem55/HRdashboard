import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import components.webparts as wp
import components.graph as gp
from components.get_data import GetData
import components.calc_data as cd
import pandas as pd


def race_trend():
    print("race_trend")
    race_df = GetData.get_race_data_real().query("データ区分 == '7'")
    raceuma_df = GetData.get_raceuma_data_real().query("データ区分 == '7'")

    raceuma_df.loc[:, "競走馬コード"] = raceuma_df.apply(lambda x : str(x["競走コード"]) + str(x["馬番"]).zfill(2), axis=1)
    bet_df = GetData.get_bet_data_real()
    haraimodoshi_dict = GetData.get_haraimodoshi_dict_real()
    if len(race_df.index) == 0 or len(raceuma_df.index) == 0:
        return html.P("no data")

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
    fig7_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig7_df = pd.merge(race_df[["競走コード", "場名"]], fig7_df[["競走コード", "単勝配当", "複勝配当", "確定着順"]], on="競走コード" )
    fig7_df.loc[:, "単勝"] = fig7_df["確定着順"].apply(lambda x: 1 if x == 1 else 0)
    fig7_df.loc[:, "複勝"] = fig7_df["確定着順"].apply(lambda x: 1 if x in (1,2,3) else 0)
    fig7_gp = fig7_df.groupby("場名")[["単勝配当", "複勝配当", "単勝", "複勝"]].mean().reset_index()
    fig7_gp["単勝"] = fig7_gp["単勝"] * 100
    fig7_gp["複勝"] = fig7_gp["複勝"] * 100
    fig7_x_name = fig7_gp["場名"].tolist()
    fig7_line_y_list = [fig7_gp["単勝配当"].tolist(), fig7_gp["複勝配当"].tolist()]
    fig7_line_y_name = ["単勝回収率", "複勝回収率"]
    fig7_bar_y_list = [fig7_gp["単勝"].tolist(), fig7_gp["複勝"].tolist()]
    fig7_bar_y_name = ["単勝的中率", "複勝的中率"]
    fig7 = gp.multiple_line_and_bar_chart(fig7_x_name, fig7_line_y_list, fig7_line_y_name, fig7_bar_y_list, fig7_bar_y_name)
    fig7.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    if len(bet_df.index) != 0:
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
        fig8.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

        # 券種別結果
        summary_bet_df = cd.get_summary_bet_df(bet_df)
        fig9_df = summary_bet_df
        fig9_x_list = fig9_df["式別名"]
        fig9_y_list = fig9_df["合計"]
        fig9 = gp.simple_waterfall_chart(fig9_x_list, fig9_y_list)
        fig9.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})
    else:
        print("empty bet_df")
        fig8 = ""
        fig9 = ""

    # 単勝配当分布
    fig10_sr = cd.calc_cut_sr(haraimodoshi_dict["tansho_df"]["払戻"], [100, 200, 500, 1000, 3000, 5000])
    fig10 = gp.pie_chart(fig10_sr.index.values.categories.left.values, fig10_sr.values)
    fig10.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝配当分布
    fig11_sr = cd.calc_cut_sr(haraimodoshi_dict["fukusho_df"]["払戻"], [100, 150, 200, 300, 500, 1000])
    fig11 = gp.pie_chart(fig11_sr.index.values.categories.left.values, fig11_sr.values)
    fig11.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連配当分布
    fig12_sr = cd.calc_cut_sr(haraimodoshi_dict["umaren_df"]["払戻"], [100, 300, 500, 1000, 3000, 5000, 10000])
    fig12 = gp.pie_chart(fig12_sr.index.values.categories.left.values, fig12_sr.values)
    fig12.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単配当分布
    fig13_sr = cd.calc_cut_sr(haraimodoshi_dict["umatan_df"]["払戻"], [100, 500, 1000, 3000, 5000, 10000, 20000])
    fig13 = gp.pie_chart(fig13_sr.index.values.categories.left.values, fig13_sr.values)
    fig13.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド配当分布
    fig14_sr = cd.calc_cut_sr(haraimodoshi_dict["wide_df"]["払戻"], [100, 200, 300, 500, 1000, 2000, 3000])
    fig14 = gp.pie_chart(fig14_sr.index.values.categories.left.values, fig14_sr.values)
    fig14.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # 三連複配当分布
    fig15_sr = cd.calc_cut_sr(haraimodoshi_dict["sanrenpuku_df"]["払戻"], [100, 500, 1000, 3000, 5000, 10000, 20000])
    fig15 = gp.pie_chart(fig15_sr.index.values.categories.left.values, fig15_sr.values)
    fig15.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連的中1
    fig20_base = race_df.query("UMAREN_ARE >= 50 and 場名 in ('園田','笠松','高知','水沢','盛岡','川崎','船橋','大井','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig20_base_set = set(fig20_base)
    fig20_jiku1 = raceuma_df.query("馬券評価順位 <= 2 and 得点 >= 51 and JIKU_RATE >= 47 and WIN_RATE >= 57 and 確定着順 in (1,2)")["競走馬コード"]
    fig20_jiku1_temp_set = set(fig20_jiku1)
    fig20_jiku1_set =set(map(lambda x: x[:11], list(fig20_jiku1_temp_set)))
    fig20_jiku2 = raceuma_df.query(f"得点 >= 40 and 確定着順 in (1,2)")["競走馬コード"]
    fig20_jiku2_temp_set = set(fig20_jiku2) - set(fig20_jiku1_temp_set)
    fig20_jiku2_set =set(map(lambda x: x[:11], list(fig20_jiku2_temp_set)))
    fig20_odds = haraimodoshi_dict["umaren_df"].query(f"払戻 >= 3000 and 払戻 <= 9000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig20_odds_set = set(fig20_odds) & fig20_base_set
    fig20_level1 = fig20_base_set
    fig20_level2 = fig20_base_set.intersection(fig20_jiku1_set)
    fig20_level3 = fig20_level2.intersection(fig20_jiku2_set)
    fig20_level4 = fig20_level3.intersection(fig20_odds_set)
    fig20_number = [len(fig20_level1), len(fig20_level2) , len(fig20_level3), len(fig20_level4)]
    fig20_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig20_data = dict(number=fig20_number, stage=fig20_stage)
    fig20 = gp.basic_funnel_plot(fig20_data)
    fig20.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連的中2
    fig21_base = race_df.query("UMAREN_ARE < 50 and 場名 in ('園田','笠松','高知','佐賀','水沢','盛岡','川崎','名古屋','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig21_base_set = set(fig21_base)
    fig21_jiku1 = raceuma_df.query("馬券評価順位 <= 2 and 得点 >= 53 and 予想人気 <= 5 and デフォルト得点 >= 51 and JIKU_RATE >= 54 and JIKU_RANK <= 3 and WIN_RATE >= 57 and WIN_RANK <= 2 and 確定着順 in (1,2)")["競走馬コード"]
    fig21_jiku1_temp_set = set(fig21_jiku1)
    fig21_jiku1_set =set(map(lambda x: x[:11], list(fig21_jiku1_temp_set)))
    fig21_jiku2 = raceuma_df.query(f"得点 >= 43 and 馬券評価順位 <= 8 and JIKU_RANK <= 9 and 予想人気 >= 4 and 確定着順 in (1,2)")["競走馬コード"]
    fig21_jiku2_temp_set = set(fig21_jiku2) - set(fig21_jiku1_temp_set)
    fig21_jiku2_set =set(map(lambda x: x[:11], list(fig21_jiku2_temp_set)))
    fig21_odds = haraimodoshi_dict["umaren_df"].query(f"払戻 >= 2000 and 払戻 <= 5000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig21_odds_set = set(fig21_odds) & fig21_base_set
    fig21_level1 = fig21_base_set
    fig21_level2 = fig21_base_set.intersection(fig21_jiku1_set)
    fig21_level3 = fig21_level2.intersection(fig21_jiku2_set)
    fig21_level4 = fig21_level3.intersection(fig21_odds_set)
    fig21_number = [len(fig21_level1), len(fig21_level2) , len(fig21_level3), len(fig21_level4)]
    fig21_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig21_data = dict(number=fig21_number, stage=fig21_stage)
    fig21 = gp.basic_funnel_plot(fig21_data)
    fig21.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中1
    fig22_base = race_df.query("場名 in ('園田','笠松','金沢','高知','水沢','川崎','船橋','名古屋','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig22_base_set = set(fig22_base)
    fig22_jiku1 = raceuma_df.query("得点 >= 48 and 馬券評価順位 <= 5 and JIKU_RATE >= 50 and WIN_RATE >= 45 and 確定着順 == 1")["競走馬コード"]
    fig22_jiku1_temp_set = set(fig22_jiku1)
    fig22_jiku1_set =set(map(lambda x: x[:11], list(fig22_jiku1_temp_set)))
    fig22_jiku2 = raceuma_df.query(f"得点 >= 43 and 馬券評価順位 <= 6 and デフォルト得点 >= 45 and JIKU_RATE >= 42 and 確定着順 == 2")["競走馬コード"]
    fig22_jiku2_temp_set = set(fig22_jiku2) - set(fig22_jiku1_temp_set)
    fig22_jiku2_set =set(map(lambda x: x[:11], list(fig22_jiku2_temp_set)))
    fig22_odds = haraimodoshi_dict["umatan_df"].query(f"払戻 >= 5000 and 払戻 <= 14000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig22_odds_set = set(fig22_odds) & fig22_base_set
    fig22_level1 = fig22_base_set
    fig22_level2 = fig22_base_set.intersection(fig22_jiku1_set)
    fig22_level3 = fig22_level2.intersection(fig22_jiku2_set)
    fig22_level4 = fig22_level3.intersection(fig22_odds_set)
    fig22_number = [len(fig22_level1), len(fig22_level2) , len(fig22_level3), len(fig22_level4)]
    fig22_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig22_data = dict(number=fig22_number, stage=fig22_stage)
    fig22 = gp.basic_funnel_plot(fig22_data)
    fig22.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中2
    fig23_base = race_df.query("場名 in ('浦和','園田','笠松','高知','佐賀','水沢','盛岡','川崎','船橋','大井','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig23_base_set = set(fig23_base)
    fig23_jiku1 = raceuma_df.query("得点 >= 54 and 馬券評価順位 == 1 and デフォルト得点 >= 53 and JIKU_RATE >= 55 and WIN_RANK <= 2 and 確定着順 == 1")["競走馬コード"]
    fig23_jiku1_temp_set = set(fig23_jiku1)
    fig23_jiku1_set =set(map(lambda x: x[:11], list(fig23_jiku1_temp_set)))
    fig23_jiku2 = raceuma_df.query(f"得点 >= 43 and 馬券評価順位 <= 8 and 確定着順 == 2")["競走馬コード"]
    fig23_jiku2_temp_set = set(fig23_jiku2) - set(fig23_jiku1_temp_set)
    fig23_jiku2_set =set(map(lambda x: x[:11], list(fig23_jiku2_temp_set)))
    fig23_odds = haraimodoshi_dict["umatan_df"].query(f"払戻 >= 2000 and 払戻 <= 6000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig23_odds_set = set(fig23_odds) & fig23_base_set
    fig23_level1 = fig23_base_set
    fig23_level2 = fig23_base_set.intersection(fig23_jiku1_set)
    fig23_level3 = fig23_level2.intersection(fig23_jiku2_set)
    fig23_level4 = fig23_level3.intersection(fig23_odds_set)
    fig23_number = [len(fig23_level1), len(fig23_level2) , len(fig23_level3), len(fig23_level4)]
    fig23_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig23_data = dict(number=fig23_number, stage=fig23_stage)
    fig23 = gp.basic_funnel_plot(fig23_data)
    fig23.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中3
    fig24_base = race_df.query("場名 in ('浦和','園田','笠松','高知','水沢','盛岡','川崎','大井')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig24_base_set = set(fig24_base)
    fig24_jiku1 = raceuma_df.query("得点 >= 43 and 馬券評価順位 <= 8 and WIN_RATE >= 47 and ANA_RANK <= 7 and 確定着順 == 1")["競走馬コード"]
    fig24_jiku1_temp_set = set(fig24_jiku1)
    fig24_jiku1_set =set(map(lambda x: x[:11], list(fig24_jiku1_temp_set)))
    fig24_jiku2 = raceuma_df.query(f"得点 >= 51 and JIKU_RANK <= 4 and 確定着順 == 2")["競走馬コード"]
    fig24_jiku2_temp_set = set(fig24_jiku2) - set(fig24_jiku1_temp_set)
    fig24_jiku2_set =set(map(lambda x: x[:11], list(fig24_jiku2_temp_set)))
    fig24_odds = haraimodoshi_dict["umatan_df"].query(f"払戻 >= 9000 and 払戻 <= 20000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig24_odds_set = set(fig24_odds) & fig24_base_set
    fig24_level1 = fig24_base_set
    fig24_level2 = fig24_base_set.intersection(fig24_jiku1_set)
    fig24_level3 = fig24_level2.intersection(fig24_jiku2_set)
    fig24_level4 = fig24_level3.intersection(fig24_odds_set)
    fig24_number = [len(fig24_level1), len(fig24_level2) , len(fig24_level3), len(fig24_level4)]
    fig24_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig24_data = dict(number=fig24_number, stage=fig24_stage)
    fig24 = gp.basic_funnel_plot(fig24_data)
    fig24.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド的中1
    fig25_base = race_df.query("場名 in ('笠松','佐賀','水沢','盛岡','川崎','大井','姫路','名古屋','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig25_base_set = set(fig25_base)
    fig25_jiku1 = raceuma_df.query("得点 >= 51 and デフォルト得点 <= 55 and JIKU_RANK <= 6 and WIN_RANK <= 4 and 確定着順 in (1,2,3)")["競走馬コード"]
    fig25_jiku1_temp_set = set(fig25_jiku1)
    fig25_jiku1_set =set(map(lambda x: x[:11], list(fig25_jiku1_temp_set)))
    fig25_jiku2 = raceuma_df.query(f"得点 >= 42 and JIKU_RANK <= 10 and 確定着順 in (1,2,3)")["競走馬コード"]
    fig25_jiku2_temp_set = set(fig25_jiku2) - set(fig25_jiku1_temp_set)
    fig25_jiku2_set =set(map(lambda x: x[:11], list(fig25_jiku2_temp_set)))
    fig25_odds = haraimodoshi_dict["wide_df"].query(f"払戻 >= 3000 and 払戻 <= 6000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig25_odds_set = set(fig25_odds) & fig25_base_set
    fig25_level1 = fig25_base_set
    fig25_level2 = fig25_base_set.intersection(fig25_jiku1_set)
    fig25_level3 = fig25_level2.intersection(fig25_jiku2_set)
    fig25_level4 = fig25_level3.intersection(fig25_odds_set)
    fig25_number = [len(fig25_level1), len(fig25_level2) , len(fig25_level3), len(fig25_level4)]
    fig25_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig25_data = dict(number=fig25_number, stage=fig25_stage)
    fig25 = gp.basic_funnel_plot(fig25_data)
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