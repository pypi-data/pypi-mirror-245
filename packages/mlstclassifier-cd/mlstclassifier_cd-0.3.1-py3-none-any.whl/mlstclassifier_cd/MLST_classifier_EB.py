#!/usr/bin/env python3

import pandas as pd
import sys
import joblib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import argparse
import re

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Error: Number of argument must be 3")
        print("Usage: MLSTclassifier_cd input_path output_path")
        sys.exit(1)


    # Define the command-line arguments
    parser = argparse.ArgumentParser(description='input, output and input type')
    parser.add_argument('input_directory', type=str, action='store', help='intput should be a path to the input directory') # The input is a path to a directory
    parser.add_argument('output_file', type=str, action='store', help='output should be a path to the output file')
    args = parser.parse_args()

    # Used to extract the value of the alleles in a mlst or fastmlst output (made with chatGPT)
    def extract_number(v):
        match = re.search(r'\([~-]?(\d+)[\?]?\)', v) # Use regular expression to find the number within brackets and handle ~ and -
        if match: # If a match is found, return the extracted number as an integer
            return int(match.group(1))
        else:
            return "NA" # If no match is found, return "NA"
    
    # Takes a df with each line corresponding to a sample and extract the allele value
    def modify_df(dataframe):
        col_to_extract = [0,3,4,5,6,7,8,9]
        col_genes = [3,4,5,6,7,8,9]
        df = dataframe.iloc[:, col_to_extract].copy()
        df.loc[:, col_genes] = df[col_genes].map(extract_number) # Apply the 'extract_number' function to each element in the selected columns
        df.rename(columns={0: 'sample',3: 'adk',4: 'atpA',5: 'dxr',6: 'glyA',7: 'recA',8: 'sodA',9: 'tpi'}, inplace=True) # Rename the columns to be recognized for the prediction
        return df
    
    # Takes a path to the dir containing the mlst or fastmlst files. Combine the information in each file in a df
    def create_df(dir_path):
        data_mlst = []
        data_fastmlst = []

        for filename in os.listdir(dir_path):
            f = os.path.join(dir_path, filename)
            if f.endswith(".fastmlst"):
                    with open(f, 'r') as f:
                        line = f.readline().strip()
                        data_fastmlst.append(line)
                        df_fastmlst = pd.DataFrame(data_fastmlst, columns=['line'])
                        df_fastmlst = df_fastmlst['line'].str.split(',', expand=True)
                        final_df = modify_df(df_fastmlst)
            elif f.endswith(".mlst"):
                with open(f, 'r') as f:
                        line = f.readline().strip()
                        data_mlst.append(line)
                        df_mlst = pd.DataFrame(data_mlst, columns=['line'])
                        df_mlst = df_mlst['line'].str.split('\t', expand=True)
                        final_df = modify_df(df_mlst)
        return final_df
    
    # Checks if the path given in argument exits and call creat_df to transform the input into readable data for the model
    if os.path.exists(args.input_directory) == True:
        df = create_df(args.input_directory)

    # Load the pre-trained model
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_directory, "KNN_model_061223.sav")
        model = joblib.load(model_path)
    except FileNotFoundError:
        print("Error: Model file not found.")
        sys.exit(1)


    # Extract features (X) from the DataFrame and make predictions
    df = df.dropna() # Drop missing values if some are present
    X = df[['adk', 'atpA', 'dxr', 'glyA', 'recA', 'sodA', 'tpi']] # Extract columns corresponding to the 7 genes as features 'X'
    #print(X.head())
    df['predicted_clade'] = model.predict(X) # Make predictions using the pre-trained model and add them as a new column 'predicted_clade' in the DataFrame 'df'
    

    # Save the raw count in a separated file called count.csv:
    output_dir = os.path.dirname(args.output_file)
    count = df['predicted_clade'].value_counts() # Extract value count
    count_df = pd.DataFrame(count) # Create a df with value count
    with open(os.path.join(output_dir, "count.csv"), "w") as f: # Create the file count.csv with the value count df
        count_df.to_csv(f, index=True)
    

    # Create a pie chart with the value counts (made with chatGPT)
    fig = make_subplots(1, 1, specs=[[{"type": "pie"}]])
    fig.add_trace(
        go.Pie(
            labels=df['predicted_clade'].value_counts().index,
            values=df['predicted_clade'].value_counts().values,
            textinfo="label+percent",
            showlegend=False,
        ),
        row=1, col=1
    )
    fig.update_layout(title_text="Predicted Clade Distribution")
    
    # Save the pie chart as an HTML file:
    fig.write_html(os.path.join(output_dir, "pie_chart.html"))
    

    # Write the DataFrame with the added column of predictions to the output CSV file:
    try:
        with open(args.output_file, 'w') as f:   # Open the output CSV file
            df.to_csv(f, index=False)   # Write the DataFrame 'df' to the CSV file 'f', excluding the index column
    except PermissionError:
        print("Error: Unable to write to output CSV file.")
        sys.exit(1)


if __name__ == "__main__":
    main()   # Call the main function if the script is run as the main program (not imported as a module)