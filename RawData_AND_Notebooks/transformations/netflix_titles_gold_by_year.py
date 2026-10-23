from pyspark import pipelines as dp
from pyspark.sql.functions import col, count

@dp.table
def netflix_titles_gold_by_year_pipeline():
    

    titles = spark.read.table(
        "workspace.default.netflix_titles_silver"
    )

    yearly_counts = (
        titles
            .filter(col("release_year").between(1900,2026))
            .groupBy("release_year")
            .agg(
                count("*").alias("total_titles")
            )
    )
    return yearly_counts
