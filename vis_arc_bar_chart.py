import numpy as np
import pandas as pd
from bokeh.palettes import Category10 as palette
from bokeh.models import ColumnDataSource, Label, LabelSet
from bokeh.plotting import figure


def arc_bar_chart(
    df: pd.DataFrame,
    absolute_values_col_name: str,
    total_values_col_name: str,
    id_col_name: str,
    title: str = "Arc Bar Chart",
    absolute_values_spiral_grid_lines_visibility: bool = False,
    relative_values_radial_grid_lines_visibility: bool = True,
    total_values_circular_grid_lines_visibility: bool = False,
):

    padding = 0.3
    major_tick_interval = 1e8

    colors = palette[len(df.index)]

    #
    # Generating the figure
    #
    max_total_value = df[total_values_col_name].max()
    max_radius = max_total_value * (1 + padding)
    max_radius_plot = max_radius * 1.25
    p = figure(
        height=700,
        width=700,
        title=title,
        # x_axis_label="population", # Bokeh is not showing axis label in middle of chart
        x_range=(-max_radius_plot, max_radius_plot),
        y_range=(-max_radius_plot, max_radius_plot),
    )
    p.yaxis.visible = False
    p.xaxis.fixed_location = 0
    p.xaxis.bounds = (0, max_radius)
    p.xgrid.visible = False
    p.ygrid.visible = False
    # Adding x-axis label manually
    xaxis_label = Label(
        x=max_radius * 0.4, y=-max_radius * 0.15, text=total_values_col_name
    )
    p.add_layout(xaxis_label)

    #
    # Drawing grid lines
    #
    grid_line_color = "#e5e5e5"
    minor_tick_interval = major_tick_interval / 5
    if relative_values_radial_grid_lines_visibility:
        # tick for every 5 percent
        angular_ticks_values = np.arange(0, np.pi * 2, np.pi / 10)
        p.segment(
            x0=0,
            y0=0,
            x1=[max_radius * np.cos(theta) for theta in angular_ticks_values],
            y1=[max_radius * np.sin(theta) for theta in angular_ticks_values],
            color=grid_line_color,
            level="underlay",
        )
        angle_tick_labels_cds = ColumnDataSource(
            data=dict(
                x=[max_radius * 1.03 * np.cos(theta) for theta in angular_ticks_values],
                y=[max_radius * 1.03 * np.sin(theta) for theta in angular_ticks_values],
                angle=angular_ticks_values,
                text=[
                    "{:.2f}".format(value)
                    for value in (angular_ticks_values * 0.5 / np.pi)
                ],
            )
        )
        angle_tick_labels = LabelSet(
            source=angle_tick_labels_cds,
            x="x",
            y="y",
            text="text",
            angle="angle",
            x_offset=0,
            y_offset=0,
            render_mode="canvas",
        )
        p.add_layout(angle_tick_labels)

    if total_values_circular_grid_lines_visibility:
        x_major_ticks_values = np.arange(
            major_tick_interval, max_radius, major_tick_interval
        )
        p.ellipse(
            x=0,
            y=0,
            width=x_major_ticks_values * 2,
            height=x_major_ticks_values * 2,
            line_color=grid_line_color,
            fill_color=None,
            level="underlay",
        )
    if absolute_values_spiral_grid_lines_visibility:
        resolution = 3600
        angles = np.arange(
            np.pi * 2 / resolution,
            np.pi * 2 + np.pi * 2 / resolution,
            np.pi * 2 / resolution,
        )
        tick_radii = np.arange(minor_tick_interval, max_radius, minor_tick_interval)
        p.multi_line(
            xs=[
                [(tr * 2 * np.pi * np.cos(theta)) / theta for theta in angles]
                for tr in tick_radii
            ],
            ys=[
                [(tr * 2 * np.pi * np.sin(theta)) / theta for theta in angles]
                for tr in tick_radii
            ],
            line_color=grid_line_color,
            level="underlay",
        )
        # trimming the spirals to bound it within the polar coordinate circle
        p.multi_polygons(
            xs=[
                [
                    [
                        [
                            -max_radius_plot,
                            max_radius_plot,
                            max_radius_plot,
                            -max_radius_plot,
                        ],
                        [max_radius * np.cos(theta) for theta in angles],
                    ]
                ]
            ],
            ys=[
                [
                    [
                        [
                            -max_radius_plot,
                            -max_radius_plot,
                            max_radius_plot,
                            max_radius_plot,
                        ],
                        [max_radius * np.sin(theta) for theta in angles],
                    ]
                ]
            ],
            fill_color="white",
            line_color=None,
            level="underlay",
        )

    fractional_values_angles_dfs = (
        df[absolute_values_col_name] / df[total_values_col_name]
    ) * (2 * np.pi)
    fractional_values_x_dfs = df[total_values_col_name] * np.cos(
        fractional_values_angles_dfs
    )
    fractional_values_y_dfs = df[total_values_col_name] * np.sin(
        fractional_values_angles_dfs
    )
    lollipop_arc_cds = ColumnDataSource(
        data=dict(
            radius=df[total_values_col_name].tolist(),
            end_angle=fractional_values_angles_dfs.tolist(),
            line_color=colors,
            legend_field=df[id_col_name].tolist(),
        )
    )
    p.arc(
        source=lollipop_arc_cds,
        radius="radius",
        end_angle="end_angle",
        line_color="line_color",
        legend_field="legend_field",
        x=0,
        y=0,
        start_angle=0.0,
        line_width=3,
    )
    lollipop_arc_gaps_angles = np.concatenate(
        [
            np.arange(
                minor_tick_interval * (2 * np.pi) / r,
                orig_end_angle,
                minor_tick_interval * (2 * np.pi) / r,
            )
            for (r, orig_end_angle) in zip(
                df[total_values_col_name].tolist(),
                fractional_values_angles_dfs.tolist(),
            )
        ]
    )
    lollipop_arc_gaps_radius = np.concatenate(
        [
            [r]
            * len(
                np.arange(
                    minor_tick_interval * (2 * np.pi) / r,
                    orig_end_angle,
                    minor_tick_interval * (2 * np.pi) / r,
                )
            )
            for (r, orig_end_angle) in zip(
                df[total_values_col_name].tolist(),
                fractional_values_angles_dfs.tolist(),
            )
        ]
    )
    lollipop_arc_gaps_labels = np.concatenate(
        [
            [id]
            * len(
                np.arange(
                    minor_tick_interval * (2 * np.pi) / r,
                    orig_end_angle,
                    minor_tick_interval * (2 * np.pi) / r,
                )
            )
            for (id, r, orig_end_angle) in zip(
                df[id_col_name].tolist(),
                df[total_values_col_name].tolist(),
                fractional_values_angles_dfs.tolist(),
            )
        ]
    )

    lollipop_arc_gaps_cds = ColumnDataSource(
        data=dict(
            x=lollipop_arc_gaps_radius * np.cos(lollipop_arc_gaps_angles),
            y=lollipop_arc_gaps_radius * np.sin(lollipop_arc_gaps_angles),
            legend_field=lollipop_arc_gaps_labels,
        )
    )
    p.circle(
        source=lollipop_arc_gaps_cds,
        x="x",
        y="y",
        legend_field="legend_field",
        fill_color="white",
        line_color="white",
        size=5,
    )
    lollipop_circles_cds = ColumnDataSource(
        data=dict(
            x=fractional_values_x_dfs.tolist(),
            y=fractional_values_y_dfs.tolist(),
            fill_color=colors,
            line_color=colors,
            legend_field=df[id_col_name].tolist(),
        )
    )
    p.circle(
        source=lollipop_circles_cds,
        x="x",
        y="y",
        fill_color="fill_color",
        line_color="line_color",
        legend_field="legend_field",
        size=7,
    )

    #
    # Outer ring
    #
    p.ellipse(
        x=0,
        y=0,
        width=[max_radius * 2, max_radius * 1.02 * 2],
        height=[max_radius * 2, max_radius * 1.02 * 2],
        line_color=grid_line_color,
        fill_color=None,
        level="underlay",
    )
    fractional_values_x_outer_ring_dfs = (max_radius * 1.01) * np.cos(
        fractional_values_angles_dfs
    )
    fractional_values_y_outer_ring_dfs = (max_radius * 1.01) * np.sin(
        fractional_values_angles_dfs
    )
    outer_ring_circles_cds = ColumnDataSource(
        data=dict(
            x=fractional_values_x_outer_ring_dfs.tolist(),
            y=fractional_values_y_outer_ring_dfs.tolist(),
            fill_color=colors,
            line_color=colors,
            legend_field=df[id_col_name].tolist(),
        )
    )
    p.circle(
        source=outer_ring_circles_cds,
        x="x",
        y="y",
        fill_color="fill_color",
        line_color="line_color",
        legend_field="legend_field",
        size=7,
    )
    outer_ring_dotted_lines_cds = ColumnDataSource(
        data=dict(
            x0=fractional_values_x_dfs.tolist(),
            y0=fractional_values_y_dfs.tolist(),
            x1=fractional_values_x_outer_ring_dfs.tolist(),
            y1=fractional_values_y_outer_ring_dfs.tolist(),
            line_color=colors,
            legend_field=df[id_col_name].tolist(),
        )
    )
    p.segment(
        source=outer_ring_dotted_lines_cds,
        x0="x0",
        y0="y0",
        x1="x1",
        y1="y1",
        line_color="line_color",
        legend_field="legend_field",
        line_dash="dotted",
        alpha=0.5,
    )

    return p
