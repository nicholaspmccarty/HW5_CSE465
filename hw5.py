import datetime
import os

class DataProcessedEvent:
    handlers = []

    @staticmethod
    def add_handler(handler):
        DataProcessedEvent.handlers.append(handler)

    @staticmethod
    def trigger():
        for handler in DataProcessedEvent.handlers:
            handler()


def main():
    start_time = datetime.datetime.now()

    common_city = CommonCity("commonCityNames.txt")
    common_city.find_common_cities()

    lat_lon = LatLon("LatLon.txt")
    city_states = CityStates("CityStates.txt")

    DataProcessedEvent.add_handler(lambda: print("Data processing complete."))

    population = city_states.try_get_population("New York")
    if population is not None:
        print(f"Population of New York: {population}")

    end_time = datetime.datetime.now()
    elapsed_time = (end_time - start_time).total_seconds() * 1000
    print(f"Elapsed Time: {elapsed_time} ms")


class IZipProcessor:
    def load_data(self):
        pass

    def do_process(self):
        pass


class CommonCity(IZipProcessor):
    def __init__(self, filename):
        self.filename = filename
        self.state_cities = {}
        self.load_data()

    def load_data(self):
        with open("states.txt", "r") as file:
            states = file.readlines()
        for state in states:
            self.state_cities[state.strip()] = set()

    def do_process(self):
        self.find_common_cities()

    def find_common_cities(self):
        with open("zipcodes.txt", "r") as file:
            lines = file.readlines()
        for line in lines:
            parts = line.split('\t')
            if len(parts) > 4:
                city = parts[3]
                state = parts[4]
                if state in self.state_cities:
                    self.state_cities[state].add(city)

        common_cities = set.intersection(*self.state_cities.values())

        with open(self.filename, "w") as file:
            for city in sorted(common_cities):
                file.write(f"{city}\n")

class LatLon(IZipProcessor):
    def __init__(self, output_file_name):
        self.output_file_name = output_file_name
        self.zip_lat_long = {}
        self.load_data()

    def load_data(self):
        with open("zipcodes.txt", "r") as file:
            lines = file.readlines()
        zip_codes = set(line.strip() for line in open("zips.txt", "r"))
        for line in lines:
            parts = line.split('\t')
            if len(parts) > 7:
                zip_code, lat, lon = parts[1], parts[6], parts[7]
                if zip_code in zip_codes and zip_code not in self.zip_lat_long:
                    self.zip_lat_long[zip_code] = f"{lat} {lon}"
