import dash_bootstrap_components as dbc
import components.webparts as wp
import components.graph as gp

import components.calc_data as cd
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
from datetime import datetime as dt

def return_analytics():
    return dbc.Container([
            dbc.Row([
                wp.dbc_top_title("return analytics")
            ], className="h-30"),
            dbc.Row([
                dcc.DatePickerRange(
                    id='return-analytics-date-picker-range',
                    min_date_allowed=dt(2019, 1, 1),
                    initial_visible_month=dt(2020, 1, 1),
                )]),
                html.Div(id="return_analytics")
        ],
        style={"height": "90vh"},
        fluid=True
    )

def return_analytics_render(raceuma_df, bet_df, haraimodoshi_dict):
    daily_summary_bet_df = cd.get_daily_summary_bet_df(bet_df)
    tansho_bet_df = daily_summary_bet_df.query('式別名 == "単勝　"').copy()
    prev_tansho_bet_df = tansho_bet_df.drop(tansho_bet_df.tail(1).index)
    fig1_value = cd.calc_return_rate(tansho_bet_df)
    fig1_reference = cd.calc_return_rate(prev_tansho_bet_df)

    fukusho_bet_df = daily_summary_bet_df.query('式別名 == "複勝　"').copy()
    prev_fukusho_bet_df = fukusho_bet_df.drop(fukusho_bet_df.tail(1).index)
    fig2_value = cd.calc_return_rate(fukusho_bet_df)
    fig2_reference = cd.calc_return_rate(prev_fukusho_bet_df)

    umaren_bet_df = daily_summary_bet_df.query('式別名 == "馬連　"').copy()
    prev_umaren_bet_df = umaren_bet_df.drop(umaren_bet_df.tail(1).index)
    fig3_value = cd.calc_return_rate(umaren_bet_df)
    fig3_reference = cd.calc_return_rate(prev_umaren_bet_df)

    umatan_bet_df = daily_summary_bet_df.query('式別名 == "馬単　"').copy()
    prev_umatan_bet_df = umatan_bet_df.drop(umatan_bet_df.tail(1).index)
    fig4_value = cd.calc_return_rate(umatan_bet_df)
    fig4_reference = cd.calc_return_rate(prev_umatan_bet_df)

    wide_bet_df = daily_summary_bet_df.query('式別名 == "ワイド"').copy()
    prev_wide_bet_df = wide_bet_df.drop(wide_bet_df.tail(1).index)
    fig5_value = cd.calc_return_rate(wide_bet_df)
    fig5_reference = cd.calc_return_rate(prev_wide_bet_df)

    sanrenpuku_bet_df = daily_summary_bet_df.query('式別名 == "三連複"').copy()
    prev_sanrenpuku_bet_df = sanrenpuku_bet_df.drop(sanrenpuku_bet_df.tail(1).index)
    fig6_value = cd.calc_return_rate(sanrenpuku_bet_df)
    fig6_reference = cd.calc_return_rate(prev_sanrenpuku_bet_df)

    weekly_summary_bet_df = cd.get_weekly_summary_bet_df(bet_df)
    fig7_multi_df = weekly_summary_bet_df.rename(columns={"合計": "Volume", "回収率": "Value"})

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

    fig9_df = cd.get_place_bet_df(bet_df)
    fig9_df = fig9_df.groupby("場名")[["結果", "金額", "レース", "的中"]].sum().reset_index()
    fig9_df.loc[:, "回収率"] = fig9_df.apply(lambda x: (x["結果"] / x["金額"]) * 100, axis=1)
    fig9_df.loc[:, "的中率"] = fig9_df.apply(lambda x: (x["的中"] / x["レース"]) * 100, axis=1)
    fig9_x = fig9_df["場名"].tolist()
    fig9_y_value1 = fig9_df["的中率"].tolist()
    fig9_y_value2 = fig9_df["回収率"].tolist()
    fig9_y_title1 = "的中率"
    fig9_y_title2 = "回収率"


    fig10_sr = cd.calc_cut_sr(haraimodoshi_dict["tansho_df"]["払戻"], [100, 200, 500, 1000, 3000, 5000])
    fig11_sr = cd.calc_cut_sr(haraimodoshi_dict["fukusho_df"]["払戻"], [100, 150, 200, 300, 500, 1000])
    fig12_sr = cd.calc_cut_sr(haraimodoshi_dict["umaren_df"]["払戻"], [100, 300, 500, 1000, 3000, 5000, 10000])
    fig13_sr = cd.calc_cut_sr(haraimodoshi_dict["umatan_df"]["払戻"], [100, 500, 1000, 3000, 5000, 10000, 20000])
    fig14_sr = cd.calc_cut_sr(haraimodoshi_dict["wide_df"]["払戻"], [100, 200, 300, 500, 1000, 2000, 3000])
    fig15_sr = cd.calc_cut_sr(haraimodoshi_dict["sanrenpuku_df"]["払戻"], [100, 500, 1000, 3000, 5000, 10000, 20000])

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

    fig16_df.loc[:, "Value"] = fig16_df["Value"].apply(lambda x: np.log(x))
    fig16_x = "Label"
    fig16_y = "Value"
    fig16_color = "color"

    fig1 = gp.add_steps_threshold_anda_delta(fig1_value, fig1_reference)
    fig1.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig2 = gp.add_steps_threshold_anda_delta(fig2_value, fig2_reference)
    fig2.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig3 = gp.add_steps_threshold_anda_delta(fig3_value, fig3_reference)
    fig3.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig4 = gp.add_steps_threshold_anda_delta(fig4_value, fig4_reference)
    fig4.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig5 = gp.add_steps_threshold_anda_delta(fig5_value, fig5_reference)
    fig5.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig6 = gp.add_steps_threshold_anda_delta(fig6_value, fig6_reference)
    fig6.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig7 = gp.label_lines_with_annotations(fig7_multi_df)
    fig7.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})
    fig8 = gp.visualizing_the_distribution(fig8_df)
    fig8.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})
    fig9 = gp.bar_chart_with_line_plot(fig9_x, fig9_y_value1, fig9_y_value2 , fig9_y_title1, fig9_y_title2)
    fig9.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})
    fig10 = gp.pie_chart(fig10_sr.index.values.categories.left.values, fig10_sr.values)
    fig10.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})
    fig11 = gp.pie_chart(fig11_sr.index.values.categories.left.values, fig11_sr.values)
    fig11.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})
    fig12 = gp.pie_chart(fig12_sr.index.values.categories.left.values, fig12_sr.values)
    fig12.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})
    fig13 = gp.pie_chart(fig13_sr.index.values.categories.left.values, fig13_sr.values)
    fig13.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})
    fig14 = gp.pie_chart(fig14_sr.index.values.categories.left.values, fig14_sr.values)
    fig14.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})
    fig15 = gp.pie_chart(fig15_sr.index.values.categories.left.values, fig15_sr.values)
    fig15.update_layout(height=200, margin={'t': 0, 'b': 0, 'l': 0})
    fig16 = gp.choosing_the_algorithm(fig16_df, fig16_x, fig16_y, fig16_color, 15)
    fig16.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})
    fig17 = gp.styled_categorical_dot_plot(fig17_y, fig17_x1, fig17_x2, fig17_name1, fig17_name2)
    fig17.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})


    return [dbc.Row([
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
            ], className="h-50", ),]
