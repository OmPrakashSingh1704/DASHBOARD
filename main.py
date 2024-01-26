import tempfile
import streamlit as st
import pandas as pd
import mysql.connector
from io import BytesIO
import plotly.graph_objects as go
import random
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import sweetviz
import dtale
from ydata_profiling import profile_report

st.set_page_config(page_title="FINANCIAL DASHBOARD", page_icon=":bar_chart:", layout="wide")

st.title(" :chart_with_upwards_trend: BARCLAYS FINANCIAL DASHBOARD")
st.markdown('_DASHBOARD v0.1.0_')
st.markdown("<style>div.block-container{padding-top:1rem; display: flex;}</style>", unsafe_allow_html=True)

st.header("Configuration")

# Toggle to select the data source
data_source = st.toggle("Select Data Source (ON -> MySQL Server/ OFF -> UPLOAD FILE)", ["MySQL Server", "File Upload"])

# Initial values for select boxes
selected_database = None
selected_table = None

if data_source:
    st.info("You selected MySQL Server as the data source.")

    col1,col2=st.columns((2))

    # Get MySQL credentials from the user
    with col1:
        mysql_username = st.text_input("Enter MySQL Username:")
    with col2:
        mysql_password = st.text_input("Enter MySQL Password:", type="password")

    # Connect to MySQL with provided credentials
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=mysql_username,
            passwd=mysql_password,
            # database='barclays'  # Replace with your actual database name
        )

        cursor = connection.cursor()

        cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in cursor.fetchall()]
        selected_database = st.selectbox("Select Database", [""] + databases)  # Add an empty option

        if selected_database:
            # Use the selected database
            connection.database = selected_database

            # Get a list of tables in the selected database
            cursor.execute(f"SHOW TABLES FROM {selected_database}")
            tables = [table[0] for table in cursor.fetchall()]
            selected_table = st.selectbox("Select Table", [""] + tables)  # Add an empty option

            if selected_table:
                # Read data from MySQL table
                df = pd.read_sql(f"SELECT * FROM {selected_table}", connection)
            else:
                st.warning("Please select a table.")

    except mysql.connector.Error as err:
        st.error("PLEASE ENTER YOUR CREDENTIALS")
        st.stop()
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

else:
    st.info("You have selected to upload a file as a data source.")
    # File upload section remains the same
    f1 = st.file_uploader(":file_folder: UPLOAD A FILE", type=["csv", 'txt', 'xlsx', 'xls'])
    if f1 is None:
        st.info(" Upload a file through config", icon="ℹ️")
        st.stop()

    @st.cache_data
    def load_data(file):
        # Get the file name
        file_name = file.name.lower()

        # Read data based on file format
        if file_name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file_name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format. Please upload a CSV, TXT, XLS, or XLSX file.")
            st.stop()

        return df

    df = load_data(f1)

