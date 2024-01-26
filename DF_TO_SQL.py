import pandas as pd
from sqlalchemy import create_engine

# MySQL connection details
mysql_user = 'your_mysql_user'
mysql_password = 'your_mysql_password'
mysql_host = 'localhost'
mysql_database = 'your_database_name'

# CSV file path
csv_file_path = 'Financial Sample.csv'

# Read CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Create a MySQL connection using SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}')

# Write DataFrame to MySQL table
df.to_sql(name='your_table_name', con=engine, if_exists='replace', index=False)

print(f"Table 'your_table_name' created successfully in MySQL.")
