# California Wildfire Risk Prediction


Each year there are about 80,000 wildfires in the United States (Williams, Sky B.T., 2018), most of which are very small and go unnoticed, however some become an un-containable forest fire that destroys everything in its path. These wildfires can be incredibly dangerous, claiming a reported 1,114 lives between 1920 and 2015 (www.nifc.gov), thus it has become increasingly important to learn about what causes wildfires, what drives their size and spread, and what contributes to their behavior such that these learnings can benefit the fire suppression and prevention efforts.
In recent decades, it has become increasingly noticeable that climate patterns have contributed to variations in magnitude, frequency and duration of wildfires. Our goal in this project is to develop a machine learning model to predict future wildfire occurrences and severity based on location, local climate, and land surface conditions. Impact- wise, we believe that more powerful modeling techniques made possible with learning and inference-based models can increase the predictive, and ultimately preventative, power of fire risk management. We will explore various different techniques to shed light on optimal model types, as well as useful feature types. The scope of this project is limited to the wildfires of the State of California, although our process detailed below should generalize across locales.

## Dataset
We used datasets from Google Earth Engine where data is collected from 9 satellite imagery and geospatial data sources. Given a latitude/longitude coordinate and date/time range, these sources provide information on temperature, precipitation, elevation, leaf area, soil type, human modification, forest area, radiation, and fire data. We sampled 100,000 random locations from within a bounding region of the State of California, and for each location we gathered a total of 45 features and 2 labels from 2017. The two labels indicate whether a fire has occurred, and the uncertainty/severity level of the fire.

Data Sources:
1. Climate (OREGONSTATE/PRISM/AN81d) - US climate data is gathered from the PRISM dataset which is
helpful in collecting air pressure and temperature data (Daly et al., 2008).
2. Precipitation (OpenLandMap/CLM/CLM_PRECIPITATION_SM2RAIN_M/v01) - the dataset is used to gather
monthly precipitation data (Hengl, 2007).
3. Elevation (CGIAR/SRTM90_V4) - the SRTM dataset is used to collect elevation metrics (Jarvis et al.,2008).
4. Leaf Area (MODIS/006/MCD15A3H) - the leaf area data from pixel estimations is gathered using MODIS
sensors on NASA’s satellites (Myneni et al., 2015).
5. Soil Type (CSP/ERGo/1_0/US/lithology) - the US Lithology dataset is used to distinguish between 21 different
kinds of soil type (Theobald et al., 2015).
6. Human Modification (CSP/HM/GlobalHumanModification) - we have also gathered data from the global
Human Modification dataset on the human modification of terrestrial lands (Kennedy et al., 2019).
7. Forest Area (JAXA/ALOS/PALSAR/YEARLY/FNF) - to strengthen our model’s understanding of the land
categories, we added data from the global forest map on forest, non-forest, and water classes (Shimada, 2007).
8. Wind and Radiations (IDAHO_EPSCOR/GRIDMET) - we used the Gridded Surface Meteorological dataset
which also includes various surface radiation fields (Abatzoglou, 2012).
9. Burned Area (MODIS/006/MCD64A1) - finally, we used the MODIS Terra burned area dataset for the wildfire
labels (Giglio, 2015).

## Methods

Since we are interested in predicting future fires and the severity of those fires, we split our prediction task into 1) a fire/no-fire classification task and 2) a fire severity prediction task.
Figure 1: Two-level wildfire risk assessment pipeline
The fire/no-fire classification task uses all 45 features to predict the fire/no-fire label for each location in the training set. However, because the number of no-fire cases greatly outnumbers the fire cases, we train using a smaller datasetconsisting of a 50/50 distribution between fire and no-fire cases. This ensures that the model does not simply predict no-fire for every datapoint. After training the fire/no-fire classifier in this way, we then test it using a full dataset consisting of the natural distribution between fire and no-fire cases. For the fire/no-fire classification, we experimented with seven different models to compare the effectiveness of each: Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, AdaBoost, SVM, and Ridge Classifier.
The fire severity prediction task also uses all 45 features to predict the fire uncertainty, although this model only trains using fire occurrence data points. The fire uncertainty is a metric from 1-100 (although most are between 1-20). Because we wanted precision and recall metrics that we could compare to the results of the fire/no-fire classifier and because we wanted to test similar models on both, we treated this prediction task as a classification task as well. We tested the following 7 models for effectiveness on the fire severity task: Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, Multilayer Perceptron, K Nearest Neighbors, and Gaussian Process.

