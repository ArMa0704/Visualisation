import pandas as pd
import numpy as np
import scipy.stats as stats
def load_data():

    # Load dataset into a DataFrame
    df = pd.read_csv("Data/Raw/all_data.csv")

    # TODO : data preprocessing
    #preprocessing done with the help of a notebook off the kaggle website with slight changes to adapt it to our use (https://www.kaggle.com/code/saloni1712/credit-score-classification/notebook#-Credit-Score-Classification-)
    def fill_missing_with_group_mode(df, groupby, column):

        mode_per_group = df.groupby(groupby)[column].transform(lambda x: x.mode().iat[0])
        df[column] = df[column].fillna(mode_per_group)


    def clean_categorical_field(df, groupby, column, replace_value=None):
        #substitute non-existing and garbage values with np.nan
        if replace_value != None:
            df[column] = df[column].replace(replace_value, np.nan)

        fill_missing_with_group_mode(df, groupby, column)

    def fix_inconsistent_values(df, groupby, column):
        df_dropped = df[df[column].notna()].groupby(groupby)[column].apply(list)
        x, y = df_dropped.apply(lambda x: stats.mode(x)).apply([min, max])
        mini, maxi = x[0], y[0]

        # assign Wrong Values to NaN
        col = df[column].apply(lambda x: np.NaN if ((x < mini) | (x > maxi) | (x < 0)) else x)

        # fill with local mode
        mode_by_group = df.groupby(groupby)[column].transform(lambda x: x.mode()[0] if not x.mode().empty else np.NaN)
        df[column] = col.fillna(mode_by_group)
        df[column].fillna(df[column].mean(), inplace=True)


    def clean_numerical_field(df, groupby, column, strip=None, datatype=None, replace_value=None):
        # substitute non-existing and garbage values with np.nan
        if replace_value != None:
            df[column] = df[column].replace(replace_value, np.nan)
        # clean a string of unqanted characters
        if df[column].dtype == object and strip is not None:
            df[column] = df[column].str.strip(strip)
        # change datatype into the required datatype
        if datatype is not None:
            df[column] = df[column].astype(datatype)
        fix_inconsistent_values(df, groupby, column)

    def Month_Converter(val):
        # convert years and moths into a sum of months
        if pd.notnull(val):
            years = int(val.split(' ')[0])
            month = int(val.split(' ')[3])
            return (years * 12) + month
        else:
            return val
    # change Num_of_Loan into integers and remove unwanted characters
    features_to_be_num = ['Num_of_Loan']
    for feature in features_to_be_num:
        df[feature] = df[feature].str.extract('(\d+)').astype(int)
    # change those attributes into floats and remove unwanted characters
    features_to_be_num = ['Outstanding_Debt', 'Annual_Income', 'Amount_invested_monthly', 'Monthly_Balance']
    for feature in features_to_be_num:
        df[feature] = df[feature].str.extract(r'(\d+\.\d+)').astype(float)
    # cleaning and imputation process for each variable
    column_name = 'Name'
    group_by = 'Customer_ID'
    clean_categorical_field(df, group_by, column_name)

    column_name = 'SSN'
    group_by = 'Customer_ID'
    garbage_value = '#F%$D@*&8'
    clean_categorical_field(df, group_by, column_name, garbage_value)

    column_name = 'Payment_Behaviour'
    group_by = 'Customer_ID'
    garbage_value = '!@9#%8'
    clean_categorical_field(df, group_by, column_name, garbage_value)

    column_name = 'Age'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name, strip='_', datatype='int')

    column_name = 'Annual_Income'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name, strip='_', datatype='float')

    column_name = 'Monthly_Inhand_Salary'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name)

    column_name = 'Num_Bank_Accounts'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name)

    column_name = 'Num_Credit_Card'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name)

    column_name = 'Interest_Rate'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name)

    column_name = 'Num_of_Loan'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name)

    column_name = 'Num_of_Delayed_Payment'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name, strip='_', datatype='float')

    column_name = 'Num_Credit_Inquiries'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name)

    column_name = 'Outstanding_Debt'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name, strip='_', datatype=float)

    df['Credit_History_Age'] = df['Credit_History_Age'].apply(lambda x: Month_Converter(x)).astype(float)
    column_name = 'Credit_History_Age'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name, datatype=float)

    column_name = 'Amount_invested_monthly'
    group_by = 'Customer_ID'
    clean_numerical_field(df, group_by, column_name, datatype=float, strip='_')
    # change all the null-values in type of loan into a new category named Not Specified
    df['Type_of_Loan'].replace([np.NaN], 'Not Specified', inplace=True)
    return df



