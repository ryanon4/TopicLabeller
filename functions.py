import ast

import pandas as pd


def filter_mesh_terms(input_dataframe, mesh_column_name="mesh_terms", mesh_terms_include = ["D006801"], mesh_terms_exclude = ["D000465"]):
    input_dataframe = input_dataframe.reset_index()
    for i, row in input_dataframe.iterrows():
        terms = ast.literal_eval(row[mesh_column_name])
        if all(k in terms for k in set(mesh_terms_include)):
            # Fits Inclusion Criteria
            continue
        else:
            # Doesent contain the required criteria
            input_dataframe.drop(i, inplace=True)
        #if all(k in terms for k in set(mesh_terms_exclude)):
        #    # In Exclusion Criteria, delete.
        #    input_dataframe.drop(i, inplace=True)

    dataframe = input_dataframe.reset_index(level=None)
    return dataframe


def get_topic_document(topic_id, model, documents_df ,num_docs=10):
    doc_ids = list(model.search_documents_by_topic(topic_id, num_docs=num_docs,return_documents=True)[2])
    documents = documents_df.iloc[doc_ids]
    # TODO deduplication needs looking into from data entry perspective.
    documents = documents.drop_duplicates(subset=["title"])
    #for i, doc in documents.iterrows()
    return documents


