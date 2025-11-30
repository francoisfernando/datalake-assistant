#!/bin/bash

# Define the file containing the lines
INPUT_FILE="table_list.csv"


export PGHOST=localhost
export PGDATABASE=sakila
export PGUSER=sakila
export PGTABLE=actor
export PGPASSWORD=p_ssW0rd


# Loop through each line in the file
while IFS= read -r line; do
    # Remove whitespace characters from the line
    line="${line//[[:space:]]/}"
    export PGTABLE=$line
    echo "Exporting table: $PGTABLE"
    pg2parquet export --host $PGHOST --dbname $PGDATABASE --user $PGUSER --password $PGPASSWORD --table $PGTABLE --output-file "parquet-export/${PGTABLE}/${PGTABLE}.parquet"
done < "$INPUT_FILE"
