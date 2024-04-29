import datetime
import os
import time


"""
  Homework#5

  Add your name here: Nicholas McCarty

  You are free to create as many classes within the hw5.py file or across 
  multiple files as you need. However, ensure that the hw5.py file is the 
  only one that contains a __main__ method. This specific setup is crucial 
  because your instructor will run the hw5.py file to execute and evaluate 
  your work.
"""

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
    start_time = time.perf_counter()  # Do not remove this line

    common_city = CommonCity("commonCityNames.txt")
    common_city.find_common_cities()

    lat_lon = LatLon("LatLon.txt")
    city_states = CityStates("CityStates.txt")

    DataProcessedEvent.add_handler(lambda: print("Data processing complete."))

    population = city_states.try_get_population("New York")
    if population is not None:
        print(f"Population of New York: {population}")

    end_time = time.perf_counter()
    # Calculate the runtime in milliseconds
    runtime_ms = (end_time - start_time) * 1000
    print(f"The runtime of the program is {runtime_ms} milliseconds.") 


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
        self.do_process()

    def load_data(self):
        with open("zipcodes.txt", "r") as file:
            lines = file.readlines()
        zip_codes = set(map(str.strip, open("zips.txt", "r")))
        for parts in map(lambda line: line.split('\t'), lines):
            if len(parts) > 7:
                zip_code, lat, lon = parts[1], parts[6], parts[7]
                if zip_code in zip_codes and zip_code not in self.zip_lat_long:
                    self.zip_lat_long[zip_code] = f"{lat} {lon}"

    def get_multiple_populations(self, *cities):
      return {city: self.try_get_population(city) for city in cities}

    def do_process(self):
        with open(self.output_file_name, "w") as file:
            for zip_code, lat_lon in self.zip_lat_long.items():
                file.write(f"{zip_code}: {lat_lon}\n")

class CityStates(IZipProcessor):
    def __init__(self, output_file_name):
        self.output_file_name = output_file_name
        self.cities = set()
        self.city_populations = {}
        self.load_data()

    def load_data(self):
        with open("cities.txt", "r") as file:
            self.cities = set(line.strip().upper() for line in file.readlines())
        self.do_process()

    def do_process(self):
        city_states = {}
        with open("zipcodes.txt", "r") as file:
            lines = file.readlines()

        for line in lines:
            parts = line.split('\t')
            if len(parts) > 4:
                city, state, population = parts[3].upper().strip(), parts[4].strip(), parts[5].strip()
                if city in self.cities:
                    if city not in city_states:
                        city_states[city] = set()
                    city_states[city].add(state)
                    if population.isdigit():
                        self.city_populations[city] = int(population)

        with open(self.output_file_name, "w") as file:
            for city, states in city_states.items():
                population_info = f" (Population: {self.city_populations.get(city, 'Unknown')})"
                file.write(f"{city}{population_info}: {', '.join(states)}\n")

    def try_get_population(self, city):
        return self.city_populations.get(city.upper())


if __name__ == "__main__":
    main()

def mapped_conversion(data):
    mapped_data = list(map(str.upper, data))
  
    filtered_data = list(filter(lambda x: x.startswith('A'), mapped_data))
    
    print("Mapped data:", mapped_data)
    print("Filtered data:", filtered_data)
