# This is a tutorial mostly pasted from https://github.com/google/earthengine-api/blob/master/python/examples/ipynb/TF_demo1_keras.ipynb
# It takes in some data from Earth Engine and it outputs it as a CSV file in your Google Drive
# I think you need to do the following before running this:
# pip install earthengine-api
# In the command line, run: earthengine authenticate
# - and log in with your Google account

# Import the Earth Engine API and initialize it.
import ee
import regions

# Define the URL format used for Earth Engine generated map tiles.
EE_TILES = 'https://earthengine.googleapis.com/map/{mapid}/{{z}}/{{x}}/{{y}}?token={token}'

ee.Initialize()

# Burned area data from https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD64A1

TEMPERATURE = 'OREGONSTATE/PRISM/AN81d'
PRECIPITATION = 'JAXA/GPM_L3/GSMaP/v6/operational'
ELEVATION = 'CGIAR/SRTM90_V4'
LEAF_AREA = 'MODIS/006/MCD15A3H'
SOIL_TYPE = 'CSP/ERGo/1_0/US/lithology'
EVAPORATION = 'CAS/IGSNRR/PML/V2'

BURNED_AREA = 'MODIS/006/MCD64A1'

image_collection = ee.ImageCollection(BURNED_AREA)

# # The image input data is a 2018 cloud-masked median composite.
image = image_collection.filterDate('2018-01-01', '2018-12-31').median()

# Change the following two lines to use your own training data.
region = regions.california()
labels = ee.FeatureCollection.randomPoints(region, 10000)


# Sample the image at the points and add a random column.
sample = image.sampleRegions(collection=labels, scale=30) #.randomColumn()

# Partition the sample approximately 70-30.
# training = sample.filter(ee.Filter.lt('random', 0.7))
# testing = sample.filter(ee.Filter.gte('random', 0.7))
training = sample

# Names for output files.
trainFilePrefix = 'Training_demo_'
testFilePrefix = 'Testing_demo_'

# This is list of all the properties we want to export.
# featureNames = list(bands)
# featureNames.append(label)

# Create the tasks.
trainingTask = ee.batch.Export.table.toDrive(
  collection=training,
  description='Burned',
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
  time.sleep(10)
print('Done with training export.')