import pandas as pd
from simple_salesforce import Salesforce

def init_cysh():
    with open('C:\\Users\\City_Year\\Desktop\\salesforce_credentials.txt', 'r') as f:
        read_data = f.read()
        sf_creds = eval(read_data)
        
    cysh = Salesforce(instance_url=sf_creds['instance_url'],
                      password=sf_creds['password'],
                      username=sf_creds['username'],
                      security_token=sf_creds['security_token'])
    
    return cysh

def get_cysh_df(sf_object, sf_fields, rename_id=False, rename_name=False, sf=cysh):
    sf_fields_str = ", ".join(sf_fields)
    querystring = (f"SELECT {sf_fields_str} FROM {sf_object}")
    query_return = cysh.query_all(querystring)

    query_list = []
    for row in query_return['records']:
        record = []
        for column in sf_fields:
            col_data = row[column]
            record.append(col_data)
        query_list.append(record)
    
    df = pd.DataFrame(query_list, columns=sf_fields)
    
    if rename_id==True:
        df.rename(columns={'Id':sf_object}, inplace=True)
    if rename_name==True:
        df.rename(columns={'Name':(sf_object+'_Name')}, inplace=True)

    return df

cysh = init_cysh()