if 'df' in locals():
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = pd.to_datetime(df['Date']).dt.year

    # st.sidebar.header("Choose Your Filters: ")
    #
    # Segment = st.sidebar.multiselect('Pick a Segment: ', df['Segment'].unique())
    # if not Segment:
    #     df2 = df.copy()
    # else:
    #     df2 = df[df['Segment'].isin(Segment)]
    #
    # Country = st.sidebar.multiselect("Pick a Country", df['Country'].unique())
    # if not Country:
    #     df3 = df2.copy()
    # else:
    #     df3 = df2[df2['Country'].isin(Country)]
    #
    # Product = st.sidebar.multiselect("Pick a Product", df["Product"].unique())

    with st.expander("Data Preview"):
        tab1,tab2=st.tabs(["DataFrame",'dTale'])
        with tab1:
            st.dataframe(
                df.style.background_gradient(cmap='Oranges'),
                column_config={"Year": st.column_config.NumberColumn(format="%d")},
                use_container_width=True
            )

            # Convert DataFrame to BytesIO object
            csv_file = BytesIO()
            df.to_csv(csv_file, index=False)
            csv_file.seek(0)

            # Download button
            st.download_button(
                label="Download Dataset",
                data=csv_file,
                file_name=f"{selected_database}_{selected_table}.csv",
                mime="text/csv",
            )
        with tab2:
            mydtale=dtale.show(df).main_url()
            st.components.v1.iframe(mydtale, height=450, scrolling=True)
            if st.button("OPEN IN BROWSER"):
                dtale.show(df).open_browser()
    def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                value=value,
                gauge={"axis": {"visible": False}},
                number={
                    "prefix": prefix,
                    "suffix": suffix,
                    "font.size": 28,
                },
                title={
                    "text": label,
                    "font": {"size": 24},
                },
            )
        )

        if show_graph:
            fig.add_trace(
                go.Scatter(
                    y=random.sample(range(0, 101), 30),
                    hoverinfo="skip",
                    fill="tozeroy",
                    fillcolor=color_graph,
                    line={
                        "color": color_graph,
                    },
                )
            )

        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=False, fixedrange=True)
        fig.update_layout(
            # paper_bgcolor="lightgrey",
            margin=dict(t=30, b=0),
            showlegend=False,
            plot_bgcolor="white",
            height=100,
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_gauge(
        indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
    ):
        fig = go.Figure(
            go.Indicator(
                value=indicator_number,
                mode="gauge+number",
                domain={"x": [0, 1], "y": [0, 1]},
                number={
                    "suffix": indicator_suffix,
                    "font.size": 26,
                },
                gauge={
                    "axis": {"range": [0, max_bound], "tickwidth": 1},
                    "bar": {"color": indicator_color},
                },
                title={
                    "text": indicator_title,
                    "font": {"size": 28},
                },
            )
        )
        fig.update_layout(
            # paper_bgcolor="lightgrey",
            height=200,
            margin=dict(l=10, r=10, t=50, b=10, pad=8),
        )
        st.plotly_chart(fig, use_container_width=True)


    top_left_column, top_right_column = st.columns((2, 1))
    with top_left_column:
        column_1, column_2, column_3, column_4 = st.columns(4)

        with column_1:
            plot_metric(
                "Total Accounts Receivable",
                6621280,
                prefix="$",
                suffix="",
                show_graph=True,
                color_graph="rgba(0, 104, 201, 0.2)",
            )
            plot_gauge(1.86, "#0068C9", "%", "Current Ratio", 3)

        with column_2:
            plot_metric(
                "Total Accounts Payable",
                1630270,
                prefix="$",
                suffix="",
                show_graph=True,
                color_graph="rgba(255, 43, 43, 0.2)",
            )
            plot_gauge(10, "#FF8700", " days", "In Stock", 31)

        with column_3:
            plot_metric("Equity Ratio", 75.38, prefix="", suffix=" %", show_graph=False)
            plot_gauge(7, "#FF2B2B", " days", "Out Stock", 31)

        with column_4:
            plot_metric("Debt Equity", 1.10, prefix="", suffix=" %", show_graph=False)
            plot_gauge(28, "#29B09D", " days", "Delay", 31)

    with top_right_column:
        # st.subheader("Segment Vs. Gross Sales")
        fig=px.bar(df,
                    y='Gross Sales',
                   x='Segment',
                   color='Country',
                    # title='Gross Sales of Every Segment Country-wise',
                   barmode='relative',
                   title="Segment Vs. Gross Sales"
                   )
        st.plotly_chart(fig,use_container_width=True)

    col01,col02=st.columns((1,2))

    with col01:
        st.subheader('Units Sold per Segment')
        with plt.style.context('Solarize_Light2'):
            fig0=px.pie(df,values='Units Sold',names='Segment',hole=0.5)
            fig0.update_traces(text=df['Segment'],textposition='outside')
            st.plotly_chart(fig0,use_container_width=True)

    with col02:
        all_months = df['Month Name'].unique()
        products = df['Product'].unique()
        rows = []
        for i in all_months:
            for j in products:
                tot_pro = df[(df['Product'] == j) & (df['Month Name'] == i)]['Profit'].sum()
                rows.append([j, i, tot_pro])
        unpivoted_data=pd.DataFrame(columns=['Product','Month Name','Profit'],data=rows)
        # Define the custom order for months
        custom_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                        'November', 'December']

        # Convert 'Month Name' to a categorical type with the custom order
        unpivoted_data['Month Name'] = pd.Categorical(unpivoted_data['Month Name'], categories=custom_order, ordered=True)

        # Sort the DataFrame by the 'Month Name' column
        unpivoted_data = unpivoted_data.sort_values(by='Month Name')
        fig1 = px.line(unpivoted_data,
                      x='Month Name',
                      y='Profit',
                      color='Product',
                      markers=True,
                      text='Profit',
                      title="Monthly Profit of Products"
                      )
        fig1.update_traces(textposition='top center')
        st.plotly_chart(fig1, use_container_width=True)

    rows=[]
    for i in all_months:
        for j in products:
            tot_pro = df[(df['Product'] == j) & (df['Month Name'] == i)]['Units Sold'].sum()
            rows.append([i,j,tot_pro])
    unpivoted_data = pd.DataFrame(columns=['Month Name', 'Product', 'Units Sold'], data=rows)
    # Define the custom order for months
    custom_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                    'November', 'December']

    unpivoted_data['Month Name'] = pd.Categorical(unpivoted_data['Month Name'], categories=custom_order, ordered=True)
    unpivoted_data = unpivoted_data.sort_values(by='Month Name')
    fig2 = px.line(unpivoted_data,
                  x='Month Name',
                  y='Units Sold',
                  color='Product',
                  markers=True,
                  text='Units Sold',
                  title="Monthly Unit Sold of Products"
                  )
    fig2.update_traces(textposition='top center')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Sales Vs. Months")
    fig3=px.violin(df,x='Month Name',y=' Sales',box=True,hover_data=df.columns)
    st.plotly_chart(fig3,use_container_width=True)

    st.subheader('Hierarchical view of Sales using TreeMap')
    fig4=px.treemap(df,path=['Country','Segment','Product'],values=' Sales',color='Product')
    fig4.update_layout(height=550)
    st.plotly_chart(fig4,use_container_width=True)

    st.subheader('Month wise Product Sales Summary')
    with st.expander("Summary_Table"):
        df_sample=df[0:5][['Country','Segment','Product','Units Sold','Manufacturing Price','Sale Price','Profit']]
        fig5=ff.create_table(df_sample,colorscale='Cividis')
        st.plotly_chart(fig5,use_container_width=True)

        st.markdown('Month wise Product table')
        Product_Year=pd.pivot_table(data=df,values=' Sales',index=['Product'],columns='Month Name')
        st.write(Product_Year.style.background_gradient(cmap='Blues'))

    data1=px.scatter(df,x=' Sales',y='Profit',size='Units Sold')
    data1['layout'].update(title='Relationship between Sales and Profits using Scatter Plot.',
                           titlefont=dict(size=20),
                           xaxis=dict(title='Sales',titlefont=dict(size=19)),
                           yaxis=dict(title='Profit',titlefont=dict(size=19)))
    st.plotly_chart(data1,use_container_width=True)

    st.subheader('Explore Data Summary with SweetViz or Pandas Profiling Report.  (This might take long to load)')
    with st.container(height=600):
        col11, col12 = st.tabs(["SweetViz", "Pandas Profile"])
        with col11:
            st.markdown('SWEETVIZ REPORT')
            report0=sweetviz.analyze(df)
            temp_html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
            report0.show_html(filepath=temp_html_file.name,open_browser=False)
            st.download_button(label="Download SweetViz Report", data=temp_html_file.name,
                               file_name="SWEETVIZ_REPORT.html")
            # Display the Sweetviz report using an iframe
            with st.container(height=400):
                st.components.v1.html(open(temp_html_file.name, 'r').read(),scrolling=True,height=400)

        with col12:
            st.markdown('PANDAS PROFILE REPORT ')

            pr = profile_report.ProfileReport(df)
            html_content=pr.to_html()
            st.download_button(label="Download Pandas Profiling Report", data=html_content,
                               file_name="Pandas_profiling_report.html")
            with st.container(height=400):
                st.components.v1.html(html_content,scrolling=True,height=400)