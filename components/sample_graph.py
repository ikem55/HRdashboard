import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import math
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import re

# https://plotly.com/python/

def simple_line():
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    return fig

def line_with_column_encoding_color():
    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color='country')
    return fig

def label_lines_with_annotations():
    title = 'Main Source for News'
    labels = ['Television', 'Newspaper', 'Internet', 'Radio']
    colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

    mode_size = [8, 8, 12, 8]
    line_size = [2, 2, 4, 2]

    x_data = np.vstack((np.arange(2001, 2014),) * 4)

    y_data = np.array([
        [74, 82, 80, 74, 73, 72, 74, 70, 70, 66, 66, 69],
        [45, 42, 50, 46, 36, 36, 34, 35, 32, 31, 31, 28],
        [13, 14, 20, 24, 20, 24, 24, 40, 35, 41, 43, 50],
        [18, 21, 18, 21, 16, 14, 13, 18, 17, 16, 19, 23],
    ])

    fig = go.Figure()

    for i in range(0, 4):
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
                                 name=labels[i],
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
            linecolor='rgb(204, 204, 204)',
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
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):
        # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                xanchor='right', yanchor='middle',
                                text=label + ' {}%'.format(y_trace[0]),
                                font=dict(family='Arial',
                                          size=16),
                                showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[11],
                                xanchor='left', yanchor='middle',
                                text='{}%'.format(y_trace[11]),
                                font=dict(family='Arial',
                                          size=16),
                                showarrow=False))
    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                            xanchor='left', yanchor='bottom',
                            text='Main Source for News',
                            font=dict(family='Arial',
                                      size=30,
                                      color='rgb(37,37,37)'),
                            showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                            xanchor='center', yanchor='top',
                            text='Source: PewResearch Center & ' +
                                 'Storytelling with data',
                            font=dict(family='Arial',
                                      size=12,
                                      color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)
    return fig

def filled_line():
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    x_rev = x[::-1]

    # Line 1
    y1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y1_upper = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    y1_lower = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y1_lower = y1_lower[::-1]

    # Line 2
    y2 = [5, 2.5, 5, 7.5, 5, 2.5, 7.5, 4.5, 5.5, 5]
    y2_upper = [5.5, 3, 5.5, 8, 6, 3, 8, 5, 6, 5.5]
    y2_lower = [4.5, 2, 4.4, 7, 4, 2, 7, 4, 5, 4.75]
    y2_lower = y2_lower[::-1]

    # Line 3
    y3 = [10, 8, 6, 4, 2, 0, 2, 4, 2, 0]
    y3_upper = [11, 9, 7, 5, 3, 1, 3, 5, 3, 1]
    y3_lower = [9, 7, 5, 3, 1, -.5, 1, 3, 1, -1]
    y3_lower = y3_lower[::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x + x_rev,
        y=y1_upper + y1_lower,
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='Fair',
    ))
    fig.add_trace(go.Scatter(
        x=x + x_rev,
        y=y2_upper + y2_lower,
        fill='toself',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        name='Premium',
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=x + x_rev,
        y=y3_upper + y3_lower,
        fill='toself',
        fillcolor='rgba(231,107,243,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='Ideal',
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y1,
        line_color='rgb(0,100,80)',
        name='Fair',
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y2,
        line_color='rgb(0,176,246)',
        name='Premium',
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y3,
        line_color='rgb(231,107,243)',
        name='Ideal',
    ))

    fig.update_traces(mode='lines')
    return fig

def bar_chart():
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x='year', y='pop')
    return fig

def customized_bar_chart():
    data = px.data.gapminder()

    data_canada = data[data.country == 'Canada']
    fig = px.bar(data_canada, x='year', y='pop',
                 hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
                 labels={'pop': 'population of Canada'}, height=400)
    return fig

def facetted_subplots():
    df = px.data.tips()
    fig = px.bar(df, x="sex", y="total_bill", color="smoker", barmode="group",
                 facet_row="time", facet_col="day",
                 category_orders={"day": ["Thur", "Fri", "Sat", "Sun"],
                                  "time": ["Lunch", "Dinner"]})
    return fig

def basic_bar_chart_with_plotly():
    animals = ['giraffes', 'orangutans', 'monkeys']

    fig = go.Figure([go.Bar(x=animals, y=[20, 14, 23])])
    return fig

