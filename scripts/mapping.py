from datetime import datetime

def infer_season(date_value, season_intervals):
    date_obj = datetime.strptime(date_value, "%Y-%m-%d")

    for season, interval in season_intervals.items():
        start_date, end_date = map(lambda x: datetime.strptime(x, "%m-%d"), interval.split("/"))
        start_date = start_date.replace(year=date_obj.year)
        end_date = end_date.replace(year=date_obj.year)
        if start_date > end_date:
            end_date = end_date.replace(year=date_obj.year + 1)
        if start_date <= date_obj <= end_date:
            return season

    return None  # Return None if no matching season is found

