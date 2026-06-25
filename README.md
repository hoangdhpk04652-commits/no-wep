import pandas as pd
import pyodbc

class UserModel:

    @staticmethod
    def get_data():

        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\MSSQLSERVER01;"
            "DATABASE=thi;"
            "Trusted_Connection=yes;"
        )

        query = """
        SELECT
            Detail_ID,
            Invoice_ID,
            Customer_ID,
            Order_Date,
            Store_Location,
            Payment_Method,
            Product_ID,
            Product_Name,
            Category,
            Quantity,
            Cost_Price,
            Sale_Price,
            Invoice_Total_Discount
        FROM dbo.dataset_hoadon_sanpham
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return df