def grouped_bar_chart():
    animals = ['giraffes', 'orangutans', 'monkeys']

    fig = go.Figure(data=[
        go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
        go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    return fig

def stacked_bar_chart():
    animals = ['giraffes', 'orangutans', 'monkeys']

    fig = go.Figure(data=[
        go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
        go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
    ])
    # Change the bar mode
    fig.update_layout(barmode='stack')
    return fig

def bar_chart_with_hover_text():
    x = ['Product A', 'Product B', 'Product C']
    y = [20, 14, 23]

    # Use the hovertext kw argument for hover text
    fig = go.Figure(data=[go.Bar(x=x, y=y,
                                 hovertext=['27% market share', '24% market share', '19% market share'])])
    # Customize aspect
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text='January 2013 Sales Report')
    return fig

def bar_chart_with_direct_labels():
    x = ['Product A', 'Product B', 'Product C']
    y = [20, 14, 23]

    # Use textposition='auto' for direct text
    fig = go.Figure(data=[go.Bar(
        x=x, y=y,
        text=y,
        textposition='auto',
    )])
    return fig

def controlling_text_fontsize_with_uniformtext():
    df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")
    fig = px.bar(df, y='pop', x='country', text='pop')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig

def pie_chart():
    # This dataframe has 244 lines, but 4 distinct values for `day`
    df = px.data.tips()
    fig = px.pie(df, values='tip', names='day')
    return fig

def buble_chart():
    # Load data, define hover text and bubble size
    data = px.data.gapminder()
    df_2007 = data[data['year'] == 2007]
    df_2007 = df_2007.sort_values(['continent', 'country'])

    hover_text = []
    bubble_size = []

    for index, row in df_2007.iterrows():
        hover_text.append(('Country: {country}<br>' +
                           'Life Expectancy: {lifeExp}<br>' +
                           'GDP per capita: {gdp}<br>' +
                           'Population: {pop}<br>' +
                           'Year: {year}').format(country=row['country'],
                                                  lifeExp=row['lifeExp'],
                                                  gdp=row['gdpPercap'],
                                                  pop=row['pop'],
                                                  year=row['year']))
        bubble_size.append(math.sqrt(row['pop']))

    df_2007['text'] = hover_text
    df_2007['size'] = bubble_size
    sizeref = 2. * max(df_2007['size']) / (100 ** 2)

    # Dictionary with dataframes for each continent
    continent_names = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']
    continent_data = {continent: df_2007.query("continent == '%s'" % continent)
                      for continent in continent_names}

    # Create figure
    fig = go.Figure()

    for continent_name, continent in continent_data.items():
        fig.add_trace(go.Scatter(
            x=continent['gdpPercap'], y=continent['lifeExp'],
            name=continent_name, text=continent['text'],
            marker_size=continent['size'],
        ))

    # Tune marker appearance and layout
    fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                                  sizeref=sizeref, line_width=2))

    fig.update_layout(
        title='Life Expectancy v. Per Capita GDP, 2007',
        xaxis=dict(
            title='GDP per capita (2000 dollars)',
            gridcolor='white',
            type='log',
            gridwidth=2,
        ),
        yaxis=dict(
            title='Life Expectancy (years)',
            gridcolor='white',
            gridwidth=2,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
    )
    return fig

def basic_dot_plot():
    schools = ["Brown", "NYU", "Notre Dame", "Cornell", "Tufts", "Yale",
               "Dartmouth", "Chicago", "Columbia", "Duke", "Georgetown",
               "Princeton", "U.Penn", "Stanford", "MIT", "Harvard"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[72, 67, 73, 80, 76, 79, 84, 78, 86, 93, 94, 90, 92, 96, 94, 112],
        y=schools,
        marker=dict(color="crimson", size=12),
        mode="markers",
        name="Women",
    ))

    fig.add_trace(go.Scatter(
        x=[92, 94, 100, 107, 112, 114, 114, 118, 119, 124, 131, 137, 141, 151, 152, 165],
        y=schools,
        marker=dict(color="gold", size=12),
        mode="markers",
        name="Men",
    ))

    fig.update_layout(title="Gender Earnings Disparity",
                      xaxis_title="Annual Salary (in thousands)",
                      yaxis_title="School")
    return fig

def styled_categorical_dot_plot():
    country = ['Switzerland (2011)', 'Chile (2013)', 'Japan (2014)',
               'United States (2012)', 'Slovenia (2014)', 'Canada (2011)',
               'Poland (2010)', 'Estonia (2015)', 'Luxembourg (2013)', 'Portugal (2011)']
    voting_pop = [40, 45.7, 52, 53.6, 54.1, 54.2, 54.5, 54.7, 55.1, 56.6]
    reg_voters = [49.1, 42, 52.7, 84.3, 51.7, 61.1, 55.3, 64.2, 91.1, 58.9]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=voting_pop,
        y=country,
        name='Percent of estimated voting age population',
        marker=dict(
            color='rgba(156, 165, 196, 0.95)',
            line_color='rgba(156, 165, 196, 1.0)',
        )
    ))
    fig.add_trace(go.Scatter(
        x=reg_voters, y=country,
        name='Percent of estimated registered voters',
        marker=dict(
            color='rgba(204, 204, 204, 0.95)',
            line_color='rgba(217, 217, 217, 1.0)'
        )
    ))

    fig.update_traces(mode='markers', marker=dict(line_width=1, symbol='circle', size=16))

    fig.update_layout(
        title="Votes cast for ten lowest voting age population in OECD countries",
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='rgb(102, 102, 102)',
            tickfont_color='rgb(102, 102, 102)',
            showticklabels=True,
            dtick=10,
            ticks='outside',
            tickcolor='rgb(102, 102, 102)',
        ),
        margin=dict(l=140, r=40, b=50, t=80),
        legend=dict(
            font_size=10,
            yanchor='middle',
            xanchor='right',
        ),
        width=800,
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='white',
        hovermode='closest',
    )
    return fig

def basic_horizontal_bar_chart():
    df = px.data.tips()
    fig = px.bar(df, x="total_bill", y="sex", color='day', orientation='h',
                 hover_data=["tip", "size"],
                 height=400,
                 title='Restaurant bills')
    return fig

