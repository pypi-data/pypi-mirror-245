# from pyspark.sql import SparkSession
# from pyspark.ml.feature import VectorAssembler
# from pyspark.ml.clustering import KMeans
# from pyspark.ml.evaluation import ClusteringEvaluator
# from pyspark.sql.functions import col, sqrt, pow, sum

# spark = SparkSession.builder.appName("AnomalyDetection").getOrCreate()

# # Sample PySpark DataFrame
# df = spark.read.csv("path_to_your_data.csv", header=True, inferSchema=True)

# # Assume df is your PySpark DataFrame and 'features' are your columns for anomaly detection
# feature_columns = ['feature1', 'feature2']  # replace with your actual columns

# assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
# df_vector = assembler.transform(df).select('features')

# # Train a k-means model
# kmeans = KMeans().setK(3).setSeed(1)
# model = kmeans.fit(df_vector)

# # Make predictions
# predictions = model.transform(df_vector)

# # Evaluate clustering by computing Silhouette score
# evaluator = ClusteringEvaluator()

# silhouette = evaluator.evaluate(predictions)
# print("Silhouette with squared euclidean distance = " + str(silhouette))

# # Identifying the cluster centers
# centers = model.clusterCenters()

# # Calculate the distance of each point from its cluster center
# def distance_from_center(features, center):
#     return sqrt(sum([pow(features[i] - center[i], 2) for i in range(len(center))]))

# # Register the UDF
# distance_udf = F.udf(distance_from_center)

# # Assume we have a DataFrame with a 'features' column and 'prediction' column from k-means
# # Add a new column with the distance from the cluster center
# for i, center in enumerate(centers):
#     predictions = predictions.withColumn(f'distance_from_center_{i}',
#                                          distance_udf(col('features'), F.array([F.lit(c) for c in center])))

# # Now you can filter out the outliers based on the distance from the cluster centers
# # You can choose a distance threshold based on your understanding of the data
# distance_threshold = 5.0
# outliers = predictions.filter(f'distance_from_center >= {distance_threshold}')

# # Show potential outliers
# outliers.show()
