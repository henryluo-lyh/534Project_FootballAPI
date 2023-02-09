import plotly.graph_objects as go
import plotly.offline as pyo
import altair as alt

def vis_radar(vis_df):
    name_1= vis_df.iloc[0,0]
    name_2 = vis_df.iloc[1,0]
    stats = list(set(vis_df["stats"]))
    stats.sort()
    stats_1 = vis_df.query("`player.lastname` == '{}'".format(name_1))["value"].tolist()
    stats_2 = vis_df.query("`player.lastname` == '{}'".format(name_2))["value"].tolist()

    # stats_1_norm = [float(i)/max(stats_1) for i in stats_1]
    # stats_2_norm = [float(i)/max(stats_2) for i in stats_2]
    categories = stats
    categories = [*categories, categories[0]]

    player_1 = stats_1
    player_2 = stats_2
    player_1 = [*player_1, player_1[0]]
    player_2 = [*player_2, player_2[0]]


    fig = go.Figure(
        data=[
            go.Scatterpolar(r=player_1, theta=categories, fill='toself', name=name_1),
            go.Scatterpolar(r=player_2, theta=categories, fill='toself', name=name_2)
        ],
        layout=go.Layout(
            title=go.layout.Title(text='player comparison'),
            polar={'radialaxis': {'visible': True}},
            showlegend=True
        )
    )

    pyo.plot(fig)
    
    
def vis_bar(vis_df):

    plot = alt.Chart(vis_df).mark_bar(opacity=0.4).encode(
        alt.X('value:Q', stack=False),
        alt.Y('stats:N'),
        alt.Color('player\.lastname:N', title='player'))
    return plot