# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 11:41:52 2023

@author: MD
"""

import pandas as pd
import matplotlib.pyplot as plt

git_url = 'https://raw.githubusercontent.com/CodersLab/DataLab_intro/main/raw/BankChurners.csv'
row_data = 'C:/MD/Dokumenty/python/data_analysis/credit_cards/BankChurner_ColumnsRenamed.csv'
selected_data = 'C:/MD/Dokumenty/python/data_analysis/credit_cards/BankChurner_Deactivated.csv'
not_selected_data = 'C:/MD/Dokumenty/python/data_analysis/credit_cards/BankChurner_Active.csv'

 

def read_kaggle_file(filepath, sep=',', header=0, encoding='UTF-8'):
    return pd.read_csv(git_url, sep=sep, header=header, encoding=encoding)

def read_file(filepath, sep=';'):
    return pd.read_csv(filepath, sep=sep)

def save_file(data_frame, filepath, index=False, sep=';'):
    return data_frame.to_csv(filepath, index=index, sep=sep) 

def analyse_column(column_name):
    result = df.groupby(by=[column_name])["Is_Active"].\
        agg(["mean",
        "count", 
        lambda x: sum(1-x), 
        lambda x: sum(1-x)/len(x) - 0.16 # group % of deactivated cards - total % of deactivated cards (16%)
        ])
    result.columns = ["Active_Ratio", "Group_Size", "Deactivated_Amount", "Deviation_From_Global"]
    return result

def visualize_analysis(df, compare_value):
    plt.figure(figsize=(15,10))
    x = df.index.astype(str)
    y = df["Active_Ratio"]
    plt.bar(x, y)
    plt.xlabel("Group")
    plt.ylabel("Active ratio")
    plt.title("Active ratio by groups")
    plt.axhline(compare_value, color="red", linestyle="--")
    plt.show()




if __name__ == "__main__":
    
    
    df = read_kaggle_file(git_url)
    df = df.rename(columns={'CLIENTNUM': 'Client_ID'}) # change column name for better one
    df = df.drop(columns=[
        'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1', \
        'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2'
        ]) # drop columns accordingly to suggestion in set description
    description = df.describe() # basic statistics
    save_file(df, row_data)


    # DATA MODIFICATION
    df = read_file(row_data)
    
    # Attrition_Flag
    # "Attrition_Flag" has str values which is unconvenient
    df["Is_Active"] = 1 # adding new column with int values for further analysis
    is_active = df["Attrition_Flag"] == "Attrited Customer" # generate boolean Series
    df.loc[is_active, "Is_Active"] = 0 # change "Is_Active" value for 0 if False
    
    # Income Category
    # "Income_Category" categories need to be ordered for further presentation
    # Change categories names:
    income_below_40k = df["Income_Category"] == "Less than $40K"
    df.loc[income_below_40k, "Income_Category"] = "1. < $40K"
    income_below_60k = df["Income_Category"] == "$40K - $60K"
    df.loc[income_below_60k, "Income_Category"] = "2. $40K - 60K"
    income_below_80k = df["Income_Category"] == "$60K - $80K"
    df.loc[income_below_80k, "Income_Category"] = "3. $60K - 80K"
    income_below_120k = df["Income_Category"] == "$80K - $120K"
    df.loc[income_below_120k, "Income_Category"] = "4. $80K - 120K"
    income_above_120k = df["Income_Category"] == "$120K +"
    df.loc[income_above_120k, "Income_Category"] = "5. 120K+"
    income_unknown = df["Income_Category"] == "Unknown"
    df.loc[income_unknown, "Income_Category"] = "6. Unknown"

    # Education_Level
    # "Education_Level" categories need to be ordered for further presentation
    # Change categories names:
    uneducated = df["Education_Level"] == "Uneducated"
    df.loc[uneducated, "Education_Level"] = "1. Uneducated"
    college = df["Education_Level"] == "College"
    df.loc[college, "Education_Level"] = "2. College"
    high_school = df["Education_Level"] == "High School"
    df.loc[high_school, "Education_Level"] = "3. High School"
    graduate = df["Education_Level"] == "Graduate"
    df.loc[graduate, "Education_Level"] = "4. Graduate"
    post_graduate = df["Education_Level"] == "Post-Graduate"
    df.loc[post_graduate, "Education_Level"] = "5. Post-Graduate"
    doctorate = df["Education_Level"] == "Doctorate"
    df.loc[doctorate, "Education_Level"] = "6. Doctorate"
    unknown = df["Education_Level"] == "Unknown"
    df.loc[unknown, "Education_Level"] = "7. Unknown" 

    # Card_Category
    # "Card_Category" categories need to be ordered for further presentation
    # Change categories names:
    blue_cards = df["Card_Category"] == "Blue"
    df.loc[blue_cards, "Card_Category"] = "1. Blue"
    silver_cards = df["Card_Category"] == "Silver"
    df.loc[silver_cards, "Card_Category"] = "2. Silver"
    gold_cards = df["Card_Category"] == "Gold"
    df.loc[gold_cards, "Card_Category"] = "3. Gold"
    platinum_cards = df["Card_Category"] == "Platinum"
    df.loc[platinum_cards, "Card_Category"] = "4. Platinum"
 
    
    # DATA ANALYSIS
    global_mean = df["Is_Active"].mean() # used for plot as compare_value
    
    # Client_ID
    client_id = analyse_column("Client_ID")
    # client_id_plot = visualize_analysis(client_id, global_mean)

    # Gender
    gender_analysis = analyse_column("Gender")
    visualize_analysis(gender_analysis, global_mean)
    # no significant differences (Deviation_From_Global column) between the percentage of lost customers in each of the groups

    # Education_Level
    education_analysis = analyse_column("Education_Level")
    visualize_analysis(education_analysis, global_mean)
    # 6. Doctrate group significantly deviates from the overall average, but group size is too low
    
    # Income_Category
    income_analysis = analyse_column("Income_Category")
    visualize_analysis(income_analysis, global_mean)
    # group which deviates the most is 3. $60K - 80K, but the difference level is lower than 3%
    
    # Months_on_book
    # Months_on_book is a continuous variable, we need to divide it into categories
    # by changing months to years and creating bins
    df["Years_on_book"] = pd.cut(x = df["Months_on_book"]/12, bins = [1,2,3,4,5])
    months_analysis = analyse_column("Years_on_book")
    # no significant differences
    
    # Card_Category
    card_analysis = analyse_column("Card_Category")
    # All group sizes, exept for 1. Blue, are too low

    # Months_Inactive_12_mon
    # Column to be skipped in analysis, since the number of months without activity in the last months is potentially a card deactivation factor
    
    # Customer_Age
    # Customer_Age is a continuous variable, we need to divide it into categories
    bins = list(range(25, 60, 5)) # creating age bins from 25 to 55 years
    bins.append(75) # adding bin for oldest people from 55 to 75
    df["Customer_Age_agg"] = pd.cut(df["Customer_Age"], bins=bins)
    customer_age_analysis = analyse_column("Customer_Age_agg")
    visualize_analysis(customer_age_analysis, global_mean)
    # no significant differences
    
    # Total_Trans_Amt
    # Customer_Age is a continuous variable, we need to divide it into categories
    bins = list(range(500, 5500, 500))
    bins.append(20000)
    df["Total_Trans_Amt_agg"] = pd.cut(df["Total_Trans_Amt"], bins=bins)
    total_trans_amt_analysis = analyse_column("Total_Trans_Amt_agg")
    visualize_analysis(total_trans_amt_analysis, global_mean)
    # (500, 1000] - significant difference, but group size is too low
    # (1500, 2000] - to low (4,8%) deviation from global for further analysis
    # (2000, 2500] - good for further analysis
    # (2500, 3000] - good for further analysis
    
    # Total_Trans_Ct
    # # Customer_Age is a continuous variable, we need to divide it into categories
    df["Total_Trans_Ct_agg"] = pd.cut(df["Total_Trans_Ct"], bins=range(0, 150, 10))
    total_trans_ct_analysis = analyse_column("Total_Trans_Ct_agg")
    visualize_analysis(total_trans_ct_analysis, global_mean)
    # (30, 40] - high deviation, sufficient group size, good for further analysis
    # (40, 50] - high deviation, sufficient group size, good for further analysis
    
    
    # PIVOT TABLE
    # Analysis of relation between Total_Trans_Amt and Total_Trans_Ct
    amt_vs_ct = pd.pivot_table(
    df,  # data feame for analysis
    index="Total_Trans_Ct_agg",  # column to be placed in rows
    columns="Total_Trans_Amt_agg",  # column to be placed in columns
    values="Gender",  # column to be aggregated
    aggfunc="count"  # aggregation function
    )
    # No visible correlation, more precise analysis should be with use of linear correlation analysis

    # Selecting groups for further analysis
    amt_selector = df["Total_Trans_Amt_agg"].astype(str).isin(["(2000, 2500]", "(2500, 3000]"])
    ct_selector = df["Total_Trans_Ct_agg"].astype(str).isin(["(30, 40]", "(40, 50]"])
    to_select = amt_selector | ct_selector  # chosing either amt_selector or ct_selector
    selected = df.loc[to_select]
    not_selected = df.loc[~to_select]

    # Saving data into new files
    save_file(selected, selected_data)
    save_file(not_selected, not_selected_data)



