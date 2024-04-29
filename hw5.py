import datetime

def main():
    start_time = datetime.datetime.now()
    # Placeholder for processing logic

    end_time = datetime.datetime.now()
    elapsed_time = (end_time - start_time).total_seconds() * 1000
    print(f"Elapsed Time: {elapsed_time} ms")

if __name__ == "__main__":
    main()

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
    DataProcessedEvent.add_handler(lambda: print("Data processing complete."))

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