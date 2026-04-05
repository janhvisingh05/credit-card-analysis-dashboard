from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.figure_factory as ff
from io import BytesIO

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Updated muted palette (removed pink #fff6f9)
muted_palette = [
    "#cfe4fc", "#dbebfd", "#e7f2fe", "#f3f8fe", "#cad5ef",
    "#d4ddf2", "#e0e6f5", "#e4efef", "#cfe5e5"
]

# Plotly template base style
plotly_template = dict(layout=dict(
    plot_bgcolor='rgba(255,255,255,0.95)',
    paper_bgcolor='rgba(255,255,255,0.95)',
    font=dict(color='#333', size=9),
    margin=dict(t=30, b=50, l=40, r=20),
    xaxis=dict(showgrid=False, zeroline=False, title_font=dict(size=10), tickfont=dict(size=8)),
    yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', zeroline=False, title_font=dict(size=10), tickfont=dict(size=8))
))

def plot_to_html(fig):
    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def apply_styling(fig, color):
    fig.update_layout(
        height=210,
        width=540,
        margin=dict(t=30, b=50, l=40, r=20),
        font=dict(size=9),
        plot_bgcolor='rgba(255,255,255,0.95)',
        paper_bgcolor='rgba(255,255,255,0.95)',
        hoverlabel=dict(bgcolor="white", font_size=10)
    )
    for trace in fig.data:
        if trace.type == 'pie':
            trace.hole = 0.45
            trace.marker.colors = muted_palette[:len(trace.labels)]
        else:
            if hasattr(trace, 'marker'):
                trace.marker.color = color
                trace.marker.line = dict(color='rgba(0,0,0,0.1)', width=0.8)
    fig.update_xaxes(tickfont=dict(size=8))
    fig.update_yaxes(tickfont=dict(size=8))
    return fig

@app.route('/', methods=['GET', 'POST'])
def index():
    graphs_by_tab = {
        "Customer Overview": [],
        "Spending Insights": [],
        "Repayment Trends": [],
        "Spend vs Repay": [],
        "Product Limits": []
    }
    summary_metrics = []
    insights = []

    if request.method == 'POST':
        file = request.files['file']
        session['data'] = file.read()
        return redirect('/')

    if 'data' in session:
        excel_data = pd.ExcelFile(BytesIO(session['data']))
        acquisition_df = excel_data.parse('Customer Acqusition')
        spend_df = excel_data.parse('Spend')
        repayment_df = excel_data.parse('Repayment')

        acquisition_df.columns = acquisition_df.columns.str.strip()
        spend_df.columns = spend_df.columns.str.strip()
        repayment_df.columns = repayment_df.columns.str.strip()

        total_customers = acquisition_df['Customer'].nunique()
        avg_age = round(acquisition_df['Age'].mean(), 1)
        total_limit = acquisition_df['Limit'].sum()
        avg_limit = round(acquisition_df['Limit'].mean(), 1)
        total_spent = spend_df['Amount'].sum()
        avg_spent = round(spend_df['Amount'].mean(), 1)
        total_repaid = repayment_df['Amount'].sum()
        avg_repaid = round(repayment_df['Amount'].mean(), 1)

        summary_metrics = [
            {"label": "Total Customers", "value": total_customers, "emoji": "👥"},
            {"label": "Avg. Age", "value": avg_age, "emoji": "🎂"},
            {"label": "Total Limit", "value": f"{total_limit:,}", "emoji": "💳"},
            {"label": "Avg. Limit", "value": f"{avg_limit:,}", "emoji": "📊"},
            {"label": "Total Spent", "value": f"{total_spent:,}", "emoji": "💰"},
            {"label": "Avg. Spent", "value": f"{avg_spent:,}", "emoji": "💼️"},
            {"label": "Total Repaid", "value": f"{total_repaid:,}", "emoji": "💸"},
            {"label": "Avg. Repaid", "value": f"{avg_repaid:,}", "emoji": "🔁"}
        ]

        segment_counts = acquisition_df['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']

        city_counts = acquisition_df['City'].value_counts().reset_index()
        city_counts.columns = ['City', 'Count']

        type_counts = spend_df['Type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']

        limit_dist_fig = ff.create_distplot([acquisition_df['Limit']], group_labels=['Limit'], show_hist=False, show_rug=False)
        limit_dist_fig.update_layout(title_text='Limit Distribution', template=plotly_template)

        avg_limit_pie = px.pie(acquisition_df.groupby('Segment')['Limit'].mean().reset_index(), names='Segment', values='Limit', title='Avg Limit by Segment', template=plotly_template)

        all_graphs = [
            ('Customer Overview', [
                px.histogram(acquisition_df, x='Age', nbins=20, title='Age Distribution', template=plotly_template),
                px.pie(acquisition_df, names='Segment', title='Segment Distribution', template=plotly_template),
                px.pie(segment_counts, names='Segment', values='Count', title='Segment Share', template=plotly_template),
                px.bar(city_counts, x='City', y='Count', title='Top Cities', template=plotly_template)
            ]),
            ('Spending Insights', [
                px.box(spend_df, x='Type', y='Amount', title='Spending by Type', template=plotly_template),
                px.line(spend_df.groupby('Month')['Amount'].sum().reset_index(), x='Month', y='Amount', title='Monthly Spend', template=plotly_template),
                px.bar(type_counts, x='Type', y='Count', title='Spend Type Frequency', template=plotly_template),
                px.histogram(spend_df, x='Amount', nbins=30, title='Spend Amount Spread', template=plotly_template)
            ]),
            ('Repayment Trends', [
                px.line(repayment_df.groupby('Month')['Amount'].sum().reset_index(), x='Month', y='Amount', title='Monthly Repayment', template=plotly_template),
                px.histogram(repayment_df, x='Amount', nbins=30, title='Repayment Amount Spread', template=plotly_template)
            ]),
            ('Spend vs Repay', [
                px.scatter(pd.merge(
                    spend_df.groupby('Costomer')['Amount'].sum().reset_index(),
                    repayment_df.groupby('Costomer')['Amount'].sum().reset_index(),
                    on='Costomer', suffixes=('_spend', '_repay')
                ), x='Amount_spend', y='Amount_repay', title='Spend vs Repay', template=plotly_template),
                px.bar(pd.merge(
                    spend_df.groupby('Costomer')['Amount'].sum().reset_index(),
                    repayment_df.groupby('Costomer')['Amount'].sum().reset_index(),
                    on='Costomer', suffixes=('_spend', '_repay')
                ).nlargest(10, 'Amount_spend'), x='Costomer', y='Amount_spend', title='Top Spenders', template=plotly_template),
                px.bar(pd.merge(
                    spend_df.groupby('Costomer')['Amount'].sum().reset_index(),
                    repayment_df.groupby('Costomer')['Amount'].sum().reset_index(),
                    on='Costomer', suffixes=('_spend', '_repay')
                ).nlargest(10, 'Amount_repay'), x='Costomer', y='Amount_repay', title='Top Repaid Customers', template=plotly_template)
            ]),
            ('Product Limits', [
                limit_dist_fig,
                avg_limit_pie
            ])
        ]

        color_index = 0
        for tab, figs in all_graphs:
            styled_figs = []
            for fig in figs:
                color = muted_palette[color_index % len(muted_palette)]
                styled_figs.append(plot_to_html(apply_styling(fig, color)))
                color_index += 1
            graphs_by_tab[tab] = styled_figs

        insights = [
            "🔍 Most customers are in the 30–40 age range.",
            "💸 Repayment amount is closely tracking spend.",
            "🌆 Majority of users belong to top 5 cities.",
            "💳 Platinum card holders have highest limits.",
            "🍬️ Shopping, Air Tickets and Food are top spending categories.",
            "📉 Repayment patterns drop slightly in early 2006.",
            "📈 Top 10 customers are responsible for large chunks of spend and repay.",
            "🌟 Spend vs Repay shows strong positive correlation."
        ]

    return render_template('index.html', graphs=graphs_by_tab, summary_metrics=summary_metrics, insights=insights)

if __name__ == '__main__':
    app.run(debug=True, port=61968)

 
