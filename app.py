import pandas as pd 
import streamlit as st
import numpy as np

st.set_page_config(
		page_title='Simple Item Recommendations',
		layout='wide'
	)
st.header('Simple Item Recommendations')
if st.button('Generate/Update Similarity Matrix'):
	exec(open("similarity_generator.py").read())
	st.write('Similarity matrix updated')

try:
	from get_recommendation import get_item_recommendation
	purchase_data = pd.read_csv('purchase_history_sampling.csv')
	product_data = pd.read_csv('product_details_sampling.csv')
	similarity_matrix = pd.read_csv('similarity_matrix_customer.csv').set_index('customer_id')
	similarity_matrix_product = pd.read_csv('similarity_matrix_product.csv').set_index('product_id')

	customer_id = st.text_input('Customer ID', placeholder="Type the customer ID...")
	n_recommendation = st.number_input('Total Recommendations', value=10)

	purchase_data['customer_id'] = purchase_data['customer_id'].astype('str')
	already_bought = purchase_data.query('customer_id == @customer_id')
	assert not already_bought.empty, 'Customer ID has no transaction'
	already_bought = already_bought.groupby('product_id').agg({
		'customer_id': 'count',
		'purchase_date': 'max'
		})
	already_bought.columns = ['total_bought', 'last_transactions']

	recommendation = get_item_recommendation(
		product_data, purchase_data, customer_id, similarity_matrix, similarity_matrix_product, n_recommendation)
	df = pd.DataFrame(recommendation).T
	df = df.sort_values(
			by = ['index_value', 'n_bought', 'product_similarity'],
			ascending = False
		)
	recommendation_index = df.index.astype(int).to_list()[:n_recommendation]
	recommendation_df = product_data.set_index('product_id')
	recommendation_df = recommendation_df.loc[recommendation_index]


	col1, col2 = st.columns(2)
	with col1:
		st.subheader('Already Bought Items')
		st.dataframe(
			already_bought
			)
	with col2:
		st.subheader('Recommended Items')
		st.dataframe(recommendation_df)
except AssertionError:
	st.write('Costumer ID is not found')

except FileNotFoundError:
	st.write('Some files are missing')