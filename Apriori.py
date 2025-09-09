import pandas as pd
from itertools import combinations
from collections import defaultdict
from colorama import init, Fore, Style
import plotly.graph_objects as go
import plotly.io as pio

#######################################################################################################################################################################################################
#
#                 Apriori and Association Rules without the need of mlxtend
#
#                         python3 -m pip install colorama
#                         - Load a RansomAtlas_v1.0.xls containing Name, TTPs
#                         - Calculate frequency of each group of TTPs if the group contains at least 4 members ( groups of 4, 5, 6....)
#                         - Export in Apriori_Asso_Rules_common_ttp_groups_control_file.html the proofs of appearance and frequency
#                         - Export in Apriori_Asso_Rules_sorted_FINAL.html the summary without details of all the TTP groups along with number of occurrences and frequency
#
#######################################################################################################################################################################################################

# Initialize colorama
init(autoreset=True)

# Load the dataset
file_path = 'RansomAtlas_v1.0.xlsx'
df = pd.read_excel(file_path)

# Initialize dictionary for TTP group frequencies
ttp_group_freq = defaultdict(int)

# Add an ID column based on the index
df['ID'] = df.index + 1

# Create a list to store sorted TTPs and a dictionary to store TTPs with their IDs and Names
ttps_list = []
row_info = {}


for _, row in df.iterrows():
    ttps = row['TTPs']
    if isinstance(ttps, str):
        sorted_row = sorted(ttps.split(', '))
    else:
        sorted_row = []
    ttps_list.append(sorted_row)
    row_info[row['ID']] = {'Name': row['Name'], 'TTPs': sorted_row}


# Create a dictionary to store common TTPs
common_ttp_dict = defaultdict(list)

# Compare each sorted_row with others to find common items
for i, row1 in enumerate(ttps_list):
    for j, row2 in enumerate(ttps_list):
        if i != j:
            common_items = set(row1).intersection(set(row2))
            if len(common_items) >= 4:  # Only consider if 4 or more items are common
                common_ttp_dict[tuple(common_items)].append((df.iloc[i]['ID'], df.iloc[j]['ID']))

# Function to highlight common items
def highlight_common_items(row_ttp, common_items):
    highlighted_row = []
    for item in row_ttp:
        if item in common_items:
            highlighted_row.append(f'<span style="color:red; font-weight:bold;">{item}</span>')
        else:
            highlighted_row.append(item)
    return highlighted_row

# Calculate occurrences and frequency percentage for each TTP group
for common_items in common_ttp_dict.keys():
    occurrences = len(set([id_pair[0] for id_pair in common_ttp_dict[common_items]]))  # Count unique IDs only
    frequency_percentage = (occurrences / len(df)) * 100
    ttp_group_freq[common_items] = (occurrences, frequency_percentage)

# Sort the TTP groups by frequency (lower frequency first)
sorted_ttp_groups = sorted(ttp_group_freq.items(), key=lambda x: x[1][1])

