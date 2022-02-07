import sys

from business import find_business
from distance import lonlat_distance
from geocoder import get_coordinates
from mapapi_pg import show_map


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    if toponym_to_find:
        lat, lon = get_coordinates(toponym_to_find)
        adress_ll = f"{lat},{lon}"
        span = "0.005,0.005"
        print(adress_ll, span, "аптека")
        organization = find_business(adress_ll, span, "аптека")
        point = organization["geometry"]["coordinates"]
        org_lat = float(point[0])
        org_lon = float(point[1])
        point_params = f"pt={org_lat},{org_lon}"

        point_params += f"~{adress_ll}"

        print(organization["properties"]["CompanyMetaData"])
        name = organization["properties"]["CompanyMetaData"]["name"]
        address = organization["properties"]["CompanyMetaData"]["address"]
        time = organization["properties"]["CompanyMetaData"].get("Hours", None)
        if time:
            time = time["text"]
        else:
            time = "нет информации"
        distancee = lonlat_distance((lon, lat), (org_lon, org_lat))
        snippet = f"Название:\t{name}\nАдрес:  \t{address}\nВремя работы:\t{time}\n" \
                  f"Расстояние:\t{distancee} м"
        print(snippet)

        show_map(map_type="map", add_params=point_params)


if __name__ == '__main__':
    main()
