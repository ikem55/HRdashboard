import dash_bootstrap_components as dbc
import components.webparts as wp
import components.graph as gp
import components.calc_data as cd
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt

def toppage():
    return dbc.Container([
            dbc.Row([
                wp.dbc_top_title("Dashboard top")
            ], className="h-30"),
            dbc.Row([
                dcc.DatePickerRange(
                    id='toppage-date-picker-range',
                    min_date_allowed=dt(2019, 1, 1),
                    initial_visible_month=dt(2020, 1, 1),
                )]),
                html.Div(id="top_dashoboard")
        ],
        style={"height": "90vh"},
        fluid=True
    )

def toppage_render(raceuma_df, bet_df):
    print("toppage_render")

    daily_bet_df = cd.get_daily_bet_df(bet_df)
    daily_rank1_raceuma_df = cd.get_daily_rank1_raceuma_df(raceuma_df)
    summary_bet_df = cd.get_summary_bet_df(bet_df)
    place_bet_df = cd.get_place_bet_df(bet_df)

    prev_daily_bet_df = daily_bet_df.drop(daily_bet_df.tail(1).index)
    prev_daily_rank1_raceuma_df = daily_rank1_raceuma_df.drop(daily_bet_df.tail(1).index)
    place_bet_df = place_bet_df[place_bet_df["金額"] != 0].copy()

    fig1_value = daily_bet_df["合計"].sum()
    fig1_reference = prev_daily_bet_df["合計"].sum()
    fig2_value = daily_bet_df["結果"].sum() / daily_bet_df["金額"].sum() * 100
    fig2_reference = prev_daily_bet_df["結果"].sum() / prev_daily_bet_df["金額"].sum() * 100
    fig2_list_sr = daily_bet_df["回収率"].tolist()
    fig3_value = daily_rank1_raceuma_df["単勝配当"].mean()
    fig3_reference = prev_daily_rank1_raceuma_df["単勝配当"].mean()
    fig4_value = daily_rank1_raceuma_df["複勝配当"].mean()
    fig4_reference = prev_daily_rank1_raceuma_df["複勝配当"].mean()
    fig5_df = daily_bet_df[["日付", "合計"]]
    fig5_df.loc[:, "合計"] = fig5_df["合計"].cumsum()
    fig5_x_label = "日付"
    fig5_y_label = "合計"
    fig6_df = summary_bet_df
    fig6_x_list = fig6_df["式別名"]
    fig6_y_list = fig6_df["合計"]
    fig8_df = summary_bet_df[summary_bet_df["金額"] != 0].copy()
    fig8_type_list = fig8_df["式別名"]
    fig8_value_list = (fig8_df["結果"] / fig8_df["金額"]) * 100

    fig7_x_list = (place_bet_df["的中"] / place_bet_df["レース"]) * 100
    fig7_y_list = (place_bet_df["結果"] / place_bet_df["金額"]) * 100
    fig7_z_list = place_bet_df["結果"]
    fig7_name_list = place_bet_df["場名"]
    fig7_x_title = "的中率"
    fig7_y_title = "回収率"

    fig = gp.data_cards(fig1_value, fig1_reference)
    fig.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig2 = gp.showing_information_above(fig2_value, fig2_reference, fig2_list_sr)
    fig2.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig3 = gp.add_steps_threshold_anda_delta(fig3_value, fig3_reference)
    fig3.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig4 = gp.add_steps_threshold_anda_delta(fig4_value, fig4_reference)
    fig4.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig5 = gp.time_series_with_range_selector_buttions(fig5_df, fig5_x_label, fig5_y_label)
    fig5.update_layout(height=350, margin={'t': 0, 'b': 0, 'l': 0})
    fig6 = gp.simple_waterfall_chart(fig6_x_list, fig6_y_list)
    fig6.update_layout(height=350, margin={'t': 0, 'b': 0, 'l': 0})

    fig7 = gp.buble_chart(fig7_x_list, fig7_y_list, fig7_z_list, fig7_name_list, fig7_x_title, fig7_y_title)
    fig7.update_layout(height=700, margin={'t': 0, 'b': 0, 'l': 0})
    fig8 = gp.multi_bullet(fig8_type_list, fig8_value_list)
    fig8.update_layout(height=700, margin={'t': 0, 'b': 0, 'l': 0})

    print("start rendering")
    return [dbc.Row([
                wp.dbc_title("回収", 4),
                wp.dbc_title("回収率", 4),
                wp.dbc_title("軸馬単勝回収率", 2),
                wp.dbc_title("軸馬複勝回収率", 2),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig", 4, fig),
                wp.dbc_graph("fig2", 4, fig2),
                wp.dbc_graph("fig3", 2, fig3),
                wp.dbc_graph("fig4", 2, fig4),
            ], className="h-20"),
            dbc.Row([
                wp.dbc_title("券種毎回収率", 3),
                wp.dbc_title("残高推移", 4),
                wp.dbc_title("場所別回収的中率", 5),
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
            ], className="h-50",),]
