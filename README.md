# CTA Database App

## This GitHub repository hosts a Python application designed to analyze and interact with the Chicago Transit Authority (CTA) database. The app leverages SQLite to manage and query transit data, providing users with insightful analyses and visualizations using Matplotlib. This utility is a comprehensive tool for exploring various aspects of CTA's transit system data, from station details to ridership trends.

### Features
* Data Interaction: Utilizes SQLite3 to interact with the CTA database, enabling efficient data retrieval and manipulation.
* Analytical Commands: Offers nine distinct commands allowing users to query specific data points and generate statistics from the transit database.
* Visualization: Integrates Matplotlib to plot data, enhancing the data analysis experience with visual representations.
* User-Friendly Interface: Provides a simple command-line interface for users to input their queries and receive immediate feedback and results.
* Comprehensive Statistics: Includes a function to print general statistics about the database, offering a quick overview of key data points.

### Command Descriptions
1. Find Stations: Allows users to search for stations by name, supporting wildcard characters for flexible queries.
2. Ridership by Station: Analyzes and displays ridership details for a specified station, including percentage breakdowns by day type.
3. Weekday Ridership: Outputs the weekday ridership for each station, presenting the data in a percentage format to highlight distribution.
4. Line Details: Retrieves and displays stop information for a specific CTA line color, including direction and accessibility details.
5. Stops Analysis: Enumerates the number of stops for each line color and direction, offering insights into the distribution of CTA's service coverage.
6. Yearly Ridership at Station: Details the annual ridership at a chosen station, with an option to visualize the data.
7. Monthly Ridership at Station: Provides a month-by-month breakdown of ridership for a selected station and year, with a visualization feature.
8. Daily Ridership Comparison: Compares the daily ridership between two stations for a specified year, illustrating trends and differences.
9. Proximity Search: Identifies stations within a one-mile radius of a given latitude and longitude, useful for location-based analysis.
