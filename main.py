import sys

from geocoder import get_coordinates, get_ll_span
from mapapi_pg import show_map


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    if toponym_to_find:
        lat, lon = get_coordinates(toponym_to_find)
        ll, spn = get_ll_span(toponym_to_find)
        ll_spn = f"ll={ll}&spn={spn}"

        point = f"pt={ll}"
        show_map(ll_spn, "map", add_params=point)


if __name__ == '__main__':
    main()