## Experiments & results

### Baseline with Logistic Regression
Initially we started by experimenting with distance-based Logistic Regression (LR) classifier as our baseline. For this exploration we used all the 45 features and have randomly split overall 80,588 samples as 80% training set and 20% test set. We’ve trained LR using 5-fold cross-validation technique and found that the precision result of fire risk prediction was only 15.2%. In order to understand why the LR classifier was poorly predicting the fire uncertainty, we explored the distribution of all sample datasets and learned that the no-fire samples (i.e. uncertainty of 100) occupies the vast majority of the datasets (98.69 as depicted in Figure 2) and the number of fire samples (i.e. uncertainty < 20) was extremely low when compared to the no-fire datasets. This imbalance in terms of quantity of fire and no-fire was causing noticeable bias in the above LR predictor

### Two level risk assessment

One level LR classifier ended up containing a large amount of false alarms and poor forecast of destructive fires. This motivated us to discard one-level system and moved to multi-level systems, which was similar to the idea used in a multi-layer feed forward Neural Networks. We came up with two-level pipelined system. The first level is to give a rough judgement of fire and no-fire. The second level predictor focuses on the fire risk prediction and only trains using fire occurrence data points if the first level determines an occurrence of fire. Such separation allows us to pay extra attention on those huge, destructive fire cases. After applying this two-level pipelined system, we could achieve 23% in precision and 40% in recall for fire severity estimation. Meanwhile, the precision and recall of no-fire was close to 100% and 77% respectively. Then we tried normalization and a few combinations of hyperparameters involving solver and class_weight. But it was difficult for the linear-based LR model to go above 30%. We started considering whether the features pruned in LR classifier could be utilized to increase the precision of fire risk. Then we turned our attention on tree-based models.
### Tree-based models
The first tree-based model we tried was Gradient Boosting classifier (GBClassifier), which is an additive model in a forward stage-wise fashion. For the fire-no-fire prediction level, the number of estimators was set to 3000 and number of features used at each node was a fraction of the number of features used in the model. The GBClassifier contains more hyperparameters, which allows us to tune the model in multiple ways. The tree structure is affected by max_depth and min_samples_leaf. The max_depth controls the degree of features’ interactions. We can get a higher variance by increasing max_depth. The min_samples_leaf decides the sufficient number of samples per leaf, which will increase bias if a larger value is given. The learning_rate determines the prediction shrinking rate of each tree. A larger learning_rate value normally requires a higher number of estimators, which is a tradeoff between accuracy and runtime. The hyperparameters of subsample and max_features are used by stochastic gradient boosting to do the training set subsampling and find the best split node.
Instead of experimenting each hyperparameter manually, we fed them into GridSearchCV to do exhaustive search over the specified hyperparameter ranges. We created a worksheet on CodaLab, once again using the 5-CV K-Fold method to protect against misleading error metrics from random data patterns. We repeated above same steps for the second-level fire risk prediction system. It took about half a day for each Bundle to output the optimal hyperparameter combination by using 4 CPUs and 2GB RAM. The fire-no-fire predictor showed 23% precision and 83% recall.

### Results and processing time improvements for Gradient Boosting
Further, by down-sampling the no-fire samples to the size of 10,000, we can increase the precision value to 66% without sacrificing recall value. In the fire uncertainty predictor, the precision and recall values were improved by 51% and 52%, respectively. The result implies that tree-based classifiers fit fire uncertainty better. And non-linear relations among features is important for accurate fire risk prediction. This was also verified when we experimented on Multilayer Perceptron, which gave the precision of 52% and the recall of 51%. In order to increase accuracy, we increased the number of estimators to 5,000. It took more than one day to generate the optimal hyperparameter set but the resulting difference is less than 1%. By drawing the deviance
graph of training set and testing set (Figure 3), we found that the difference between training and test set didn’t change after the boosting iterations of 400. This discovery indicated that the number of estimators can be reduced from 3000 to 400 without affecting the current accuracy, and it would save a lot of processing time.

