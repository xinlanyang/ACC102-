# ACC102-
## Project Title
Interactive Analysis Project on Financial Performance of Leading Enterprises in the Beverage Industry 
## 1.Problem & User
This project is designed for enterprise financial analysis and industry benchmarking scenarios, targeting business course learners, beginners in financial analysis, and industry investors. Currently, the competition in the coffee beverage industry is intensifying, making it difficult for investors and learners to intuitively compare the multi-year profit performance of multiple leading companies. This project creates a lightweight interactive dashboard to quickly assess the financial capabilities of multiple companies across multiple years, assisting in business decision-making.
## 2. Data
• Data source: WRDS Compustat Global Listed Companies Standard Financial Database
• Access date: April 2026
• Time range: Complete fiscal years from 2019 to 2024
• Target companies: Starbucks (SBUX), Coca-Cola (KO), PepsiCo (PEP), Keurig Dr Pepper (KDP)
• Key fields: Stock code, fiscal year, net profit, total assets, shareholders' equity, EBIT, short-term liabilities, operating income
• Data preprocessing: Remove missing values, filter extreme outliers to ensure the validity of all analysis indicators and visual charts.
### 3. Methods
1. Build an interactive web analysis dashboard based on Python + Streamlit, which can be launched locally without front-end code.
2. Call the official WRDS API to remotely and batchly obtain standardized annual financial raw data of 4 specified enterprises in compliance.
3. Automatically calculate four core profitability indicators: ROE, ROA, ROC, and net profit margin.
4. Use Matplotlib to generate 6 sets of professional visual charts covering all operational dimensions, including trend line charts, grouped comparison bar charts, and market share pie charts.
5. Configure a local data cache mechanism to greatly reduce the waiting time for repeated data loading and improve page fluency.
6. Built-in custom analysis year range slider, all charts and indicators are automatically updated synchronously with the selected time period.
7. Support one-click export of filtered full financial data to Excel, and open an online entry for viewing complete raw data tables.
### 4. Key Findings
1. The four leading beverage companies included in the analysis have strong overall profitability, with long-term ROE maintained in a healthy and reasonable range, and the industry has strong overall anti-operational risk capabilities.
2. Starbucks has a prominent brand premium, leading in net profit margin and asset operation efficiency among all sample companies.
3. Coca-Cola and PepsiCo have a leading advantage in operating income, occupying most of the beverage industry's market revenue share.
4. The overall profit level of the industry fluctuated slightly and steadily during the 5-year period from 2019 to 2024, with no large-scale decline, and the beverage industry has a high degree of maturity.
5. The differentiated business layout and market strategies of various enterprises are directly reflected in the obvious differences in core financial indicators such as corporate capital structure and profit return.
## 5. How to Run
### Warehouse File Structure
1.requirement.txt
2.app.py
### Running Steps
1. Open the terminal and install all required dependencies:
pip install streamlit wrds pandas matplotlib openpyxl
2. Prepare a valid WRDS database account and password in advance.
3. Save the complete code as app.py in a local folder, and enter the folder directory in the terminal.
4. Run the startup command in the terminal: streamlit run app.py
5. The local browser will open automatically. Enter the WRDS account and password, wait for the data to load, and you can use all functions such as data analysis, chart viewing, and data export.
6. Product Link / Demo
All interactive functions can be fully experienced by running locally. This project can be deployed to Streamlit Cloud with one click later, generating a permanent public online demo link for easy access and sharing at any time without local environment configuration.
## 6. Limitations & Next Steps
### Limitations
1. The analysis sample only selects 5 leading enterprises in the beverage industry, and the coverage of the entire category and industry is insufficient.
2. Only annual summary financial data is used for analysis, and quarterly high-frequency operating data and stock price performance data are not included for linkage analysis.
3. No in-depth regression modeling analysis is conducted in combination with external influencing factors such as macroeconomic trends and consumer price indices.
### Next Steps
1. Expand the sample of listed companies in multiple categories and industries, and extend the statistical period of financial data to broaden the analysis boundary.
2. Add multi-dimensional financial analysis indicators such as corporate solvency, growth rate, and cash flow health to improve the analysis system.
3. Integrate AI large models to realize automatic labeling of abnormal financial data and automatic generation of industry operation analysis reports.
4. Upgrade interactive functions, add custom high-level operations such as independent selection of comparison enterprises and multi-dimensional indicator filtering.
5. Complete stable cloud deployment and launch a publicly accessible online version.
