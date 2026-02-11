import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Step 1: Load the CSV file
file_path = 'C:/Users/LuzHu/Desktop/6级频率表归一化.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Step 2: Remove the diagonal elements by setting them to zero
data_without_self = data.copy()
for index in data.index:
    group = data.loc[index, 'Unnamed: 0']
    data_without_self.loc[index, group] = 0

# Step 3: Normalize the data for each group
normalized_data = data_without_self.copy()
categories = data.columns[1:]  # Define the categories
for index in normalized_data.index:
    total = normalized_data.loc[index, categories].sum()
    for category in categories:
        normalized_data.loc[index, category] = normalized_data.loc[index, category] / total

# Step 4: Define the color palette
base_colors = ['#EA1F1F', '#E88421', '#E5C923', '#FFF924', '#9DEF1B', '#42D726', '#449657', '#4CCCB3', '#369BA8', '#2B7EBC', '#3626D1', '#A128CE', '#999999']
num_categories = len(categories)

if num_categories > len(base_colors):
    cmap = plt.get_cmap('tab20', num_categories)  # Use 'tab20' colormap to generate more colors
    colors = [cmap(i) for i in range(num_categories)]
    colors = [f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}' for r, g, b, _ in colors]  # Convert to hex
else:
    colors = base_colors

# Step 5: Plot the normalized stacked bar chart with specified colors using Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
bottom = np.zeros(len(normalized_data))
for i, category in enumerate(categories):
    ax.bar(normalized_data['Unnamed: 0'], normalized_data[category], bottom=bottom, label=category, color=colors[i % len(colors)])
    bottom += normalized_data[category].values
ax.set_xlabel('Group')
ax.set_ylabel('Proportion')
ax.set_title('Normalized Comparison of Group Composition')
ax.legend(title='Group', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(False)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 6: Plot the normalized stacked bar chart with specified colors using Plotly
fig = go.Figure()

for i, category in enumerate(categories):
    fig.add_trace(go.Bar(
        x=normalized_data['Unnamed: 0'],
        y=normalized_data[category],
        name=category,
        marker_color=colors[i % len(colors)]
    ))

fig.update_layout(
    barmode='stack',
    xaxis_title='Group',
    yaxis_title='Proportion',
    title='Normalized Comparison of Group Composition',
    legend_title='Group'
)

fig.show()