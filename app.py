import streamlit as st
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Beverage Financial Analysis", page_icon="☕", layout="wide")
st.title("☕ Beverage Industry Financial Analysis (2019–2024)")
st.markdown("---")

wrds_user = st.text_input("Enter your WRDS username", placeholder="Your WRDS ID")
wrds_pwd = st.text_input("Enter your WRDS password", placeholder="Your WRDS Password", type="password")

if not wrds_user or not wrds_pwd:
    st.info("👈 Please enter your WRDS username AND password to load data")
    st.stop()


@st.cache_data(show_spinner="Loading data from WRDS...")
def load_financial_data(wrds_username, wrds_password):
    db = wrds.Connection(wrds_username=wrds_username, wrds_password=wrds_password)
    tickers = ["SBUX", "NSRGF", "KO", "PEP", "KDP"]
    start_year, end_year = 2019, 2024

    query = f"""
        SELECT tic, fyear, ib, at, ceq, ebit, dlc, revt
        FROM comp.funda
        WHERE tic IN ({','.join([f"'{t}'" for t in tickers])})
          AND fyear BETWEEN {start_year} AND {end_year}
          AND indfmt='INDL' AND datafmt='STD' AND consol='C'
        ORDER BY tic, fyear
    """

    df = db.raw_sql(query)
    db.close()

    # Calculate key ratios
    df["ROE"] = df["ib"] / df["ceq"]
    df["ROA"] = df["ib"] / df["at"]
    df["ROC"] = df["ebit"] / (df["at"] - df["dlc"])
    df["Net_Profit_Margin"] = df["ib"] / df["revt"]

    # Data cleaning
    df = df.dropna(subset=["ROE", "ROA", "ROC", "Net_Profit_Margin"])
    df = df[(df["ROE"].abs() < 5) & (df["ROA"].abs() < 3) & 
            (df["ROC"].abs() < 3) & (df["Net_Profit_Margin"].abs() < 1)]

    # Company names
    company_names = {
        "SBUX": "Starbucks",
        "NSRGF": "Nestlé",
        "KO": "Coca-Cola",
        "PEP": "PepsiCo",
        "KDP": "Keurig Dr Pepper"
    }
    df["Company"] = df["tic"].map(company_names)

    # Latest year data
    latest = df.loc[df.groupby("tic")["fyear"].idxmax()].reset_index(drop=True)
    return df, latest

df, latest = load_financial_data(wrds_user, wrds_pwd)


st.subheader(" Download Full Data (Excel)")

@st.cache_data
def generate_excel(df, latest):
    output_path = "Beverage_Financial_Data.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, sheet_name="Full_Historical_Data", index=False)
        latest.to_excel(writer, sheet_name="Latest_Summary", index=False)
    return output_path

excel_path = generate_excel(df, latest)
with open(excel_path, "rb") as f:
    st.download_button(
        label=" Download Excel File",
        data=f,
        file_name="Beverage_Financial_Data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("---")


colors = ['#ff6b6b','#f7c843','#4ecdc4','#6c5ce7','#2ecc71']

# Plot 1: ROE Trend
st.subheader("📈 ROE Trend (2019–2024)")
fig1, ax1 = plt.subplots(figsize=(12,5))
for tic in df["tic"].unique():
    sub = df[df["tic"] == tic]
    ax1.plot(sub["fyear"], sub["ROE"], marker='o', linewidth=2, label=sub["Company"].iloc[0])
ax1.set_title("ROE Trend")
ax1.set_xlabel("Year")
ax1.set_ylabel("ROE")
ax1.legend()
ax1.grid(alpha=0.3)
st.pyplot(fig1)

# Plot 2: Profitability Comparison
st.subheader(" Latest Year Profitability Comparison")
fig2, ax2 = plt.subplots(figsize=(12,5))
x = range(len(latest))
w = 0.25
ax2.bar([i - w for i in x], latest["ROE"], w, label='ROE', color='#ff6b6b')
ax2.bar(x,                 latest["ROA"], w, label='ROA', color='#4ecdc4')
ax2.bar([i + w for i in x], latest["ROC"], w, label='ROC', color='#f7c843')
ax2.set_xticks(x)
ax2.set_xticklabels(latest["Company"], rotation=10)
ax2.set_ylabel("Ratio")
ax2.legend()
st.pyplot(fig2)

# Plot 3: Revenue Share Pie Chart
st.subheader(" Latest Year Revenue Share")
fig3, ax3 = plt.subplots(figsize=(8,8))
rev_data = latest.set_index("Company")["revt"]
ax3.pie(rev_data, labels=rev_data.index, autopct='%1.1f%%', colors=colors, startangle=90)
ax3.set_title("Revenue Share")
st.pyplot(fig3)

# Plot 4: Net Profit Margin Trend
st.subheader(" Net Profit Margin Trend (2019–2024)")
fig4, ax4 = plt.subplots(figsize=(12,5))
width = 0.15
years = sorted(df["fyear"].unique())

for i, tic in enumerate(df["tic"].unique()):
    sub = df[df["tic"] == tic]
    margins = []
    for y in years:
        val = sub[sub["fyear"] == y]["Net_Profit_Margin"]
        margins.append(val.iloc[0] if not val.empty else 0)
    ax4.bar([y + width*(i-2) for y in years], margins, width, label=sub["Company"].iloc[0])

ax4.set_xlabel("Year")
ax4.set_ylabel("Net Profit Margin")
ax4.set_xticks(years)
ax4.legend()
ax4.grid(axis='y', alpha=0.3)
st.pyplot(fig4)

st.subheader("🔍 Key Financial Indicators (Latest Year)")
for _, row in latest.iterrows():
    st.write(f"**{row['Company']}** | ROE: {row['ROE']:.2%} | ROA: {row['ROA']:.2%} | ROC: {row['ROC']:.2%} | NPM: {row['Net_Profit_Margin']:.2%}")

# Show full data table
with st.expander(" View Full Historical Data"):
    st.dataframe(df)