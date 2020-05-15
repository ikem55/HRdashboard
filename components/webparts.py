
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import numpy as np
import dash_table.FormatTemplate as FormatTemplate
import components.calc_data as cd
import components.graph as gp
import plotly.graph_objects as go

def cp_data_cards_return(daily_bet_df, prev_daily_bet_df):
    # 回収
    fig1_value = daily_bet_df["合計"].sum()
    fig1_reference = prev_daily_bet_df["合計"].sum()
    fig1 = gp.data_cards(fig1_value, fig1_reference)
    return fig1

def cp_showing_information_above_return_rate(daily_bet_df, prev_daily_bet_df):
    # 回収率
    fig2_value = daily_bet_df["結果"].sum() / daily_bet_df["金額"].sum() * 100
    fig2_reference = prev_daily_bet_df["結果"].sum() / prev_daily_bet_df["金額"].sum() * 100
    fig2_list_sr = daily_bet_df["回収率"].tolist()
    fig2 = gp.showing_information_above(fig2_value, fig2_reference, fig2_list_sr)
    return fig2

def cp_add_steps_threshold_anda_delta_tansho_return(daily_rank1_raceuma_df, prev_daily_rank1_raceuma_df):
    # 単勝回収率
    fig3_value = daily_rank1_raceuma_df["単勝配当"].mean()
    fig3_reference = prev_daily_rank1_raceuma_df["単勝配当"].mean()
    fig3 = gp.add_steps_threshold_anda_delta(fig3_value, fig3_reference)
    return fig3

def cp_add_steps_threshold_anda_delta_fukusho_return(daily_rank1_raceuma_df, prev_daily_rank1_raceuma_df):
    # 複勝回収率
    fig4_value = daily_rank1_raceuma_df["複勝配当"].mean()
    fig4_reference = prev_daily_rank1_raceuma_df["複勝配当"].mean()
    fig4 = gp.add_steps_threshold_anda_delta(fig4_value, fig4_reference)
    return fig4

def cp_time_series_with_range_selector_buttions_balance_change(daily_bet_df):
    # 残高推移1
    fig5_df = daily_bet_df[["日付", "合計"]]
    fig5_df.loc[:, "合計"] = fig5_df["合計"].cumsum()
    fig5_x_label = "日付"
    fig5_y_label = "合計"
    fig5 = gp.time_series_with_range_selector_buttions(fig5_df, fig5_x_label, fig5_y_label)
    return fig5

def cp_simple_waterfall_chart_balance_change(summary_bet_df):
    # 残高推移2
    fig6_df = summary_bet_df
    fig6_x_list = fig6_df["式別名"]
    fig6_y_list = fig6_df["合計"]
    fig6 = gp.simple_waterfall_chart(fig6_x_list, fig6_y_list)
    return fig6

def cp_buble_chart_place_return_hit(place_bet_df):
    # 場所別回収率的中率払戻
    fig7_x_list = (place_bet_df["的中"] / place_bet_df["レース"]) * 100
    fig7_y_list = (place_bet_df["結果"] / place_bet_df["金額"]) * 100
    fig7_z_list = place_bet_df["結果"] + 1
    fig7_name_list = place_bet_df["場名"]
    fig7_x_title = "的中率"
    fig7_y_title = "回収率"
    fig7 = gp.buble_chart(fig7_x_list, fig7_y_list, fig7_z_list, fig7_name_list, fig7_x_title, fig7_y_title)
    return fig7

def cp_multi_bullet(summary_bet_df):
    # 券種毎回収率
    fig8_df = summary_bet_df[summary_bet_df["金額"] != 0].copy()
    fig8_type_list = fig8_df["式別名"]
    fig8_value_list = (fig8_df["結果"] / fig8_df["金額"]) * 100
    fig8 = gp.multi_bullet(fig8_type_list, fig8_value_list)
    return fig8

def cp_pie_chart_score_1(raceuma_df):
    # 得点１位着順
    fig9_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig9_df.loc[:, "確定着順"] = fig9_df["確定着順"].apply(lambda x: str(x) + "着" if x in (1,2,3) else "着外")
    fig9_gp = fig9_df[["確定着順", "競走コード"]].groupby("確定着順").count().reset_index()
    fig9_gp.columns = ["labels", "values"]
    fig9_labels = fig9_gp["labels"].tolist()
    fig9_values = fig9_gp["values"].tolist()
    fig9 = gp.pie_chart(fig9_labels, fig9_values)
    return fig9

def cp_pie_chart_ninki_1(raceuma_df):
    # １番人気
    fig4_df = raceuma_df[raceuma_df["単勝人気"] == 1].copy()
    fig4_df.loc[:, "確定着順"] = fig4_df["確定着順"].apply(lambda x: str(x) + "着" if x in (1,2,3) else "着外")
    fig4_gp = fig4_df[["確定着順", "競走コード"]].groupby("確定着順").count().reset_index()
    fig4_gp.columns = ["labels", "values"]
    fig4_labels = fig4_gp["labels"].tolist()
    fig4_values = fig4_gp["values"].tolist()
    fig4 = gp.pie_chart(fig4_labels, fig4_values)
    return fig4

def cp_multiple_line_and_bar_chart_place_tanpuku_return(race_df, raceuma_df):
    # 場所別単複回収率・的中率
    fig10_df = raceuma_df[raceuma_df["馬券評価順位"] == 1].copy()
    fig10_df = pd.merge(race_df[["競走コード", "場名"]], fig10_df[["競走コード", "単勝配当", "複勝配当", "確定着順"]], on="競走コード")
    fig10_df.loc[:, "単勝"] = fig10_df["確定着順"].apply(lambda x: 1 if x == 1 else 0)
    fig10_df.loc[:, "複勝"] = fig10_df["確定着順"].apply(lambda x: 1 if x in (1, 2, 3) else 0)
    fig10_gp = fig10_df.groupby("場名")[["単勝配当", "複勝配当", "単勝", "複勝"]].mean().reset_index()
    fig10_gp["単勝"] = fig10_gp["単勝"] * 100
    fig10_gp["複勝"] = fig10_gp["複勝"] * 100
    fig10_x_name = fig10_gp["場名"].tolist()
    fig10_line_y_list = [fig10_gp["単勝配当"].tolist(), fig10_gp["複勝配当"].tolist()]
    fig10_line_y_name = ["単勝回収率", "複勝回収率"]
    fig10_bar_y_list = [fig10_gp["単勝"].tolist(), fig10_gp["複勝"].tolist()]
    fig10_bar_y_name = ["単勝的中率", "複勝的中率"]
    fig10 = gp.multiple_line_and_bar_chart(fig10_x_name, fig10_line_y_list, fig10_line_y_name, fig10_bar_y_list,
                                           fig10_bar_y_name)
    return fig10

def cp_multiple_line_and_bar_chart_place_bet_return(bet_df):
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
    return fig11



