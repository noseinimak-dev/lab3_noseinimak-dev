#!/bin/bash
# feed-analyzer.sh - Top 5 Most Active Users from twitter_dataset.csv
# Usage: ./feed-analyzer.sh [path/to/twitter_dataset.csv]

FILE="${1:-twitter_dataset.csv}"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    echo "Usage: ./feed-analyzer.sh twitter_dataset.csv"
    exit 1
fi

# Find which column number holds "Username" by reading the header row
COL=$(head -n 1 "$FILE" | tr -d '\r' | tr ',' '\n' | grep -n -x "Username" | cut -d: -f1)

if [ -z "$COL" ]; then
    echo "Error: No 'Username' column found in the header of '$FILE'."
    exit 1
fi

echo "Top 5 Most Active Users in $FILE"
echo "(count  username)"
echo "--------------------------------"

# 1. skip the header row
# 2. take the Username column
# 3. keep only real usernames (a letter first, then letters/digits/underscores);
#    this drops pieces of multi-line tweets, which are not usernames
# 4. count duplicates, sort by highest count, show the top 5
tail -n +2 "$FILE" | cut -s -d',' -f"$COL" | tr -d '\r' | grep -E '^[A-Za-z][A-Za-z0-9_]*$' | sort | uniq -c | sort -nr | head -5 