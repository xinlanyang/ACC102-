# ACC102-
## Project Overview
This project retrieves financial data from the WRDS database for major companies in the global coffee and beverage industry, calculates key financial ratios, and generates professional visualizations for comparative analysis.
The code has been fully optimized for secure WRDS login, manual password input, and error-free execution.
## Sample Companies
• SBUX: Starbucks Corporation
• NSRGF: Nestlé S.A.
• KO: Coca-Cola Company
• PEP: PepsiCo Inc.
• KDP: Keurig Dr Pepper Inc.
Requirements
• Python 3.8 or higher
• Required packages:pip install wrds pandas matplotlib
A valid WRDS account with access to Compustat data
## Features
1. WRDS Data Extraction
Pulls annual financial data from comp.funda for the period 2019–2024.
2. Key Financial Metrics
◦ ROE (Return on Equity) = Net Income / Total Equity
◦ ROA (Return on Assets) = Net Income / Total Assets
◦ Net Profit Margin = Net Income / Total Revenue
3. Data Visualization
◦ Line chart: ROE trend over time
◦ Grouped bar chart: Profitability comparison (latest year)
◦ Pie chart: Revenue share by company
◦ Grouped bar chart: Net profit margin trend
4. Secure & Robust Login
◦ Manual username and password input every run
◦ Password caching disabled
◦ Safe database connection handling to avoid repeated-close errors
## How to Run
1. Execute the main Python script.
2. When prompted, enter your WRDS username and password.
3. The program automatically loads and cleans data.
4. Four visualizations will be displayed sequentially.
5. A summary of key financial indicators is printed in the console.
## Key Conclusions
• Coca-Cola (KO) and PepsiCo (PEP) achieve the strongest ROE, showing superior shareholder returns.
• Starbucks (SBUX) maintains stable and well‑balanced profitability across all metrics.
• Nestlé (NSRGF) performs steadily, while Keurig Dr Pepper (KDP) has relatively lower but consistent margins.
• Large‑cap firms dominate total revenue, reflecting strong scale advantages.
• Profitability trends (ROE, net margin) have been stable across 2019–2024, showing mature business models.
## Notes
This project is for academic and research use only. All data is obtained legally through WRDS and must be used in compliance with relevant terms and policies.
