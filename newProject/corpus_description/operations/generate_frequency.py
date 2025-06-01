import pandas as pd
import numpy as np
import os
from fields import *

NO_ITEMS_AVAILABLE = 'none available'
OUTPUT_TRESHOLD = 10000

def generate_frequency_df(df_without_duplicates, item_counts, number_of_articles):

    number_of_unique_citations_with_item = df_without_duplicates[INDEX_COLUMN].nunique()
    item_counts_df = item_counts.reset_index()
    item_counts_df.columns = [ITEMS_COLUMN, 'count']
    # Add missing data if any citation lacks the item
    item_counts_df = calculate_missing_items(number_of_unique_citations_with_item, number_of_articles, item_counts_df)
    # Calculate percentages
    item_counts_df['f'] = 100 * item_counts_df[COUNT_COLUMN] / number_of_articles
    # Limit output to top ~10,000 items based on dynamic frequency threshold
    return limit_output(item_counts_df)
    # Generate cumulative distribution (Zipf-style)

def limit_output(item_counts_df):
    counts_sorted = item_counts_df.sort_values(by=COUNT_COLUMN, ascending=False)
    if len(counts_sorted) > OUTPUT_TRESHOLD:
        threshold = 1
        while (counts_sorted[COUNT_COLUMN] > threshold).sum() > OUTPUT_TRESHOLD:
            threshold += 1
        counts_sorted = counts_sorted[counts_sorted[COUNT_COLUMN] > threshold]
    return counts_sorted

def calculate_missing_items(number_of_unique_citations_with_item, number_of_articles, item_counts_df):
    if number_of_unique_citations_with_item < number_of_articles:
        return pd.concat([
            item_counts_df,
            pd.DataFrame([{
                ITEMS_COLUMN: NO_ITEMS_AVAILABLE, 
                COUNT_COLUMN: number_of_articles - number_of_unique_citations_with_item}])
        ], ignore_index=True)
    
def calculate_distributions(item_counts_df):
    distributions = item_counts_df.groupby(COUNT_COLUMN).size().reset_index(name=NUMBER_OF_ITEMS)
    distributions = distributions.sort_values(COUNT_COLUMN)
    distributions[CUMULATIVE] = distrib[NUMBER_OF_ITEMS][::-1].cumsum()[::-1]
    xx = distributions[COUNT_COLUMN].tolist()
    yy = distributions[CUMULATIVE].tolist()[:-1]  # drop last cumulative value for compatibility
    return xx, yy


def write_distributions_file(xx, yy, field_name, output_file_field):
    with open(output_file_field, 'a') as out:
        out.write(',\n\t"p%s":[%s, %s]' % (field_name, xx, yy))



    

    

    

