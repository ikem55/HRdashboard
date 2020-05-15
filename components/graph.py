import plotly.express as px
import plotly.graph_objects as go
import math
import numpy as np
import scipy.stats
from plotly.subplots import make_subplots
import itertools
# https://plotly.com/python/

def data_cards(value, reference):
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=value,
        delta={'position': "top", 'reference': reference},
        # title={"text": "Users online"},
        domain={'x': [0, 1], 'y': [0, 1]}))

    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5), )
    return fig

def showing_information_above(value, reference, list_sr):
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=value,
        delta={"reference": reference, "valueformat": ".0f"},
        domain={'y': [0, 1], 'x': [0.25, 0.75]}))

    fig.add_trace(go.Scatter(
        y=list_sr))

    fig.update_layout(xaxis={'range': [0, len(list_sr)]})
    fig.update_layout(margin=dict(l=5, r=5, t=30, b=5), )
    return fig

def add_steps_threshold_anda_delta(value, reference):
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=value,
        mode="gauge+number+delta",
        delta={'reference': reference},
        gauge={'axis': {'range': [None, 130]},
               'steps': [
                   {'range': [0, 85], 'color': "lightgray"},
                   {'range': [85, 100], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 110}}))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

def time_series_with_range_selector_buttions(df, x_label, y_label):
    fig = px.line(df, x=x_label, y=y_label)

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="todate"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),)
    return fig

def simple_waterfall_chart(x_list, y_list):
    fig = go.Figure(go.Waterfall(
        name="20", orientation="v",
        measure=["relative"] * (len(x_list) - 1) + ["total"],
        x=x_list,
        textposition="outside",
        y=y_list,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
        showlegend=False
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

def buble_chart(x_list, y_list, z_list, name_list, x_title, y_title):
    sizeref = 2. * max(z_list) / (100 ** 2)

    # Create figure
    fig = go.Figure()
    for i in range(len(x_list)):
        fig.add_trace(go.Scatter(
            x=[x_list[i]], y=[y_list[i]], marker_size=[z_list[i]], name=name_list[i]
        ))

    # Tune marker appearance and layout
    fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                                  sizeref=sizeref, line_width=2))

    fig.update_layout(
        xaxis=dict(
            title=x_title,
            type='log',
            gridwidth=2,
        ),
        yaxis=dict(
            title=y_title,
            gridwidth=2,
        ),
    )
    fig.update_layout(margin=dict(l=5, r=5, t=20, b=50),)
    return fig

def multi_bullet(type_list, value_list):
    fig = go.Figure()
    count = len(type_list)
    height_rate = 0.9 / count
    for i in range(count):
        fig.add_trace(go.Indicator(
            mode="number+gauge", value=value_list[i],
            domain={'x': [0.25, 1],
                    'y': [0.08 + height_rate * i,  height_rate * (i+1)] },
            title={'text': type_list[i]},
            gauge={
                'shape': "bullet",
                'axis': {'range': [None, 150]},
                'threshold': {
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.75,
                    'value': 120},
                'steps': [
                    {'range': [0, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "lightgray"}],
                'bar': {'color': "black"}}))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

def label_lines_with_annotations(multi_df):
    # dfはmultiindex、level0が横軸,level1が集計、Volume列が大小、Valueが値とする

    np_data = multi_df["Value"].unstack(level=0)
    y_labels = np_data.index.values
    x_labels = list(set(multi_df.index.get_level_values(0).values))
    labels_rank = scipy.stats.zscore(multi_df["Volume"].sum(level=1).tolist()).tolist()
    colors = []
    mode_size = []
    line_size = []
    for i in range(len(y_labels)):
        colors.append(f'rgb(115, {round(115 + 60 * labels_rank[i],0)}, {round(115 + 60 * labels_rank[i],0)})')
        mode_size.append(math.ceil(8 + 2 * labels_rank[i]))
        line_size.append(math.ceil(5 + 2 * labels_rank[i]))

    x_data = np.vstack((sorted(x_labels), ) * len(y_labels))

    y_data = np_data.values

    fig = go.Figure()

    for i in range(len(y_labels)):
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
                                 name=y_labels[i],
                                 line=dict(color=colors[i], width=line_size[i]),
                                 connectgaps=True,
                                 ))

        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
            marker=dict(color=colors[i], size=mode_size[i])
        ))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=True,
        plot_bgcolor='white'
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, y_labels, colors):
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[len(x_labels)-1],
                                xanchor='left', yanchor='middle',
                                text='{}%'.format(y_trace[len(x_labels)-1]),
                                font=dict(family='Arial',
                                          size=16),
                                showarrow=False))

    fig.update_layout(annotations=annotations)
    fig.update_layout(legend_orientation="h")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig


def visualizing_the_distribution(df):
    # 横軸にValue,分類にLabelをセットしたDFを渡す
    fig = px.histogram(df, x="Value", color="Label", marginal="box",  # can be `box`, `violin`
                       range_x=[0, 5000],
                       opacity=0.4)#, hover_data=df.columns)
    fig.update_layout(barmode='overlay')
    fig.update_layout(legend_orientation="h")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig


