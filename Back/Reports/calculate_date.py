from datetime import datetime

def calculate_start_end_date_from_period(period):
    if period == "Месяц":
        current_month, current_year = datetime.now().month, datetime.now().year

        end_month = current_month + 1 if current_month != 12 else 1
        end_year = current_year if current_month != 12 else current_year + 1

        start_date = datetime.strptime(
            f"{current_year}-{current_month}-01 00:00:00",
            "%Y-%m-%d %H:%M:%S"

        )

        end_date = datetime.strptime(
            f"{end_year}-{end_month}-1 00:00:00",
            "%Y-%m-%d %H:%M:%S"
        )

    elif period == "Год":
        current_year = datetime.now().year
        end_year = current_year + 1

        start_date = datetime.strptime(
            f"{current_year}-01-01 00:00:00",
            "%Y-%m-%d %H:%M:%S"
        )

        end_date = datetime.strptime(
            f"{end_year}-01-01 00:00:00",
            "%Y-%m-%d %H:%M:%S"
        )

    else:
        start_date = datetime.strptime(
            "0001-01-01 00:00:00",
            "%Y-%m-%d %H:%M:%S"
        )

        end_date = datetime.now().replace(microsecond=0)
    return start_date, end_date