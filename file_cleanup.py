from pyspark import SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import os
import re

sc = SparkContext('local')
spark = SparkSession(sc)

rootdir = './input/raw'

t_agg = input("Enter met, nut, or water to aggregate that data:")
except_t = 'You must enter met, nut, or water. Instead you entered {}'
if(t_agg not in ["met", "nut","water"]):
    raise Exception(except_t.format(t_agg))

file_list = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        file_list.append(os.path.join(subdir, file))

text = [file for file in file_list if any(txt in file for txt in ['.txt'])]
regex = re.compile(r'.*(Readme).*|.*(checkpoint).*')
text_list = [i for i in text if not regex.match(i)]
text_list

met_list = [file for file in text_list if any(txt in file for txt in ['meteorological'])]
nut_list = [file for file in text_list if any(txt in file for txt in ['nutrient'])]
water_list = [file for file in text_list if any(txt in file for txt in ['water quality'])]

if(t_agg == "met"):
    print("Aggregating meteorlogical data...")

    met_2004 = [file for file in met_list if any(txt in file for txt in ['2004'])]
    met_2005 = [file for file in met_list if any(txt in file for txt in ['2005'])]
    met_2006 = [file for file in met_list if any(txt in file for txt in ['2006'])]

    met05_data = spark.read.option("header", "true") \
        .option("delimiter", "\t") \
        .option("inferSchema", "true") \
        .csv(met_2005)
    met05_data = met05_data.drop(*['USRCODES'])

    met06_data = spark.read.option("header", "true") \
        .option("delimiter", "\t") \
        .option("inferSchema", "true") \
        .csv(met_2006)
    met06_data = met06_data.drop(*['USRCODES'])

    met04_data = spark.read.option("header", "true") \
        .option("delimiter", ",") \
        .option("inferSchema", "true") \
        .csv(met_2004)
    # dropping all F_ columns (deemed unnecessary)
    dropped_cols = [f for f in met04_data.columns if f[0] == 'F']
    met04_data = met04_data.drop(*dropped_cols)
    # splitting date and time into two separate columns
    split_col = F.split(met04_data['DateTimeStamp'], '\ ')
    met04_data = met04_data.withColumn('SMPLDATE', split_col.getItem(0)).withColumn('SMPLTIME', split_col.getItem(1))
    met04_data = met04_data.drop(*['DateTimeStamp','USRCODES'])

    met04_data.toPandas().to_csv("./input/clean/agg/NOAA_meteor_data_2004.csv")
    met05_data.toPandas().to_csv("./input/clean/agg/NOAA_meteor_data_2005.csv")
    met06_data.toPandas().to_csv("./input/clean/agg/NOAA_meteor_data_2006.csv")

    print("Done! Exported to ./input/clean/agg")

if(t_agg == "nut"):
    print("Aggregating nutritional data...")

    nut_2004 = [file for file in nut_list if any(txt in file for txt in ['2004'])]
    nut_2005 = [file for file in nut_list if any(txt in file for txt in ['2005'])]
    nut_2006 = [file for file in nut_list if any(txt in file for txt in ['2006'])]

    nut05_data = spark.read.option("header", "true") \
        .option("delimiter", "\t") \
        .option("inferSchema", "true") \
        .csv(nut_2005)

    nut06_data = spark.read.option("header", "true") \
        .option("delimiter", "\t") \
        .option("inferSchema", "true") \
        .csv(nut_2006)

    nut04_data = spark.read.option("header", "true") \
        .option("delimiter", "\t") \
        .option("inferSchema", "true") \
        .csv(nut_2004)

    nut04_data.toPandas().to_csv("./input/clean/agg/NOAA_nutrient_data_2004.csv")
    nut05_data.toPandas().to_csv("./input/clean/agg/NOAA_nutrient_data_2005.csv")
    nut06_data.toPandas().to_csv("./input/clean/agg/NOAA_nutrient_data_2006.csv")

    print("Done! Exported to ./input/clean/agg")

if(t_agg == "water"):
    print("Aggregating water quality data...")

    water_2004 = [file for file in water_list if any(txt in file for txt in ['2004'])]
    water_2005 = [file for file in water_list if any(txt in file for txt in ['2005'])]
    water_2006 = [file for file in water_list if any(txt in file for txt in ['2006'])]

    water05_data = spark.read.option("header", "true") \
        .option("delimiter", "\t") \
        .option("inferSchema", "true") \
        .csv(water_2005)

    water06_data = spark.read.option("header", "true") \
        .option("delimiter", "\t") \
        .option("inferSchema", "true") \
        .csv(water_2006)

    water04_data = spark.read.option("header", "true") \
        .option("delimiter", "\t") \
        .option("inferSchema", "true") \
        .csv(water_2004)

    water04_data.toPandas().to_csv("./input/clean/agg/NOAA_water_data_2004.csv")
    water05_data.toPandas().to_csv("./input/clean/agg/NOAA_water_data_2005.csv")
    water06_data.toPandas().to_csv("./input/clean/agg/NOAA_water_data_2006.csv")

    print("Done! Exported to ./input/clean/agg")