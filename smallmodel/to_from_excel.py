import pandas as pd


def csv_to_excel(mets_csv, rxns_csv, paras_csv, excel_file):
    # Read the CSV files
    mets = pd.read_csv(mets_csv, skipinitialspace=True)
    rxns = pd.read_csv(rxns_csv, skipinitialspace=True)
    paras = pd.read_csv(paras_csv, skipinitialspace=True)

    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(excel_file, engine='auto') as writer:
        # Write each DataFrame to a specific sheet
        mets.to_excel(writer, sheet_name='Metabolites', index=False)
        rxns.to_excel(writer, sheet_name='Reactions', index=False)
        paras.to_excel(writer, sheet_name='Parameters', index=False)


def excel_to_dfs(excel_file):
    # Read the Excel file
    xls = pd.ExcelFile(excel_file)

    # Parse the sheets into DataFrames
    mets = pd.read_excel(xls, 'Metabolites')
    rxns = pd.read_excel(xls, 'Reactions')
    paras = pd.read_excel(xls, 'Parameters')

    return mets, rxns, paras


if __name__ == "__main__":
    # File paths
    mets_csv = "small_FA_mets.csv"
    rxns_csv = "small_FA_rxns.csv"
    paras_csv = "small_FA_paras.csv"
    excel_file = "FA_Liver_Model.xlsx"

    # Convert CSV files to Excel
    csv_to_excel(mets_csv, rxns_csv, paras_csv, excel_file)

    # Import the Excel file and get DataFrames
    mets_df, rxns_df, paras_df = excel_to_dfs(excel_file)

    # Print the DataFrames to verify
    print(mets_df)
    print(rxns_df)
    print(paras_df)
