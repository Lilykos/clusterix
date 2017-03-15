
![alt tag](http://i.imgur.com/CH6tN10.png)
# Clusterix: A visual analytics approach to data clustering


Clusterix is a web-based visual analytics tool that aspires to support clustering tasks by users, while having analysts at the center of the workflow. Clusterix provides the facilities to:

* Load and preview CSV data files;
* create a 2D projection of the dataset
* select any combination of fields to be used for projection/clustering;
* select and run one or more clustering algorithms (K-Means, Agglomerative Clustering, Mean Shift) with varying parameters;
* view and interact with the results in a browser environment;
* save time and use an iterative approach;
* modify the parameters or input data to correct the clustering output.

Such an iterative, visual analytics approach allows users to quickly determine the best clustering algorithm and parameters for their data, and to correct any errors in the clustering output. Clusterix has been applied to the clustering of heterogeneous data sets


## Usage

First you need to install the requirements:

`pip install -r requirements.txt`


To run the project:

`python manage.py runserver`

This command will run Clusterix on [http://127.0.0.1:5000](http://127.0.0.1:5000) where you will be able to use the interface to upload data files, and select the algorithms/options that you want.


## Features

#### File input (CSV only currently)
* Data Preview
* Field selection
* Text Features (Vectorizers, stemming, stopwords, etc)

#### Vectorizers
* Count Vactorizer
* Tf-Idf Vectorizer
* Hashing Vectorizer


#### Decomposition
* PCA
* SVD
* MDS
* t-SNE

#### Algorithms
* K-Means
* Agglomerative Clustering
* Mean Shift
* DBSCAN

#### Plot Features
* Scatterplot vizualizations
* Full text/column search for the nodes
* Brushing and zoom for targeted inspection
* Various clustering metrics (TF-IDF, etc)


## Screenshots

### Wine Data

![alt tag](http://i.imgur.com/AAudgAD.png)

![alt tag](http://i.imgur.com/DsDXYct.png)