def color_palette_for_bar_chart():
    top_labels = ['Strongly<br>agree', 'Agree', 'Neutral', 'Disagree',
                  'Strongly<br>disagree']

    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
              'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
              'rgba(190, 192, 213, 1)']

    x_data = [[21, 30, 21, 16, 12],
              [24, 31, 19, 15, 11],
              [27, 26, 23, 11, 13],
              [29, 24, 15, 18, 14]]

    y_data = ['The course was effectively<br>organized',
              'The course developed my<br>abilities and skills ' +
              'for<br>the subject', 'The course developed ' +
              'my<br>ability to think critically about<br>the subject',
              'I would recommend this<br>course to a friend']

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                )
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=120, r=10, t=140, b=80),
        showlegend=False,
    )

    annotations = []

    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                                x=xd[0] / 2, y=yd,
                                text=str(xd[0]) + '%',
                                font=dict(family='Arial', size=14,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=xd[0] / 2, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='Arial', size=14,
                                              color='rgb(67, 67, 67)'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
            # labeling the rest of percentages for each bar (x_axis)
            annotations.append(dict(xref='x', yref='y',
                                    x=space + (xd[i] / 2), y=yd,
                                    text=str(xd[i]) + '%',
                                    font=dict(family='Arial', size=14,
                                              color='rgb(248, 248, 255)'),
                                    showarrow=False))
            # labeling the Likert scale
            if yd == y_data[-1]:
                annotations.append(dict(xref='x', yref='paper',
                                        x=space + (xd[i] / 2), y=1.1,
                                        text=top_labels[i],
                                        font=dict(family='Arial', size=14,
                                                  color='rgb(67, 67, 67)'),
                                        showarrow=False))
            space += xd[i]

    fig.update_layout(annotations=annotations)
    return fig

def bar_chart_with_line_plot():
    y_saving = [1.3586, 2.2623000000000002, 4.9821999999999997, 6.5096999999999996,
                7.4812000000000003, 7.5133000000000001, 15.2148, 17.520499999999998
                ]
    y_net_worth = [93453.919999999998, 81666.570000000007, 69889.619999999995,
                   78381.529999999999, 141395.29999999999, 92969.020000000004,
                   66090.179999999993, 122379.3]
    x = ['Japan', 'United Kingdom', 'Canada', 'Netherlands',
         'United States', 'Belgium', 'Sweden', 'Switzerland']

    # Creating two subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    fig.append_trace(go.Bar(
        x=y_saving,
        y=x,
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        ),
        name='Household savings, percentage of household disposable income',
        orientation='h',
    ), 1, 1)

    fig.append_trace(go.Scatter(
        x=y_net_worth, y=x,
        mode='lines+markers',
        line_color='rgb(128, 0, 128)',
        name='Household net worth, Million USD/capita',
    ), 1, 2)

    fig.update_layout(
        title='Household savings & net worth for eight OECD countries',
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0, 0.85],
        ),
        yaxis2=dict(
            showgrid=False,
            showline=True,
            showticklabels=False,
            linecolor='rgba(102, 102, 102, 0.8)',
            linewidth=2,
            domain=[0, 0.85],
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0, 0.42],
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0.47, 1],
            side='top',
            dtick=25000,
        ),
        legend=dict(x=0.029, y=1.038, font_size=10),
        margin=dict(l=100, r=20, t=70, b=70),
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
    )

    annotations = []

    y_s = np.round(y_saving, decimals=2)
    y_nw = np.rint(y_net_worth)

    # Adding labels
    for ydn, yd, xd in zip(y_nw, y_s, x):
        # labeling the scatter savings
        annotations.append(dict(xref='x2', yref='y2',
                                y=xd, x=ydn - 20000,
                                text='{:,}'.format(ydn) + 'M',
                                font=dict(family='Arial', size=12,
                                          color='rgb(128, 0, 128)'),
                                showarrow=False))
        # labeling the bar net worth
        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=yd + 3,
                                text=str(yd) + '%',
                                font=dict(family='Arial', size=12,
                                          color='rgb(50, 171, 96)'),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper',
                            x=-0.2, y=-0.109,
                            text='OECD "' +
                                 '(2015), Household savings (indicator), ' +
                                 'Household net worth (indicator). doi: ' +
                                 '10.1787/cfc6f499-en (Accessed on 05 June 2015)',
                            font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)
    return fig

def sunburst_of_a_rectangular():
    df = px.data.tips()
    fig = px.sunburst(df, path=['day', 'time', 'sex'], values='total_bill')
    return fig

def sankey_diagram():
    import urllib, json
    url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    # override gray link colors with 'source' colors
    opacity = 0.4
    # change 'magenta' to its 'rgba' value to add opacity
    data['data'][0]['node']['color'] = ['rgba(255,0,255, 0.8)' if color == "magenta" else color for color in
                                        data['data'][0]['node']['color']]
    data['data'][0]['link']['color'] = [data['data'][0]['node']['color'][src].replace("0.8", str(opacity))
                                        for src in data['data'][0]['link']['source']]

    fig = go.Figure(data=[go.Sankey(
        valueformat=".0f",
        valuesuffix="TWh",
        # Define nodes
        node=dict(
            pad=15,
            thickness=15,
            line=dict(color="black", width=0.5),
            label=data['data'][0]['node']['label'],
            color=data['data'][0]['node']['color']
        ),
        # Add links
        link=dict(
            source=data['data'][0]['link']['source'],
            target=data['data'][0]['link']['target'],
            value=data['data'][0]['link']['value'],
            label=data['data'][0]['link']['label'],
            color=data['data'][0]['link']['color']
        ))])

    fig.update_layout(
        title_text="Energy forecast for 2050<br>Source: Department of Energy & Climate Change, Tom Counsell via <a href='https://bost.ocks.org/mike/sankey/'>Mike Bostock</a>",
        font_size=10)
    return fig

def treemap():
    df = px.data.gapminder().query("year == 2007")
    df["world"] = "world"  # in order to have a single root node
    fig = px.treemap(df, path=['world', 'continent', 'country'], values='pop',
                     color='lifeExp', hover_data=['iso_alpha'],
                     color_continuous_scale='RdBu',
                     color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))
    return fig

def bar_chart_with_error_bars():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Control',
        x=['Trial 1', 'Trial 2', 'Trial 3'], y=[3, 6, 4],
        error_y=dict(type='data', array=[1, 0.5, 1.5])
    ))
    fig.add_trace(go.Bar(
        name='Experimental',
        x=['Trial 1', 'Trial 2', 'Trial 3'], y=[4, 7, 3],
        error_y=dict(type='data', array=[0.5, 1, 2])
    ))
    fig.update_layout(barmode='group')
    return fig

def display_the_underlying_data():
    df = px.data.tips()
    fig = px.box(df, x="time", y="total_bill", points="all")
    return fig

