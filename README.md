# Financial Dashboard Readme

This Financial Dashboard is a Streamlit web application designed to provide insights into financial data. Users can choose between two data sources: MySQL Server or File Upload. The dashboard includes various visualizations and summaries to help analyze and understand the financial data.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/HAWK1704/DASHBOARD
   cd financial-dashboard
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   streamlit run main.py
   ```

   This command will start the Streamlit web application, and you can access it in your web browser.

## Features

### Data Source Selection

- Toggle between MySQL Server and File Upload as data sources.
- For MySQL Server, enter your MySQL username and password.

### Data Preview and Exploration

- View a preview of the loaded data, including options to download the dataset.
- Explore the data using the dTale interactive tool in a separate tab.

### Financial Metrics and Visualizations

- Display key financial metrics and ratios, such as Accounts Receivable, Accounts Payable, Current Ratio, In Stock, Equity Ratio, Debt Equity, Out Stock, and Delay.
- Visualize sales and profits across different segments, countries, and products.
- Explore unit sold per segment, monthly profit of products, and monthly unit sold of products.

### Sales Analysis

- Visualize sales distribution across months using a violin plot.
- Present a hierarchical view of sales using a TreeMap.
- Display a month-wise product sales summary table.

### Relationship Analysis

- Explore the relationship between sales and profits using a scatter plot.

### Data Summaries with SweetViz and Pandas Profiling

- Generate SweetViz and Pandas Profiling reports for a comprehensive data summary.
- Download the generated reports for further analysis.

## Dependencies

- Streamlit
- Pandas
- Plotly
- Matplotlib
- MySQL Connector
- dTale
- SweetViz
- ydata_profiling

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests. Your feedback and contributions are highly appreciated.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