### Additional tree-based models
Further, we used the same training set to fit other models including AdaBoost, SVM, Ridge Classifier, K Neighbors and Gaussian Process Classifier, but their results are not better than that of GBClassifier.
Below are the accuracy metrics from experimenting with various models, for both prediction tasks.

Fire/no-fire model performance


Fire severity model performance


## Model analysis

Comparison of Gradient Boosting and Multilayer Perceptron (Models with optimal results)
Fire severity classification using GBClassifier showed significant improvement relative to the classification using the traditional distance-based model, with ~62% increase in precision and ~15% in recall when training data using two- level pipelined system. Significant improvements in classification accuracy were observed for most fire uncertainties, with considerably less misclassification for high severity fires (uncertainty < 20). Though the precision and recall results are similar for GBClassifier and Multilayer Perceptron, GBClassifier performed better in terms of misclassification, which could be observed from the confusion matrix of fire uncertainty (Figure 4). The false predicted fire severity was much closer to the diagonal, while the results of Multilayer Perceptron were sparsely spread along the diagonal.

Extreme Gradient Boosting
The benefit of down-sampling no-fire data points further led us to search for a better pipeline model using auto ML tools. The generated optimal pipeline result demonstrated that single-level XGBClassifier was still preferred when we trained on compact no-fire dataset, but two-level either Random Forest-XGBClassifier or BernoulliNB- XGBClassifier were the better choice if more no-fire data points were included in training. That is, multi-level predictors can reveal more information when training dataset is imbalanced. Besides using a smaller no-fire dataset to balance the number of fire severity samples, this search result implies another way to resolve the sample imbalance is by stacking multiple classifiers.
Comparison of Logistic Regression (Baseline), Gradient Boosting (Optimal Model) and Stacked Random Forest - XGBoost

## Feature analysis

Top 3 Partial Dependence
The following plots highlights the impact of top 3 features (surface downward shortwave radiation (srad), wind direction and wind velocity) on causing wildfires for both Random Forest and Gradient Boosting.

Key observations for Gradient Boosting
For the fire/no-fire classification, studying the relationship (Figure 7) among the wind velocity, wind direction and shortwave radiation (srad) we found that the main factors causing wildfire events were high surface temperature along with low-to-moderate wind velocity, and wind that originated in the south was more likely to cause wildfires.


For the fire severity prediction, the most important features for the Gradient Boosting model are elevation, daily maximum temperature and global human modification. The relationship graphs (Figure 8) of these three features showed that we had more destructive fires in the area with high human modification (e.g. settlement, electrical infrastructure, agriculture, transportation, etc.) and areas with such high human modification value were mostly located at low elevation. Additionally, precipitation was another relevant feature, which was the fourth important feature in both prediction systems.

## Conclusion
Based on the list of experimentations performed, we conclude that the ensemble models can predict most fire cases correctly and also give low false prediction for no-fire cases, the Random Forest and Gradient Boosting perform better on wildfire prediction and Gradient Boosting and Multilayer Perceptron can predict fire severity more desirably. Furthermore, fire/no-fire prediction is dominated by a small number of features, while fire severity is based on the effect of overall features. The wind velocity, wind direction and surface temperature are important factors for occurrence of fire, and human activity in the region of fire worsens its severity. Thus, these results suggest that careful thought regarding the use of natural resources would be beneficial in lowering fire risk.

## References

