#!/bin/bash
# feed-analyzer.sh - Top 5 Most Active Users from twitter_dataset.csv
# Usage: ./feed-analyzer.sh [path/to/twitter_dataset.csv]

FILE="${1:-twitter_dataset.csv}"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    echo "Usage: ./feed-analyzer.sh twitter_dataset.csv"
    exit 1
fi

echo "Top 5 Most Active Users in $FILE"
echo "(count  username)"
echo "--------------------------------"

# Skip header, take column 2 (Username), count duplicates, sort by count, show top 5
tail -n +2 "$FILE" | cut -d',' -f2 | sort | uniq -c | sort -nr | head -5