def choosing_the_algorithm():
    df = px.data.tips()

    fig = px.box(df, x="day", y="total_bill", color="smoker")
    fig.update_traces(quartilemethod="exclusive")  # or "inclusive", or "linear" by default
    return fig

def difference_between_quartile_algorithms():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    df = pd.DataFrame(dict(
        linear=data,
        inclusive=data,
        exclusive=data
    )).melt(var_name="quartilemethod")

    fig = px.box(df, y="value", facet_col="quartilemethod", color="quartilemethod",
                 boxmode="overlay", points='all')

    fig.update_traces(quartilemethod="linear", jitter=0, col=1)
    fig.update_traces(quartilemethod="inclusive", jitter=0, col=2)
    fig.update_traces(quartilemethod="exclusive", jitter=0, col=3)
    return fig

def basic_horizontal_box_plot():
    x0 = np.random.randn(50)
    x1 = np.random.randn(50) + 2  # shift mean

    fig = go.Figure()
    # Use x instead of y argument for horizontal plot
    fig.add_trace(go.Box(x=x0))
    fig.add_trace(go.Box(x=x1))
    return fig

def grouped_box_plot():
    x = ['day 1', 'day 1', 'day 1', 'day 1', 'day 1', 'day 1',
         'day 2', 'day 2', 'day 2', 'day 2', 'day 2', 'day 2']

    fig = go.Figure()

    fig.add_trace(go.Box(
        y=[0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        x=x,
        name='kale',
        marker_color='#3D9970'
    ))
    fig.add_trace(go.Box(
        y=[0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2],
        x=x,
        name='radishes',
        marker_color='#FF4136'
    ))
    fig.add_trace(go.Box(
        y=[0.1, 0.3, 0.1, 0.9, 0.6, 0.6, 0.9, 1.0, 0.3, 0.6, 0.8, 0.5],
        x=x,
        name='carrots',
        marker_color='#FF851B'
    ))

    fig.update_layout(
        yaxis_title='normalized moisture',
        boxmode='group'  # group together boxes of the different traces for each value of x
    )
    return fig

def rainbow_box_plot():
    N = 30  # Number of boxes

    # generate an array of rainbow colors by fixing the saturation and lightness of the HSL
    # representation of colour and marching around the hue.
    # Plotly accepts any CSS color format, see e.g. http://www.w3schools.com/cssref/css_colors_legal.asp.
    c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, N)]

    # Each box is represented by a dict that contains the data, the type, and the colour.
    # Use list comprehension to describe N boxes, each with a different colour and with different randomly generated data:
    fig = go.Figure(data=[go.Box(
        y=3.5 * np.sin(np.pi * i / N) + i / N + (1.5 + 0.5 * np.cos(np.pi * i / N)) * np.random.rand(10),
        marker_color=c[i]
    ) for i in range(int(N))])

    # format the layout
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(zeroline=False, gridcolor='white'),
        paper_bgcolor='rgb(233,233,233)',
        plot_bgcolor='rgb(233,233,233)',
    )
    return fig

def fully_styled_box_plot():
    x_data = ['Carmelo Anthony', 'Dwyane Wade',
              'Deron Williams', 'Brook Lopez',
              'Damian Lillard', 'David West', ]

    N = 50

    y0 = (10 * np.random.randn(N) + 30).astype(np.int)
    y1 = (13 * np.random.randn(N) + 38).astype(np.int)
    y2 = (11 * np.random.randn(N) + 33).astype(np.int)
    y3 = (9 * np.random.randn(N) + 36).astype(np.int)
    y4 = (15 * np.random.randn(N) + 31).astype(np.int)
    y5 = (12 * np.random.randn(N) + 40).astype(np.int)

    y_data = [y0, y1, y2, y3, y4, y5]

    colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)',
              'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)']

    fig = go.Figure()

    for xd, yd, cls in zip(x_data, y_data, colors):
        fig.add_trace(go.Box(
            y=yd,
            name=xd,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=cls,
            marker_size=2,
            line_width=1)
        )

    fig.update_layout(
        title='Points Scored by the Top 9 Scoring NBA Players in 2012',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )
    return fig

def histogram_with_plotly_express():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill")
    return fig

def visualizing_the_distribution():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", color="sex", marginal="rug",  # can be `box`, `violin`
                       hover_data=df.columns)
    return fig

def styled_histogram():
    x0 = np.random.randn(500)
    x1 = np.random.randn(500) + 1

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=x0,
        histnorm='percent',
        name='control',  # name used in legend and hover labels
        xbins=dict(  # bins used for histogram
            start=-4.0,
            end=3.0,
            size=0.5
        ),
        marker_color='#EB89B5',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=x1,
        histnorm='percent',
        name='experimental',
        xbins=dict(
            start=-3.0,
            end=4,
            size=0.5
        ),
        marker_color='#330C73',
        opacity=0.75
    ))

    fig.update_layout(
        title_text='Sampled Results',  # title of plot
        xaxis_title_text='Value',  # xaxis label
        yaxis_title_text='Count',  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1  # gap between bars of the same location coordinates
    )
    return fig

def cumulative_histogram():
    x = np.random.randn(500)
    fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True)])
    return fig

def specify_aggregation_function():
    x = ["Apples", "Apples", "Apples", "Oranges", "Bananas"]
    y = ["5", "10", "3", "10", "5"]

    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count", y=y, x=x, name="count"))
    fig.add_trace(go.Histogram(histfunc="sum", y=y, x=x, name="sum"))
    return fig

