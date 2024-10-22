# imports several functions from PySpark used for data processing
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, regexp_replace, col, lower, trim


# Initialize Spark session and create application named "WordFrequency"
spark = SparkSession.builder.appName("WordFrequency").getOrCreate()


# Load the text file
logFile = "news_data.txt"  


# Read a text file and change into the Spark DataFrame
logData = spark.read.text(logFile).cache()

# logData.show()
# +--------------------+
# |               value|
# +--------------------+
# |             HAMLET,|
# |  PRINCE OF DENMARK.|
# |              ACT I.|
# |Scene I.—ELSINORE...|
# |Francisco on his ...|
# |                    |
# |   Ber. Who's there?|
# |                    |
# |Fran. (R.) Nay, a...|
# |                    |
# |Ber. Long live th...|
# |                    |
# |               Fran.|
# |           Bernardo?|
# |                    |
# |                Ber.|
# |                 He.|
# |                    |
# |Fran. You come mo...|
# |                    |
# +--------------------+


# wordsData_1 Goal : Remove all the special cases, make words into lowercase, and put each word to individual rows.
# wordsData_1 Steps
## 1. remove leading and trailing spaces from logData "value" column data --> trim(col("value"))
## 2. convert all text to lowercase and split the text by non-word character --> split(lower(), "\\W+")
## 3. converts each array of words into individual rows --> explode()
## 4. rename the resulting column ---> alias()
## 5. select a specific column from the logData DataFrame. --> logData.select()
wordsData_1 = logData.select(explode(split(lower(trim(col("value"))), "\\W+")).alias("word"))

# wordsData_1.show()
# +---------+
# |     word|
# +---------+
# |   hamlet|
# |         |
# |   prince|
# |       of|
# |  denmark|
# |         |
# |      act|
# |        i|
# |         |
# |    scene|
# |        i|
# | elsinore|
# |        a|
# | platform|
# |   before|
# |      the|
# |   castle|
# |    night|
# |         |
# |francisco|
# +---------+


# wordsData_2 Goal : Filter out any rows where the "word" column contains empty strings, ensuring only valid words remain in the DataFrame.
wordsData_2 = wordsData_1.filter(col("word")!="")

# wordsData_2.show()
# +---------+
# |     word|
# +---------+
# |   hamlet|
# |   prince|
# |       of|
# |  denmark|
# |      act|
# |        i|
# |    scene|
# |        i|
# | elsinore|
# |        a|
# | platform|
# |   before|
# |      the|
# |   castle|
# |    night|
# |francisco|
# |       on|
# |      his|
# |     post|
# |    enter|
# +---------+


# wordCounts Goal : group each word, count the word frequency, and sort by descending order
# wordCounts Steps
## 1. groups the rows by each unique word, so all occurences of a word are combined togehter --> wordsData_2.groupBy('word')
## 2. count how many times each word appears in the grouped data --> .count()
## 3. Sort the column 'count' results in descending order --> .orderBy(col('count').desc())
wordCounts = wordsData_2.groupBy('word').count().orderBy(col('count').desc())

# Show the top 20 most frequent words
wordCounts.show(20, truncate=False)
# +----+-----+                                                                    
# |word|count|
# +----+-----+
# |the |1208 |
# |to  |769  |
# |and |760  |
# |i   |728  |
# |of  |695  |
# |a   |556  |
# |you |459  |
# |in  |436  |
# |my  |395  |
# |is  |349  |
# |it  |349  |
# |that|318  |
# |not |265  |
# |ham |261  |
# |his |255  |
# |this|243  |
# |s   |235  |
# |your|229  |
# |with|229  |
# |for |217  |
# +----+-----+

breakpoint
# Stop the Spark session
spark.stop()