1. Google Earth Engine, https://earthengine.google.com/
2. Pechony O, Shindell DT (2010). Driving forces of global wildfires over the past millennium and the
forthcoming century. PNAS, http://www.pnas.org/content/107/45/19167
3. Eidenshink J, Schwind B, Brewer K, Zhu Z, Quayle B, Howard S (2007). A Project for Monitoring Trends in
Burn Severity. Fire Ecology, https://doi.org/10.4996/fireecology.0301003
4. Heisig, J. (2018, April 12). Step by Step: Burn Severity mapping in Google Earth Engine. UN Spider,
http://www.un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/burn-
severity-earth-engine
5. Carolynne Hultquist, Gang Chen, Kaiguang Zhao: A comparison Gaussian process regression, random forests and support vector regression for burn severity assessment in diseased forest: 2014 https://pages.uncc.edu/gang-chen/wp-content/uploads/sites/184/2014/10/Hultquist_RSL_2014_Machine- Learning-Diseased-Forests.pdf
6. Williams, Sky B.T.: Wildfire Destruction - A Random Forest Classification of Forest Fires: 2018
https://towardsdatascience.com/wildfire-destruction-a-random-forest-classification-of-forest-fires-
e08070230276
7. L. Collins, P. Gfiggioen, G. Newell, A. Mellor: The utility of Random Forests for wildfire severity mapping: 2018
http://freepaper.me/PDF/?pdfURL=aHR0cHM6Ly9mcmVlcGFwZXIubWUvbi83QTh5SFRlQjdlMEFNLVVPQk VUcXV3L1BERi9mNC9mNGZhOWUzMjRlZGYzMWYzMjcxZjA4ZWZkNzFlNGJjNi5wZGY=&doi=10.1016/j.rs e.2018.07.005
8. Daly, C., Halbleib, M., Smith, J.I., Gibson, W.P., Doggett, M.K., Taylor, G.H., Curtis, J., and Pasteris, P.A. 2008. Physiographically-sensitive mapping of temperature and precipitation across the conterminous United States. International Journal of Climatology, 28: 2031-2064
9. Daly, C., J.I. Smith, and K.V. Olson. 2015. Mapping atmospheric moisture climatologies across the conterminous United States. PloS ONE 10(10):e0141140. doi:10.1371/journal.pone.0141140.
10. Hengl, T. 2007. Monthly Precipitation in Mm At 1 Km Resolution Based on Sm2rain-ascat 2007-2018, Imerge, Chelsa Climate and Worldclim https://zenodo.org/record/3256275#.XetO9y-ZMUE
11. Jarvis, A., H.I. Reuter, A. Nelson, E. Guevara. 2008. Hole-filled SRTM for the globe Version 4, available from the CGIAR-CSI SRTM 90m Database: http://srtm.csi.cgiar.org.
12. Myneni, R., Knyazikhin, Y., Park, T. (2015). MCD15A3H MODIS/Terra+Aqua Leaf Area Index/FPAR 4-day L4 Global 500m SIN Grid V006 [Data set]. NASA EOSDIS Land Processes DAAC. Accessed 2019-12-07 from https://doi.org/10.5067/MODIS/MCD15A3H.006
13. Theobald, D. M., Harrison-Atlas, D., Monahan, W. B., & Albano, C. M. (2015). Ecologically-relevant maps of landforms and physiographic diversity for climate adaptation planning. PloS one, 10(12), e0143619
14. Kennedy, C.M., J.R. Oakleaf, D.M. Theobald, S. Baurch-Murdo, and J. Kiesecker. 2019. Managing the middle: A shift in conservation priorities based on the global human modification gradient. Global Change Biology 00:1-16. https://doi.org/10.1111/gcb.14549
15. Shimada, M., Itoh, T., Motooka, T., Watanabe, M., Tomohiro, S., Thapa, R., and Lucas, R., "New Global Forest/Non-forest Maps from ALOS PALSAR Data (2007-2010)", Remote Sensing of Environment, 155, pp. 13- 31, December 2014. doi:10.1016/j.rse.2014.04.014.
16. Giglio, L., Justice, C., Boschetti, L., Roy, D. (2015). MCD64A1 MODIS/Terra+Aqua Burned Area Monthly L3 Global 500m SIN Grid V006 [Data set]. NASA EOSDIS Land Processes DAAC. Accessed 2019-12-07 from https://doi.org/10.5067/MODIS/MCD64A1.006
17. Abatzoglou J. T., Development of gridded surface meteorological data for ecological applications and modelling, International Journal of Climatology. (2012) doi: https://doi.org/10.1002/joc.3413

