import pandas as pd

from entropic.process import Pipeline
from entropic import results


class Process(Pipeline):
    source_paths = ["../tests/mocks/"]
    extract_with = pd.read_csv


p = Process()
p.run()


if __name__ == "__main__":
    for iteration in results.all:
        print(iteration.source_path)
        for sample in iteration.samples:
            print(sample.data.raw.head())
