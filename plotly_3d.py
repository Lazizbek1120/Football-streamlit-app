import plotly.graph_objects as go

def generate_3d(layout):
    fig = go.Figure()

    x_start = 0
    for room in layout:
        fig.add_trace(go.Mesh3d(
            x=[x_start, x_start+room["width"], x_start+room["width"], x_start],
            y=[0, 0, room["height"], room["height"]],
            z=[0, 0, 0, 0],
            opacity=0.5
        ))
        x_start += room["width"]

    return fig