def custom_binning():
    x = ['1970-01-01', '1970-01-01', '1970-02-01', '1970-04-01', '1970-01-02',
         '1972-01-31', '1970-02-13', '1971-04-19']

    fig = make_subplots(rows=3, cols=2)

    trace0 = go.Histogram(x=x, nbinsx=4)
    trace1 = go.Histogram(x=x, nbinsx=8)
    trace2 = go.Histogram(x=x, nbinsx=10)
    trace3 = go.Histogram(x=x,
                          xbins=dict(
                              start='1969-11-15',
                              end='1972-03-31',
                              size='M18'),  # M18 stands for 18 months
                          autobinx=False
                          )
    trace4 = go.Histogram(x=x,
                          xbins=dict(
                              start='1969-11-15',
                              end='1972-03-31',
                              size='M4'),  # 4 months bin size
                          autobinx=False
                          )
    trace5 = go.Histogram(x=x,
                          xbins=dict(
                              start='1969-11-15',
                              end='1972-03-31',
                              size='M2'),  # 2 months
                          autobinx=False
                          )

    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 2)
    fig.append_trace(trace2, 2, 1)
    fig.append_trace(trace3, 2, 2)
    fig.append_trace(trace4, 3, 1)
    fig.append_trace(trace5, 3, 2)
    return fig

def combined_statistical_representations():
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", y="tip", color="sex",
                       marginal="box",  # or violin, rug
                       hover_data=df.columns)
    return fig

def plot_multiple_datasets():
    # Add histogram data
    x1 = np.random.randn(200) - 2
    x2 = np.random.randn(200)
    x3 = np.random.randn(200) + 2
    x4 = np.random.randn(200) + 4

    # Group data together
    hist_data = [x1, x2, x3, x4]

    group_labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4']

    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
    return fig

def density_heatmaps():
    df = px.data.tips()

    fig = px.density_heatmap(df, x="total_bill", y="tip", marginal_x="histogram", marginal_y="histogram")
    return fig

def sharing_bin_setting_between_2d_histgrams():
    fig = make_subplots(2, 2)
    fig.add_trace(go.Histogram2d(
        x=[1, 2, 2, 3, 4],
        y=[1, 2, 2, 3, 4],
        coloraxis="coloraxis",
        xbins={'start': 1, 'size': 1}), 1, 1)
    fig.add_trace(go.Histogram2d(
        x=[4, 5, 5, 5, 6],
        y=[4, 5, 5, 5, 6],
        coloraxis="coloraxis",
        ybins={'start': 3, 'size': 1}), 1, 2)
    fig.add_trace(go.Histogram2d(
        x=[1, 2, 2, 3, 4],
        y=[1, 2, 2, 3, 4],
        bingroup=1,
        coloraxis="coloraxis",
        xbins={'start': 1, 'size': 1}), 2, 1)
    fig.add_trace(go.Histogram2d(
        x=[4, 5, 5, 5, 6],
        y=[4, 5, 5, 5, 6],
        bingroup=1,
        coloraxis="coloraxis",
        ybins={'start': 3, 'size': 1}), 2, 2)
    return fig

def scatter_matrix():
    df = px.data.iris()
    fig = px.scatter_matrix(df,
                            dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"],
                            color="species")
    return fig

def radar_charts():
    df = pd.DataFrame(dict(
        r=[1, 5, 2, 2, 3],
        theta=['processing cost', 'mechanical properties', 'chemical stability',
               'thermal stability', 'device integration']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    return fig

def multiple_trace_rader_chart():
    categories = ['processing cost', 'mechanical properties', 'chemical stability',
                  'thermal stability', 'device integration']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[1, 5, 2, 2, 3],
        theta=categories,
        fill='toself',
        name='Product A'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[4, 3, 2.5, 1, 2],
        theta=categories,
        fill='toself',
        name='Product B'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False
    )
    return fig

def time_series_sing_axis_of_type_date():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

    fig = px.line(df, x='Date', y='AAPL.High')
    return fig

def time_series_plot_with_custom_date_range():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

    fig = px.line(df, x='Date', y='AAPL.High', range_x=['2016-07-01', '2016-12-31'])
    return fig

def time_series_with_range_slider():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

    fig = px.line(df, x='Date', y='AAPL.High', title='Time Series with Rangeslider')

    fig.update_xaxes(rangeslider_visible=True)
    return fig

def time_series_with_range_selector_buttions():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

    fig = px.line(df, x='Date', y='AAPL.High', title='Time Series with Range Slider and Selectors')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig

def simple_candlestick_with_pandas():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['AAPL.Open'],
                                         high=df['AAPL.High'],
                                         low=df['AAPL.Low'],
                                         close=df['AAPL.Close'])])
    return fig

def simple_waterfall_chart():
    fig = go.Figure(go.Waterfall(
        name="20", orientation="v",
        measure=["relative", "relative", "total", "relative", "relative", "total"],
        x=["Sales", "Consulting", "Net revenue", "Purchases", "Other expenses", "Profit before tax"],
        textposition="outside",
        text=["+60", "+80", "", "-40", "-20", "Total"],
        y=[60, 80, 0, -40, -20, 0],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
        title="Profit and loss statement 2018",
        showlegend=True
    )
    return fig

def horizontal_waterfall_chart():
    fig = go.Figure(go.Waterfall(
        name="2018", orientation="h", measure=["relative", "relative", "relative", "relative", "total", "relative",
                                               "relative", "relative", "relative", "total", "relative", "relative",
                                               "total", "relative", "total"],
        y=["Sales", "Consulting", "Maintenance", "Other revenue", "Net revenue", "Purchases", "Material expenses",
           "Personnel expenses", "Other expenses", "Operating profit", "Investment income", "Financial income",
           "Profit before tax", "Income tax (15%)", "Profit after tax"],
        x=[375, 128, 78, 27, None, -327, -12, -78, -12, None, 32, 89, None, -45, None],
        connector={"mode": "between", "line": {"width": 4, "color": "rgb(0, 0, 0)", "dash": "solid"}}
    ))

    fig.update_layout(title="Profit and loss statement 2018")
    return fig

def basic_funnel_plot():
    data = dict(
        number=[39, 27.4, 20.6, 11, 2],
        stage=["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent"])
    fig = px.funnel(data, x='number', y='stage')
    return fig

def basic_area_funnel_plot():
    fig = go.Figure(go.Funnelarea(
        text=["The 1st", "The 2nd", "The 3rd", "The 4th", "The 5th"],
        values=[5, 4, 3, 2, 1]
    ))
    return fig

def single_angular_gauge_chart():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=450,
        title={'text': "Speed"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    return fig

def bullet_gauge():
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta",
        gauge={'shape': "bullet"},
        delta={'reference': 300},
        value=220,
        domain={'x': [0.1, 1], 'y': [0.2, 0.9]},
        title={'text': "Avg order size"}))
    return fig

