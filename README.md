### Problem Statement ###

This project uses the Ames Housing Dataset to assist stakeholders with an interest in increasing home value by identifying home features that have the largest predictive relationship with sale price. Linear regression is used to design a model that can accept important features from the data set and make predictions of sale price based on those features.  The model is evaluated by R2 score and root mean squared error, showing both how the model accounts for variability in price and how close we can expect estimates based on the model to be.  Models were also submitted to Kaggle as part of a competitive model evaluation process.

### Structure of this Repo ###

README.md

Presentation Slides

Code folder:
- Part 1: Introduction, investigation of null values and data types.
- Part 2: EDA, investigating best features for regression.
- Part 3: Data Engineering, converting categorical data to numerical, feature interactions, outlier/null removal.
- Part 4: Transformation and Regression, analysis, conclusions, recommendations.
- presentation-graphs: Used to recreate specific graphs in a more presentation-friendly stlye
- cleantools.py: A custom module used for handling null values and converting data types.
- graphtools.py: A custom module used to graphing.

Datasets folder:
- Train and Test data provided for this project.
- Train and Test 1 and 2: intermediate and final versions of the data after cleaning and engineering.
- Final Submission: A copy of the Kaggle submission that scored best on the public leaderboard.

### Data Exploration ###

A full description of the Ames Housing Dataset can be found [here](http://jse.amstat.org/v19n3/decock/DataDocumentation.txt).  It includes sale price and 78 other features for several homes.  The subset used for this model contained information for 2051 homes.

Initial analysis revealed some missing information.  Part 1 of the projects focuses on investigating those values.  In many cases, reasonable explanations were found, and the missing information could be accounted for.  Part 2 focuses on isolating the features with the strongest predictive potential for sale price.  A heatmap is used to check correlation between numeric features and saleprice.  Then scatterplots are created for continuos variables, and bar graphs for discrete variables, to visualize the relationships they have with sale price and identify possible issues like large outliers.  Using all of this information, the top features of interest were identified.

Part 3 focuses on modifying data as needed before it can can be used by the regression algorithm.  Categorical data is coded numerically.  Heatmaps are used to identify strong correlations between candidate features, and in some cases, these features are combined via feature interactions.  Finally extreme outliers are removed, along with missing values that cannot be otherwise accounted for.

### Dictionary of Data Included in Final Model ###

Recall that the full Ames Housing Dataset is located [here](http://jse.amstat.org/v19n3/decock/DataDocumentation.txt).

|Feature|Type|Description|
|---|---|---|
|saleprice|int|Sale price of the house in dollar|
|id|int|House identifier necessary for Kaggle submission, exculded from model|
|half_bath|int|Number of half-bathrooms above grade|
|gr_liv_area|int|Total above ground living area|
|lot_area|int|Lot size in sq feet|
|neighborhood|int|1 if neighborhood is 1 std below the mean for average sale price, 3 if 1 std above the mean, 2 otherwise|
|overall_qual|int|Overall quality rating of the house on an increasing scale|
|fireplace_qu|float|Fireplace quality rating on increasing numeric scale with 0 being no fireplace|
|heating_qc|float|Heating quality on an increasing numeric scale|
|mas_vnr_area|float|Total masonry veneer area|
|year_built|int|Year built minus 1890 to allow for a more natural scale when using scaling algorithms|
|porch_space|int|Sum of the area of all porch types in sq feet|
|garage_total|float|Product of the original features garage area and year built, with year built subtracted by 1890 and 0 if no garage|
|bsmt_total|float|Product of the original features total basement surface area (sq ft) and basement full bathrooms|

### Regression ###

Grid Search is used to test different combinations of polynomial features for three different regression algorithms: basic linear regression, ridge regression with cross-validation on 10 cross-folds, and lasso regression with cross-validation on 10 cross-folds.  Different selections of features are also experimented with, starting gradually and adding in more features while they have a positive impact on regression metrics.

Polynomial features up to order 2 produce significant improvement in R2 score and RMSE.  However, linear regression without regularization, with ridge regularization, and with lasso regularization are very similar.  Lasso regression slighlty outperforms the other two, with R2 scores suggesting it is slighly underfit and will generalize well to new data, even with polynomial features of order 2 included.  Each algorith produces RMSE values around \\$22,000 to \\$25,000 in final testing.

### Conclusions and Recommendations ###

Final models with lasso regularization and with no regularization are compared.  They show very similar residual graphs, but their coefficients reveal that they prioritize very different features.  Through its selection process, Lasso regularization emphasizes features that we would intuitively expect to be important.  It favors individual terms over higher-order features, which is expected because features were selected to be relatively independent of each other.

Based on the most highly favored features in the lasso regression, I conclude that living space is the single most important factor in home value, aside from overall quality, which is very broad and of limited actionability.  Living space increases value whether it is in the main house, garage, or basement.  Age is also a very impactful feature, and a quality fireplace and good neighborhood add significant value.  Keeping in mind that this data is from Ames, IA, it is suggested that a fireplace may be reconceptualized as a luxury feature, which could vary if different climates.  For example, pools were quite rate in Ames, but in warmer climates, may replace fireplaces.  Such investigations in other markets could clarify the applicability of these conclusions outside of Ames, IA.

Residual plots do show some systematic error, underestimating very high prices and overestimating very low ones.  The vast majority of sales fall into a range that has very symmetric residuals.  However, it is possible that by including more specialized features, the model could better differentiate very high and very low-value homes.  This is one possibility for future work.