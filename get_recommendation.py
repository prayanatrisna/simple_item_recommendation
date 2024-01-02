import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

def get_item_recommendation(product_data,
                            purchase_data,
                            customer_id,
                            similarity_matrix,
                            similarity_matrix_product,
                            n=10):
    purchase_product_data = purchase_data.merge(
        product_data,
        on = 'product_id',
    )
    purchase_product_data['customer_id'] = purchase_product_data['customer_id'].astype(str)
    purchase_detail = purchase_product_data.query('customer_id == @customer_id')
    assert not purchase_detail.empty, "Customer ID is not found"
    purchase_detail = list(set(purchase_detail['product_id'].to_list()))
    purchase_detail = [str(i) for i in purchase_detail]
    similar_indexes = similarity_matrix[customer_id][similarity_matrix[customer_id] > 0].sort_values().index.tolist()
    similar_indexes = [str(i) for i in similar_indexes]
    
    item_recommendations = pd.DataFrame(index=product_data.product_id.astype(str),
                                        columns = ['n_bought', 'index_value'])
    pivot_table = pd.pivot_table(purchase_data,
                             values='product_id',
                             aggfunc='count',
                             index='customer_id',
                             columns='product_id')
    pivot_table = pivot_table.fillna(0)
    pivot_table.index = pivot_table.index.map(str)
    pivot_table.columns = pivot_table.columns.map(str)

    for i, similar_index in enumerate(similar_indexes):
        anterior_items = pivot_table.loc[customer_id]
        posterior_items = pivot_table.loc[similar_index]
        recommendation = posterior_items[
            (posterior_items - anterior_items > 0)&(anterior_items==0)]
        recommendation.index = recommendation.index.map(str)
        for j in recommendation.index:
            if not item_recommendations.loc[j].any():
                item_recommendations.loc[j, 'n_bought'] = recommendation.loc[j]
                item_recommendations.loc[j, 'index_value'] = 1/(i+1)
        
        if item_recommendations['n_bought'].count() >= n:
            item_recommendations = item_recommendations.fillna(0)
            break
    
    similarity_matrix_product.index = similarity_matrix_product.index.map(str)
    similarity_matrix_product.columns = similarity_matrix_product.columns.map(str)

    similarity_matrix_subproduct = similarity_matrix_product.loc[purchase_detail]
    similarity_matrix_subproduct = similarity_matrix_subproduct.drop(purchase_detail, axis=1)
    
    average_similarity = similarity_matrix_subproduct.mean()
    average_similarity.name = 'product_similarity'
    average_similarity = 1/average_similarity
    
    item_recommendations = item_recommendations.drop(purchase_detail)
    item_recommendations = item_recommendations.merge(average_similarity.to_frame(),
                                                      left_index=True,
                                                      right_index=True)
    return item_recommendations.to_dict(orient='index')
# #%%
# purchase_data = pd.read_csv('purchase_history_sampling.csv')
# product_data = pd.read_csv('product_details_sampling.csv')
# similarity_matrix = pd.read_csv('similarity_matrix_customer.csv').set_index('customer_id')
# similarity_matrix_product = pd.read_csv('similarity_matrix_product.csv').set_index('product_id')
# #%%
