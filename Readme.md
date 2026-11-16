# Lab 3: The Social Media Data Detective

Analyzes `twitter_dataset.csv` (downloaded from Kaggle) using Python and Bash.

## Files
- `data-detective.py` - Python analysis (Quests 1-4)
- `feed-analyzer.sh` - Bash script for the Top 5 most active users
- `twitter_dataset.csv` - the dataset
- `Readme.md` - this file

## How to run
```
python data-detective.py
./feed-analyzer.sh twitter_dataset.csv
```
On Windows, use `py data-detective.py` and run the shell script in Git Bash.

## How it works
- **Quest 1 (Data Auditor):** Rows with blank Text are removed. Blank or invalid Likes/Retweets become 0 and are converted to integers. The program prints how many rows were removed and fixed.
- **Quest 2 (Viral Post):** A loop keeps track of the tweet with the highest Likes and prints its Username, Likes and Text.
- **Quest 3 (Custom Sort):** Selection Sort, written by hand, orders a copy of the list by Likes from highest to lowest. The top 10 are taken by slicing.
- **Quest 4 (Content Filter):** The user enters a word (for example, Python). A case-insensitive search builds a new list of matching tweets, then prints its length and the tweets.
- **Shell script:** `tail` skips the header, `cut -d',' -f2` extracts Username, then `sort | uniq -c | sort -nr | head -5` shows the Top 5 users.

## Error handling
The program shows a clear message for a missing file, an empty file, missing columns, a file with no tweets, blank Text, blank or invalid Likes/Retweets, and empty search input.

## Notes
- Only the Python standard library is used (`csv`, `sys`, `os`). The `csv` module comes from the provided starter template and is used only to read the file.
- No `.sort()`, `sorted()` or `max()` are used.
- Selection Sort can take a few seconds on a large dataset.
- `cut` splits on commas, so a username containing a comma could be miscounted.