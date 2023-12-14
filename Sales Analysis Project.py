# Databricks notebook source
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType

schema = StructType([
    StructField("product_id", IntegerType(), True),
    StructField("customer_id", StringType(), True),
    StructField("order_date", DateType(), True),
    StructField("location", StringType(), True),
    StructField("source_order", StringType(), True)
])

sales_df = spark.read.format("csv").option("inferschema", "true").schema(schema).load('/FileStore/tables/sales_csv.txt')
display(sales_df)






# DBTITLE 1,Deriving year, month, quarter
from pyspark.sql.functions import month, quarter, year

sales_df = sales_df.withColumn('order_year', year(sales_df.order_date))
sales_df = sales_df.withColumn('order_quarter', quarter(sales_df.order_date))
sales_df = sales_df.withColumn('order_month', month(sales_df.order_date))
display(sales_df)



# DBTITLE 1,Menu dataframe
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType

schema = StructType([
    StructField("product_id", IntegerType(), True),
    StructField("product_name", StringType(), True),
    StructField("price", StringType(), True),

])

menu_df = spark.read.format("csv").option("inferschema", "true").schema(schema).load('/FileStore/tables/menu_csv.txt')
display(menu_df)



# DBTITLE 1,Total amount spent by each customer
total_amount_spent = (sales_df.join(menu_df, 'product_id').groupBy('customer_id').agg({'price':'sum'}).orderBy('customer_id'))

display(total_amount_spent)



# DBTITLE 1,Total amount spent by each food category
total_amount_spent = (sales_df.join(menu_df, 'product_id').groupBy('product_name').agg({'price':'sum'}).orderBy('product_name'))

display(total_amount_spent)



# DBTITLE 1,Total Amount spent in each month
df1 = (sales_df.join(menu_df, 'product_id').groupBy('order_month').agg({'price':'sum'}).orderBy('order_month'))

display(df1)



# DBTITLE 1,Yearly sales
df2 = (sales_df.join(menu_df, 'product_id').groupBy('order_year').agg({'price':'sum'}).orderBy('order_year'))

display(df2)



# DBTITLE 1,Quarterly sales
df2 = (sales_df.join(menu_df, 'product_id').groupBy('order_quarter').agg({'price':'sum'}).orderBy('order_quarter'))

display(df2)



# DBTITLE 1,How many times each product purchased
from pyspark.sql.functions import count 

most_df = (sales_df.join(menu_df, 'product_id').groupBy('product_id','product_name').agg(count('product_id').alias('product_count'))).orderBy('product_count', ascending = 0).drop('product_id')

display(most_df)



# DBTITLE 1,Top 3 ordered items
from pyspark.sql.functions import count 

most_df = (sales_df.join(menu_df, 'product_id').groupBy('product_id','product_name').agg(count('product_id').alias('product_count'))).orderBy('product_count', ascending = 0).drop('product_id').limit(3)

display(most_df)



# DBTITLE 1,Top ordered item
from pyspark.sql.functions import count 

most_df = (sales_df.join(menu_df, 'product_id').groupBy('product_id','product_name').agg(count('product_id').alias('product_count'))).orderBy('product_count', ascending = 0).drop('product_id').limit(1)

display(most_df)


# DBTITLE 1,Frequency of customer visited the restaurant
from pyspark.sql.functions import countDistinct

df = (sales_df.filter(sales_df.source_order == "Restaurant").groupBy('customer_id').agg(countDistinct("order_date")))

display(df)


# DBTITLE 1,Total sales by each country
df3 = (sales_df.join(menu_df, 'product_id').groupBy('location').agg({'price':'sum'}))

display(df3)


# DBTITLE 1,Total sales by order_source
df3 = (sales_df.join(menu_df, 'product_id').groupBy('source_order').agg({'price':'sum'}))

display(df3)
