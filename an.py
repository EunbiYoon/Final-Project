import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col

# Step 1: Set up SparkSession
spark = SparkSession.builder \
    .appName("NewsAnalysis") \
    .getOrCreate()

# Step 2: Read the text file containing JSON data
# Replace 'news_data.txt' with the actual path to your text file
rdd = spark.sparkContext.textFile("news_data.txt")

# Step 3: Parse each line as JSON using Python's json library
def parse_json(line):
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None

# Convert JSON strings to Python dictionaries, filtering out any that failed to parse
parsed_rdd = rdd.map(parse_json).filter(lambda x: x is not None)

# Step 4: Convert the parsed RDD to a DataFrame
df = spark.createDataFrame(parsed_rdd)

# Verify the schema to understand the structure (Optional)
df.printSchema()

# Step 5: Extract and explode the 'articles' field if it exists
if 'articles' in df.columns:
    articles_df = df.select(explode(col("articles")).alias("article"))

    # Step 6: Flatten the structure and select relevant fields
    flattened_df = articles_df.select(
        "article.source.name",
        "article.author",
        "article.title",
        "article.description",
        "article.url",
        "article.publishedAt",
        "article.content"
    )

    # Display the first few rows (Optional)
    flattened_df.show(5, truncate=False)

    # Step 7: Save the processed DataFrame to CSV files
    flattened_df.write.csv("flattened_articles.csv", header=True)
else:
    print("The 'articles' field is missing in the parsed JSON.")

# Step 8: Stop the Spark session
spark.stop()
