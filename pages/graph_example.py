import dash_bootstrap_components as dbc
import components.webparts as wp
import components.sample_graph as gp

def graph_example():
    fig01 = gp.simple_line()
    fig02 = gp.line_with_column_encoding_color()
    fig03 = gp.label_lines_with_annotations()
    fig04 = gp.filled_line()
    fig05 = gp.bar_chart()
    fig06 = gp.customized_bar_chart()
    fig07 = gp.facetted_subplots()
    fig08 = gp.basic_bar_chart_with_plotly()
    fig09 = gp.grouped_bar_chart()
    fig10 = gp.stacked_bar_chart()
    fig11 = gp.bar_chart_with_hover_text()
    fig12 = gp.bar_chart_with_direct_labels()
    fig13 = gp.controlling_text_fontsize_with_uniformtext()
    fig14 = gp.pie_chart()
    fig15 = gp.buble_chart()
    fig16 = gp.basic_dot_plot()
    fig17 = gp.styled_categorical_dot_plot()
    fig18 = gp.basic_horizontal_bar_chart()
    fig19 = gp.color_palette_for_bar_chart()
    fig20 = gp.bar_chart_with_line_plot()
    fig21 = gp.sunburst_of_a_rectangular()
    fig22 = gp.sankey_diagram()
    fig23 = gp.treemap()
    fig24 = gp.bar_chart_with_error_bars()
    fig25 = gp.display_the_underlying_data()
    fig26 = gp.choosing_the_algorithm()
    fig27 = gp.difference_between_quartile_algorithms()
    fig28 = gp.basic_horizontal_box_plot()
    fig29 = gp.grouped_box_plot()
    fig30 = gp.rainbow_box_plot()

    return \
        dbc.Container([
            dbc.Row([
                    wp.dbc_top_title("グラフサンプル")
                ],className="h-30"),
            dbc.Row([
                    wp.dbc_title("simple_line", 4),
                    wp.dbc_title("line_with_column_encoding_color", 4),
                    wp.dbc_title("label_lines_with_annotations", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig01", 4, fig01),
                    wp.dbc_graph("fig02", 4, fig02),
                    wp.dbc_graph("fig03", 4, fig03),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("filled_line", 4),
                    wp.dbc_title("bar_chart", 4),
                    wp.dbc_title("customized_bar_chart", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig04", 4, fig04),
                    wp.dbc_graph("fig05", 4, fig05),
                    wp.dbc_graph("fig06", 4, fig06),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("facetted_subplots", 4),
                    wp.dbc_title("basic_bar_chart_with_plotly", 4),
                    wp.dbc_title("grouped_bar_chart", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig07", 4, fig07),
                    wp.dbc_graph("fig08", 4, fig08),
                    wp.dbc_graph("fig09", 4, fig09),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("stacked_bar_chart", 4),
                    wp.dbc_title("bar_chart_with_hover_text", 4),
                    wp.dbc_title("bar_chart_with_direct_labels", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig10", 4, fig10),
                    wp.dbc_graph("fig11", 4, fig11),
                    wp.dbc_graph("fig12", 4, fig12),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("controlling_text_fontsize_with_uniformtext", 4),
                    wp.dbc_title("pie_chart", 4),
                    wp.dbc_title("buble_chart", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig13", 4, fig13),
                    wp.dbc_graph("fig14", 4, fig14),
                    wp.dbc_graph("fig15", 4, fig15),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("basic_dot_plot", 4),
                    wp.dbc_title("styled_categorical_dot_plot", 4),
                    wp.dbc_title("basic_horizontal_bar_chart", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig16", 4, fig16),
                    wp.dbc_graph("fig17", 4, fig17),
                    wp.dbc_graph("fig18", 4, fig18),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("color_palette_for_bar_chart", 4),
                    wp.dbc_title("bar_chart_with_line_plot", 4),
                    wp.dbc_title("sunburst_of_a_rectangular", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig19", 4, fig19),
                    wp.dbc_graph("fig20", 4, fig20),
                    wp.dbc_graph("fig21", 4, fig21),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("sankey_diagram", 4),
                    wp.dbc_title("treemap", 4),
                    wp.dbc_title("bar_chart_with_error_bars", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig22", 4, fig22),
                    wp.dbc_graph("fig23", 4, fig23),
                    wp.dbc_graph("fig24", 4, fig24),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("display_the_underlying_data", 4),
                    wp.dbc_title("choosing_the_algorithm", 4),
                    wp.dbc_title("difference_between_quartile_algorithms", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig25", 4, fig25),
                    wp.dbc_graph("fig26", 4, fig26),
                    wp.dbc_graph("fig27", 4, fig27),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("basic_horizontal_box_plot", 4),
                    wp.dbc_title("grouped_box_plot", 4),
                    wp.dbc_title("rainbow_box_plot", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig28", 4, fig28),
                    wp.dbc_graph("fig29", 4, fig29),
                    wp.dbc_graph("fig30", 4, fig30),
                ], className="h-50"),
        ],
        style={"height": "90vh"},
        fluid=True
        )