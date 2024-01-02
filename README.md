# Simple Item Recommendation

## How to run
* Download all the scripts from the repository
* Create virtual environment with Python by running this script in the command line:
```
python -m venv env
```
* Activate the newly created virtual environment by running this script:
```
env\Scripts\activate
```
* The virtual environment is active if the path on the command line begin with `(env)`
* Install all the required packages by running this script:
```
pip install -r requirements.txt
```
* Wait until the package installations are completed.
* Run the app server with the following script:
```
streamlit run app.py
```
* The local page served as app will be opened

## How to use
* The transaction data is served in `purchase_history_sampling.csv`. If you want to add/update/delete the transaction, you can manage in this .csv
* The product data is served in `product_details_sampling.csv`. The same applies for this .csv
* Similarity matrix are generated from the previous data. The similarity matrix need to be updated if the transaction data is updated. The button for updating the similarity matrix is provided in the app.
* The app receives 2 inputs:
  * Customer ID, which indicates the customer ID. If wrong/blank id is inputed the app will show nothing.
  * Total recommendations, which indicate the number of recommendations generated. The default number is 10, though it can be changed.
* The app will show 2 outputs:
  * The already-bought item list
  * The recommendations list that consists of n number of items (depending on the input)

## Explanation
The explanation of the methodology can be found in [here](https://tartan-sorrel-634.notion.site/Skilvul-Test-Assesment-75913e0c53c141bb9066af5e18603889)