def showing_information_above():
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=492,
        delta={"reference": 512, "valueformat": ".0f"},
        title={"text": "Users online"},
        domain={'y': [0, 1], 'x': [0.25, 0.75]}))

    fig.add_trace(go.Scatter(
        y=[325, 324, 405, 400, 424, 404, 417, 432, 419, 394, 410, 426, 413, 419, 404, 408, 401, 377, 368, 361, 356, 359,
           375, 397, 394, 418, 437, 450, 430, 442, 424, 443, 420, 418, 423, 423, 426, 440, 437, 436, 447, 460, 478, 472,
           450, 456, 436, 418, 429, 412, 429, 442, 464, 447, 434, 457, 474, 480, 499, 497, 480, 502, 512, 492]))

    fig.update_layout(xaxis={'range': [0, 62]})
    return fig

def data_cards():
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=400,
        number={'prefix': "$"},
        delta={'position': "top", 'reference': 320},
        domain={'x': [0, 1], 'y': [0, 1]}))

    fig.update_layout(paper_bgcolor="lightgray")
    return fig

def display_several_numbers():
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=200,
        domain={'x': [0, 0.5], 'y': [0, 0.5]},
        delta={'reference': 400, 'relative': True, 'position': "top"}))

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=350,
        delta={'reference': 400, 'relative': True},
        domain={'x': [0, 0.5], 'y': [0.5, 1]}))

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=450,
        title={
            "text": "Accounts<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"},
        delta={'reference': 400, 'relative': True},
        domain={'x': [0.6, 1], 'y': [0, 1]}))
    return fig

def basic_gauge():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=270,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Speed"}))
    return fig

def add_steps_threshold_anda_delta():
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=450,
        mode="gauge+number+delta",
        title={'text': "Speed"},
        delta={'reference': 380},
        gauge={'axis': {'range': [None, 500]},
               'steps': [
                   {'range': [0, 250], 'color': "lightgray"},
                   {'range': [250, 400], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))
    return fig

def custom_gauge_chart():
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=420,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Speed", 'font': {'size': 24}},
        delta={'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
        gauge={
            'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 250], 'color': 'cyan'},
                {'range': [250, 400], 'color': 'royalblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 490}}))

    fig.update_layout(paper_bgcolor="lavender", font={'color': "darkblue", 'family': "Arial"})
    return fig

def basic_bullet_charts():
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta",
        gauge={'shape': "bullet"},
        value=220,
        delta={'reference': 300},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Profit"}))
    fig.update_layout(height=250)
    return fig

def add_steps_and_threshold():
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta", value=220,
        domain={'x': [0.1, 1], 'y': [0, 1]},
        title={'text': "<b>Profit</b>"},
        delta={'reference': 200},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 300]},
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75,
                'value': 280},
            'steps': [
                {'range': [0, 150], 'color': "lightgray"},
                {'range': [150, 250], 'color': "gray"}]}))
    fig.update_layout(height=250)
    return fig

def custom_bullet():
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta", value=220,
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={'reference': 280, 'position': "top"},
        title={'text': "<b>Profit</b><br><span style='color: gray; font-size:0.8em'>U.S. $</span>",
               'font': {"size": 14}},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 300]},
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75, 'value': 270},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 150], 'color': "cyan"},
                {'range': [150, 250], 'color': "royalblue"}],
            'bar': {'color': "darkblue"}}))
    fig.update_layout(height=250)
    return fig

def multi_bullet():
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number+gauge+delta", value=180,
        delta={'reference': 200},
        domain={'x': [0.25, 1], 'y': [0.08, 0.25]},
        title={'text': "Revenue"},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 300]},
            'threshold': {
                'line': {'color': "black", 'width': 2},
                'thickness': 0.75,
                'value': 170},
            'steps': [
                {'range': [0, 150], 'color': "gray"},
                {'range': [150, 250], 'color': "lightgray"}],
            'bar': {'color': "black"}}))

    fig.add_trace(go.Indicator(
        mode="number+gauge+delta", value=35,
        delta={'reference': 200},
        domain={'x': [0.25, 1], 'y': [0.4, 0.6]},
        title={'text': "Profit"},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 100]},
            'threshold': {
                'line': {'color': "black", 'width': 2},
                'thickness': 0.75,
                'value': 50},
            'steps': [
                {'range': [0, 25], 'color': "gray"},
                {'range': [25, 75], 'color': "lightgray"}],
            'bar': {'color': "black"}}))

    fig.add_trace(go.Indicator(
        mode="number+gauge+delta", value=220,
        delta={'reference': 200},
        domain={'x': [0.25, 1], 'y': [0.7, 0.9]},
        title={'text': "Satisfaction"},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 300]},
            'threshold': {
                'line': {'color': "black", 'width': 2},
                'thickness': 0.75,
                'value': 210},
            'steps': [
                {'range': [0, 150], 'color': "gray"},
                {'range': [150, 250], 'color': "lightgray"}],
            'bar': {'color': "black"}}))
    fig.update_layout(height=400, margin={'t': 0, 'b': 0, 'l': 0})
    return fig

