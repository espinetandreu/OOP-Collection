import pandas as pd
from se_package.classes import Index, Symbol, analyze, generate_ngrams


# ========= TRANSFORM DF ===========

def transform_dataframe(df, desc_col_list):
    ''' Concatenates columns and lowercase '''

    df["description"] = df[desc_col_list].apply(" ".join, axis=1)
    df = df[df['description'].notna()]
    df['description'] = df['description'].str.lower()
    return df


# ======== GENERATE INDEX ==========

def generate_index(df, id_col):
    '''Builds the index and 
       analyzed_description for enclosed "" words (OR search)'''

    index = Index()
    analyzed_description = {}
    for i in range(len(df)):
        sym = Symbol(df.loc[i, id_col], df.loc[i, "description"])
        index.index_symbol(sym)
        analyzed_description[sym.ID] = set(
            [gram for token in analyze(sym.description) for gram in generate_ngrams(token)])

    return index, analyzed_description


# ======== GENERATE THE DATAFRAME ==========

# Function that compiles the search engine given the parameters
def generate_result(df, query, index, analyzed_description, id_col):
    ''' Compiles the search engine given the parameters '''

    # In case the query is NAN
    if isinstance(query, str):
        if len(analyze(query)) != 0:
            query = query.lower()
            # Compile engine search
            and_search_results, or_search_results = index.search(query, analyzed_description)
            # If there are only nonenclosed words (AND)
            if not or_search_results:
                # Save the results in a dataframe
                result = df[df[id_col].isin(and_search_results)]
            else:
                search_results_df = pd.DataFrame(or_search_results, columns=[id_col, 'SEARCH_SCORE'])
                if and_search_results:
                    search_results_df = search_results_df[search_results_df[id_col].isin(and_search_results)]
                result = search_results_df.merge(df, on=id_col, how='inner')
                result.sort_values(by=['SEARCH_SCORE'], ascending=False, inplace=True)
        return result[list(result.columns.values[:-1])]





