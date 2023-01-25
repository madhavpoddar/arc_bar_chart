import math
import numpy as np

from bokeh.models import ColumnDataSource
from bokeh.models import Legend, LegendItem, HoverTool
from bokeh.plotting import figure


def circular_bar_chart(df, countries, countries_superset, colors):

    df_t = df[df["date"] == df["date"].max()]
    max_radius = df_t[df_t["location"].isin(countries_superset)]["population"].max()
    p = figure(
        height=550,
        # width=500,
        title="Circular bar chart: Displays both absolute(arc length) and relative(angle) measure",
        x_axis_label="population",
        y_axis_label="population",
        x_range=(-max_radius * 1.3, max_radius * 1.3),
        y_range=(-max_radius * 1.3, max_radius * 1.3),
    )

    glyphs = {}
    for i in range(len(countries_superset)):
        source = ColumnDataSource(df_t[df_t["location"] == countries_superset[i]])
        glyphs[countries_superset[i]] = p.arc(
            x=0,
            y=0,
            radius="population",
            start_angle=0.0,
            end_angle="people_fully_vaccinated_angle",
            source=source,
            line_color=colors[i],
            line_width=3,
            # legend_label=countries[i],
        )
        glyphs[countries_superset[i]].visible = countries_superset[i] in countries
    
    legend_items = [LegendItem(label=country, renderers=[glyphs[country]]) for country in countries]
    p.add_layout(Legend(items=legend_items))

    for theta in np.arange(0, math.pi * 2, math.pi / 10):
        p.line(
            x=[0, max_radius * 1.15 * math.cos(theta)],
            y=[0, max_radius * 1.15 * math.sin(theta)],
            color="lightgray",
            level="underlay",
        )
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.axis.visible = False

    p.legend.location = "bottom_right"

    return p, glyphs