def table_and_chart_subplots():
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/Mining-BTC-180.csv")

    for i, row in enumerate(df["Date"]):
        p = re.compile(" 00:00:00")
        datetime = p.split(df["Date"][i])[0]
        df.iloc[i, 1] = datetime

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}],
               [{"type": "scatter"}],
               [{"type": "scatter"}]]
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Mining-revenue-USD"],
            mode="lines",
            name="mining revenue"
        ),
        row=3, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Hash-rate"],
            mode="lines",
            name="hash-rate-TH/s"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Date", "Number<br>Transactions", "Output<br>Volume (BTC)",
                        "Market<br>Price", "Hash<br>Rate", "Cost per<br>trans-USD",
                        "Mining<br>Revenue-USD", "Trasaction<br>fees-BTC"],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[df[k].tolist() for k in df.columns[1:]],
                align="left")
        ),
        row=1, col=1
    )
    fig.update_layout(
        height=800,
        showlegend=False,
        title_text="Bitcoin mining stats for 180 days",
    )
    return fig

def horizontal_table_and_chart():
    table_data = [['Team', 'Wins', 'Losses', 'Ties'],
                  ['Montréal<br>Canadiens', 18, 4, 0],
                  ['Dallas Stars', 18, 5, 0],
                  ['NY Rangers', 16, 5, 0],
                  ['Boston<br>Bruins', 13, 8, 0],
                  ['Chicago<br>Blackhawks', 13, 8, 0],
                  ['LA Kings', 13, 8, 0],
                  ['Ottawa<br>Senators', 12, 5, 0]]

    fig = ff.create_table(table_data, height_constant=60)

    teams = ['Montréal Canadiens', 'Dallas Stars', 'NY Rangers',
             'Boston Bruins', 'Chicago Blackhawks', 'LA Kings', 'Ottawa Senators']
    GFPG = [3.54, 3.48, 3.0, 3.27, 2.83, 2.45, 3.18]
    GAPG = [2.17, 2.57, 2.0, 2.91, 2.57, 2.14, 2.77]

    trace1 = go.Scatter(x=teams, y=GFPG,
                        marker=dict(color='#0099ff'),
                        name='Goals For<br>Per Game',
                        xaxis='x2', yaxis='y2')
    trace2 = go.Scatter(x=teams, y=GAPG,
                        marker=dict(color='#404040'),
                        name='Goals Against<br>Per Game',
                        xaxis='x2', yaxis='y2')

    fig.add_traces([trace1, trace2])

    # initialize xaxis2 and yaxis2
    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}

    # Edit layout for subplots
    fig.layout.xaxis.update({'domain': [0, .5]})
    fig.layout.xaxis2.update({'domain': [0.6, 1.]})

    # The graph's yaxis MUST BE anchored to the graph's xaxis
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.yaxis2.update({'title': 'Goals'})

    # Update the margins to add a title and see graph x-labels.
    fig.layout.margin.update({'t': 50, 'b': 100})
    fig.layout.update({'title': '2016 Hockey Stats'})
    return fig

def vertical_table_and_chart():
    # Add table data
    table_data = [['Team', 'Wins', 'Losses', 'Ties'],
                  ['Montréal<br>Canadiens', 18, 4, 0],
                  ['Dallas Stars', 18, 5, 0],
                  ['NY Rangers', 16, 5, 0],
                  ['Boston<br>Bruins', 13, 8, 0],
                  ['Chicago<br>Blackhawks', 13, 8, 0],
                  ['Ottawa<br>Senators', 12, 5, 0]]

    # Initialize a figure with ff.create_table(table_data)
    fig = ff.create_table(table_data, height_constant=60)

    # Add graph data
    teams = ['Montréal Canadiens', 'Dallas Stars', 'NY Rangers',
             'Boston Bruins', 'Chicago Blackhawks', 'Ottawa Senators']
    GFPG = [3.54, 3.48, 3.0, 3.27, 2.83, 3.18]
    GAPG = [2.17, 2.57, 2.0, 2.91, 2.57, 2.77]

    # Make traces for graph
    trace1 = go.Bar(x=teams, y=GFPG, xaxis='x2', yaxis='y2',
                    marker=dict(color='#0099ff'),
                    name='Goals For<br>Per Game')
    trace2 = go.Bar(x=teams, y=GAPG, xaxis='x2', yaxis='y2',
                    marker=dict(color='#404040'),
                    name='Goals Against<br>Per Game')

    # Add trace data to figure
    fig.add_traces([trace1, trace2])

    # initialize xaxis2 and yaxis2
    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}

    # Edit layout for subplots
    fig.layout.yaxis.update({'domain': [0, .45]})
    fig.layout.yaxis2.update({'domain': [.6, 1]})

    # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})
    fig.layout.yaxis2.update({'title': 'Goals'})

    # Update the margins to add a title and see graph x-labels.
    fig.layout.margin.update({'t': 75, 'l': 50})
    fig.layout.update({'title': '2016 Hockey Stats'})

    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    fig.layout.update({'height': 800})
    return fig

