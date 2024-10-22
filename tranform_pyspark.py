from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, lower, trim

# set up sparksession
spark = SparkSession.builder.appName("TextSentimentAnalysis").getOrCreate()

# load the text file
log_file="news_data.json"
#log_data = spark.read.json(log_file).cache()
df = spark.read.option("multiline", "true").json(log_file)
df.printSchema() 
df.show(truncate=False) 

# Step 3: Check if 'articles' field exists
if 'articles' in df.columns:
    print("Step 3: 'articles' field exists in the DataFrame")

    # Step 4: Explode the 'articles' field to get individual articles
    articles_df = df.select(explode(col("articles")).alias("article"))
    print("Step 4: Exploded 'articles' field into individual rows")
    articles_df.printSchema()
    articles_df.show(truncate=False)

# read data
#articles_df = log_data.select(explode(split(lower(trim(col("value"))), "\\W+")).alias("word"))

# extract 
#log_data.show(truncate=False)

breakpoint
spark.stop()

