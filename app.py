import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(page_title="Beverage Financial Analysis", page_icon="☕", layout="wide")
st.title("☕ Beverage Industry Financial Analysis (2019–2024)")
st.markdown("---")

data = [
    ["KDP",2019,1254,49518,23257,2665,1703,11120,0.053919,0.025324,0.055736,0.11277,"Keurig Dr Pepper"],
    ["KDP",2020,1325,49779,23829,2914,2461,11618,0.055605,0.026618,0.061583,0.114047,"Keurig Dr Pepper"],
    ["KDP",2021,2146,50598,24972,3093,459,12683,0.085936,0.042413,0.061689,0.169203,"Keurig Dr Pepper"],
    ["KDP",2022,1436,51837,25126,2880,1090,14057,0.057152,0.027702,0.056752,0.102156,"Keurig Dr Pepper"],
    ["KDP",2023,2181,52130,25676,3210,3466,14814,0.084943,0.041838,0.065963,0.147226,"Keurig Dr Pepper"],
    ["KDP",2024,1441,53430,24243,3625,2895,15351,0.05944,0.02697,0.071732,0.09387,"Keurig Dr Pepper"],
    ["KO",2019,8920,86381,18981,10541,15528,37266,0.469944,0.103263,0.148773,0.23936,"Coca-Cola"],
    ["KO",2020,7747,87296,19299,9837,2990,33014,0.40142,0.088744,0.116682,0.234658,"Coca-Cola"],
    ["KO",2021,9771,94354,22999,11334,4955,38655,0.252775,0.103557,0.12678,0.252775,"Coca-Cola"],
    ["KO",2022,9542,92763,24105,12124,3113,43004,0.395851,0.102864,0.135237,0.221886,"Coca-Cola"],
    ["KO",2023,10714,97703,25941,13289,6878,45754,0.413014,0.109659,0.146314,0.234165,"Coca-Cola"],
    ["KO",2024,10631,100549,24856,14120,2437,47061,0.427704,0.10573,0.143917,0.225898,"Coca-Cola"],
    ["PEP",2019,7314,78547,14786,10714,3362,67161,0.494657,0.093116,0.142502,0.108902,"PepsiCo"],
    ["PEP",2020,7120,92918,13454,10660,4240,70372,0.529211,0.076627,0.12021,0.101177,"PepsiCo"],
    ["PEP",2021,7618,92377,16043,11363,4754,79474,0.474849,0.082466,0.129681,0.095855,"PepsiCo"],
    ["PEP",2022,8910,92187,17149,12263,3897,86392,0.519564,0.096651,0.138895,0.103135,"PepsiCo"],
    ["PEP",2023,9074,100495,18503,13839,7066,91471,0.490407,0.090293,0.148123,0.099201,"PepsiCo"],
    ["PEP",2024,9578,99467,18041,14505,7724,91854,0.530902,0.096293,0.158105,0.104274,"PepsiCo"],
    ["SBUX",2019,3599.2,19219.6,-6232.2,3928.3,0,26508.6,-0.577517,0.187267,0.20439,0.135775,"Starbucks"],
    ["SBUX",2020,928.3,29374.5,-7805.1,1299.6,2937.5,23518,-0.118935,0.031602,0.049158,0.039472,"Starbucks"],
    ["SBUX",2021,4199.3,31392.6,-5321.2,4447.2,2250.2,29060.6,-0.789164,0.133767,0.152602,0.144501,"Starbucks"],
    ["SBUX",2022,3281.6,27978.4,-8706.6,4425.8,3169.7,32250.3,-0.376909,0.11729,0.178397,0.101754,"Starbucks"],
    ["SBUX",2023,4124.5,29445.5,-7994.8,5503,3127.4,35975.6,-0.515898,0.140072,0.209096,0.114647,"Starbucks"],
    ["SBUX",2024,3760.9,31339.3,-7448.9,5107.6,2712,36176.2,-0.504893,0.120006,0.178417,0.103961,"Starbucks"]
]

df = pd.DataFrame(data, columns=[
    "tic","fyear","ib","at","ceq","ebit","dlc","revt","ROE","ROA","ROC","Net_Profit_Margin","Company"
])


latest = df.loc[df.groupby("tic")["fyear"].idxmax()].reset_index(drop=True)


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
        label="📥 Download Excel File",
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


st.subheader(" Latest Year Profitability Comparison")
fig2, ax2 = plt.subplots(figsize=(12,5))
x = range(len(latest))
w = 0.25
ax2.bar([i-w for i in x], latest["ROE"], w, label='ROE', color='#ff6b6b')
ax2.bar(x, latest["ROA"], w, label='ROA', color='#4ecdc4')
ax2.bar([i+w for i in x], latest["ROC"], w, label='ROC', color='#f7c843')
ax2.set_xticks(x, latest["Company"], rotation=10)
ax2.set_ylabel("Ratio")
ax2.legend()
st.pyplot(fig2)


st.subheader(" Latest Year Revenue Share")
fig3, ax3 = plt.subplots(figsize=(8,8))
rev_data = latest.set_index("Company")["revt"]
ax3.pie(rev_data, labels=rev_data.index, autopct='%1.1f%%', colors=colors, startangle=90)
ax3.set_title("Revenue Share")
st.pyplot(fig3)


st.subheader(" Net Profit Margin Trend (2019–2024)")
fig4, ax4 = plt.subplots(figsize=(12,5))
width = 0.15
years = sorted(df["fyear"].unique())
for i, tic in enumerate(df["tic"].unique()):
    sub = df[df["tic"] == tic]
    margins = []
    for y in years:
        val = sub[sub["fyear"] == y]["Net_Profit_Margin"]
        margins.append(val.values[0] if not val.empty else 0)
    ax4.bar([y + width*(i-2) for y in years], margins, width, label=sub["Company"].iloc[0])
ax4.set_xlabel("Year")
ax4.set_ylabel("Net Profit Margin")
ax4.set_xticks(years)
ax4.legend()
ax4.grid(axis='y', alpha=0.3)
st.pyplot(fig4)


st.subheader(" Key Financial Indicators (Latest Year)")
for _, row in latest.iterrows():
    st.write(f"**{row['Company']}** | ROE: {row['ROE']:.2%} | ROA: {row['ROA']:.2%} | ROC: {row['ROC']:.2%} | NPM: {row['Net_Profit_Margin']:.2%}")


with st.expander(" View Full Historical Data"):
    st.dataframe(df)
