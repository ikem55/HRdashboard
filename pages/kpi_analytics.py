import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import components.webparts as wp
import components.sample_graph as gp

from datetime import datetime as dt

def kpi_analytics():
    return dbc.Container([
            dbc.Row([
                wp.dbc_top_title("kpi analytics")
            ], className="h-30"),
            dbc.Row([
                dcc.DatePickerRange(
                    id='kpi-analytics-date-picker-range',
                    min_date_allowed=dt(2019, 1, 1),
                    initial_visible_month=dt(2020, 1, 1),
                )]),
                html.Div(id="kpi_analytics")
        ],
        style={"height": "90vh"},
        fluid=True
    )

def kpi_analytics_render():
    fig1 = gp.pie_chart()
    fig1.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig2 = gp.add_steps_threshold_anda_delta()
    fig2.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig3 = gp.add_steps_threshold_anda_delta()
    fig3.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig4 = gp.pie_chart()
    fig4.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig5 = gp.add_steps_threshold_anda_delta()
    fig5.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig6 = gp.add_steps_threshold_anda_delta()
    fig6.update_layout(height=100, margin={'t': 0, 'b': 0, 'l': 0})
    fig10 = gp.basic_funnel_plot()
    fig10.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})
    fig11 = gp.basic_funnel_plot()
    fig11.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})
    fig12 = gp.basic_funnel_plot()
    fig12.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})
    fig13 = gp.basic_funnel_plot()
    fig13.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})


    return [dbc.Row([
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
                wp.dbc_title("馬連的中（母数、オッズ、軸１、軸２）", 3),
                wp.dbc_title("馬単的中", 3),
                wp.dbc_title("ワイド的中", 3),
                wp.dbc_title("三連複的中", 3),
            ], className="h-8"),
            dbc.Row([
                wp.dbc_graph("fig10", 3, fig10),
                wp.dbc_graph("fig11", 3, fig11),
                wp.dbc_graph("fig12", 3, fig12),
                wp.dbc_graph("fig13", 3, fig13),
            ], className="h-50"),]
