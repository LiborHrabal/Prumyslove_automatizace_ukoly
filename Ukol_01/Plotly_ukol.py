# Create 3D graf with plottlz
# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go

PATH = "datasets\\robot_imu_comparison\\sens1_01_trajectory.csv"
# Load the robotic_arm dataset
dataset = pd.read_csv(PATH)

#Create 3D scatter plot
fig = go.Scatter3d( 
    x=dataset['x'],
    y=dataset['y'],
    z=dataset['z'],
    mode='markers+lines',
    marker=dict(size=3, color=dataset['z'], colorscale='Plasma', opacity=0.9, colorbar=dict(title='z')),
    line=dict(width=1, color='gray')
)

fig = go.Figure(data=[fig])
fig.update_layout(
    scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'),
    title='3D scatter (graph_objects)',
    margin=dict(l=0, r=0, b=0, t=40)
)

fig.show()
fig.write_html("Plotly_grapf.html")
