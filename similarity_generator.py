import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

purchase_data = pd.read_csv('purchase_history_sampling.csv')
product_data = pd.read_csv('product_details_sampling.csv')
product_data = pd.concat([product_data,
                          pd.get_dummies(product_data['category'])],axis=1)
product_data = product_data.drop('category', axis=1)  
#%%
pivot_table = pd.pivot_table(purchase_data,
                             values='product_id',
                             aggfunc='count',
                             index='customer_id',
                             columns='product_id')
pivot_table = pivot_table.fillna(0)
#%%
similarity_matrix = pd.DataFrame(cdist(pivot_table, pivot_table),
                                 index = pivot_table.index,
                                 columns = pivot_table.index,
                                 )

subproduct_data = product_data.drop('product_id', axis=1)
subproduct_data = MinMaxScaler().fit_transform(subproduct_data)
similarity_matrix_product = pd.DataFrame(
    cdist(subproduct_data, subproduct_data),
    index = product_data.product_id,
    columns = product_data.product_id,
    )
similarity_matrix.to_csv('similarity_matrix_customer.csv')
similarity_matrix_product.to_csv('similarity_matrix_product.csv')