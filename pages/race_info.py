import dash_bootstrap_components as dbc
import components.webparts as wp
import dash_core_components as dcc
import dash_html_components as html
import components.graph as gp
from datetime import datetime as dt
from components.get_data import GetData
import pandas as pd
import numpy as np

def race_info():
    return dbc.Container([
        dbc.Row([
            wp.dbc_top_title("race info")
        ], className="h-30"),
        dbc.Row([
            dcc.DatePickerSingle(
                id='raceinfo-date-picker-single',
                min_date_allowed=dt(2019, 1, 1),
                max_date_allowed=dt(2020, 4, 30),
                initial_visible_month=dt(2020, 4, 1),
                date=dt(2020, 4, 1).date()
            ),
            dcc.Dropdown(
                id="raceinfo-dropdown-keibajo",
                options=[],
                value=""
            ),
            dcc.Dropdown(
                id="raceinfo-dropdown-raceid",
                options=[],
                value=""
            ),
        ], className="h-8"),
        html.Div(id="raceinfo-race-detail")
    ],
        style={"height": "90vh"},
        fluid=True
    )

def raceuma_info_render(shap_sr):
    shap_sr = pd.concat([shap_sr.head(20), shap_sr.tail(20)])
    fig1_df = pd.DataFrame(shap_sr).reset_index()
    fig1_df.columns = ["name", "value"]
    print(fig1_df.head(50))

    fig1 = gp.controlling_text_fontsize_with_uniformtext(fig1_df)
    fig1.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    return [dbc.Row([
                wp.dbc_graph("fig1", 12, fig1),
            ], className="h-50"),
        ]

def race_info_render(race_df, raceuma_df):
    race_sr = race_df.iloc[0]
    term_start_date = "2019-12-01"
    term_end_date = race_sr["月日"].strftime("%Y-%m-%d")
    print(term_end_date)
    ketto_toroku_bango_list = raceuma_df["血統登録番号"].tolist()
    raceuma_prev_df = GetData.get_raceuma_prev_df(term_start_date, term_end_date, ketto_toroku_bango_list)
    raceuma_prev_df = pd.merge(raceuma_df[["血統登録番号", "馬名"]], raceuma_prev_df, on="血統登録番号")

    raceuma_df = raceuma_df.sort_values("馬番", ascending=False)
    fig1_df = raceuma_df[["馬名", "デフォルト得点", "得点V3", "WIN_RATE", "JIKU_RATE", "ANA_RATE"]].set_index("馬名")
    fig1_df.loc[:, "デフォルト得点"] = fig1_df["デフォルト得点"] / 3
    fig1_df.loc[:, "得点V3"] = fig1_df["得点V3"] / 3
    fig1_df.loc[:, "WIN_RATE"] = fig1_df["WIN_RATE"] * 0.55 / 3
    fig1_df.loc[:, "JIKU_RATE"] = fig1_df["JIKU_RATE"] * 0.20 / 3
    fig1_df.loc[:, "ANA_RATE"] = fig1_df["ANA_RATE"] * 0.25 / 3
    fig1_df = fig1_df.stack().reset_index()
    fig1_df.columns = ["name", "label", "value"]

    fig2_df = raceuma_df[["馬名", "SCORE", "デフォルト得点"]]
    fig2_x = fig2_df["馬名"].tolist()
    fig2_y_value1 = fig2_df["SCORE"].tolist()
    fig2_y_value2 = fig2_df["デフォルト得点"].tolist()
    fig2_y_title1 = "SCORE"
    fig2_y_title2 = "デフォルト得点"


    fig3_x_list = raceuma_df["デフォルト得点"].tolist()
    fig3_y_list = raceuma_df["SCORE"].tolist()
    fig3_z_list = raceuma_df["得点V3"].tolist()
    fig3_name_list = raceuma_df["馬名"].tolist()
    fig3_x_title = "デフォルト得点"
    fig3_y_title = "SCORE"

    fig4_df = raceuma_df[["馬名", "デフォルト得点", "得点V3", "WIN_RATE", "JIKU_RATE", "ANA_RATE"]]
    fig4_categories = ["デフォルト得点", "得点V3", "WIN_RATE", "JIKU_RATE", "ANA_RATE"]
    fig4_names = fig4_df["馬名"].tolist()
    fig4_values = fig4_df[fig4_categories].values

    fig5_df = raceuma_prev_df[["馬名", "先行率"]]
    fig5_names = fig5_df["馬名"].drop_duplicates().tolist()
    fig5_values = fig5_df.groupby("馬名")["先行率"].apply(list).apply(lambda x: np.array(x)).values

    fig6_df = raceuma_prev_df[["馬名", "タイム指数"]]
    fig6_names = fig6_df["馬名"].drop_duplicates().tolist()
    fig6_values = fig6_df.groupby("馬名")["タイム指数"].apply(list).apply(lambda x: np.array(x)).values

    fig7_df = raceuma_df[["馬番", "馬名", "性別コード", "予想タイム指数順位", "予想タイム指数", "デフォルト得点", "得点", "騎手名"]]

    fig1 = gp.basic_horizontal_bar_chart(fig1_df)
    fig1.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})
    fig2 = gp.basic_dot_plot(fig2_x, fig2_y_value1,fig2_y_value2, fig2_y_title1, fig2_y_title2)
    fig2.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})
    fig3 = gp.buble_chart(fig3_x_list, fig3_y_list, fig3_z_list, fig3_name_list, fig3_x_title, fig3_y_title)
    fig3.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})
    fig4 = gp.multiple_trace_rader_chart(fig4_categories, fig4_names, fig4_values)
    fig4.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})
    fig5 = gp.basic_horizontal_box_plot(fig5_names, fig5_values)
    fig5.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})
    fig6 = gp.basic_horizontal_box_plot(fig6_names, fig6_values)
    fig6.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    raceuma_dropdown_option = raceuma_df[["馬名", "馬番"]].rename(
        columns={"馬名": "label", "馬番": "value"}).to_dict(orient='record')
    return [dbc.Row([
                wp.dbc_race_info(race_sr),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_title("得点", 6),
                wp.dbc_title("最大得点分布", 6),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig1", 6, fig1),
                wp.dbc_graph("fig2", 6, fig2),
            ], className="h-50"),
            dbc.Row([
                wp.dbc_title("得点バブル", 6),
                wp.dbc_title("レーダーチャート", 6),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig3", 6, fig3),
                wp.dbc_graph("fig4", 6, fig4),
            ], className="h-50"),
            dbc.Row([
                wp.dbc_title("先行率", 6),
                wp.dbc_title("タイム指数", 6),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig5", 6, fig5),
                wp.dbc_graph("fig6", 6, fig6),
            ], className="h-50"),
            dbc.Row([
                wp.dbc_title("得点根拠", 6),
                dcc.Dropdown(
                    id="raceinfo-dropdown-raceuma",
                    options=raceuma_dropdown_option,
                    style={"width": "300px"}
                ),
            ], className="h-8"),
            html.Div(id="raceinfo-raceuma-detail"),
            html.Div(id="raceinfo-raceuma-shap"),
            wp.dbc_table("fig7", 16, fig7_df)
        ]

