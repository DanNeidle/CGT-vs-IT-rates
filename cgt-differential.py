
# tax rate on dividends is highest marginal combined national/state rate taking account of imputation systems, tax credits and tax allowances. Source: https://stats.oecd.org/index.aspx?DataSetCode=TABLE_II4, column K

# labour income is combined national/state including employee social security (not employer). Source https://stats.oecd.org/Index.aspx?DataSetCode=TABLE_I7 "all in rate" column F

# CGT rate is highest marginal combined national/state rate on shares. Source: https://taxsummaries.pwc.com/quick-charts/capital-gains-tax-cgt-rates and Tax Policy Associates


# these are rates for local residents. Some countries (e.g. France) in principle tax foreigners on local gains (although tax treaties mean in practice it rarely applies). Other countries like the UK/US only tax local residents on gains in stock/shares

import plotly.graph_objs as go
from openpyxl import load_workbook

wb = load_workbook(filename='IT_CGT_top_marginal_rates.xlsx')
sheet = wb['CGT_vs_IT']

# Initialize lists to hold your data
countries = []
it_ss_rates = []
cgt_rates = []
it_dividend_rates = []

# The data starts at row 2 to skip the headers and is in columns A, B, C
for row in sheet.iter_rows(min_row=2, max_col=4, values_only=True):
    countries.append(row[0])
    it_ss_rates.append(row[1])
    it_dividend_rates.append(row[2])
    cgt_rates.append(row[3])


# Sort the list of tuples by the CGT rate in descending order (highest first) 
country_rate_tuples = list(zip(countries, it_ss_rates, it_dividend_rates, cgt_rates))
sorted_country_rate_tuples = sorted(country_rate_tuples, key=lambda x: x[3], reverse=True)
countries, it_ss_rates, it_dividend_rates, cgt_rates = zip(*sorted_country_rate_tuples)

fig = go.Figure()

# Add arrows for each country
for i, (country, it_ss_rate, it_dividend_rate, cgt_rate) in enumerate(zip(countries, it_ss_rates, it_dividend_rates, cgt_rates)):
    
    
    # add IT/dividend rate
    fig.add_shape(
        type="line",
        x0=i,
        y0=it_dividend_rate,
        x1=i,
        y1=cgt_rate,
        line=dict(
            color="red" if country == "United Kingdom" else "blue",
            width=3
        ),
        xref="x",
        yref="y"
    )
    
    # Add arrowhead
    fig.add_trace(go.Scatter(
        x=[i],
        y=[cgt_rate],
        mode='markers',
        marker=dict(
            color="red" if country == "United Kingdom" else "blue",
            size=10,
            symbol='arrow-bar-up' if cgt_rate > it_dividend_rate else 'arrow-bar-down'
        ),
        showlegend=False
    ))
    

# Set the layout of the figure
fig.update_layout(
    title='Income Tax vs. Capital Gains Tax Rates by Country',
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(len(countries))),
        ticktext=countries
    ),
    yaxis=dict(
        title='Tax Rate (%)',
        range=[0, 0.6], 
        tickmode='array',
        tickvals=[i/10 for i in range(11)],  
        ticktext=[f'{i*10}%' for i in range(11)], 
        tickformat=',.0%'
    ),
    height=800,
    width=1400
)

# Show the figure
fig.show()