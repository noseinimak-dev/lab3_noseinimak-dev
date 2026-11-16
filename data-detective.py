import csv
import sys
import os

REQUIRED_COLUMNS = ["Username", "Text", "Retweets", "Likes"]


def load_raw_data(filename):
    """Loads the CSV file into a list of dictionaries exactly as it is (messy)."""
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        print("Make sure twitter_dataset.csv is in the same folder as this script.")
        sys.exit(1)

    raw_tweets = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Empty file: there is no header row at all
            if reader.fieldnames is None:
                print(f"Error: '{filename}' is empty. Please download the dataset again.")
                sys.exit(1)

            # Check that the columns we need exist
            missing = []
            for column in REQUIRED_COLUMNS:
                if column not in reader.fieldnames:
                    missing.append(column)
            if len(missing) > 0:
                print("Error: The CSV is missing column(s): " + ", ".join(missing))
                print("Columns found: " + ", ".join(reader.fieldnames))
                sys.exit(1)

            for row in reader:
                raw_tweets.append(row)
    except (OSError, UnicodeDecodeError, csv.Error) as err:
        print(f"Error: Could not read '{filename}': {err}")
        sys.exit(1)

    return raw_tweets


def to_number(value):
    """Turn text into a whole number. Blank or invalid text becomes 0."""
    try:
        return int(float(value)), False      # False = nothing was fixed
    except (ValueError, TypeError):
        return 0, True                       # True = we had to fix it


def clean_data(tweets):
    """QUEST 1: remove tweets with no Text, replace blank Likes/Retweets with 0."""
    cleaned = []
    removed = 0
    fixed = 0

    for tweet in tweets:
        text = tweet["Text"]

        # No text? Skip this tweet.
        if text is None or text.strip() == "":
            removed += 1
            continue

        # Fix Likes and Retweets (and make them numbers)
        likes, likes_fixed = to_number(tweet["Likes"])
        retweets, retweets_fixed = to_number(tweet["Retweets"])
        tweet["Likes"] = likes
        tweet["Retweets"] = retweets

        if likes_fixed or retweets_fixed:
            fixed += 1

        cleaned.append(tweet)

    print(f"Rows removed (missing Text): {removed}")
    print(f"Rows fixed (blank/invalid Likes or Retweets set to 0): {fixed}")
    print(f"Total bad rows handled: {removed + fixed}")
    print(f"Clean tweets left: {len(cleaned)}\n")
    return cleaned


def find_viral_tweet(tweets):
    """QUEST 2: find the tweet with the most Likes (no max())."""
    winner = tweets[0]

    for tweet in tweets:
        if tweet["Likes"] > winner["Likes"]:
            winner = tweet

    print("--- Viral Tweet ---")
    print("Username:", winner["Username"])
    print("Likes:", winner["Likes"])
    print("Text:", winner["Text"], "\n")


def custom_sort_by_likes(tweets):
    """QUEST 3: selection sort, highest Likes first (no .sort())."""
    sorted_list = []
    for tweet in tweets:          # make a copy so the original stays the same
        sorted_list.append(tweet)

    n = len(sorted_list)
    for i in range(n - 1):
        biggest = i
        for j in range(i + 1, n):
            if sorted_list[j]["Likes"] > sorted_list[biggest]["Likes"]:
                biggest = j

        # swap the biggest into position i
        temp = sorted_list[i]
        sorted_list[i] = sorted_list[biggest]
        sorted_list[biggest] = temp

    return sorted_list


def search_tweets(tweets, keyword):
    """QUEST 4: collect every tweet whose Text contains the keyword."""
    matches = []
    for tweet in tweets:
        if keyword.lower() in tweet["Text"].lower():
            matches.append(tweet)
    return matches


if __name__ == "__main__":
    dataset = load_raw_data("twitter_dataset.csv")

    if len(dataset) == 0:
        print("Error: The file has headers but no tweets in it.")
        sys.exit(1)
    print(f"Loaded {len(dataset)} raw tweets.\n")

    # Quest 1
    clean_dataset = clean_data(dataset)
    if len(clean_dataset) == 0:
        print("Error: No usable tweets left after cleaning, so there is nothing to analyze.")
        sys.exit(1)

    # Quest 2
    find_viral_tweet(clean_dataset)

    # Quest 3
    print("Sorting... (may take a few seconds)")
    ordered = custom_sort_by_likes(clean_dataset)
    print("\n--- Top 10 Most Liked Tweets ---")
    for tweet in ordered[:10]:
        print(tweet["Username"], "|", tweet["Likes"], "likes")
        print("  ", tweet["Text"])

    # Quest 4
    word = input("\nEnter a search word (example: Python): ").strip()
    if word == "":
        print("Error: please type a word, for example: Python")
    else:
        results = search_tweets(clean_dataset, word)
        print(f"\n{len(results)} tweets matched '{word}'.\n")
        for tweet in results:
            print(tweet["Username"], ":", tweet["Text"])