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
    fig1_value = daily_bet_df["合計"].sum()
    fig1_reference = prev_daily_bet_df["合計"].sum()
    fig1 = gp.data_cards(fig1_value, fig1_reference)
    fig1.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 回収率
    fig2_value = daily_bet_df["結果"].sum() / daily_bet_df["金額"].sum() * 100
    fig2_reference = prev_daily_bet_df["結果"].sum() / prev_daily_bet_df["金額"].sum() * 100
    fig2_list_sr = daily_bet_df["回収率"].tolist()
    fig2 = gp.showing_information_above(fig2_value, fig2_reference, fig2_list_sr)
    fig2.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 単勝回収率
    fig3_value = daily_rank1_raceuma_df["単勝配当"].mean()
    fig3_reference = prev_daily_rank1_raceuma_df["単勝配当"].mean()
    fig3 = gp.add_steps_threshold_anda_delta(fig3_value, fig3_reference)
    fig3.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 複勝回収率
    fig4_value = daily_rank1_raceuma_df["複勝配当"].mean()
    fig4_reference = prev_daily_rank1_raceuma_df["複勝配当"].mean()
    fig4 = gp.add_steps_threshold_anda_delta(fig4_value, fig4_reference)
    fig4.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 残高推移1
    fig5_df = daily_bet_df[["日付", "合計"]]
    fig5_df.loc[:, "合計"] = fig5_df["合計"].cumsum()
    fig5_x_label = "日付"
    fig5_y_label = "合計"
    fig5 = gp.time_series_with_range_selector_buttions(fig5_df, fig5_x_label, fig5_y_label)
    fig5.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    # 残高推移2
    fig6_df = summary_bet_df
    fig6_x_list = fig6_df["式別名"]
    fig6_y_list = fig6_df["合計"]
    fig6 = gp.simple_waterfall_chart(fig6_x_list, fig6_y_list)
    fig6.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別回収率的中率払戻
    fig7_x_list = (place_bet_df["的中"] / place_bet_df["レース"]) * 100
    fig7_y_list = (place_bet_df["結果"] / place_bet_df["金額"]) * 100
    fig7_z_list = place_bet_df["結果"] + 1
    fig7_name_list = place_bet_df["場名"]
    fig7_x_title = "的中率"
    fig7_y_title = "回収率"
    fig7 = gp.buble_chart(fig7_x_list, fig7_y_list, fig7_z_list, fig7_name_list, fig7_x_title, fig7_y_title)
    fig7.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 券種毎回収率
    fig8_df = summary_bet_df[summary_bet_df["金額"] != 0].copy()
    fig8_type_list = fig8_df["式別名"]
    fig8_value_list = (fig8_df["結果"] / fig8_df["金額"]) * 100
    fig8 = gp.multi_bullet(fig8_type_list, fig8_value_list)
    fig8.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 得点１位着順
    fig9_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig9_df.loc[:, "確定着順"] = fig9_df["確定着順"].apply(lambda x: str(x) + "着" if x in (1,2,3) else "着外")
    fig9_gp = fig9_df[["確定着順", "競走コード"]].groupby("確定着順").count().reset_index()
    fig9_gp.columns = ["labels", "values"]
    fig9_labels = fig9_gp["labels"].tolist()
    fig9_values = fig9_gp["values"].tolist()
    fig9 = gp.pie_chart(fig9_labels, fig9_values)
    fig9.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別単複回収率・的中率
    fig10_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig10_df = pd.merge(race_df[["競走コード", "場名"]], fig10_df[["競走コード", "単勝配当", "複勝配当", "確定着順"]], on="競走コード" )
    fig10_df.loc[:, "単勝"] = fig10_df["確定着順"].apply(lambda x: 1 if x == 1 else 0)
    fig10_df.loc[:, "複勝"] = fig10_df["確定着順"].apply(lambda x: 1 if x in (1,2,3) else 0)
    fig10_gp = fig10_df.groupby("場名")[["単勝配当", "複勝配当", "単勝", "複勝"]].mean().reset_index()
    fig10_gp["単勝"] = fig10_gp["単勝"] * 100
    fig10_gp["複勝"] = fig10_gp["複勝"] * 100
    fig10_x_name = fig10_gp["場名"].tolist()
    fig10_line_y_list = [fig10_gp["単勝配当"].tolist(), fig10_gp["複勝配当"].tolist()]
    fig10_line_y_name = ["単勝回収率", "複勝回収率"]
    fig10_bar_y_list = [fig10_gp["単勝"].tolist(), fig10_gp["複勝"].tolist()]
    fig10_bar_y_name = ["単勝的中率", "複勝的中率"]
    fig10 = gp.multiple_line_and_bar_chart(fig10_x_name, fig10_line_y_list,fig10_line_y_name, fig10_bar_y_list, fig10_bar_y_name)
    fig10.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 場所別馬券回収率・的中率
    fig11_df = bet_df.copy()
    fig11_df["レース"] = 1
    fig11_df.loc[:, "的中"] = fig11_df["結果"].apply(lambda x: 1 if x > 0 else 0)
    fig11_gp = fig11_df.groupby("場名")[["金額", "結果", "的中", "レース"]].sum().reset_index()
    fig11_gp.loc[:, "回収率"] = fig11_gp.apply(lambda x: x["結果"] / x["金額"] * 100, axis=1)
    fig11_gp.loc[:, "的中率"] = fig11_gp.apply(lambda x: x["的中"] / x["レース"] * 100, axis=1)
    fig11_x_name = fig11_gp["場名"].tolist()
    fig11_line_y_list = [fig11_gp["回収率"].tolist(), fig11_gp["的中率"].tolist()]
    fig11_line_y_name = ["回収率", "的中率"]
    fig11_bar_y_list = [fig11_gp["金額"].tolist(), fig11_gp["結果"].tolist()]
    fig11_bar_y_name = ["金額", "結果"]
    fig11 = gp.multiple_line_and_bar_chart(fig11_x_name, fig11_line_y_list, fig11_line_y_name, fig11_bar_y_list, fig11_bar_y_name)
    fig11.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})


    # 馬連的中1
    fig12_base = race_df.query("UMAREN_ARE >= 50 and 場名 in ('園田','笠松','高知','水沢','盛岡','川崎','船橋','大井','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig12_base_set = set(fig12_base)
    fig12_jiku1 = raceuma_df.query("馬券評価順位 <= 2 and 得点 >= 51 and JIKU_RATE >= 47 and WIN_RATE >= 57 and 確定着順 in (1,2)")["競走馬コード"]
    fig12_jiku1_temp_set = set(fig12_jiku1)
    fig12_jiku1_set =set(map(lambda x: x[:11], list(fig12_jiku1_temp_set)))
    fig12_jiku2 = raceuma_df.query(f"得点 >= 40 and 確定着順 in (1,2)")["競走馬コード"]
    fig12_jiku2_temp_set = set(fig12_jiku2) - set(fig12_jiku1_temp_set)
    fig12_jiku2_set =set(map(lambda x: x[:11], list(fig12_jiku2_temp_set)))
    fig12_odds = haraimodoshi_dict["umaren_df"].query(f"払戻 >= 3000 and 払戻 <= 9000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig12_odds_set = set(fig12_odds) & fig12_base_set
    fig12_level1 = fig12_base_set
    fig12_level2 = fig12_base_set.intersection(fig12_jiku1_set)
    fig12_level3 = fig12_level2.intersection(fig12_jiku2_set)
    fig12_level4 = fig12_level3.intersection(fig12_odds_set)
    fig12_number = [len(fig12_level1), len(fig12_level2) , len(fig12_level3), len(fig12_level4)]
    fig12_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig12_data = dict(number=fig12_number, stage=fig12_stage)
    fig12 = gp.basic_funnel_plot(fig12_data)
    fig12.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連的中2
    fig13_base = race_df.query("UMAREN_ARE < 50 and 場名 in ('園田','笠松','高知','佐賀','水沢','盛岡','川崎','名古屋','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig13_base_set = set(fig13_base)
    fig13_jiku1 = raceuma_df.query("馬券評価順位 <= 2 and 得点 >= 53 and 予想人気 <= 5 and デフォルト得点 >= 51 and JIKU_RATE >= 54 and JIKU_RANK <= 3 and WIN_RATE >= 57 and WIN_RANK <= 2 and 確定着順 in (1,2)")["競走馬コード"]
    fig13_jiku1_temp_set = set(fig13_jiku1)
    fig13_jiku1_set =set(map(lambda x: x[:11], list(fig13_jiku1_temp_set)))
    fig13_jiku2 = raceuma_df.query(f"得点 >= 43 and 馬券評価順位 <= 8 and JIKU_RANK <= 9 and 予想人気 >= 4 and 確定着順 in (1,2)")["競走馬コード"]
    fig13_jiku2_temp_set = set(fig13_jiku2) - set(fig13_jiku1_temp_set)
    fig13_jiku2_set =set(map(lambda x: x[:11], list(fig13_jiku2_temp_set)))
    fig13_odds = haraimodoshi_dict["umaren_df"].query(f"払戻 >= 2000 and 払戻 <= 5000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig13_odds_set = set(fig13_odds) & fig13_base_set
    fig13_level1 = fig13_base_set
    fig13_level2 = fig13_base_set.intersection(fig13_jiku1_set)
    fig13_level3 = fig13_level2.intersection(fig13_jiku2_set)
    fig13_level4 = fig13_level3.intersection(fig13_odds_set)
    fig13_number = [len(fig13_level1), len(fig13_level2) , len(fig13_level3), len(fig13_level4)]
    fig13_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig13_data = dict(number=fig13_number, stage=fig13_stage)
    fig13 = gp.basic_funnel_plot(fig13_data)
    fig13.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中1
    fig14_base = race_df.query("場名 in ('園田','笠松','金沢','高知','水沢','川崎','船橋','名古屋','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig14_base_set = set(fig14_base)
    fig14_jiku1 = raceuma_df.query("得点 >= 48 and 馬券評価順位 <= 5 and JIKU_RATE >= 50 and WIN_RATE >= 45 and 確定着順 == 1")["競走馬コード"]
    fig14_jiku1_temp_set = set(fig14_jiku1)
    fig14_jiku1_set =set(map(lambda x: x[:11], list(fig14_jiku1_temp_set)))
    fig14_jiku2 = raceuma_df.query(f"得点 >= 43 and 馬券評価順位 <= 6 and デフォルト得点 >= 45 and JIKU_RATE >= 42 and 確定着順 == 2")["競走馬コード"]
    fig14_jiku2_temp_set = set(fig14_jiku2) - set(fig14_jiku1_temp_set)
    fig14_jiku2_set =set(map(lambda x: x[:11], list(fig14_jiku2_temp_set)))
    fig14_odds = haraimodoshi_dict["umatan_df"].query(f"払戻 >= 5000 and 払戻 <= 14000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig14_odds_set = set(fig14_odds) & fig14_base_set
    fig14_level1 = fig14_base_set
    fig14_level2 = fig14_base_set.intersection(fig14_jiku1_set)
    fig14_level3 = fig14_level2.intersection(fig14_jiku2_set)
    fig14_level4 = fig14_level3.intersection(fig14_odds_set)
    fig14_number = [len(fig14_level1), len(fig14_level2) , len(fig14_level3), len(fig14_level4)]
    fig14_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig14_data = dict(number=fig14_number, stage=fig14_stage)
    fig14 = gp.basic_funnel_plot(fig14_data)
    fig14.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中2
    fig15_base = race_df.query("場名 in ('浦和','園田','笠松','高知','佐賀','水沢','盛岡','川崎','船橋','大井','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig15_base_set = set(fig15_base)
    fig15_jiku1 = raceuma_df.query("得点 >= 54 and 馬券評価順位 == 1 and デフォルト得点 >= 53 and JIKU_RATE >= 55 and WIN_RANK <= 2 and 確定着順 == 1")["競走馬コード"]
    fig15_jiku1_temp_set = set(fig15_jiku1)
    fig15_jiku1_set =set(map(lambda x: x[:11], list(fig15_jiku1_temp_set)))
    fig15_jiku2 = raceuma_df.query(f"得点 >= 43 and 馬券評価順位 <= 8 and 確定着順 == 2")["競走馬コード"]
    fig15_jiku2_temp_set = set(fig15_jiku2) - set(fig15_jiku1_temp_set)
    fig15_jiku2_set =set(map(lambda x: x[:11], list(fig15_jiku2_temp_set)))
    fig15_odds = haraimodoshi_dict["umatan_df"].query(f"払戻 >= 2000 and 払戻 <= 6000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig15_odds_set = set(fig15_odds) & fig15_base_set
    fig15_level1 = fig15_base_set
    fig15_level2 = fig15_base_set.intersection(fig15_jiku1_set)
    fig15_level3 = fig15_level2.intersection(fig15_jiku2_set)
    fig15_level4 = fig15_level3.intersection(fig15_odds_set)
    fig15_number = [len(fig15_level1), len(fig15_level2) , len(fig15_level3), len(fig15_level4)]
    fig15_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig15_data = dict(number=fig15_number, stage=fig15_stage)
    fig15 = gp.basic_funnel_plot(fig15_data)
    fig15.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単的中3
    fig16_base = race_df.query("場名 in ('浦和','園田','笠松','高知','水沢','盛岡','川崎','大井')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig16_base_set = set(fig16_base)
    fig16_jiku1 = raceuma_df.query("得点 >= 43 and 馬券評価順位 <= 8 and WIN_RATE >= 47 and ANA_RANK <= 7 and 確定着順 == 1")["競走馬コード"]
    fig16_jiku1_temp_set = set(fig16_jiku1)
    fig16_jiku1_set =set(map(lambda x: x[:11], list(fig16_jiku1_temp_set)))
    fig16_jiku2 = raceuma_df.query(f"得点 >= 51 and JIKU_RANK <= 4 and 確定着順 == 2")["競走馬コード"]
    fig16_jiku2_temp_set = set(fig16_jiku2) - set(fig16_jiku1_temp_set)
    fig16_jiku2_set =set(map(lambda x: x[:11], list(fig16_jiku2_temp_set)))
    fig16_odds = haraimodoshi_dict["umatan_df"].query(f"払戻 >= 9000 and 払戻 <= 20000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig16_odds_set = set(fig16_odds) & fig16_base_set
    fig16_level1 = fig16_base_set
    fig16_level2 = fig16_base_set.intersection(fig16_jiku1_set)
    fig16_level3 = fig16_level2.intersection(fig16_jiku2_set)
    fig16_level4 = fig16_level3.intersection(fig16_odds_set)
    fig16_number = [len(fig16_level1), len(fig16_level2) , len(fig16_level3), len(fig16_level4)]
    fig16_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig16_data = dict(number=fig16_number, stage=fig16_stage)
    fig16 = gp.basic_funnel_plot(fig16_data)
    fig16.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド的中1
    fig17_base = race_df.query("場名 in ('笠松','佐賀','水沢','盛岡','川崎','大井','姫路','名古屋','門別')")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig17_base_set = set(fig17_base)
    fig17_jiku1 = raceuma_df.query("得点 >= 51 and デフォルト得点 <= 55 and JIKU_RANK <= 6 and WIN_RANK <= 4 and 確定着順 in (1,2,3)")["競走馬コード"]
    fig17_jiku1_temp_set = set(fig17_jiku1)
    fig17_jiku1_set =set(map(lambda x: x[:11], list(fig17_jiku1_temp_set)))
    fig17_jiku2 = raceuma_df.query(f"得点 >= 42 and JIKU_RANK <= 10 and 確定着順 in (1,2,3)")["競走馬コード"]
    fig17_jiku2_temp_set = set(fig17_jiku2) - set(fig17_jiku1_temp_set)
    fig17_jiku2_set =set(map(lambda x: x[:11], list(fig17_jiku2_temp_set)))
    fig17_odds = haraimodoshi_dict["wide_df"].query(f"払戻 >= 3000 and 払戻 <= 6000")["競走コード"].astype(str).apply(lambda x: x[:11])
    fig17_odds_set = set(fig17_odds) & fig17_base_set
    fig17_level1 = fig17_base_set
    fig17_level2 = fig17_base_set.intersection(fig17_jiku1_set)
    fig17_level3 = fig17_level2.intersection(fig17_jiku2_set)
    fig17_level4 = fig17_level3.intersection(fig17_odds_set)
    fig17_number = [len(fig17_level1), len(fig17_level2) , len(fig17_level3), len(fig17_level4)]
    fig17_stage = ["対象レース数", "軸１通過", "軸２通過", "配当通過"]
    fig17_data = dict(number=fig17_number, stage=fig17_stage)
    fig17 = gp.basic_funnel_plot(fig17_data)
    fig17.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬連配当分布
    fig18_umaren_df = haraimodoshi_dict["umaren_df"]
    fig18_df = pd.merge(fig18_umaren_df, race_df[["競走コード", "月日", "年月"]], on ="競走コード")
    fig18_df.loc[:, "月日"] = fig18_df["月日"].apply(lambda x: x.strftime("%y/%m/%d"))
    fig18_df = fig18_df.rename(columns={"月日": "label", "払戻": "value"})
    fig18_df["color"] = "馬連"
    fig18 = gp.choosing_the_algorithm(fig18_df, "label", "value", "color", 7000)
    fig18.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単配当分布
    fig19_umatan_df = haraimodoshi_dict["umatan_df"]
    fig19_df = pd.merge(fig19_umatan_df, race_df[["競走コード", "月日", "年月"]], on ="競走コード")
    fig19_df.loc[:, "月日"] = fig19_df["月日"].apply(lambda x: x.strftime("%y/%m/%d"))
    fig19_df = fig19_df.rename(columns={"月日": "label", "払戻": "value"})
    fig19_df["color"] = "馬単"
    fig19 = gp.choosing_the_algorithm(fig19_df, "label", "value", "color", 15000)
    fig19.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    # ワイド配当分布
    fig20_wide_df = haraimodoshi_dict["wide_df"]
    fig20_df = pd.merge(fig20_wide_df, race_df[["競走コード", "月日", "年月"]], on="競走コード")
    fig20_df.loc[:, "月日"] = fig20_df["月日"].apply(lambda x: x.strftime("%y/%m/%d"))
    fig20_df = fig20_df.rename(columns={"月日": "label", "払戻": "value"})
    fig20_df["color"] = "ワイド"
    fig20 = gp.choosing_the_algorithm(fig20_df, "label", "value", "color", 3000)
    fig20.update_layout(height=250, margin={'t': 0, 'b': 0, 'l': 0})

    # 三連複配当分布
    fig21_sanrenpuku_df = haraimodoshi_dict["sanrenpuku_df"]
    fig21_df = pd.merge(fig21_sanrenpuku_df, race_df[["競走コード", "月日", "年月"]], on="競走コード")
    fig21_df.loc[:, "月日"] = fig21_df["月日"].apply(lambda x: x.strftime("%y/%m/%d"))
    fig21_df = fig21_df.rename(columns={"月日": "label", "払戻": "value"})
    fig21_df["color"] = "三連複"
    fig21 = gp.choosing_the_algorithm(fig21_df, "label", "value", "color", 15000)
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
