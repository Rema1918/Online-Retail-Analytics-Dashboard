# Interactive Analytics Dashboard

## Project Overview
This project develops an interactive analytics dashboard using Python, Streamlit, and Plotly to explore retail sales data. The dashboard allows users to filter data dynamically, monitor key performance indicators (KPIs), and understand sales trends through interactive visualizations.

## Objectives
- Build an interactive and user-friendly analytics dashboard.
- Provide dynamic filters for dates, categories, and numerical values.
- Display key business metrics using KPI cards.
- Visualize sales trends and product performance.
- Allow users to explore data through interactive charts.
- Handle empty filter results gracefully.

## Tools and Technologies
- **Python** – data processing and application logic
- **Pandas** – data manipulation and analysis
- **Streamlit** – interactive dashboard development
- **Plotly** – interactive data visualization

## Dataset
The dashboard uses the UCI Online Retail dataset, which contains transaction details from an online retail business.

**Dataset Source:** [UCI Machine Learning Repository – Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

## Key Features

### 1. Interactive Filters
Users can filter the dataset by date range, categorical values, and numerical ranges.

### 2. KPI Cards
The dashboard displays key metrics such as:
- Total Revenue
- Number of Orders
- Number of Products
- Number of Countries

### 3. Interactive Visualizations
- Monthly revenue trend using a line chart
- Top products by revenue using a bar chart
- Country-wise sales analysis
- Relationship analysis using a scatter plot

### 4. Dynamic Dashboard Updates
KPI cards and charts update automatically based on the selected filters.

### 5. Empty Results Handling
When no records match the selected filters, the dashboard displays a clear message instead of an empty or broken visualization.

### 6. Responsive User Interface
The dashboard is designed to provide a clear and accessible experience across different screen sizes.

## Project Structure
- `app.py` – main Streamlit dashboard application
- `requirements.txt` – required Python libraries
- `data/` – sample dataset used by the dashboard
- `README.md` – project documentation

## How to Run the Project

1. Clone or download the repository.
2. Install the required dependencies:

   `pip install -r requirements.txt`

3. Run the Streamlit application:

   `streamlit run app.py`

4. Open the local URL displayed in the terminal to access the dashboard.

## Expected Outcomes
- Interactive exploration of retail sales data
- Quick access to key business performance indicators
- Improved understanding of sales trends and product performance
- Dynamic visualizations based on user-selected filters

## Conclusion
This project demonstrates how interactive dashboards can make data analysis more accessible by combining dynamic filters, KPI metrics, and visualizations in a single application.


