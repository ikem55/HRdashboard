import dash_bootstrap_components as dbc
import components.webparts as wp
import dash_core_components as dcc
import dash_html_components as html
import components.graph as gp
from datetime import datetime as dt
from components.get_data import GetData
import pandas as pd
import numpy as np
import datetime

def race_info():
    return dbc.Container([
        dbc.Row([
            dcc.DatePickerSingle(
                id='raceinfo-date-picker-single',
                min_date_allowed=dt(2019, 12, 1),
                initial_visible_month=dt.today(),
                date=datetime.date(dt.now().year, dt.now().month, dt.now().day)
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
            wp.dbc_top_title("race info")
        ], className="h-30"),
        dcc.Loading(id="race-info-loading",
                    children=[html.Div(id="raceinfo-race-detail")])
    ],
        style={"height": "90vh"},
        fluid=True
    )

def raceuma_info_render(shap_df_win, shap_df_jiku, shap_df_are):
    # 勝ち根拠
    fig1_df = pd.concat([shap_df_win.head(20), shap_df_win.tail(20)])
    fig1_df = fig1_df.sort_values("value")
    fig1 = gp.controlling_text_fontsize_with_uniformtext(fig1_df)
    fig1.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 軸根拠
    fig2_df = pd.concat([shap_df_jiku.head(20), shap_df_jiku.tail(20)])
    fig2_df = fig2_df.sort_values("value")
    fig2 = gp.controlling_text_fontsize_with_uniformtext(fig2_df)
    fig2.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 荒れ根拠
    fig3_df = pd.concat([shap_df_are.head(20), shap_df_are.tail(20)])
    fig3_df = fig3_df.sort_values("value")
    fig3 = gp.controlling_text_fontsize_with_uniformtext(fig3_df)
    fig3.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    return [dbc.Row([
            wp.dbc_title("勝ち根拠", 4),
            wp.dbc_title("軸根拠", 4),
            wp.dbc_title("荒れ根拠", 4),
        ], className="h-8"),
        dbc.Row([
            wp.dbc_graph("fig1", 4, fig1),
            wp.dbc_graph("fig2", 4, fig2),
            wp.dbc_graph("fig3", 4, fig3),
        ], className="h-50"),
        ]

def race_info_render(race_df, raceuma_df, shap_df_umaren_are, shap_df_umatan_are, shap_df_sanrenpuku_are):
    race_sr = race_df.iloc[0]
    term_start_date = "2019-12-01"
    term_end_date = race_sr["月日"].strftime("%Y-%m-%d")
    print(term_end_date)
    ketto_toroku_bango_list = raceuma_df["血統登録番号"].tolist()
    raceuma_prev_df = GetData.get_raceuma_prev_df(term_start_date, term_end_date, ketto_toroku_bango_list)
    raceuma_prev_df = pd.merge(raceuma_df[["血統登録番号", "馬名"]], raceuma_prev_df, on="血統登録番号")
    raceuma_df = raceuma_df.sort_values("馬番", ascending=False)

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
    fig1.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 最大得点分布
    fig2_df = raceuma_df[["馬名", "SCORE", "デフォルト得点"]]
    fig2_x = fig2_df["馬名"].tolist()
    fig2_y_value1 = fig2_df["SCORE"].tolist()
    fig2_y_value2 = fig2_df["デフォルト得点"].tolist()
    fig2_y_title1 = "SCORE"
    fig2_y_title2 = "デフォルト得点"
    fig2 = gp.basic_dot_plot(fig2_x, fig2_y_value1,fig2_y_value2, fig2_y_title1, fig2_y_title2)
    fig2.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 得点バブル
    fig3_x_list = raceuma_df["デフォルト得点"].tolist()
    fig3_y_list = raceuma_df["SCORE"].tolist()
    fig3_z_list = raceuma_df["得点V3"].tolist()
    fig3_name_list = raceuma_df["馬名"].tolist()
    fig3_x_title = "デフォルト得点"
    fig3_y_title = "SCORE"
    fig3 = gp.buble_chart(fig3_x_list, fig3_y_list, fig3_z_list, fig3_name_list, fig3_x_title, fig3_y_title)
    fig3.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # レーダーチャート
    fig4_df = raceuma_df[["馬名", "デフォルト得点", "得点V3", "WIN_RATE", "JIKU_RATE", "ANA_RATE"]]
    fig4_categories = ["デフォルト得点", "得点V3", "WIN_RATE", "JIKU_RATE", "ANA_RATE"]
    fig4_names = fig4_df["馬名"].tolist()
    fig4_values = fig4_df[fig4_categories].values
    fig4 = gp.multiple_trace_rader_chart(fig4_categories, fig4_names, fig4_values)
    fig4.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # 先行率
    fig5_df = raceuma_prev_df[["馬名", "先行率"]]
    fig5_names = fig5_df["馬名"].drop_duplicates().tolist()
    fig5_values = fig5_df.groupby("馬名")["先行率"].apply(list).apply(lambda x: np.array(x)).values
    fig5 = gp.basic_horizontal_box_plot(fig5_names, fig5_values)
    fig5.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # タイム指数
    fig6_df = raceuma_prev_df[["馬名", "タイム指数"]]
    fig6_names = fig6_df["馬名"].drop_duplicates().tolist()
    fig6_values = fig6_df.groupby("馬名")["タイム指数"].apply(list).apply(lambda x: np.array(x)).values
    fig6 = gp.basic_horizontal_box_plot(fig6_names, fig6_values)
    fig6.update_layout(height=500, margin={'t': 0, 'b': 0, 'l': 0})

    # テーブルデータ
    fig7_df = raceuma_df[["馬番", "馬名", "性別コード", "予想タイム指数順位", "予想タイム指数", "デフォルト得点", "得点", "騎手名"]]

    # 馬連荒れ根拠
    fig8_df = pd.concat([shap_df_umaren_are.head(20), shap_df_umaren_are.tail(20)])
    fig8_df = fig8_df.sort_values("value")
    fig8 = gp.controlling_text_fontsize_with_uniformtext(fig8_df)
    fig8.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 馬単荒れ根拠
    fig9_df = pd.concat([shap_df_umatan_are.head(20), shap_df_umatan_are.tail(20)])
    fig9_df = fig9_df.sort_values("value")
    fig9 = gp.controlling_text_fontsize_with_uniformtext(fig9_df)
    fig9.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    # 三連複荒れ根拠
    fig10_df = pd.concat([shap_df_sanrenpuku_are.head(20), shap_df_sanrenpuku_are.tail(20)])
    fig10_df = fig10_df.sort_values("value")
    fig10 = gp.controlling_text_fontsize_with_uniformtext(fig10_df)
    fig10.update_layout(height=300, margin={'t': 0, 'b': 0, 'l': 0})

    raceuma_dropdown_option = raceuma_df[["馬名", "馬番"]].rename(
        columns={"馬名": "label", "馬番": "value"}).to_dict(orient='record')
    return dcc.Loading(id="race-info-render-loading", children=[dbc.Row([
                wp.dbc_race_info(race_sr),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_title("馬連荒れ根拠", 4),
                wp.dbc_title("馬単荒れ根拠", 4),
                wp.dbc_title("三連複荒れ根拠", 4),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig8", 4, fig8),
                wp.dbc_graph("fig9", 4, fig9),
                wp.dbc_graph("fig10", 4, fig10),
            ], className="h-30"),
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
            dcc.Loading(id="raceuma-info-loading",
                        children=[html.Div(id="raceinfo-raceuma-detail")]),
            wp.dbc_table("fig7", 16, fig7_df)
        ])

