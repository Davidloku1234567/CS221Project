# This is a tutorial mostly pasted from https://github.com/google/earthengine-api/blob/master/python/examples/ipynb/TF_demo1_keras.ipynb
# It takes in some data from Earth Engine and it outputs it as a CSV file in your Google Drive
# I think you need to do the following before running this:
# pip install earthengine-api
# In the command line, run: earthengine authenticate
# - and log in with your Google account

# Import the Earth Engine API and initialize it.
import ee
# import folium
# print(folium.__version__)

# Define the URL format used for Earth Engine generated map tiles.
EE_TILES = 'https://earthengine.googleapis.com/map/{mapid}/{{z}}/{{x}}/{{y}}?token={token}'

ee.Initialize()

# Use these bands for prediction.
bands = ['BurnDate', 'Uncertainty', 'FirstDay', 'LastDay']
# Burned area data from https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD64A1
burned = ee.ImageCollection('MODIS/006/MCD64A1')

# # Cloud masking function.
# def maskL8sr(image):
#   cloudShadowBitMask = ee.Number(2).pow(3).int()
#   cloudsBitMask = ee.Number(2).pow(5).int()
#   qa = image.select('pixel_qa')
#   mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(
#     qa.bitwiseAnd(cloudsBitMask).eq(0))
#   return image.updateMask(mask).select(bands).divide(10000)
#
# # The image input data is a 2018 cloud-masked median composite.
image = burned.filterDate('2018-01-01', '2018-12-31').median()
# image = l8sr.filterDate('2018-01-01', '2018-12-31').map(maskL8sr).median()

# Use folium to visualize the imagery.
# mapid = image.getMapId({'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 0.3})
# map = folium.Map(location=[38., -122.5])
# folium.TileLayer(
#     tiles=EE_TILES.format(**mapid),
#     attr='Google Earth Engine',
#     overlay=True,
#     name='median composite',
#   ).add_to(map)
# map.add_child(folium.LayerControl())
# map

# print('IMAGE', image)

# Change the following two lines to use your own training data.
# labels = ee.FeatureCollection('projects/google/demo_landcover_labels')
region = ee.Geometry.Rectangle(-119.224, 34.669, -99.536, 50.064)
labels = ee.FeatureCollection.randomPoints(region)
# labels = ee.FeatureCollection(ee.Geometry.Point(16.37, 48.225));
label = 'BurnDate'

# print('LABELS', labels)

# Sample the image at the points and add a random column.
sample = image.sampleRegions(collection=labels, properties=[label], scale=30).randomColumn()
# sample = image.sampleRegions(scale=30).randomColumn()

# print('SAMPLE', sample)
# sample = image.stratifiedSample(
#   numPoints= 100,
#   classBand= 'BurnDate',
#   region= ee.Geometry.Polygon([[[-73, 42],[-73, 41],[-72, 41],[-72, 42]]]),
#   scale= 1000,
#   geometries= True,
# )

# Partition the sample approximately 70-30.
training = sample.filter(ee.Filter.lt('random', 0.7))
testing = sample.filter(ee.Filter.gte('random', 0.7))

from pprint import pprint

# Print the first couple points to verify.
pprint({'training': training.first().getInfo()})
pprint({'testing': testing.first().getInfo()})


outputBucket = 'stanford-cs221-wildfire-fall-2019'

# Make sure the bucket exists.
# print('Found Cloud Storage bucket.' if tf.gfile.Exists('gs://' + outputBucket) else 'Output Cloud Storage bucket does not exist.')



# Names for output files.
trainFilePrefix = 'Training_demo_'
testFilePrefix = 'Testing_demo_'

# This is list of all the properties we want to export.
featureNames = list(bands)
featureNames.append(label)

# Create the tasks.
trainingTask = ee.batch.Export.table.toDrive(
  collection=training,
  description='burnExample',
  fileFormat='CSV'
)


# trainingTask = ee.batch.Export.table.toCloudStorage(
#   collection=training,
#   description='Training Export',
#   fileNamePrefix=trainFilePrefix,
#   bucket=outputBucket,
#   fileFormat='TFRecord',
#   selectors=featureNames)
#
# testingTask = ee.batch.Export.table.toCloudStorage(
#   collection=testing,
#   description='Testing Export',
#   fileNamePrefix=testFilePrefix,
#   bucket=outputBucket,
#   fileFormat='TFRecord',
#   selectors=featureNames)

# Start the tasks.
trainingTask.start()
# testingTask.start()

# Print all tasks.
print(ee.batch.Task.list())

# Poll the training task until it's done.
import time
while trainingTask.active():
  print('Polling for task (id: {}).'.format(trainingTask.id))
  time.sleep(5)
print('Done with training export.')