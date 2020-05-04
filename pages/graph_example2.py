import dash_bootstrap_components as dbc
import components.webparts as wp
import components.sample_graph as gp

def graph_example2():
    fig01 = gp.fully_styled_box_plot()
    fig02 = gp.histogram_with_plotly_express()
    fig03 = gp.visualizing_the_distribution()
    fig04 = gp.styled_histogram()
    fig05 = gp.cumulative_histogram()
    fig06 = gp.specify_aggregation_function()
    fig07 = gp.custom_binning()
    fig08 = gp.combined_statistical_representations()
    fig09 = gp.plot_multiple_datasets()
    fig10 = gp.density_heatmaps()
    fig11 = gp.sharing_bin_setting_between_2d_histgrams()
    fig12 = gp.scatter_matrix()
    fig13 = gp.radar_charts()
    fig14 = gp.multiple_trace_rader_chart()
    fig15 = gp.time_series_sing_axis_of_type_date()
    fig16 = gp.time_series_plot_with_custom_date_range()
    fig17 = gp.time_series_with_range_slider()
    fig18 = gp.time_series_with_range_selector_buttions()
    fig19 = gp.simple_candlestick_with_pandas()
    fig20 = gp.simple_waterfall_chart()
    fig21 = gp.horizontal_waterfall_chart()
    fig22 = gp.basic_funnel_plot()
    fig23 = gp.basic_area_funnel_plot()
    fig24 = gp.single_angular_gauge_chart()
    fig25 = gp.bullet_gauge()
    fig26 = gp.showing_information_above()
    fig27 = gp.data_cards()
    fig28 = gp.display_several_numbers()
    fig29 = gp.basic_gauge()
    fig30 = gp.add_steps_threshold_anda_delta()
    fig31 = gp.custom_gauge_chart()
    fig32 = gp.basic_bullet_charts()
    fig33 = gp.add_steps_and_threshold()
    fig34 = gp.custom_bullet()
    fig35 = gp.multi_bullet()
    fig36 = gp.table_and_chart_subplots()
    fig37 = gp.horizontal_table_and_chart()
    fig38 = gp.vertical_table_and_chart()
    fig39 = gp.update_button()
    fig40 = gp.simple_slider_control()
    fig41 = gp.update_dropdown()
    fig42 = gp.basic_range_slider_and_range_selectors()

    return \
        dbc.Container([
            dbc.Row([
                    wp.dbc_top_title("グラフサンプル2")
                ],className="h-30"),
            dbc.Row([
                    wp.dbc_title("fully_styled_box_plot", 4),
                    wp.dbc_title("histogram_with_plotly_express", 4),
                    wp.dbc_title("visualizing_the_distribution", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig01", 4, fig01),
                    wp.dbc_graph("fig02", 4, fig02),
                    wp.dbc_graph("fig03", 4, fig03),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("styled_histogram", 4),
                    wp.dbc_title("cumulative_histogram", 4),
                    wp.dbc_title("specify_aggregation_function", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig04", 4, fig04),
                    wp.dbc_graph("fig05", 4, fig05),
                    wp.dbc_graph("fig06", 4, fig06),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("custom_binning", 4),
                    wp.dbc_title("combined_statistical_representations", 4),
                    wp.dbc_title("plot_multiple_datasets", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig07", 4, fig07),
                    wp.dbc_graph("fig08", 4, fig08),
                    wp.dbc_graph("fig09", 4, fig09),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("density_heatmaps", 4),
                    wp.dbc_title("sharing_bin_setting_between_2d_histgrams", 4),
                    wp.dbc_title("scatter_matrix", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig10", 4, fig10),
                    wp.dbc_graph("fig11", 4, fig11),
                    wp.dbc_graph("fig12", 4, fig12),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("radar_charts", 4),
                    wp.dbc_title("multiple_trace_rader_chart", 4),
                    wp.dbc_title("time_series_sing_axis_of_type_date", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig13", 4, fig13),
                    wp.dbc_graph("fig14", 4, fig14),
                    wp.dbc_graph("fig15", 4, fig15),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("time_series_plot_with_custom_date_range", 4),
                    wp.dbc_title("time_series_with_range_slider", 4),
                    wp.dbc_title("time_series_with_range_selector_buttions", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig16", 4, fig16),
                    wp.dbc_graph("fig17", 4, fig17),
                    wp.dbc_graph("fig18", 4, fig18),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("simple_candlestick_with_pandas", 4),
                    wp.dbc_title("simple_waterfall_chart", 4),
                    wp.dbc_title("horizontal_waterfall_chart", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig19", 4, fig19),
                    wp.dbc_graph("fig20", 4, fig20),
                    wp.dbc_graph("fig21", 4, fig21),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("basic_funnel_plot", 4),
                    wp.dbc_title("basic_area_funnel_plot", 4),
                    wp.dbc_title("single_angular_gauge_chart", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig22", 4, fig22),
                    wp.dbc_graph("fig23", 4, fig23),
                    wp.dbc_graph("fig24", 4, fig24),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("bullet_gauge", 4),
                    wp.dbc_title("showing_information_above", 4),
                    wp.dbc_title("data_cards", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig25", 4, fig25),
                    wp.dbc_graph("fig26", 4, fig26),
                    wp.dbc_graph("fig27", 4, fig27),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("display_several_numbers", 4),
                    wp.dbc_title("basic_gauge", 4),
                    wp.dbc_title("add_steps_threshold_anda_delta", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig28", 4, fig28),
                    wp.dbc_graph("fig29", 4, fig29),
                    wp.dbc_graph("fig30", 4, fig30),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("custom_gauge_chart", 4),
                    wp.dbc_title("basic_bullet_charts", 4),
                    wp.dbc_title("add_steps_and_threshold", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig31", 4, fig31),
                    wp.dbc_graph("fig32", 4, fig32),
                    wp.dbc_graph("fig33", 4, fig33),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("custom_bullet", 4),
                    wp.dbc_title("multi_bullet", 4),
                    wp.dbc_title("table_and_chart_subplots", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig34", 4, fig34),
                    wp.dbc_graph("fig35", 4, fig35),
                    wp.dbc_graph("fig36", 4, fig36),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("horizontal_table_and_chart", 4),
                    wp.dbc_title("vertical_table_and_chart", 4),
                    wp.dbc_title("update_button", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig37", 4, fig37),
                    wp.dbc_graph("fig38", 4, fig38),
                    wp.dbc_graph("fig39", 4, fig39),
                ], className="h-50"),
            dbc.Row([
                    wp.dbc_title("simple_slider_control", 4),
                    wp.dbc_title("update_dropdown", 4),
                    wp.dbc_title("basic_range_slider_and_range_selectors", 4),
                ], className="h-8"),
            dbc.Row([
                    wp.dbc_graph("fig40", 4, fig40),
                    wp.dbc_graph("fig41", 4, fig41),
                    wp.dbc_graph("fig42", 4, fig42),
                ], className="h-50"),
        ],
        style={"height": "90vh"},
        fluid=True
        )