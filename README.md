# Fraud-Detection
An efficient and automated way to detect fraud in online transactions

### Demo: 
a href="https://fraud-detection-demo.herokuapp.com/">Website</a>

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

