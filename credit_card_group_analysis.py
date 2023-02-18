# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 19:56:24 2023

@author: MD
"""

import pandas as pd
import matplotlib.pyplot as plt
from credit_cards_analysis import read_file

selected_data = 'C:/MD/Dokumenty/python/data_analysis/credit_cards/BankChurner_Deactivated.csv'
not_selected_data = 'C:/MD/Dokumenty/python/data_analysis/credit_cards/BankChurner_Active.csv'



def compare_groups(col_name):
    ct = pd.crosstab(
        index=df[col_name],  
        columns=df["Group_Name"], 
        values=df["Client_ID"],  
        aggfunc="count",  
        normalize="columns"  
    )
    ct["Diff"] = ct.apply(
        lambda x: x[0] - x[1], 
        axis=1  
    )
    return ct

def visualize_comparison(ct):
    _ct = ct.drop(columns=["Diff"])
    fig = _ct.plot(
        kind="bar",  
        title="Comparision between groups",
        figsize=(15, 10)
        )
    return fig




if __name__ == "__main__":
    
    # READING FILES
    df_deactivated = read_file(selected_data)
    df_active = read_file(not_selected_data)
    
    
    # PREPARING DATA
    df_deactivated["Group_Name"] = "Deactivated"
    df_active["Group_Name"] = "Active"
    df = pd.concat([df_active, df_deactivated]) # joining groups
    
    
    # COMPARING DATA
    
    # Gender
    gender_ct = compare_groups("Gender")
    visualize_comparison(gender_ct)
    # Female: number of cards deactivated is 6% lower than number of cards still active
    # Male: number of cards deactivated is 6% higher than number of cards still active
    
    # Education_level
    education_level_ct = compare_groups("Education_Level")
    visualize_comparison(education_level_ct)
    # No significant difference in any of groups
    
    # Marital_status
    marital_status_ct = compare_groups("Marital_Status")
    visualize_comparison(marital_status_ct)
    # Married: number of cards deactivated is 7% higher than number of cards still active
    # Single: number of cards deactivated is 4.8% lower than number of cards still active

    # Income_Category
    income_category_ct = compare_groups("Income_Category")
    visualize_comparison(income_category_ct)
    # No significant difference in any of groups
    
    # Card_Category
    card_category_ct = compare_groups("Card_Category")
    visualize_comparison(card_category_ct)
    # No significant difference in any of groups
    
    # Years_on_book
    years_on_book_ct = compare_groups("Years_on_book")
    visualize_comparison(years_on_book_ct)
    # (1, 2]: number of cards deactivated is 7% higher than number of cards still active
    # (2, 3]: number of cards deactivated is 2% lower than number of cards still active
    # (3, 4]: number of cards deactivated is 7% lower than number of cards still active
    # (4, 5]: number of cards deactivated is 2% higher than number of cards still active
    
    # Customer_Age_agg
    customer_age_ct = compare_groups("Customer_Age_agg")
    visualize_comparison(customer_age_ct)
    # Age under 40: number of cards deactivated is much more higher than number of cards still active
    # Age 40 - 55: number of cards deactivated is lower than number of cards still active
    # Age over 55: number of cards deactivated is higher than number of cards still active
    
    
    # CONCLUSIONS
    # Groups, which have the heighest number of deactivated cards:
        # males (+6%)
        # married (+7.6%)
        # clients who have a card from 1 to 2 years (+6.7%)
        # aged under 40 (about +6%, depending on category)





    