def update_button():
    # Load dataset
    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    df.columns = [col.replace("AAPL.", "") for col in df.columns]

    # Initialize figure
    fig = go.Figure()

    # Add Traces

    fig.add_trace(
        go.Scatter(x=list(df.index),
                   y=list(df.High),
                   name="High",
                   line=dict(color="#33CFA5")))

    fig.add_trace(
        go.Scatter(x=list(df.index),
                   y=[df.High.mean()] * len(df.index),
                   name="High Average",
                   visible=False,
                   line=dict(color="#33CFA5", dash="dash")))

    fig.add_trace(
        go.Scatter(x=list(df.index),
                   y=list(df.Low),
                   name="Low",
                   line=dict(color="#F06A6A")))

    fig.add_trace(
        go.Scatter(x=list(df.index),
                   y=[df.Low.mean()] * len(df.index),
                   name="Low Average",
                   visible=False,
                   line=dict(color="#F06A6A", dash="dash")))

    # Add Annotations and Buttons
    high_annotations = [dict(x="2016-03-01",
                             y=df.High.mean(),
                             xref="x", yref="y",
                             text="High Average:<br> %.2f" % df.High.mean(),
                             ax=0, ay=-40),
                        dict(x=df.High.idxmax(),
                             y=df.High.max(),
                             xref="x", yref="y",
                             text="High Max:<br> %.2f" % df.High.max(),
                             ax=0, ay=-40)]
    low_annotations = [dict(x="2015-05-01",
                            y=df.Low.mean(),
                            xref="x", yref="y",
                            text="Low Average:<br> %.2f" % df.Low.mean(),
                            ax=-40, ay=40),
                       dict(x=df.High.idxmin(),
                            y=df.Low.min(),
                            xref="x", yref="y",
                            text="Low Min:<br> %.2f" % df.Low.min(),
                            ax=0, ay=40)]

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                active=0,
                x=0.57,
                y=1.2,
                buttons=list([
                    dict(label="None",
                         method="update",
                         args=[{"visible": [True, False, True, False]},
                               {"title": "Yahoo",
                                "annotations": []}]),
                    dict(label="High",
                         method="update",
                         args=[{"visible": [True, True, False, False]},
                               {"title": "Yahoo High",
                                "annotations": high_annotations}]),
                    dict(label="Low",
                         method="update",
                         args=[{"visible": [False, False, True, True]},
                               {"title": "Yahoo Low",
                                "annotations": low_annotations}]),
                    dict(label="Both",
                         method="update",
                         args=[{"visible": [True, True, True, True]},
                               {"title": "Yahoo",
                                "annotations": high_annotations + low_annotations}]),
                ]),
            )
        ])

    # Set title
    fig.update_layout(
        title_text="Yahoo",
        xaxis_domain=[0.05, 1.0]
    )
    return fig

def simple_slider_control():
    # Create figure
    fig = go.Figure()

    # Add traces, one for each slider step
    for step in np.arange(0, 5, 0.1):
        fig.add_trace(
            go.Scatter(
                visible=False,
                line=dict(color="#00CED1", width=6),
                name="𝜈 = " + str(step),
                x=np.arange(0, 10, 0.01),
                y=np.sin(step * np.arange(0, 10, 0.01))))

    # Make 10th trace visible
    fig.data[10].visible = True

    # Create and add slider
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="restyle",
            args=["visible", [False] * len(fig.data)],
        )
        step["args"][1][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=10,
        currentvalue={"prefix": "Frequency: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders
    )
    return fig

def update_dropdown():
    # Load dataset
    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    df.columns = [col.replace("AAPL.", "") for col in df.columns]

    # Initialize figure
    fig = go.Figure()

    # Add Traces

    fig.add_trace(
        go.Scatter(x=list(df.index),
                   y=list(df.High),
                   name="High",
                   line=dict(color="#33CFA5")))

    fig.add_trace(
        go.Scatter(x=list(df.index),
                   y=[df.High.mean()] * len(df.index),
                   name="High Average",
                   visible=False,
                   line=dict(color="#33CFA5", dash="dash")))

    fig.add_trace(
        go.Scatter(x=list(df.index),
                   y=list(df.Low),
                   name="Low",
                   line=dict(color="#F06A6A")))

    fig.add_trace(
        go.Scatter(x=list(df.index),
                   y=[df.Low.mean()] * len(df.index),
                   name="Low Average",
                   visible=False,
                   line=dict(color="#F06A6A", dash="dash")))

    # Add Annotations and Buttons
    high_annotations = [dict(x="2016-03-01",
                             y=df.High.mean(),
                             xref="x", yref="y",
                             text="High Average:<br> %.3f" % df.High.mean(),
                             ax=0, ay=-40),
                        dict(x=df.High.idxmax(),
                             y=df.High.max(),
                             xref="x", yref="y",
                             text="High Max:<br> %.3f" % df.High.max(),
                             ax=0, ay=-40)]
    low_annotations = [dict(x="2015-05-01",
                            y=df.Low.mean(),
                            xref="x", yref="y",
                            text="Low Average:<br> %.3f" % df.Low.mean(),
                            ax=0, ay=40),
                       dict(x=df.High.idxmin(),
                            y=df.Low.min(),
                            xref="x", yref="y",
                            text="Low Min:<br> %.3f" % df.Low.min(),
                            ax=0, ay=40)]

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="None",
                         method="update",
                         args=[{"visible": [True, False, True, False]},
                               {"title": "Yahoo",
                                "annotations": []}]),
                    dict(label="High",
                         method="update",
                         args=[{"visible": [True, True, False, False]},
                               {"title": "Yahoo High",
                                "annotations": high_annotations}]),
                    dict(label="Low",
                         method="update",
                         args=[{"visible": [False, False, True, True]},
                               {"title": "Yahoo Low",
                                "annotations": low_annotations}]),
                    dict(label="Both",
                         method="update",
                         args=[{"visible": [True, True, True, True]},
                               {"title": "Yahoo",
                                "annotations": high_annotations + low_annotations}]),
                ]),
            )
        ])

    # Set title
    fig.update_layout(title_text="Yahoo")
    return fig

def basic_range_slider_and_range_selectors():
    # Load data
    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    df.columns = [col.replace("AAPL.", "") for col in df.columns]

    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=list(df.Date), y=list(df.High)))

    # Set title
    fig.update_layout(
        title_text="Time series with range slider and selectors"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig
