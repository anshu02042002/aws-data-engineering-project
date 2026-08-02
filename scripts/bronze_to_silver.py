from pyspark.sql import SparkSession

# ----------------------------------------
# AWS Configuration
# ----------------------------------------

BUCKET_NAME = "anshu-data-engineering-project-2026"

spark = (
    SparkSession.builder
    .appName("AWS-DE-Project")
    .config(
        "spark.jars.packages",
        "org.apache.hadoop:hadoop-aws:3.4.1"
    )
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider"
    )
    .getOrCreate()
)

print("Spark Session Created Successfully")

# ----------------------------------------
# Read Customers Bronze Data
# ----------------------------------------

customers_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(f"s3a://{BUCKET_NAME}/bronze/customers/customers.csv")
)

customers_df.show()
customers_df.printSchema()
print(customers_df.columns)


from pyspark.sql.functions import col, trim

# ----------------------------------------
# Bronze -> Silver Transformation
# ----------------------------------------

customers_silver = (
    customers_df
    .dropDuplicates(["customer_id"])
    .filter(col("customer_id").isNotNull())
    .withColumn("first_name", trim(col("first_name")))
    .withColumn("last_name", trim(col("last_name")))
    .withColumn("email", trim(col("email")))
    .withColumn("city", trim(col("city")))
    .withColumn("state", trim(col("state")))
)

print("Customers Silver Data")
customers_silver.show()


# ----------------------------------------
# Write Silver Layer
# ----------------------------------------

customers_silver.write \
    .mode("overwrite") \
    .parquet(
        f"s3a://{BUCKET_NAME}/silver/customers/"
    )

print("Customers Silver layer created successfully!")


silver_df = spark.read.parquet(
    f"s3a://{BUCKET_NAME}/silver/customers/"
)

print("Reading Silver Data")
silver_df.show()


# ----------------------------------------
# Read Products Bronze Data
# ----------------------------------------

products_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(f"s3a://{BUCKET_NAME}/bronze/products/products.csv")
)

print("Products Bronze Data")
products_df.show()
products_df.printSchema()
print(products_df.columns)



from pyspark.sql.functions import col, trim

# ----------------------------------------
# Bronze -> Silver Transformation (Products)
# ----------------------------------------

products_silver = (
    products_df
    .dropDuplicates(["product_id"])
    .filter(col("product_id").isNotNull())
    .filter(col("price") > 0)
    .withColumn("product_name", trim(col("product_name")))
    .withColumn("category", trim(col("category")))
)

print("Products Silver Data")
products_silver.show()


# ----------------------------------------
# Write Products Silver Layer
# ----------------------------------------

products_silver.write \
    .mode("overwrite") \
    .parquet(
        f"s3a://{BUCKET_NAME}/silver/products/"
    )

print("Products Silver layer created successfully!")


products_silver_df = spark.read.parquet(
    f"s3a://{BUCKET_NAME}/silver/products/"
)

print("Reading Products Silver Data")
products_silver_df.show()


# ----------------------------------------
# Read Orders Bronze Data
# ----------------------------------------

orders_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(f"s3a://{BUCKET_NAME}/bronze/orders/orders.csv")
)

print("Orders Bronze Data")
orders_df.show()
orders_df.printSchema()
print(orders_df.columns)


from pyspark.sql.functions import col

# ----------------------------------------
# Bronze -> Silver Transformation (Orders)
# ----------------------------------------

orders_silver = (
    orders_df
    .dropDuplicates(["order_id"])
    .filter(col("order_id").isNotNull())
    .filter(col("customer_id").isNotNull())
    .filter(col("product_id").isNotNull())
    .filter(col("quantity") > 0)
)

print("Orders Silver Data")
orders_silver.show()


# ----------------------------------------
# Write Orders Silver Layer
# ----------------------------------------

orders_silver.write \
    .mode("overwrite") \
    .parquet(
        f"s3a://{BUCKET_NAME}/silver/orders/"
    )

print("Orders Silver layer created successfully!")


orders_silver_df = spark.read.parquet(
    f"s3a://{BUCKET_NAME}/silver/orders/"
)

print("Reading Orders Silver Data")
orders_silver_df.show()