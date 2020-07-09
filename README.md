# Fraud-Detection
An efficient and automated way to detect fraud in online transactions

### Demo
<a href="https://fraud-detection-demo.herokuapp.com/">Website</a>

### Dataset
The original dataset can be found in <a href="https://www.kaggle.com/ntnu-testimon/paysim1">Kaggle</a>. Here, for the particular model, dataset has been modified based on initial data exploratory analysis.

### Dataset Description
A synthetic dataset generated using the simulator called PaySim as an approach to such a problem. PaySim uses aggregated data from the private dataset to generate a synthetic dataset that resembles the normal operation of transactions and injects malicious behaviour to later evaluate the performance of fraud detection methods.

### The input parameters for the prediction phase should be of this format:

* Type (CASH_OUT,TRANSFER)
* Amount
* nameOrig - Customer who started the transaction
* oldbalanceOrig - Initial balance before the transaction
* newbalanceOrig - New balance after the transaction
* nameDest - Customer who is the recipient of the transaction
* oldbalanceDest - Initial balance recipient before the transaction
* newbalanceDest - New balance recipient after the transaction
* HourOfDay - Hour of the day at which the transaction occurs