def cp_parallel_categories_diagram_umaren_1(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["UMAREN_ARE"] >= 50 and x["場名"] in ('園田','笠松','高知','水沢','盛岡','川崎','船橋','大井','門別') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["umaren_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 3000 and x["払戻"] <= 9000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["馬券評価順位"] <= 2 and x["得点"] >= 51 and x["JIKU_RATE"] >= 47 and x["WIN_RATE"] >= 57 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["馬券評価順位"] <= 2 and x["得点"] >= 51 and x["JIKU_RATE"] >= 47 and x["WIN_RATE"] >= 57 and x["確定着順"] in (1,2) else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 40 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 40 and x["確定着順"] in (1,2) else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df = group_df[["場名", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]

    level0_dim = go.parcats.Dimension(values=group_df["場名"], categoryorder='category ascending', label="場名")
    level1_dim = go.parcats.Dimension(values=group_df["馬１対象"], categoryorder='category ascending', label="馬１対象")
    level2_dim = go.parcats.Dimension(values=group_df["馬１的中"], categoryorder='category ascending', label="馬１的中")
    level3_dim = go.parcats.Dimension(values=group_df["馬２対象"], categoryorder='category ascending', label="馬２対象")
    level4_dim = go.parcats.Dimension(values=group_df["馬２的中"], categoryorder='category ascending', label="馬２的中")
    level5_dim = go.parcats.Dimension(values=group_df["的中フラグ"], categoryorder='category ascending', label="的中フラグ")
    level6_dim = go.parcats.Dimension(values=group_df["払戻フラグ"], categoryorder='category ascending', label="払戻フラグ")

    fig = go.Figure(data=[go.Parcats(dimensions=[level0_dim, level1_dim, level2_dim, level3_dim, level4_dim, level5_dim, level6_dim],
                                     hoverinfo='count',
                                     arrangement='freeform')])
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig


def cp_stacked_funnel_plot_umaren_1(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["UMAREN_ARE"] >= 50 and x["場名"] in ('園田','笠松','高知','水沢','盛岡','川崎','船橋','大井','門別') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["umaren_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 3000 and x["払戻"] <= 9000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["馬券評価順位"] <= 2 and x["得点"] >= 51 and x["JIKU_RATE"] >= 47 and x["WIN_RATE"] >= 57 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["馬券評価順位"] <= 2 and x["得点"] >= 51 and x["JIKU_RATE"] >= 47 and x["WIN_RATE"] >= 57 and x["確定着順"] in (1,2) else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 40 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 40 and x["確定着順"] in (1,2) else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df.loc[:, "総レース数"] = True
    group_df = group_df[["場名", "総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]
    basho_list = group_df["場名"].drop_duplicates().tolist()

    fig = go.Figure()
    for basho in basho_list:
        fig.add_trace(go.Funnel(
            name=basho,
            y=["総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"],
            text=[basho + "UMAREN_ARE >= 50", "馬券評価順位 <= 2 and 得点 >= 51 and JIKU_RATE >= 47 and WIN_RATE >= 57", "確定着順 in (1,2)", "得点 >= 40", "確定着順 in (1,2)", "的中", "払戻 >= 3000 and 払戻 <= 9000"],
            x=group_df.query(f"場名=='{basho}'").drop("場名", axis=1).sum().tolist(),
            textinfo="value+percent initial"
        ))
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig


def cp_basic_funnel_plot_umaren_1(race_df, raceuma_df, haraimodoshi_dict):
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
    return fig12



def cp_parallel_categories_diagram_umaren_2(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["UMAREN_ARE"] < 50 and x["場名"] in ('園田','笠松','高知','佐賀','水沢','盛岡','川崎','名古屋','門別') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["umaren_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 2000 and x["払戻"] <= 5000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["馬券評価順位"] <= 2 and x["得点"] >= 53 and x["予想人気"] <= 5 and x["デフォルト得点"] >= 51 and x["JIKU_RATE"] >= 54 and x["JIKU_RANK"] <= 3 and x["WIN_RATE"] >= 57 and x["WIN_RANK"] <= 2 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["馬券評価順位"] <= 2 and x["得点"] >= 53 and x["予想人気"] <= 5 and x["デフォルト得点"] >= 51 and x["JIKU_RATE"] >= 54 and x["JIKU_RANK"] <= 3 and x["WIN_RATE"] >= 57 and x["WIN_RANK"] <= 2 and x["確定着順"] in (1,2) else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 and x["JIKU_RANK"] <= 9 and x["予想人気"] >= 4 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 and x["JIKU_RANK"] <= 9 and x["予想人気"] >= 4 and x["確定着順"] in (1,2) else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df = group_df[["場名", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]

    level0_dim = go.parcats.Dimension(values=group_df["場名"], categoryorder='category ascending', label="場名")
    level1_dim = go.parcats.Dimension(values=group_df["馬１対象"], categoryorder='category ascending', label="馬１対象")
    level2_dim = go.parcats.Dimension(values=group_df["馬１的中"], categoryorder='category ascending', label="馬１的中")
    level3_dim = go.parcats.Dimension(values=group_df["馬２対象"], categoryorder='category ascending', label="馬２対象")
    level4_dim = go.parcats.Dimension(values=group_df["馬２的中"], categoryorder='category ascending', label="馬２的中")
    level5_dim = go.parcats.Dimension(values=group_df["的中フラグ"], categoryorder='category ascending', label="的中フラグ")
    level6_dim = go.parcats.Dimension(values=group_df["払戻フラグ"], categoryorder='category ascending', label="払戻フラグ")

    fig = go.Figure(data=[go.Parcats(dimensions=[level0_dim, level1_dim, level2_dim, level3_dim, level4_dim, level5_dim, level6_dim],
                                     hoverinfo='count',
                                     arrangement='freeform')])
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig


def cp_stacked_funnel_plot_umaren_2(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["UMAREN_ARE"] < 50 and x["場名"] in ('園田','笠松','高知','佐賀','水沢','盛岡','川崎','名古屋','門別') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["umaren_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 2000 and x["払戻"] <= 5000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["馬券評価順位"] <= 2 and x["得点"] >= 53 and x["予想人気"] <= 5 and x["デフォルト得点"] >= 51 and x["JIKU_RATE"] >= 54 and x["JIKU_RANK"] <= 3 and x["WIN_RATE"] >= 57 and x["WIN_RANK"] <= 2 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["馬券評価順位"] <= 2 and x["得点"] >= 53 and x["予想人気"] <= 5 and x["デフォルト得点"] >= 51 and x["JIKU_RATE"] >= 54 and x["JIKU_RANK"] <= 3 and x["WIN_RATE"] >= 57 and x["WIN_RANK"] <= 2 and x["確定着順"] in (1,2) else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 and x["JIKU_RANK"] <= 9 and x["予想人気"] >= 4 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 and x["JIKU_RANK"] <= 9 and x["予想人気"] >= 4 and x["確定着順"] in (1,2) else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df.loc[:, "総レース数"] = True
    group_df = group_df[["場名", "総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]
    basho_list = group_df["場名"].drop_duplicates().tolist()

    fig = go.Figure()
    for basho in basho_list:
        fig.add_trace(go.Funnel(
            name=basho,
            y=["総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"],
            text=[basho + "UMAREN_ARE < 50", "馬券評価順位 <= 2 and 得点 >= 53 and 予想人気 <= 5 and デフォルト得点 >= 51 and JIKU_RATE >= 54 and JIKU_RANK <= 3 and WIN_RATE >= 57 and WIN_RANK <= 2", "確定着順 in (1,2)",
                  "得点 >= 43 and 馬券評価順位 <= 8 and JIKU_RANK <= 9 and 予想人気 >= 4", "確定着順 in (1,2)", "的中", "払戻 >= 2000 and 払戻 <= 5000"],
            x=group_df.query(f"場名=='{basho}'").drop("場名", axis=1).sum().tolist(),
            textinfo="value+percent initial"
        ))
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig


def cp_basic_funnel_plot_umaren_2(race_df, raceuma_df, haraimodoshi_dict):
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
    return fig13


def cp_parallel_categories_diagram_umatan_1(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["場名"] in ('園田','笠松','金沢','高知','水沢','川崎','船橋','名古屋','門別') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["umatan_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 5000 and x["払戻"] <= 14000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 48 and x["馬券評価順位"] <= 5 and x["JIKU_RATE"] >= 50 and x["WIN_RATE"] >= 45 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 48 and x["馬券評価順位"] <= 5 and x["JIKU_RATE"] >= 50 and x["WIN_RATE"] >= 45 and x["確定着順"] == 1 else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 6 and x["デフォルト得点"] >= 45 and x["JIKU_RATE"] >= 42 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 6 and x["デフォルト得点"] >= 45 and x["JIKU_RATE"] >= 42 and x["確定着順"] == 2 else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df = group_df[["場名", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]

    level0_dim = go.parcats.Dimension(values=group_df["場名"], categoryorder='category ascending', label="場名")
    level1_dim = go.parcats.Dimension(values=group_df["馬１対象"], categoryorder='category ascending', label="馬１対象")
    level2_dim = go.parcats.Dimension(values=group_df["馬１的中"], categoryorder='category ascending', label="馬１的中")
    level3_dim = go.parcats.Dimension(values=group_df["馬２対象"], categoryorder='category ascending', label="馬２対象")
    level4_dim = go.parcats.Dimension(values=group_df["馬２的中"], categoryorder='category ascending', label="馬２的中")
    level5_dim = go.parcats.Dimension(values=group_df["的中フラグ"], categoryorder='category ascending', label="的中フラグ")
    level6_dim = go.parcats.Dimension(values=group_df["払戻フラグ"], categoryorder='category ascending', label="払戻フラグ")

    fig = go.Figure(data=[go.Parcats(dimensions=[level0_dim, level1_dim, level2_dim, level3_dim, level4_dim, level5_dim, level6_dim],
                                     hoverinfo='count',
                                     arrangement='freeform')])
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig


def cp_stacked_funnel_plot_umatan_1(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["場名"] in ('園田','笠松','金沢','高知','水沢','川崎','船橋','名古屋','門別') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["umatan_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 5000 and x["払戻"] <= 14000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 48 and x["馬券評価順位"] <= 5 and x["JIKU_RATE"] >= 50 and x["WIN_RATE"] >= 45 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 48 and x["馬券評価順位"] <= 5 and x["JIKU_RATE"] >= 50 and x["WIN_RATE"] >= 45 and x["確定着順"] == 1 else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 6 and x["デフォルト得点"] >= 45 and x["JIKU_RATE"] >= 42 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 6 and x["デフォルト得点"] >= 45 and x["JIKU_RATE"] >= 42 and x["確定着順"] == 2 else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df.loc[:, "総レース数"] = True
    group_df = group_df[["場名", "総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]
    basho_list = group_df["場名"].drop_duplicates().tolist()

    fig = go.Figure()
    for basho in basho_list:
        fig.add_trace(go.Funnel(
            name=basho,
            y=["総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"],
            text=[basho, "得点 >= 48 and 馬券評価順位 <= 5 and JIKU_RATE >= 50 and WIN_RATE >= 45", "確定着順 == 1",
                  "得点 >= 43 and 馬券評価順位 <= 6 and デフォルト得点 >= 45 and JIKU_RATE >= 42", "確定着順 == 2", "的中", "払戻 >= 5000 and 払戻 <= 14000"],
            x=group_df.query(f"場名=='{basho}'").drop("場名", axis=1).sum().tolist(),
            textinfo="value+percent initial"
        ))
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig

def cp_basic_funnel_plot_umatan_1(race_df, raceuma_df, haraimodoshi_dict):
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
    return fig14


def cp_parallel_categories_diagram_umatan_2(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["場名"] in ('浦和','園田','笠松','高知','佐賀','水沢','盛岡','川崎','船橋','大井','門別') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["umatan_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 2000 and x["払戻"] <= 6000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 54 and x["馬券評価順位"] == 1 and x["デフォルト得点"] >= 53 and x["JIKU_RATE"] >= 55 and x["WIN_RANK"] <= 2 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 54 and x["馬券評価順位"] == 1 and x["デフォルト得点"] >= 53 and x["JIKU_RATE"] >= 55 and x["WIN_RANK"] <= 2 and x["確定着順"] == 1 else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 and x["確定着順"] == 2 else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df = group_df[["場名", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]

    level0_dim = go.parcats.Dimension(values=group_df["場名"], categoryorder='category ascending', label="場名")
    level1_dim = go.parcats.Dimension(values=group_df["馬１対象"], categoryorder='category ascending', label="馬１対象")
    level2_dim = go.parcats.Dimension(values=group_df["馬１的中"], categoryorder='category ascending', label="馬１的中")
    level3_dim = go.parcats.Dimension(values=group_df["馬２対象"], categoryorder='category ascending', label="馬２対象")
    level4_dim = go.parcats.Dimension(values=group_df["馬２的中"], categoryorder='category ascending', label="馬２的中")
    level5_dim = go.parcats.Dimension(values=group_df["的中フラグ"], categoryorder='category ascending', label="的中フラグ")
    level6_dim = go.parcats.Dimension(values=group_df["払戻フラグ"], categoryorder='category ascending', label="払戻フラグ")

    fig = go.Figure(data=[go.Parcats(dimensions=[level0_dim, level1_dim, level2_dim, level3_dim, level4_dim, level5_dim, level6_dim],
                                     hoverinfo='count',
                                     arrangement='freeform')])
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig


def cp_stacked_funnel_plot_umatan_2(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["場名"] in ('浦和','園田','笠松','高知','佐賀','水沢','盛岡','川崎','船橋','大井','門別') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["umatan_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 2000 and x["払戻"] <= 6000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 54 and x["馬券評価順位"] == 1 and x["デフォルト得点"] >= 53 and x["JIKU_RATE"] >= 55 and x["WIN_RANK"] <= 2 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 54 and x["馬券評価順位"] == 1 and x["デフォルト得点"] >= 53 and x["JIKU_RATE"] >= 55 and x["WIN_RANK"] <= 2 and x["確定着順"] == 1 else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 and x["確定着順"] == 2 else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df.loc[:, "総レース数"] = True
    group_df = group_df[["場名", "総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]
    basho_list = group_df["場名"].drop_duplicates().tolist()

    fig = go.Figure()
    for basho in basho_list:
        fig.add_trace(go.Funnel(
            name=basho,
            y=["総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"],
            text=[basho, "得点 >= 54 and 馬券評価順位 == 1 and デフォルト得点 >= 53 and JIKU_RATE >= 55 and WIN_RANK <= 2", "確定着順 == 1",
                  "得点 >= 43 and 馬券評価順位 <= 8" ,"確定着順 == 2", "的中", "払戻 >= 2000 and 払戻 <= 6000"],
            x=group_df.query(f"場名=='{basho}'").drop("場名", axis=1).sum().tolist(),
            textinfo="value+percent initial"
        ))
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig

def cp_basic_funnel_plot_umatan_2(race_df, raceuma_df, haraimodoshi_dict):
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
    return fig15



def cp_parallel_categories_diagram_umatan_3(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["場名"] in ('浦和','園田','笠松','高知','水沢','盛岡','川崎','大井') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["umatan_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 9000 and x["払戻"] <= 20000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 and x["WIN_RATE"] >= 47 and x["ANA_RANK"] <= 7 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 and x["WIN_RATE"] >= 47 and x["ANA_RANK"] <= 7 and x["確定着順"] == 1 else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 51 and x["JIKU_RANK"] <= 4 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 51 and x["JIKU_RANK"] <= 4 and x["確定着順"] == 2 else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df = group_df[["場名", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]

    level0_dim = go.parcats.Dimension(values=group_df["場名"], categoryorder='category ascending', label="場名")
    level1_dim = go.parcats.Dimension(values=group_df["馬１対象"], categoryorder='category ascending', label="馬１対象")
    level2_dim = go.parcats.Dimension(values=group_df["馬１的中"], categoryorder='category ascending', label="馬１的中")
    level3_dim = go.parcats.Dimension(values=group_df["馬２対象"], categoryorder='category ascending', label="馬２対象")
    level4_dim = go.parcats.Dimension(values=group_df["馬２的中"], categoryorder='category ascending', label="馬２的中")
    level5_dim = go.parcats.Dimension(values=group_df["的中フラグ"], categoryorder='category ascending', label="的中フラグ")
    level6_dim = go.parcats.Dimension(values=group_df["払戻フラグ"], categoryorder='category ascending', label="払戻フラグ")

    fig = go.Figure(data=[go.Parcats(dimensions=[level0_dim, level1_dim, level2_dim, level3_dim, level4_dim, level5_dim, level6_dim],
                                     hoverinfo='count',
                                     arrangement='freeform')])
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig


def cp_stacked_funnel_plot_umatan_3(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["場名"] in ('浦和','園田','笠松','高知','水沢','盛岡','川崎','大井') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["umatan_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 9000 and x["払戻"] <= 20000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 and x["WIN_RATE"] >= 47 and x["ANA_RANK"] <= 7 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 43 and x["馬券評価順位"] <= 8 and x["WIN_RATE"] >= 47 and x["ANA_RANK"] <= 7 and x["確定着順"] == 1 else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 51 and x["JIKU_RANK"] <= 4 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 51 and x["JIKU_RANK"] <= 4 and x["確定着順"] == 2 else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df.loc[:, "総レース数"] = True
    group_df = group_df[["場名", "総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]
    basho_list = group_df["場名"].drop_duplicates().tolist()

    fig = go.Figure()
    for basho in basho_list:
        fig.add_trace(go.Funnel(
            name=basho,
            y=["総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"],
            text=[basho, "得点 >= 43 and 馬券評価順位 <= 8 and WIN_RATE >= 47 and ANA_RANK <= 7", "確定着順 == 1",
                  "得点 >= 51 and JIKU_RANK <= 4", "確定着順 == 2", "的中", "払戻 >= 9000 and 払戻 <= 20000"],
            x=group_df.query(f"場名=='{basho}'").drop("場名", axis=1).sum().tolist(),
            textinfo="value+percent initial"
        ))
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig

def cp_basic_funnel_plot_umatan_3(race_df, raceuma_df, haraimodoshi_dict):
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
    return fig16


def cp_parallel_categories_diagram_wide_1(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["場名"] in ('笠松','佐賀','水沢','盛岡','川崎','大井','姫路','名古屋','門別') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["wide_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 3000 and x["払戻"] <= 6000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 51 and x["デフォルト得点"] <= 55 and x["JIKU_RANK"] <= 6 and x["WIN_RANK"] <= 4 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 51 and x["デフォルト得点"] <= 55 and x["JIKU_RANK"] <= 6 and x["WIN_RANK"] <= 4 and x["確定着順"] in (1,2,3) else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 42 and x["JIKU_RANK"] <= 10 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 42 and x["JIKU_RANK"] <= 10 and x["確定着順"] in (1,2,3) else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df = group_df[["場名", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]

    level0_dim = go.parcats.Dimension(values=group_df["場名"], categoryorder='category ascending', label="場名")
    level1_dim = go.parcats.Dimension(values=group_df["馬１対象"], categoryorder='category ascending', label="馬１対象")
    level2_dim = go.parcats.Dimension(values=group_df["馬１的中"], categoryorder='category ascending', label="馬１的中")
    level3_dim = go.parcats.Dimension(values=group_df["馬２対象"], categoryorder='category ascending', label="馬２対象")
    level4_dim = go.parcats.Dimension(values=group_df["馬２的中"], categoryorder='category ascending', label="馬２的中")
    level5_dim = go.parcats.Dimension(values=group_df["的中フラグ"], categoryorder='category ascending', label="的中フラグ")
    level6_dim = go.parcats.Dimension(values=group_df["払戻フラグ"], categoryorder='category ascending', label="払戻フラグ")

    fig = go.Figure(data=[go.Parcats(dimensions=[level0_dim, level1_dim, level2_dim, level3_dim, level4_dim, level5_dim, level6_dim],
                                     hoverinfo='count',
                                     arrangement='freeform')])
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig

def cp_stacked_funnel_plot_wide_1(race_df, raceuma_df, haraimodoshi_dict):
    # 馬連的中1
    race_df.loc[:, "対象レースフラグ"] = race_df.apply(lambda x: True if x["場名"] in ('笠松','佐賀','水沢','盛岡','川崎','大井','姫路','名古屋','門別') else False, axis=1)
    haraimodoshi_df = haraimodoshi_dict["wide_df"]
    haraimodoshi_df.loc[:, "払戻フラグ"] = haraimodoshi_df.apply(lambda x: True if x["払戻"] >= 3000 and x["払戻"] <= 6000 else False, axis=1)
    raceuma_df.loc[:, "馬１対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 51 and x["デフォルト得点"] <= 55 and x["JIKU_RANK"] <= 6 and x["WIN_RANK"] <= 4 else False, axis=1)
    raceuma_df.loc[:, "馬１的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 51 and x["デフォルト得点"] <= 55 and x["JIKU_RANK"] <= 6 and x["WIN_RANK"] <= 4 and x["確定着順"] in (1,2,3) else False, axis=1)
    raceuma_df.loc[:, "馬２対象"] = raceuma_df.apply(lambda x: True if x["得点"] >= 42 and x["JIKU_RANK"] <= 10 else False, axis=1)
    raceuma_df.loc[:, "馬２的中"] = raceuma_df.apply(lambda x: True if x["得点"] >= 42 and x["JIKU_RANK"] <= 10 and x["確定着順"] in (1,2,3) else False, axis=1)
    race_df = pd.merge(race_df, haraimodoshi_df, on="競走コード")
    base_df = pd.merge(race_df[["競走コード", "対象レースフラグ", "払戻フラグ"]], raceuma_df[["競走コード", "馬番", "馬１対象", "馬１的中", "馬２対象", "馬２的中"]], on="競走コード")
    base_df = base_df.query("対象レースフラグ == True")
    base_df.loc[:, "馬２対象"] = base_df.apply(lambda x: True if x["馬２対象"] and not x["馬１対象"] else False, axis=1)
    base_df.loc[:, "馬２的中"] = base_df.apply(lambda x: True if x["馬２的中"] and not x["馬１的中"] else False, axis=1)
    group_df = base_df.groupby("競走コード")[["対象レースフラグ", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "払戻フラグ"]].any().reset_index()
    group_df.loc[:, "的中フラグ"] = group_df.apply(lambda x: True if x["馬１的中"] and x["馬２的中"] else False, axis=1)
    group_df = pd.merge(group_df, race_df[["競走コード", "場名"]], on="競走コード")
    group_df.loc[:, "総レース数"] = True
    group_df = group_df[["場名", "総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"]]
    basho_list = group_df["場名"].drop_duplicates().tolist()

    fig = go.Figure()
    for basho in basho_list:
        fig.add_trace(go.Funnel(
            name=basho,
            y=["総レース数", "馬１対象", "馬１的中", "馬２対象", "馬２的中", "的中フラグ", "払戻フラグ"],
            text=[basho, "得点 >= 51 and デフォルト得点 <= 55 and JIKU_RANK <= 6 and WIN_RANK <= 4", "確定着順 in (1,2,3)",
                  "得点 >= 42 and JIKU_RANK <= 10", "確定着順 in (1,2,3)", "的中", "払戻 >= 3000 and 払戻 <= 6000"],
            x=group_df.query(f"場名=='{basho}'").drop("場名", axis=1).sum().tolist(),
            textinfo="value+percent initial"
        ))
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    return fig


def cp_basic_funnel_plot_wide_1(race_df, raceuma_df, haraimodoshi_dict):
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
    return fig17

def cp_choosing_the_algorithm_umaren_dist(race_df, haraimodoshi_dict):
    # 馬連配当分布
    fig18_umaren_df = haraimodoshi_dict["umaren_df"]
    fig18_df = pd.merge(fig18_umaren_df, race_df[["競走コード", "月日", "年月"]], on ="競走コード")
    fig18_df.loc[:, "月日"] = fig18_df["月日"].apply(lambda x: x.strftime("%y/%m/%d"))
    fig18_df = fig18_df.rename(columns={"月日": "label", "払戻": "value"})
    fig18_df["color"] = "馬連"
    fig18 = gp.choosing_the_algorithm(fig18_df, "label", "value", "color", 7000)
    return fig18

def cp_choosing_the_algorithm_umatan_dist(race_df, haraimodoshi_dict):
    # 馬単配当分布
    fig19_umatan_df = haraimodoshi_dict["umatan_df"]
    fig19_df = pd.merge(fig19_umatan_df, race_df[["競走コード", "月日", "年月"]], on ="競走コード")
    fig19_df.loc[:, "月日"] = fig19_df["月日"].apply(lambda x: x.strftime("%y/%m/%d"))
    fig19_df = fig19_df.rename(columns={"月日": "label", "払戻": "value"})
    fig19_df["color"] = "馬単"
    fig19 = gp.choosing_the_algorithm(fig19_df, "label", "value", "color", 15000)
    return fig19

def cp_choosing_the_algorithm_wide_dist(race_df, haraimodoshi_dict):
    # ワイド配当分布
    fig20_wide_df = haraimodoshi_dict["wide_df"]
    fig20_df = pd.merge(fig20_wide_df, race_df[["競走コード", "月日", "年月"]], on="競走コード")
    fig20_df.loc[:, "月日"] = fig20_df["月日"].apply(lambda x: x.strftime("%y/%m/%d"))
    fig20_df = fig20_df.rename(columns={"月日": "label", "払戻": "value"})
    fig20_df["color"] = "ワイド"
    fig20 = gp.choosing_the_algorithm(fig20_df, "label", "value", "color", 3000)
    return fig20

def cp_choosing_the_algorithm_sanrenpuku_dist(race_df, haraimodoshi_dict):
    # 三連複配当分布
    fig21_sanrenpuku_df = haraimodoshi_dict["sanrenpuku_df"]
    fig21_df = pd.merge(fig21_sanrenpuku_df, race_df[["競走コード", "月日", "年月"]], on="競走コード")
    fig21_df.loc[:, "月日"] = fig21_df["月日"].apply(lambda x: x.strftime("%y/%m/%d"))
    fig21_df = fig21_df.rename(columns={"月日": "label", "払戻": "value"})
    fig21_df["color"] = "三連複"
    fig21 = gp.choosing_the_algorithm(fig21_df, "label", "value", "color", 15000)
    return fig21

def cp_add_steps_threshold_anda_delta_tansho(daily_summary_bet_df):
    # 単勝
    tansho_bet_df = daily_summary_bet_df.query('式別名 == "単勝　"').copy()
    prev_tansho_bet_df = tansho_bet_df.drop(tansho_bet_df.tail(1).index)
    fig1_value = cd.calc_return_rate(tansho_bet_df)
    fig1_reference = cd.calc_return_rate(prev_tansho_bet_df)
    fig1 = gp.add_steps_threshold_anda_delta(fig1_value, fig1_reference)
    return fig1

def cp_add_steps_threshold_anda_delta_fukusho(daily_summary_bet_df):
    # 複勝
    fukusho_bet_df = daily_summary_bet_df.query('式別名 == "複勝　"').copy()
    prev_fukusho_bet_df = fukusho_bet_df.drop(fukusho_bet_df.tail(1).index)
    fig2_value = cd.calc_return_rate(fukusho_bet_df)
    fig2_reference = cd.calc_return_rate(prev_fukusho_bet_df)
    fig2 = gp.add_steps_threshold_anda_delta(fig2_value, fig2_reference)
    return fig2

def cp_add_steps_threshold_anda_delta_umaren(daily_summary_bet_df):
    # 馬連
    umaren_bet_df = daily_summary_bet_df.query('式別名 == "馬連　"').copy()
    prev_umaren_bet_df = umaren_bet_df.drop(umaren_bet_df.tail(1).index)
    fig3_value = cd.calc_return_rate(umaren_bet_df)
    fig3_reference = cd.calc_return_rate(prev_umaren_bet_df)
    fig3 = gp.add_steps_threshold_anda_delta(fig3_value, fig3_reference)
    return fig3

def cp_add_steps_threshold_anda_delta_umatan(daily_summary_bet_df):
    # 馬単
    umatan_bet_df = daily_summary_bet_df.query('式別名 == "馬単　"').copy()
    prev_umatan_bet_df = umatan_bet_df.drop(umatan_bet_df.tail(1).index)
    fig4_value = cd.calc_return_rate(umatan_bet_df)
    fig4_reference = cd.calc_return_rate(prev_umatan_bet_df)
    fig4 = gp.add_steps_threshold_anda_delta(fig4_value, fig4_reference)
    return fig4

def cp_add_steps_threshold_anda_delta_wide(daily_summary_bet_df):
    # ワイド
    wide_bet_df = daily_summary_bet_df.query('式別名 == "ワイド"').copy()
    prev_wide_bet_df = wide_bet_df.drop(wide_bet_df.tail(1).index)
    fig5_value = cd.calc_return_rate(wide_bet_df)
    fig5_reference = cd.calc_return_rate(prev_wide_bet_df)
    fig5 = gp.add_steps_threshold_anda_delta(fig5_value, fig5_reference)
    return fig5

def cp_add_steps_threshold_anda_delta_sanrenpuku(daily_summary_bet_df):
    # 三連複
    sanrenpuku_bet_df = daily_summary_bet_df.query('式別名 == "三連複"').copy()
    prev_sanrenpuku_bet_df = sanrenpuku_bet_df.drop(sanrenpuku_bet_df.tail(1).index)
    fig6_value = cd.calc_return_rate(sanrenpuku_bet_df)
    fig6_reference = cd.calc_return_rate(prev_sanrenpuku_bet_df)
    fig6 = gp.add_steps_threshold_anda_delta(fig6_value, fig6_reference)
    return fig6

def cp_label_lines_with_annotations_bet_return_balance(bet_df):
    # 月別券種別回収率推移
    weekly_summary_bet_df = cd.get_weekly_summary_bet_df(bet_df)
    fig7_multi_df = weekly_summary_bet_df.rename(columns={"合計": "Volume", "回収率": "Value"})
    fig7 = gp.label_lines_with_annotations(fig7_multi_df)
    return fig7

def cp_visualizing_the_distribution_haraimodoshi_dist(haraimodoshi_dict):
    # 券種別配当分布
    tansho_df = haraimodoshi_dict["tansho_df"][["払戻"]]
    tansho_df["Label"] = "単勝"
    fukusho_df = haraimodoshi_dict["fukusho_df"][["払戻"]]
    fukusho_df["Label"] = "複勝"
    umaren_df = haraimodoshi_dict["umaren_df"][["払戻"]]
    umaren_df["Label"] = "馬連"
    umatan_df = haraimodoshi_dict["umatan_df"][["払戻"]]
    umatan_df["Label"] = "馬単"
    wide_df = haraimodoshi_dict["wide_df"][["払戻"]]
    wide_df["Label"] = "ワイド"
    sanrenpuku_df = haraimodoshi_dict["sanrenpuku_df"][["払戻"]]
    sanrenpuku_df["Label"] = "三連複"
    fig8_df = pd.concat([tansho_df, fukusho_df, umaren_df, umatan_df, wide_df, sanrenpuku_df]).rename(columns={"払戻": "Value"})
    fig8 = gp.visualizing_the_distribution(fig8_df)
    return fig8

def cp_bar_chart_with_line_plot_place_bet_return(bet_df):
    # 場所別回収的中率
    fig9_df = cd.get_place_bet_df(bet_df)
    fig9_df = fig9_df.groupby("場名")[["結果", "金額", "レース", "的中"]].sum().reset_index()
    fig9_df.loc[:, "回収率"] = fig9_df.apply(lambda x: (x["結果"] / x["金額"]) * 100, axis=1)
    fig9_df.loc[:, "的中率"] = fig9_df.apply(lambda x: (x["的中"] / x["レース"]) * 100, axis=1)
    fig9_x = fig9_df["場名"].tolist()
    fig9_y_value1 = fig9_df["的中率"].tolist()
    fig9_y_value2 = fig9_df["回収率"].tolist()
    fig9_y_title1 = "的中率"
    fig9_y_title2 = "回収率"
    fig9 = gp.bar_chart_with_line_plot(fig9_x, fig9_y_value1, fig9_y_value2 , fig9_y_title1, fig9_y_title2)
    return fig9

def cp_pie_chart_tansho_dist(haraimodoshi_dict):
    # 単勝配当分布
    fig10_sr = cd.calc_cut_sr(haraimodoshi_dict["tansho_df"]["払戻"], [100, 200, 500, 1000, 3000, 5000])
    fig10 = gp.pie_chart(fig10_sr.index.values.categories.left.values, fig10_sr.values)
    return fig10

def cp_pie_chart_fukusho_dist(haraimodoshi_dict):
    # 複勝配当分布
    fig11_sr = cd.calc_cut_sr(haraimodoshi_dict["fukusho_df"]["払戻"], [100, 150, 200, 300, 500, 1000])
    fig11 = gp.pie_chart(fig11_sr.index.values.categories.left.values, fig11_sr.values)
    return fig11

def cp_pie_chart_umaren_dist(haraimodoshi_dict):
    # 馬連配当分布
    fig12_sr = cd.calc_cut_sr(haraimodoshi_dict["umaren_df"]["払戻"], [100, 300, 500, 1000, 3000, 5000, 10000])
    fig12 = gp.pie_chart(fig12_sr.index.values.categories.left.values, fig12_sr.values)
    return fig12

def cp_pie_chart_umatan_dist(haraimodoshi_dict):
    # 馬単配当分布
    fig13_sr = cd.calc_cut_sr(haraimodoshi_dict["umatan_df"]["払戻"], [100, 500, 1000, 3000, 5000, 10000, 20000])
    fig13 = gp.pie_chart(fig13_sr.index.values.categories.left.values, fig13_sr.values)
    return fig13

def cp_pie_chart_wide_dist(haraimodoshi_dict):
    # ワイド配当分布
    fig14_sr = cd.calc_cut_sr(haraimodoshi_dict["wide_df"]["払戻"], [100, 200, 300, 500, 1000, 2000, 3000])
    fig14 = gp.pie_chart(fig14_sr.index.values.categories.left.values, fig14_sr.values)
    return fig14

def cp_pie_chart_sanrenpuku_dist(haraimodoshi_dict):
    # 三連複配当分布
    fig15_sr = cd.calc_cut_sr(haraimodoshi_dict["sanrenpuku_df"]["払戻"], [100, 500, 1000, 3000, 5000, 10000, 20000])
    fig15 = gp.pie_chart(fig15_sr.index.values.categories.left.values, fig15_sr.values)
    return fig15

def cp_choosing_the_algorithm_haraimodoshi_dist(haraimodoshi_dict):
    # 券種別配当分布比較
    fig16_tansho_df = haraimodoshi_dict["tansho_df"]
    fig16_tansho_df["Label"] = "単勝"
    fig16_tansho_df_recent = fig16_tansho_df.tail(200)
    fig16_fukusho_df = haraimodoshi_dict["fukusho_df"]
    fig16_fukusho_df["Label"] = "複勝"
    fig16_fukusho_df_recent = fig16_fukusho_df.tail(200)
    fig16_umaren_df = haraimodoshi_dict["umaren_df"]
    fig16_umaren_df["Label"] = "馬連"
    fig16_umaren_df_recent = fig16_umaren_df.tail(200)
    fig16_umatan_df = haraimodoshi_dict["umatan_df"]
    fig16_umatan_df["Label"] = "馬単"
    fig16_umatan_df_recent = fig16_umatan_df.tail(200)
    fig16_wide_df = haraimodoshi_dict["wide_df"]
    fig16_wide_df["Label"] = "ワイド"
    fig16_wide_df_recent = fig16_wide_df.tail(200)
    fig16_sanrenpuku_df = haraimodoshi_dict["sanrenpuku_df"]
    fig16_sanrenpuku_df["Label"] = "三連複"
    fig16_sanrenpuku_df_recent = fig16_sanrenpuku_df.tail(200)
    fig_16_all_df = pd.concat([fig16_tansho_df, fig16_fukusho_df, fig16_umaren_df, fig16_umatan_df, fig16_wide_df, fig16_sanrenpuku_df])
    fig_16_recent_df = pd.concat([fig16_tansho_df_recent, fig16_fukusho_df_recent, fig16_umaren_df_recent, fig16_umatan_df_recent, fig16_wide_df_recent, fig16_sanrenpuku_df_recent])
    fig_16_all_df["color"] = "all"
    fig_16_recent_df["color"] = "recent200"
    fig16_df = pd.concat([fig_16_all_df, fig_16_recent_df]).rename(columns={"払戻": "Value"})
    fig16_df.loc[:, "Value"] = fig16_df["Value"].apply(lambda x: np.log(x))
    fig16_x = "Label"
    fig16_y = "Value"
    fig16_color = "color"
    fig16 = gp.choosing_the_algorithm(fig16_df, fig16_x, fig16_y, fig16_color, 15)
    return fig16

def cp_styled_categorical_dot_plot_haraimodoshi_median(haraimodoshi_dict):
    # 券種別配当中央値比較
    fig16_tansho_df = haraimodoshi_dict["tansho_df"]
    fig16_tansho_df["Label"] = "単勝"
    fig16_tansho_df_recent = fig16_tansho_df.tail(200)
    fig16_fukusho_df = haraimodoshi_dict["fukusho_df"]
    fig16_fukusho_df["Label"] = "複勝"
    fig16_fukusho_df_recent = fig16_fukusho_df.tail(200)
    fig16_umaren_df = haraimodoshi_dict["umaren_df"]
    fig16_umaren_df["Label"] = "馬連"
    fig16_umaren_df_recent = fig16_umaren_df.tail(200)
    fig16_umatan_df = haraimodoshi_dict["umatan_df"]
    fig16_umatan_df["Label"] = "馬単"
    fig16_umatan_df_recent = fig16_umatan_df.tail(200)
    fig16_wide_df = haraimodoshi_dict["wide_df"]
    fig16_wide_df["Label"] = "ワイド"
    fig16_wide_df_recent = fig16_wide_df.tail(200)
    fig16_sanrenpuku_df = haraimodoshi_dict["sanrenpuku_df"]
    fig16_sanrenpuku_df["Label"] = "三連複"
    fig16_sanrenpuku_df_recent = fig16_sanrenpuku_df.tail(200)
    fig_16_all_df = pd.concat([fig16_tansho_df, fig16_fukusho_df, fig16_umaren_df, fig16_umatan_df, fig16_wide_df, fig16_sanrenpuku_df])
    fig_16_recent_df = pd.concat([fig16_tansho_df_recent, fig16_fukusho_df_recent, fig16_umaren_df_recent, fig16_umatan_df_recent, fig16_wide_df_recent, fig16_sanrenpuku_df_recent])
    fig_16_all_df["color"] = "all"
    fig_16_recent_df["color"] = "recent200"
    fig16_df = pd.concat([fig_16_all_df, fig_16_recent_df]).rename(columns={"払戻": "Value"})
    fig17_df = fig16_df.groupby(["Label", "color"])["Value"].median().reset_index()
    fig17_y = fig17_df["Label"].drop_duplicates().tolist()
    fig17_x1 = fig17_df[fig17_df["color"] == "all"]["Value"].tolist()
    fig17_x2 = fig17_df[fig17_df["color"] == "recent200"]["Value"].tolist()
    fig17_name1 = "all"
    fig17_name2 = "recent200"
    fig17 = gp.styled_categorical_dot_plot(fig17_y, fig17_x1, fig17_x2, fig17_name1, fig17_name2)
    return fig17

def cp_controlling_text_fontsize_with_uniformtext_win_basis(shap_df_win):
    # 勝ち根拠
    fig1_df = pd.concat([shap_df_win.head(10), shap_df_win.tail(10)])
    fig1_df = fig1_df.sort_values("value")
    fig1 = gp.controlling_text_fontsize_with_uniformtext(fig1_df)
    return fig1

def cp_controlling_text_fontsize_with_uniformtext_jiku_basis(shap_df_jiku):
    # 軸根拠
    fig2_df = pd.concat([shap_df_jiku.head(10), shap_df_jiku.tail(10)])
    fig2_df = fig2_df.sort_values("value")
    fig2 = gp.controlling_text_fontsize_with_uniformtext(fig2_df)
    return fig2

def cp_controlling_text_fontsize_with_uniformtext_are_basis(shap_df_are):
    # 荒れ根拠
    fig3_df = pd.concat([shap_df_are.head(10), shap_df_are.tail(10)])
    fig3_df = fig3_df.sort_values("value")
    fig3 = gp.controlling_text_fontsize_with_uniformtext(fig3_df)
    return fig3

def cp_basic_horizontal_bar_chart_score(raceuma_df):
    # 得点
    fig1_df = raceuma_df[["馬名", "デフォルト得点", "得点V3", "WIN_RATE", "JIKU_RATE", "ANA_RATE"]].set_index("馬名")
    fig1_df.loc[:, "デフォルト得点"] = fig1_df["デフォルト得点"] / 3
    fig1_df.loc[:, "得点V3"] = fig1_df["得点V3"] / 3
    fig1_df.loc[:, "WIN_RATE"] = fig1_df["WIN_RATE"] * 0.55 / 3
    fig1_df.loc[:, "JIKU_RATE"] = fig1_df["JIKU_RATE"] * 0.20 / 3
    fig1_df.loc[:, "ANA_RATE"] = fig1_df["ANA_RATE"] * 0.25 / 3
    fig1_df = fig1_df.stack().reset_index()
    fig1_df.columns = ["name", "label", "value"]
    fig1 = gp.basic_horizontal_bar_chart(fig1_df)
    return fig1

def cp_basic_dot_plot_max_score(raceuma_df):
    # 最大得点分布
    fig2_df = raceuma_df[["馬名", "SCORE", "デフォルト得点"]]
    fig2_x = fig2_df["馬名"].tolist()
    fig2_y_value1 = fig2_df["SCORE"].tolist()
    fig2_y_value2 = fig2_df["デフォルト得点"].tolist()
    fig2_y_title1 = "SCORE"
    fig2_y_title2 = "デフォルト得点"
    fig2 = gp.basic_dot_plot(fig2_x, fig2_y_value1,fig2_y_value2, fig2_y_title1, fig2_y_title2)
    return fig2

def cp_buble_chart_score(raceuma_df):
    # 得点バブル
    fig3_x_list = raceuma_df["デフォルト得点"].tolist()
    fig3_y_list = raceuma_df["SCORE"].tolist()
    fig3_z_list = raceuma_df["得点V3"].tolist()
    fig3_name_list = raceuma_df["馬名"].tolist()
    fig3_x_title = "デフォルト得点"
    fig3_y_title = "SCORE"
    fig3 = gp.buble_chart(fig3_x_list, fig3_y_list, fig3_z_list, fig3_name_list, fig3_x_title, fig3_y_title)
    return fig3

def cp_multiple_trace_rader_chart_score(raceuma_df):
    # レーダーチャート
    fig4_df = raceuma_df[["馬名", "デフォルト得点", "得点V3", "WIN_RATE", "JIKU_RATE", "ANA_RATE"]]
    fig4_categories = ["デフォルト得点", "得点V3", "WIN_RATE", "JIKU_RATE", "ANA_RATE"]
    fig4_names = fig4_df["馬名"].tolist()
    fig4_values = fig4_df[fig4_categories].values
    fig4 = gp.multiple_trace_rader_chart(fig4_categories, fig4_names, fig4_values)
    return fig4

def cp_basic_horizontal_box_plot_senko_rate(raceuma_prev_df):
    # 先行率
    fig5_df = raceuma_prev_df[["馬名", "先行率"]]
    fig5_df['先行率'] = fig5_df['先行率'].map("{:,.2f}".format)
    fig5_names = fig5_df["馬名"].drop_duplicates().tolist()
    fig5_values = fig5_df.groupby("馬名")["先行率"].apply(list).apply(lambda x: np.array(x)).values
    fig5 = gp.basic_horizontal_box_plot(fig5_names, fig5_values)
    return fig5

def cp_basic_horizontal_box_plot_time_score(raceuma_prev_df):
    # タイム指数
    fig6_df = raceuma_prev_df[["馬名", "タイム指数"]]
    fig6_df['タイム指数'] = fig6_df['タイム指数'].map("{:,.2f}".format)
    fig6_names = fig6_df["馬名"].drop_duplicates().tolist()
    fig6_values = fig6_df.groupby("馬名")["タイム指数"].apply(list).apply(lambda x: np.array(x)).values
    fig6 = gp.basic_horizontal_box_plot(fig6_names, fig6_values)
    return fig6

def cp_controlling_text_fontsize_with_uniformtext_umaren_basis(shap_df_umaren_are):
    # 馬連荒れ根拠
    fig8_df = pd.concat([shap_df_umaren_are.head(10), shap_df_umaren_are.tail(10)])
    fig8_df = fig8_df.sort_values("value")
    fig8 = gp.controlling_text_fontsize_with_uniformtext(fig8_df)
    return fig8

def cp_controlling_text_fontsize_with_uniformtext_umatan_basis(shap_df_umatan_are):
    # 馬単荒れ根拠
    fig9_df = pd.concat([shap_df_umatan_are.head(10), shap_df_umatan_are.tail(10)])
    fig9_df = fig9_df.sort_values("value")
    fig9 = gp.controlling_text_fontsize_with_uniformtext(fig9_df)
    return fig9

def cp_controlling_text_fontsize_with_uniformtext_sanrenpuku_basis(shap_df_sanrenpuku_are):
    # 三連複荒れ根拠
    fig10_df = pd.concat([shap_df_sanrenpuku_are.head(10), shap_df_sanrenpuku_are.tail(10)])
    fig10_df = fig10_df.sort_values("value")
    fig10 = gp.controlling_text_fontsize_with_uniformtext(fig10_df)
    return fig10

def cp_basic_dot_plot_time_record(raceuma_df):
    # タイム指数、予想タイム指数
    fig6_df = raceuma_df[["馬名", "タイム指数", "予想タイム指数"]]
    fig6_x = fig6_df["馬名"].to_list()
    fig6_y_value1 = fig6_df["タイム指数"].to_list()
    fig6_y_value2 = fig6_df["予想タイム指数"].to_list()
    fig6_y_title1 = "タイム指数"
    fig6_y_title2 = "予想タイム指数"
    fig6 = gp.basic_dot_plot(fig6_x, fig6_y_value1, fig6_y_value2, fig6_y_title1, fig6_y_title2)
    return fig6

def cp_bar_chart_with_line_plot_time_record_tansho(raceuma_df):
    # タイム指数、単勝オッズ
    fig10_df = raceuma_df[["馬名", "タイム指数", "単勝オッズ"]]
    fig10_x = fig10_df["馬名"].to_list()
    fig10_y_value1 = fig10_df["タイム指数"].to_list()
    fig10_y_value2 = fig10_df["単勝オッズ"].apply(lambda x: np.log(x)).to_list()
    fig10_y_title1 = "タイム指数"
    fig10_y_title2 = "単勝オッズ"
    fig10 = gp.bar_chart_with_line_plot(fig10_x, fig10_y_value1, fig10_y_value2, fig10_y_title1, fig10_y_title2)
    return fig10

def cp_simple_line_rap(race_sr, height):
    # ラップ
    fig11_rap_text = race_sr["ラップタイム"]
    chunks, chunk_size = len(fig11_rap_text), 3
    rap_array = [fig11_rap_text[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
    rap_array = [i for i in rap_array if i != '000']
    if len(rap_array) != 0:
        fig11_df = pd.DataFrame({'value': rap_array, 'label': range(1, len(rap_array) + 1)})
        fig11 = gp.simple_line(fig11_df)
        fig11.update_layout(height=height, margin={'t': 0, 'b': 0, 'l': 0})
    else:
        fig11 = ""
    return fig11

def cp_pie_chart_tansho_approval_rate(raceuma_df):
    # 単勝支持率
    fig12_df = raceuma_df[["馬名", "単勝支持率", "タイム指数"]].sort_values("タイム指数", ascending=False)
    fig12_labels = fig12_df["馬名"].tolist()
    fig12_values = fig12_df["単勝支持率"].tolist()
    fig12 = gp.pie_chart(fig12_labels, fig12_values)
    return fig12


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def dbc_top_title(title):
    return \
        dbc.Col(
            html.H1(title),
            style={
                "size": "30px",
                "textAlign": "center",
            },
        )

def dbc_title(title, width):
    return \
        dbc.Col(
            html.H4(title),
            width=width,
            style={
                "height": "100%",
                "textAlign": "left",
                "padding": "10px"
            },
        )

def dbc_graph(graph_id, width, fig, title, height, bottom=15):
    if fig != "":
        fig.update_layout(height=height, margin={'t': 30, 'b': bottom, 'l': 55}, title=title)
        return \
        dbc.Col(
            dcc.Graph(
                id=graph_id,
                figure=fig,
                config={'displayModeBar': False}
            ),
            width=width,
            style={
                "height": "100%",
                "border-width": "40px"
            },
        )
    else:
        return dbc.Col(html.P("no data"), width=width)

def dbc_graph_with_click(graph_id, width, fig, selected_data):
    return \
        dbc.Col(
            dcc.Graph(
                id=graph_id,
                selectedData=selected_data,
                figure=fig,
                config={'displayModeBar': False}
            ),
            width=width,
            style={
                "height": "100%",
                "border-width": "10px"
            },
        )

def dbc_race_info_table(table_id, width, df):
    df['予想タイム指数'] = df['予想タイム指数'].map("{:,.2f}".format)
    df['先行指数'] = df['先行指数'].map("{:,.2f}".format)
    df['WIN_RATE'] = df['WIN_RATE'].map("{:,.2f}".format)
    df['JIKU_RATE'] = df['JIKU_RATE'].map("{:,.2f}".format)
    df['ANA_RATE'] = df['ANA_RATE'].map("{:,.2f}".format)
    df['SCORE'] = df['SCORE'].map("{:,.2f}".format)
    df['CK1_RATE'] = df['CK1_RATE'] / 100
    df['CK2_RATE'] = df['CK2_RATE'] / 100
    df['CK3_RATE'] = df['CK3_RATE'] / 100
    table = dash_table.DataTable(
        id = table_id,
        columns=[
            {'id': '枠番', 'name': '枠番', 'type': 'numeric'},
            {'id': '馬番', 'name': '馬番', 'type': 'numeric'},
            {'id': '予想展開', 'name': '予想展開', 'type': 'numeric'},
            {'id': '馬名', 'name': '馬名', 'type': 'text'},
            {'id': '性別コード', 'name': '性別コード', 'type': 'text'},
            {'id': '馬齢', 'name': '馬齢', 'type': 'numeric'},
            {'id': '負担重量', 'name': '負担重量', 'type': 'numeric'},
            {'id': '騎手名', 'name': '騎手名', 'type': 'text'},
            {'id': '調教師名', 'name': '調教師名', 'type': 'text'},
            {'id': '所属', 'name': '所属', 'type': 'text'},
            {'id': '馬券評価順位', 'name': '馬券評価順位', 'type': 'numeric'},
            {'id': '得点', 'name': '得点', 'type': 'numeric'},
            {'id': 'SCORE_RANK', 'name': 'SCORE_RANK', 'type': 'numeric'},
            {'id': 'SCORE', 'name': 'SCORE', 'type': 'numeric'},
            {'id': 'WIN_RANK', 'name': 'WIN_RANK', 'type': 'numeric'},
            {'id': 'WIN_RATE', 'name': 'WIN_RATE', 'type': 'numeric'},
            {'id': 'JIKU_RANK', 'name': 'JIKU_RANK', 'type': 'numeric'},
            {'id': 'JIKU_RATE', 'name': 'JIKU_RATE', 'type': 'numeric'},
            {'id': 'ANA_RANK', 'name': 'ANA_RANK', 'type': 'numeric'},
            {'id': 'ANA_RATE', 'name': 'ANA_RATE', 'type': 'numeric'},
            {'id': 'デフォルト得点', 'name': 'デフォルト得点', 'type': 'numeric'},
            {'id': '得点V3', 'name': '得点V3', 'type': 'numeric'},
            {'id': '予想タイム指数順位', 'name': '予想タイム指数順位', 'type': 'numeric'},
            {'id': '予想タイム指数', 'name': '予想タイム指数', 'type': 'numeric'},
            {'id': '先行指数', 'name': '先行指数', 'type': 'numeric'},
            {'id': 'CK1_RATE', 'name': 'CK1_RATE', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            {'id': 'CK2_RATE', 'name': 'CK2_RATE', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            {'id': 'CK3_RATE', 'name': 'CK3_RATE', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},

        ],
        data=df.to_dict("record"),
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['馬名', '騎手名', '調教師名', '所属']
        ],
        style_data_conditional=(
            [{'if': {'filter_query': '{{馬券評価順位}} = {}'.format(df['馬券評価順位'].min()),
                    'column_id': '馬券評価順位'},
                'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{WIN_RANK}} = {}'.format(df['WIN_RANK'].min()),
                     'column_id': 'WIN_RANK'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{JIKU_RANK}} = {}'.format(df['JIKU_RANK'].min()),
                     'column_id': 'JIKU_RANK'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{ANA_RANK}} = {}'.format(df['ANA_RANK'].min()),
                     'column_id': 'ANA_RANK'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{SCORE_RANK}} = {}'.format(df['SCORE_RANK'].min()),
                     'column_id': 'SCORE_RANK'},
              'backgroundColor': '#FF4136', 'color': 'white'}]
        ),
        sort_action="native",
        sort_mode="multi",
        fixed_rows={"headers": True}
    )
    return table


def dbc_haraimodoshi_table(table_id, width, df):
    list_group = []
    for idx, item in df.iterrows():
        list_group.append(html.H6([f"{item['式別']}: {item['馬番']}", dbc.Badge(f"{item['払戻']}円", color=get_return_odds_label(item['払戻']), className="ml-1")]))
    return html.Div(list_group)


def dbc_bet_table(table_id, width, df):
    list_group = []
    for idx, item in df.iterrows():
        list_group.append(html.H6([f"{item['式別名']}: {item['番号']} - {item['金額']}円", dbc.Badge(f"{item['結果']}円", color=get_return_odds_label(item['結果']), className="ml-1")]))
    return html.Div(list_group)

def get_return_odds_label(number):
    if number == 0:
        return "dark"
    elif number <= 500:
        return "light"
    elif number <= 1000:
        return "info"
    elif number <= 2000:
        return "success"
    elif number <= 5000:
        return "warning"
    elif number <= 10000:
        return "primary"
    elif number >= 10000:
        return "danger"
    else:
        return "secondary"

def dbc_race_result_table(table_id, width, df):
    df['タイム指数'] = df['タイム指数'].map("{:,.2f}".format)
    df['WIN_RATE'] = df['WIN_RATE'].map("{:,.2f}".format)
    df['JIKU_RATE'] = df['JIKU_RATE'].map("{:,.2f}".format)
    df['ANA_RATE'] = df['ANA_RATE'].map("{:,.2f}".format)
    df['SCORE'] = df['SCORE'].map("{:,.2f}".format)
    df['単勝オッズ'] = df['単勝オッズ'].map("{:,.1f}".format)
    df['複勝オッズ1'] = df['複勝オッズ1'].map("{:,.1f}".format)
    df['CK1_RATE'] = df['CK1_RATE'] / 100
    df['CK2_RATE'] = df['CK2_RATE'] / 100
    df['CK3_RATE'] = df['CK3_RATE'] / 100
    table = dash_table.DataTable(
        id = table_id,
        columns=[
            {'id': '枠番', 'name': '枠番', 'type': 'numeric'},
            {'id': '確定着順', 'name': '確定着順', 'type': 'numeric'},
            {'id': '馬番', 'name': '馬番', 'type': 'numeric'},
            {'id': '馬名表用', 'name': '馬名表用', 'type': 'text'},
            {'id': '性別コード', 'name': '性別コード', 'type': 'text'},
            {'id': '馬齢', 'name': '馬齢', 'type': 'numeric'},
            {'id': '負担重量', 'name': '負担重量', 'type': 'numeric'},
            {'id': '騎手名', 'name': '騎手名', 'type': 'text'},
            {'id': '単勝オッズ', 'name': '単勝オッズ', 'type': 'numeric'},
            {'id': '単勝人気', 'name': '単勝人気', 'type': 'numeric'},
            {'id': '複勝オッズ1', 'name': '複勝オッズ1', 'type': 'numeric'},
            {'id': 'コーナー順位1', 'name': 'コーナー順位1', 'type': 'numeric'},
            {'id': 'コーナー順位2', 'name': 'コーナー順位2', 'type': 'numeric'},
            {'id': 'コーナー順位3', 'name': 'コーナー順位3', 'type': 'numeric'},
            {'id': 'コーナー順位4', 'name': 'コーナー順位4', 'type': 'numeric'},
            {'id': '上がりタイム', 'name': '上がりタイム', 'type': 'numeric'},
            {'id': '展開コード', 'name': '展開コード', 'type': 'text'},
            {'id': '馬体重', 'name': '馬体重', 'type': 'numeric'},
            {'id': '調教師名', 'name': '調教師名', 'type': 'text'},
            {'id': '所属', 'name': '所属', 'type': 'text'},
            {'id': '馬券評価順位', 'name': '馬券評価順位', 'type': 'numeric'},
            {'id': '得点', 'name': '得点', 'type': 'numeric'},
            {'id': 'SCORE_RANK', 'name': 'SCORE_RANK', 'type': 'numeric'},
            {'id': 'SCORE', 'name': 'SCORE', 'type': 'numeric'},
            {'id': 'WIN_RANK', 'name': 'WIN_RANK', 'type': 'numeric'},
            {'id': 'WIN_RATE', 'name': 'WIN_RATE', 'type': 'numeric'},
            {'id': 'JIKU_RANK', 'name': 'JIKU_RANK', 'type': 'numeric'},
            {'id': 'JIKU_RATE', 'name': 'JIKU_RATE', 'type': 'numeric'},
            {'id': 'ANA_RANK', 'name': 'ANA_RANK', 'type': 'numeric'},
            {'id': 'ANA_RATE', 'name': 'ANA_RATE', 'type': 'numeric'},
            {'id': 'デフォルト得点', 'name': 'デフォルト得点', 'type': 'numeric'},
            {'id': '得点V3', 'name': '得点V3', 'type': 'numeric'},
            {'id': 'CK1_RATE', 'name': 'CK1_RATE', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            {'id': 'CK2_RATE', 'name': 'CK2_RATE', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            {'id': 'CK3_RATE', 'name': 'CK3_RATE', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},

        ],
        data=df.to_dict("record"),
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['馬名', '騎手名', '調教師名', '所属']
        ],
        style_data_conditional=(
            [{'if': {'filter_query': '{{馬券評価順位}} = {}'.format(df['馬券評価順位'].min()),
                    'column_id': '馬券評価順位'},
                'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{WIN_RANK}} = {}'.format(df['WIN_RANK'].min()),
                     'column_id': 'WIN_RANK'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{JIKU_RANK}} = {}'.format(df['JIKU_RANK'].min()),
                     'column_id': 'JIKU_RANK'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{ANA_RANK}} = {}'.format(df['ANA_RANK'].min()),
                     'column_id': 'ANA_RANK'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{SCORE_RANK}} = {}'.format(df['SCORE_RANK'].min()),
                     'column_id': 'SCORE_RANK'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{上がりタイム}} = {}'.format(df['上がりタイム'].min()),
                     'column_id': '上がりタイム'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{単勝人気}} = {}'.format(df['単勝人気'].min()),
                     'column_id': '単勝人気'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{CK1_RATE}} = {}'.format(df['CK1_RATE'].max()),
                     'column_id': 'CK1_RATE'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{CK2_RATE}} = {}'.format(df['CK2_RATE'].max()),
                     'column_id': 'CK2_RATE'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{CK3_RATE}} = {}'.format(df['CK3_RATE'].max()),
                     'column_id': 'CK3_RATE'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{デフォルト得点}} = {}'.format(df['デフォルト得点'].max()),
                     'column_id': 'デフォルト得点'},
              'backgroundColor': '#FF4136', 'color': 'white'}] +
            [{'if': {'filter_query': '{{得点V3}} = {}'.format(df['得点V3'].max()),
                     'column_id': '得点V3'},
              'backgroundColor': '#FF4136', 'color': 'white'}]
        ),
        sort_action="native",
        sort_mode="multi",
        fixed_rows={"headers": True}
    )
    return table

def get_kyakushitsu_label(value):
    if value == "逃げ":
        return dbc.Badge("逃げ", color="danger", className="mr-1")
    elif value == "先行":
        return dbc.Badge("先行", color="warning", className="mr-1")
    elif value == "差し":
        return dbc.Badge("差し", color="primary", className="mr-1")
    elif value == "追込":
        return dbc.Badge("追込", color="dark", className="mr-1")
    else:
        return ""


def dbc_race_info(race_sr, width):
    return \
        dbc.Col([
            html.H5([f"{race_sr['場名']} {race_sr['競走番号']}R {race_sr['距離']}m {race_sr['競走条件名称']} {race_sr['競走名略称']}",
            "馬連荒れ：", dbc.Badge(race_sr['UMAREN_ARE_RATE'], color=get_label_color(race_sr['UMAREN_ARE_RATE']), className="mr-1"),
            "馬単荒れ：", dbc.Badge(race_sr['UMATAN_ARE_RATE'], color=get_label_color(race_sr['UMATAN_ARE_RATE']), className="mr-1"),
            "三連複荒れ：", dbc.Badge(race_sr['SANRENPUKU_ARE_RATE'], color=get_label_color(race_sr['SANRENPUKU_ARE_RATE']), className="mr-1"),
                     ])],
            width=width,
            style={
                "height": "100%",
                "textAlign": "left",
                "padding": "10px"
            },
        )

def get_label_color(value):
    if value ==0:
        return "secondary"
    elif value <= 10:
        return "info"
    elif value <= 20:
        return "success"
    elif value <= 30:
        return "primary"
    elif value <= 50:
        return "warning"
    elif value >= 50:
        return "danger"
    else:
        return "light"

def dbc_race_result(race_sr, haraimodoshi_df, width):
    haraimodoshi_list = [f"{race_sr['天候コード']} {race_sr['馬場状態コード']} {race_sr['ペース']}"]
    for idx, item in haraimodoshi_df.iterrows():
        if item["式別"] == "tansho_df":
            if item["払戻"] >= 5000:   haraimodoshi_list.append(dbc.Badge("単勝50倍", color="danger", className="mr-1"))
            elif item["払戻"] >= 3000: haraimodoshi_list.append(dbc.Badge("単勝30倍", color="warning", className="mr-1"))
            elif item["払戻"] <= 200:  haraimodoshi_list.append(dbc.Badge("単勝2倍", color="dark", className="mr-1"))
        elif item["式別"] == "fukusho_df":
            if item["払戻"] >= 1000:   haraimodoshi_list.append(dbc.Badge("複勝10倍", color="danger", className="mr-1"))
        elif item["式別"] == "umaren_df":
            if item["払戻"] >= 8000:   haraimodoshi_list.append(dbc.Badge("馬連80倍", color="danger", className="mr-1"))
            elif item["払戻"] >= 5000: haraimodoshi_list.append(dbc.Badge("馬連50倍", color="warning", className="mr-1"))
            elif item["払戻"] <= 500:  haraimodoshi_list.append(dbc.Badge("馬連5倍", color="dark", className="mr-1"))
        elif item["式別"] == "umatan_df":
            if item["払戻"] >= 12000:   haraimodoshi_list.append(dbc.Badge("馬単120倍", color="danger", className="mr-1"))
            elif item["払戻"] >= 8000: haraimodoshi_list.append(dbc.Badge("馬単80倍", color="warning", className="mr-1"))
            elif item["払戻"] <= 500:  haraimodoshi_list.append(dbc.Badge("馬単5倍", color="dark", className="mr-1"))
        elif item["式別"] == "wide_df":
            if item["払戻"] >= 4000:   haraimodoshi_list.append(dbc.Badge("ワイド40倍", color="danger", className="mr-1"))
            elif item["払戻"] >= 2000: haraimodoshi_list.append(dbc.Badge("ワイド20倍", color="warning", className="mr-1"))
            elif item["払戻"] <= 200:  haraimodoshi_list.append(dbc.Badge("ワイド2倍", color="dark", className="mr-1"))
        elif item["式別"] == "sanrenpuku_df":
            if item["払戻"] >= 12000:   haraimodoshi_list.append(dbc.Badge("三連複120倍", color="danger", className="mr-1"))
            elif item["払戻"] >= 8000: haraimodoshi_list.append(dbc.Badge("三連複80倍", color="warning", className="mr-1"))
            elif item["払戻"] <= 500:  haraimodoshi_list.append(dbc.Badge("三連複5倍", color="dark", className="mr-1"))
    return \
        dbc.Col(
            html.H5(haraimodoshi_list),
            width=width,
            style={
                "height": "100%",
                "textAlign": "left",
                "padding": "10px"
            },
        )