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
