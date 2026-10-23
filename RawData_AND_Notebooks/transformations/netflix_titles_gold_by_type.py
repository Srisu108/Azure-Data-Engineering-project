from pyspark import pipelines as dp
from pyspark.sql.functions import col, count, round, sum as spark_sum
from pyspark.sql.window import Window


@dp.table
def netflix_titles_gold_by_type_pipeline():
    titles = spark.read.table("workspace.default.netflix_titles_silver")

    counts = (
        titles
        .filter(col("type").isin("Movie", "TV Show"))
        .groupBy("type")
        .agg(count("*").alias("total_titles"))
    )

    window = Window.rowsBetween(
        Window.unboundedPreceding,
        Window.unboundedFollowing
    )

    return counts.withColumn(
        "percentage_of_catalogue",
        round(
            col("total_titles") * 100.0 / spark_sum("total_titles").over(window),
            2
        )
    )