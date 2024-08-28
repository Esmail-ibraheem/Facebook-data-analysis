from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

# Serve static files (like CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Load and analyze the data
    data = pd.read_csv('facebook_data.csv')
    top_locations = data['location'].value_counts().head(5)
    top_interests = data['interests'].value_counts().head(5)

    # Generate plots
    age_distribution = create_histogram(data['age'], 'Age', 'Frequency', 'Distribution of User Ages')
    interaction_distribution = create_bar_chart(data['interaction_type'].value_counts(), 'Interaction Type', 'Frequency', 'Distribution of User Interactions')

    # Render the HTML page
    return f"""
    <html>
        <head>
            <title>Facebook Data Analysis</title>
            <link rel="stylesheet" href="/static/index.css">
        </head>
        <body>
            <h1>Facebook Data Analysis</h1>
            <h2>Top 5 Locations by User Count</h2>
            <ul>
                {''.join([f"<li>{loc}: {count}</li>" for loc, count in top_locations.items()])}
            </ul>
            <h2>Top 5 Interests by User Count</h2>
            <ul>
                {''.join([f"<li>{interest}: {count}</li>" for interest, count in top_interests.items()])}
            </ul>
            <h2>Distribution of User Ages</h2>
            <img src="data:image/png;base64,{age_distribution}" alt="Age Distribution">
            <h2>Distribution of User Interactions</h2>
            <img src="data:image/png;base64,{interaction_distribution}" alt="Interaction Distribution">
        </body>
    </html>
    """

def create_histogram(data, xlabel, ylabel, title):
    plt.figure()
    plt.hist(data, bins=10)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    return plot_to_base64()

def create_bar_chart(data, xlabel, ylabel, title):
    plt.figure()
    plt.bar(data.index, data)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    return plot_to_base64()

def plot_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')
