# ACC102-
## Project Title
Interactive Analysis Project on Financial Performance of Leading Enterprises in the Beverage Industry 
## 1.Problem & User
This project is designed for enterprise financial analysis and industry benchmarking scenarios, targeting business course learners, beginners in financial analysis, and industry investors. Currently, the competition in the coffee beverage industry is intensifying, making it difficult for investors and learners to intuitively compare the multi-year profit performance of multiple leading companies. This project creates a lightweight interactive dashboard to quickly assess the financial capabilities of multiple companies across multiple years, assisting in business decision-making.
## 2.Data
• Data source: WRDS Compustat Global Listed Companies Standard Financial Database
• Access date: April 2026
• Time range: Complete fiscal years from 2019 to 2024
• Target companies: Starbucks (SBUX), Nestlé (NSRGF), Coca-Cola (KO), Pepsi (PEP), Keurig Dr Pepper (KDP)
• Key fields: Stock code, fiscal year, net profit, total assets, shareholders' equity, EBIT, short-term liabilities, operating income
• Data preprocessing: Remove missing values, filter extreme outliers to ensure the validity of the indicators.
### 3. Methods
1. Build a web interactive dashboard without front-end code and with quick running using Python + Streamlit.
2. Pull standardized annual financial data in batches remotely through the official WRDS API.
3. Calculate four core profitability indicators: ROE, ROA, ROC, and net profit margin.
4. Use Matplotlib to draw trend line charts, grouped bar charts, and revenue proportion pie charts.
5. Add a local cache mechanism to significantly improve page loading speed.
6. Support one-click Excel export, raw data preview, and cache reset and refresh. 
## 4. Key Findings
The top five beverage companies have strong overall profit stability, with long-term ROE maintained in a healthy range and excellent risk resistance capabilities.
The Starbucks brand enjoys a prominent premium, leading in net profit margin and asset operation efficiency among the samples.
Coca-Cola and PepsiCo have a significant revenue gap ahead, occupying the majority of the market share in the industry.
The industry's overall profit has fluctuated slightly over the past five years without a significant decline, indicating a high level of industry maturity.
The differences in business strategies among various enterprises are directly reflected in the obvious differentiation of capital structure and return indicators. 
## 5. How to run
Warehouse file structure README.md
app.py
requirements.txt
data/ (cache data files)
figures/ (chart output) 
### Running Steps
1. Install the required dependency libraries for the project: pip install streamlit wrds pandas matplotlib openpyxl
2. Enter your valid WRDS account in the code. 
3. Enter the startup command at the terminal: streamlit run app.py
4. Open http://localhost:8501 in your local browser to use all the functions. 
## 6. Product link / Demo
You can experience the complete interactive functions by running it locally. 
Supports one-click deployment to Streamlit Cloud later, generating a permanent public online demo link for easy access and sharing at any time. 
## 7. Limitations & next steps
### Limitations
The sample only includes five leading enterprises, and the breadth of industry coverage is limited. 
Only annual financial data was used, without incorporating quarterly high-frequency data and stock price performance. 
No regression analysis was conducted in combination with external influencing factors such as macroeconomics and consumption indices. 
### Next steps
1. Expand the sample of enterprises in more industries and extend the time span of the analysis.
2. Add multi-dimensional financial indicators such as debt-paying ability, growth ability, and cash flow.
3. Integrate AI large models to achieve automatic interpretation of financial data and intelligent generation of analysis reports.
4. Add human-computer interaction filtering functions such as custom years and multiple company selections.
5. Complete stable cloud deployment and launch a publicly accessible version.
