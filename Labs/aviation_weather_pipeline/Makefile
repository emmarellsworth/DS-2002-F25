SHELL := /bin/bash

.PHONY: all fetch analyze clean
.DEFAULT_GOAL := analyze

all: analyze

fetch:
	echo "Starting fetch..."
	./fetch_metars.sh
	echo "Fetch done. Files saved in raw_metars/"

analyze: fetch
	echo "Starting analysis..."
	./analyze_data.sh
	echo "Analysis done. Results in weather_report.csv"
	echo "Pipeline finished!"

clean:
	echo "Cleaning up..."
	rm -rf raw_metars weather_report.csv
	echo "Clean done."
