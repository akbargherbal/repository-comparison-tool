import pandas as pd


def get_repo_json_tree(df, year, month):
    """
    Get the repository tree structure and metadata for the first commit
    on or after the given year and month.
    """
    year, month = int(year), int(month)

    # Create a target timestamp for the first day of the month (UTC)
    target_date = pd.to_datetime(f"{year:04d}-{month:02d}-01").tz_localize("UTC")

    # Filter for the first commit on or after the target date.
    # The DataFrame is assumed to be pre-sorted by date in app.py.
    filtered_df = df[df["DATE"] >= target_date]

    if filtered_df.empty:
        raise ValueError(f"No data found for or after {year}-{month}")

    # Get the first matching row
    result = filtered_df.iloc[0]

    json_tree = result["TREE"]
    date = result["DATE"]
    commit_hash = result["COMMIT_HASH"]
    github_link = result["GITHUB_LINK"]

    return json_tree, date, commit_hash, github_link
