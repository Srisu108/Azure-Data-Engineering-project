from pyspark import pipelines as dp
from pyspark.sql.functions import col, count, trim

@dp.table
def netflix_categories_gold_pipeline():
    # Read the clean category data from the silver layer
    categories = spark.read.table(
        "workspace.default.netflix_category_silver"
    )

    # Remove misiing or blank category values
    clean_categories = categories.filter(
        col("listed_in").isNotNull()
        & (trim(col("listed_in")) != "")
    )

    # Count the number of assignments for each category
    category_counts = (
        clean_categories
        .groupby("listed_in")
        .agg(count("*").alias("category_assignments"))
    )
    # Return the 20 most frequent categories
    return(
        category_counts
        .orderBy(col("category_assignments").desc())
        .limit(20)
        .withColumnRenamed("listed_in", "category")

    )