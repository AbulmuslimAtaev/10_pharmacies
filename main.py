import sys

from business import find_businesses
from distance import lonlat_distance
from geocoder import get_coordinates
from mapapi_pg import show_map


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    if toponym_to_find:
        lat, lon = get_coordinates(toponym_to_find)
        adress_ll = f"{lat},{lon}"
        span = "0.005,0.005"
        organization = find_businesses(adress_ll, span, "аптека")
        point_params = f"pt={adress_ll},vkbkm"
        for i in organization[:10]:
            color = "pm2grm"
            point = i["geometry"]["coordinates"]
            org_lat = float(point[0])
            org_lon = float(point[1])
            name = i["properties"]["CompanyMetaData"]["name"]
            address = i["properties"]["CompanyMetaData"]["address"]
            time = i["properties"]["CompanyMetaData"].get("Hours", None)
            if time:
                if time["Availabilities"][0].get('TwentyFourHours', None):
                    color = "pm2gnm"
                elif time["Availabilities"][0].get('Intervals', None):
                    color = "pm2dbm"
                time = time["text"]
            else:
                time = "нет информации"
            print("Название: " + name, "\t\tАдрес: " + address, time)
            point_params += f"~{org_lat},{org_lon},{color}"
        show_map(map_type="map", add_params=point_params)


if __name__ == '__main__':
    main()
