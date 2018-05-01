from api_calls import get_api_data
from sql import populate_tables


def main():
    api_data = get_api_data()
    populate_tables(api_data)


if __name__ == "__main__":
    main()
