import streamlit as st
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import os


st.set_page_config(page_title="Beverage Financial Analysis", page_icon="☕", layout="wide")

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

st.title("☕ Beverage Industry Financial Analysis (2019–2024)")
st.markdown("---")


wrds_user = st.text_input("Enter your WRDS username", placeholder="Your WRDS ID")
wrds_pwd = st.text_input("Enter your WRDS password", placeholder="Your WRDS Password", type="password")

if not wrds_user or not wrds_pwd:
    st.info("⚠️ Please enter your WRDS username AND password to load data")
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

    
    df["ROE"] = df["ib"] / df["ceq"]
    df["ROA"] = df["ib"] / df["at"]
    df["ROC"] = df["ebit"] / (df["at"] - df["dlc"])
    df["Net_Profit_Margin"] = df["ib"] / df["revt"]

    
    df = df.dropna(subset=["ROE", "ROA", "ROC", "Net_Profit_Margin"])
    df = df[(df["ROE"].abs() < 5) & (df["ROA"].abs() < 3) & 
            (df["ROC"].abs() < 3) & (df["Net_Profit_Margin"].abs() < 1)]

   
    company_names = {
        "SBUX": "Starbucks",
        "NSRGF": "Nestlé",
        "KO": "Coca-Cola",
        "PEP": "PepsiCo",
        "KDP": "Keurig Dr Pepper"
    }
    df["Company"] = df["tic"].map(company_names)

    return df


raw_df = load_financial_data(wrds_user, wrds_pwd)


st.subheader("📅 Custom Analysis Time Range Selection")
min_avail_year = int(raw_df["fyear"].min())
max_avail_year = int(raw_df["fyear"].max())

select_start, select_end = st.slider(
    "Drag to select your custom analysis year range",
    min_value=min_avail_year,
    max_value=max_avail_year,
    value=(min_avail_year, max_avail_year),
    step=1
)


filter_df = raw_df[(raw_df["fyear"] >= select_start) & (raw_df["fyear"] <= select_end)].copy()

latest_filter_df = filter_df.loc[filter_df.groupby("tic")["fyear"].idxmax()].reset_index(drop=True)

st.markdown("---")


st.subheader("📥 Download Filtered Analysis Data (Excel)")
@st.cache_data
def generate_excel(full_data, latest_data):
    output_path = "Beverage_Financial_Data.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        full_data.to_excel(writer, sheet_name="Filtered_Historical_Data", index=False)
        latest_data.to_excel(writer, sheet_name="Period_Latest_Summary", index=False)
    return output_path

excel_path = generate_excel(filter_df, latest_filter_df)
with open(excel_path, "rb") as f:
    st.download_button(
        label="📥 Download Excel File",
        data=f,
        file_name="Beverage_Filtered_Financial_Data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("---")


colors = ['#ff6b6b','#f7c843','#4ecdc4','#6c5ce7','#2ecc71']


st.subheader("📈 ROE Trend Custom Period")
fig1, ax1 = plt.subplots(figsize=(12,5))
for tic in filter_df["tic"].unique():
    sub = filter_df[filter_df["tic"] == tic]
    ax1.plot(sub["fyear"], sub["ROE"], marker='o', linewidth=2, label=sub["Company"].iloc[0])
ax1.set_title(f"ROE Trend ({select_start}–{select_end})")
ax1.set_xlabel("Year")
ax1.set_ylabel("ROE Ratio")
ax1.legend()
ax1.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig1)


st.subheader("📊 Latest Year Multi Profitability Indicators Comparison")
fig2, ax2 = plt.subplots(figsize=(12,5))
x = range(len(latest_filter_df))
w = 0.25
ax2.bar([i - w for i in x], latest_filter_df["ROE"], w, label='ROE', color='#ff6b6b')
ax2.bar(x,                 latest_filter_df["ROA"], w, label='ROA', color='#4ecdc4')
ax2.bar([i + w for i in x], latest_filter_df["ROC"], w, label='ROC', color='#f7c843')
ax2.set_xticks(x)
ax2.set_xticklabels(latest_filter_df["Company"], rotation=10)
ax2.set_ylabel("Ratio Value")
ax2.legend()
plt.tight_layout()
st.pyplot(fig2)


st.subheader("🥧 Latest Year Total Revenue Market Share")
fig3, ax3 = plt.subplots(figsize=(8,8))
rev_data = latest_filter_df.set_index("Company")["revt"]
ax3.pie(rev_data, labels=rev_data.index, autopct='%1.1f%%', colors=colors, startangle=90)
ax3.set_title(f"Revenue Share Distribution {select_end}")
plt.tight_layout()
st.pyplot(fig3)


st.subheader("📉 Net Profit Margin Custom Period Trend")
fig4, ax4 = plt.subplots(figsize=(12,5))
width = 0.15
years = sorted(filter_df["fyear"].unique())

for i, tic in enumerate(filter_df["tic"].unique()):
    sub = filter_df[filter_df["tic"] == tic]
    margins = []
    for y in years:
        val = sub[sub["fyear"] == y]["Net_Profit_Margin"]
        margins.append(val.iloc[0] if not val.empty else 0)
    ax4.bar([y + width*(i-2) for y in years], margins, width, label=sub["Company"].iloc[0])

ax4.set_xlabel("Year")
ax4.set_ylabel("Net Profit Margin Ratio")
ax4.set_xticks(years)
ax4.legend()
ax4.grid(axis='y', alpha=0.3)
plt.tight_layout()
st.pyplot(fig4)


st.subheader("🏢 Latest Year Total Asset Scale Horizontal Comparison")
fig5, ax5 = plt.subplots(figsize=(12,5))
ax5.barh(latest_filter_df["Company"], latest_filter_df["at"], color=colors)
ax5.set_xlabel("Total Assets Amount")
ax5.set_title(f"Enterprise Total Asset Scale Ranking {select_end}")
ax5.grid(axis='x', alpha=0.3)
plt.tight_layout()
st.pyplot(fig5)


st.subheader("💰 Annual Net Income Total Changing Trend")
fig6, ax6 = plt.subplots(figsize=(12,5))
for idx, tic in enumerate(filter_df["tic"].unique()):
    sub = filter_df[filter_df["tic"] == tic]
    ax6.plot(sub["fyear"], sub["ib"], marker='s', linewidth=2, color=colors[idx], label=sub["Company"].iloc[0])
ax6.set_title(f"Annual Net Income Trend ({select_start}–{select_end})")
ax6.set_xlabel("Year")
ax6.set_ylabel("Total Net Income")
ax6.legend()
ax6.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig6)


st.subheader("🔍 Filtered Period Latest Year Key Financial Indicators")
for _, row in latest_filter_df.iterrows():
    st.write(f"**{row['Company']}** | ROE: {row['ROE']:.2%} | ROA: {row['ROA']:.2%} | ROC: {row['ROC']:.2%} | Net Profit Margin: {row['Net_Profit_Margin']:.2%}")


with st.expander("📋 View Full Filtered Historical Raw Data"):
    st.dataframe(filter_df, use_container_width=True)