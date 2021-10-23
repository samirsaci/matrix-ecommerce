import pandas as pd
import json
import numpy as np

# Import DataFrame
PATH_IN = r'static\data\df_transactions.xlsx'

def order_brand(PATH_IN):
    ''' List of all brands in each order'''
    # Import DataFrame
    df_rec = pd.read_excel(PATH_IN)

    # Listing Unique Brands
    df_ordbr = pd.DataFrame(df_rec.groupby(['ORDER_NUMBER'])['BRAND'].unique())
    df_ordbr.columns = ['list_brand']
    
    # source = list brands
    list_brand = list(df_rec['BRAND'].unique())

    # boolean column per brand for each order: is brand in order ?
    for br in list_brand:
        df_ordbr[br] = df_ordbr['list_brand'].apply(lambda t: br in t)

    # unique combinations of brands boolean 
    df_con = pd.DataFrame(df_ordbr.reset_index()[df_ordbr.columns[1:]]).drop_duplicates()
    
    return list_brand, df_ordbr, df_con, df_rec

def create_nodes(df_con, n_groups):
    ''' Create nodes from df_con'''
    list_col, list_cont = [], []

    # how many brands are ordered with this brand
    for col in df_con.columns:
        list_col.append(col)
        list_cont.append((df_con[df_con[col] == True].sum() > 0).sum())
    df_nodes = pd.DataFrame({'name': list_col, 'group':list_cont})
    df_nodes.set_index('name', inplace = True)

    # group by range of values
    range_value = np.ceil(df_nodes['group'].max()/n_groups)
    df_nodes['group'] = n_groups - (df_nodes['group']/range_value).apply(np.floor).astype(int)
    
    return df_nodes

def create_links(df_rec, df_ordbr, list_brand):
    ''' Create links dataframe '''

    # Unique brands per order
    df_source = pd.DataFrame(df_rec.groupby(['ORDER_NUMBER'])['BRAND'].unique())
    df_source.columns = ['list_brand']
    
    list_source, list_target, list_value = [], [], []
    for br1 in list_brand:
        for br2 in list_brand:
            value = (df_ordbr[br1] * df_ordbr[br2]).sum()
            if value > 0:
                list_source.append(br1)
                list_target.append(br2)
                list_value.append(value)

    # Build links dataframe
    df_links = pd.DataFrame({
        'source': list_source,
        'target': list_target,
        'value':list_value
    })

    # Mapping with Brands ID
    dict_map = dict(zip(df_links['source'].unique(), [i for i in range(len(list_brand))]))
    for col in ['source', 'target']:
        df_links[col] = df_links[col].map(dict_map)
        
    return df_links

def create_json(df_nodes, df_links):
    ''' Create json from dataframes'''
    json1 = []
    for index, row in df_nodes.reset_index().iterrows():
        dico = {}
        dico['group'] = int(row['group'])
        dico['name'] = row['name']
        json1.append(dico)

    json2 = []
    for index, row in df_links.iterrows():
        dico = {}
        dico['source'] = int(row['source'])
        dico['target'] = int(row['target'])
        dico['value'] = int(row['value'])
        json2.append(dico)

    json_to = {"links": json2, "nodes": json1}
    
    return json_to


