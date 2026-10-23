
from pyspark import pipelines as dp
from pyspark.sql.functions import col, countDistinct, trim


@dp.table
def netflix_countries_gold_pipeline():

    # Read cleaned country data from the Silver layer
    countries = spark.read.table(
        "workspace.default.netflix_countries_silver"
    )

    # Remove records with missing or blank country names
    clean_countries = countries.filter(
        col("country").isNotNull()
        & (trim(col("country")) != "")
        & col("show_id").isNotNull()
    )

    # Count distinct Netflix titles associated with each country
    country_counts = (
        clean_countries
        .groupBy("country")
        .agg(
            countDistinct("show_id").alias("total_titles")
        )
    )

    # Return the country-level results
    return country_counts

