#######################
### Import Packages ###
#######################

import pandas as pd
import altair as alt

######################
### Plot Histogram ###
######################

def get_genera_plot(effective_df, subtitle, most_common = True, fig_num = -1) :
    """
    Returns a histogram of the number of trees per genus.

    Parameters
    __________
    effective_df: pandas.core.frame.DataFrame
        the dataframe to plot, must have column
        * `genus_name` representing the genus of the tree
    subtitle: str
        the subtitle of the plot
    most_common: bool, optional
        whether to plot the most common genera or the least common genera
    fig_num: int, optional
        the figure number of the plot

    Returns
    _______
    altair.vegalite.v3.api.Chart
        an Altair concatenated histogram
    next_num: int
        the figure number of the subsequent plot
    """

    if 'genus_name' not in effective_df.columns :
        raise ValueError('The dataframe must have a column `genus_name`.')

    if fig_num == -1 :
        plot_title = ' '
    else :
        plot_title = f'Figure {fig_num}'

    effective_genera = sorted(
        effective_df.groupby('genus_name')
        .size().sort_values(ascending = not(most_common))
        .head(10).index.tolist()
    )

    primary_occurrences = 'Most Common' if most_common else 'Least Common'
    secondary_occurrences = 'Least Common' if most_common else 'Most Common'

    plot_df = effective_df[
        effective_df['genus_name'].isin(effective_genera)
    ]

    plot_df = plot_df.assign(
        total_trees = len(effective_df)
    )

    genera_plot = alt.Chart(
        plot_df, title = alt.TitleParams(
            text = plot_title, subtitle = subtitle,
            anchor = 'start', fontSize = 25, subtitleFontSize = 20
        )
    ).transform_calculate(
        occurrences = alt.expr.if_(
            any(genus == alt.datum.genus_name for genus in effective_genera),
            primary_occurrences, secondary_occurrences
        ), pct = 1 / alt.datum.total_trees
    ).mark_bar().encode(
        x = alt.X('count():Q', title = 'Number of Trees'),
        y = alt.Y('genus_name:N', sort = '-x', title = 'Genus Name'),
        color = alt.Color(
            'occurrences:N', scale = alt.Scale(
                domain = ['Most Common', 'Least Common'],
                range = ['#1E90FF', '#FFA500']
            ), legend = None
        ),
        tooltip = [
            alt.Tooltip('count():Q', title = 'Number of Trees'),
            alt.Tooltip('sum(pct):Q', format = '.2%', formatType = 'number', title = '% of Total Trees')
        ]
    )

    return genera_plot, fig_num + 1