def bar_chart_with_line_plot(x, y_value1, y_value2, y_title1, y_title2):
    # Creating two subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    fig.append_trace(go.Bar(
        x=y_value1,
        y=x,
        marker=dict(
            line=dict(
                width=1),
        ),
        name=y_title1,
        orientation='h',
    ), 1, 1)

    fig.append_trace(go.Scatter(
        x=y_value2, y=x,
        mode='lines+markers',
        name=y_title2,
    ), 1, 2)

    fig.update_layout(
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
        ),
        yaxis2=dict(
            showgrid=False,
            showline=True,
            showticklabels=False,
            linewidth=2,
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            side='top',
            dtick=25000,
        ),
    )

    annotations = []

    y_s = np.round(y_value1, decimals=2)
    y_nw = np.rint(y_value2)

    # Adding labels
    for ydn, yd, xd in zip(y_nw, y_s, x):
        # labeling the scatter savings
        annotations.append(dict(xref='x2', yref='y2',
                                y=xd, x=ydn,
                                text=ydn,
                                font=dict(family='Arial', size=12,
                                          ),
                                showarrow=False))
        # labeling the bar net worth
        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=yd,
                                text=yd,
                                font=dict(family='Arial', size=12,
                                          ),
                                showarrow=False))
    fig.update_layout(annotations=annotations)
    fig.update_layout(legend_orientation="h")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig


def pie_chart(labels, values):
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, direction='clockwise',
                              hole=.4, sort=False)])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

def choosing_the_algorithm(df, x, y, color, max_y):
    fig = px.box(df, x=x, y=y, color=color)
    fig.update_traces(quartilemethod="exclusive")  # or "inclusive", or "linear" by default
    fig.update_layout(yaxis=dict(range=[0, max_y]))
    fig.update_layout(showlegend=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig


def styled_categorical_dot_plot(y, x1, x2, name1, name2):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x1,
        y=y,
        name=name1,
    ))
    fig.add_trace(go.Scatter(
        x=x2, y=y,
        name=name2,
    ))

    fig.update_traces(mode='markers', marker=dict(line_width=1, symbol='circle', size=16))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=True,
            showticklabels=True,
            dtick=10,
            ticks='outside',
        ),
        margin=dict(l=140, r=40, b=50, t=80),
        legend=dict(
            font_size=10,
            yanchor='middle',
            xanchor='right',
        ),
        hovermode='closest',
    )
    fig.update_layout(legend_orientation="h")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

def basic_horizontal_bar_chart(df):
    # name, label, valueのDFを作成
    df['value'] = df['value'].map("{:,.2f}".format)
    fig = px.bar(df, x="value", y="name", color="label", orientation='h',
                 height=400)
    fig.update_layout(legend_orientation="h")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

def basic_dot_plot(x, y_value1, y_value2, y_title1, y_title2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=y_value1,
        y=x,
        marker=dict(color="crimson", size=12),
        mode="markers",
        name=y_title1,
    ))

    fig.add_trace(go.Scatter(
        x=y_value2,
        y=x,
        marker=dict(color="gold", size=12),
        mode="markers",
        name=y_title2,
    ))

    fig.update_layout(
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
        ),
        yaxis2=dict(
            showgrid=False,
            showline=True,
            showticklabels=False,
            linewidth=2,
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            side='top',
            dtick=25000,
        ),
        margin=dict(l=100, r=20, t=70, b=70),
    )
    fig.update_layout(legend_orientation="h")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

def multiple_trace_rader_chart(categories, names, values):
    fig = go.Figure()

    for i in range(len(names)):
        fig.add_trace(go.Scatterpolar(
            r=values[i],
            theta=categories,
            fill='toself',
            name=names[i]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
            )),
        showlegend=True
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

def basic_horizontal_box_plot(names, values):

    fig = go.Figure()
    for i in range(len(names)):
        # Use x instead of y argument for horizontal plot
        fig.add_trace(go.Box(x=values[i], name=names[i]))
    fig.update_layout(showlegend=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

"""
def add_steps_and_threshold(value):
    fig = go.Figure(go.Indicator(
        mode="number+gauge", value=value,
        domain={'x': [0.1, 1], 'y': [0, 1]},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 100]},
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75,
                'value': 50},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 70], 'color': "gray"}]}))
    fig.update_layout(height=250)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig
"""

def simple_line(df):
    # x=label, y=value
    fig = px.line(df, x="label", y="value")
    fig.update_layout(yaxis=dict(range=[int(min(df["value"].tolist())) * 0.95, int(max(df["value"].tolist())) * 1.05]))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig


def controlling_text_fontsize_with_uniformtext(df):
    df['value'] = df['value'].map("{:,.3f}".format)
    fig = px.bar(df, y='value', x='name', text='value')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', yaxis=dict(range=[-0.6, 0.6]))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

def basic_funnel_plot(data):
    fig = go.Figure(go.Funnel(
        x=data['number'],
        y=data['stage']
    ))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig

def multiple_line_and_bar_chart(x_name , line_y_list, line_y_name, bar_y_list, bar_y_name):
    fig = go.Figure()

    for i in range(len(line_y_list)):
        fig.add_trace(
            go.Scatter(
                x=x_name,
                y=line_y_list[i],
                name=line_y_name[i],
                yaxis='y1'
            ))

    for i in range(len(bar_y_list)):
        fig.add_trace(
            go.Bar(
                x=x_name,
                y=bar_y_list[i],
                name=bar_y_name[i],
                yaxis='y2'
            ))
    fig.update_layout(
        yaxis=dict(side='left', showgrid=False, range=[0, max(list(itertools.chain.from_iterable(line_y_list))) * 1.1]),
        yaxis2=dict(side='right', overlaying='y', range=[0, max(list(itertools.chain.from_iterable(bar_y_list))) * 1.1], showgrid=False))
    fig.update_layout(legend_orientation="h")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), )
    return fig