# Generate HTML content for the rows with common items
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Common TTP Groups</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .scrollable {
            max-height: 800px; /* Increase the height */
            overflow-y: scroll;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 20px;
        }
        .highlight {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Common TTP Groups</h1>
    <div class="scrollable">
"""

for common_items, (occurrences, frequency_percentage) in sorted_ttp_groups:
    html_content += f"<h2><span style='font-weight:bold;'>TTP Group:</span> <span style='color:red; font-weight:bold;'>{', '.join(common_items)}</span> (<span style='font-weight:bold;'>{occurrences} occurrences, {frequency_percentage:.2f}%</span>)</h2>"
    for id1, id2 in common_ttp_dict[common_items]:
        highlighted_ttp1 = highlight_common_items(row_info[id1]['TTPs'], common_items)
        highlighted_ttp2 = highlight_common_items(row_info[id2]['TTPs'], common_items)
        html_content += f"<p>ID: {id1}, Name: {row_info[id1]['Name']}, TTPs: {', '.join(highlighted_ttp1)}</p>"
        html_content += f"<p>ID: {id2}, Name: {row_info[id2]['Name']}, TTPs: {', '.join(highlighted_ttp2)}</p>"
        html_content += "<hr>"

html_content += """
    </div>
</body>
</html>
"""

# Save the HTML content to a file
with open("Apriori_Asso_Rules_common_ttp_groups_control_file.html", "w") as file:
    file.write(html_content)

print("The common TTP groups have been exported to Apriori_Asso_Rules_common_ttp_groups_control_file.html")

# Create another HTML named Apriori_Asso_sorted.html to display TTP groups sorted by frequency
html_content_sorted = """
<!DOCTYPE html>
<html>
<head>
    <title>Apriori Association Rules - Sorted by Frequency</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .scrollable {
            max-height: 800px; /* Increase the height */
            overflow-y: scroll;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Apriori Association Rules - Sorted by Frequency</h1>
    <div class="scrollable">
"""

for ttp_group, (occurrences, frequency_percentage) in sorted_ttp_groups:
    html_content_sorted += f"<p><span style='font-weight:bold;'>TTP Group:</span> <span style='color:red; font-weight:bold;'>{', '.join(ttp_group)}</span> (<span style='font-weight:bold;'>{occurrences} occurrences, {frequency_percentage:.2f}%</span>)</p>"
    html_content_sorted += "<hr>"

html_content_sorted += """
    </div>
</body>
</html>
"""

# Save the sorted HTML content to a file
with open("Apriori_Asso_Rules_sorted_FINAL.html", "w") as file:
    file.write(html_content_sorted)

print("The sorted TTP groups have been exported to Apriori_Asso_Rules_sorted_FINAL.html")

# Define pastel colors for different values and TTPs
#colors = ['#FFB6C1', '#87CEFA', '#98FB98', '#FFD700', '#FFA07A', '#9370DB', '#FF69B4', '#B0E0E6', '#FF6347', '#40E0D0']
colors = [
    '#00FFC6', '#3EB489', '#08E8DE', '#3EFFFF', '#00BFFF',
    '#9D00FF', '#8A2BE2', '#FF1493', '#FF00C8', '#FC0FC0',
    '#FF69B4', '#FF355E', '#FFA500', '#FFFF66', '#FFD300',
    '#FDFF00', '#B0FF1A', '#00FFEF', '#00FFFF', '#00BFFF',
]

# Extract stages and values from sorted_ttp_groups for the funnel graph
stages = [', '.join(group) for group, _ in sorted_ttp_groups]
values = [occurrences for _, (occurrences, _) in sorted_ttp_groups]

# Create a color map for occurrences
occurrence_colors = {occurrence: colors[i % len(colors)] for i, occurrence in enumerate(sorted(set(values)))}

# Create the funnel graph
fig = go.Figure(go.Funnel(
    y=stages,
    x=values,
    textinfo="value+label",
    texttemplate="%{value} occurrences",
    #texttemplate="%{value} occurrences (%{percent:.2f}%)",
    marker=dict(color=[occurrence_colors[occurrence] for occurrence in values], line=dict(width=0))
))

# Update the layout for better visualization

fig.update_layout(
    title=dict(
        text='Repartition of TTP groups sorted by frequency of appearance in ransomware campaigns',
        font=dict(size=18)  # Set title font size higher than 12
    ),
    width=1700,  # Increase the width of the graph
    legend=dict(
        title="TTP Legend",
        orientation="h",
        yanchor="bottom",
        y=-1.2,  # Place the legend further down the graph
        xanchor="center",
        x=0.5,
        traceorder='normal',
        tracegroupgap=10,
        itemclick=False,
        itemdoubleclick=False,
        itemsizing='constant',
        font=dict(size=8),
        #bgcolor='rgba(0,0,0,0)'
		 bgcolor="black"
    ),
    showlegend=False  # Hide the legend for now
)

# Add TTP labels with consistent colors
for ttp, color in occurrence_colors.items():
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        #marker=dict(size=10, color=color),
        legendgroup=ttp,
        showlegend=True,
        name=ttp
    ))

# Export the funnel graph to an HTML file
pio.write_html(fig, file='funnel.html', auto_open=True)

print("The funnel graph has been exported to funnel.html")