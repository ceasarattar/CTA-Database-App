##################################################################  
# CTA Database App
# Ceasar Attar
# VSCode on MacOS
# In this App I have utilized all 9 different commands to provide the user with the desired output for each command
##################################################################  


import sqlite3
import matplotlib.pyplot as plt


##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
################################################################## 
 
 
# Function to print general statistics from the CTA database
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    print("General Statistics:")
    
    # Query to count the number of stations
    dbCursor.execute("SELECT count(*) FROM Stations;")
    row = dbCursor.fetchone()
    print("  # of stations:", f"{row[0]:,}")

    # Query to count the number of stops
    dbCursor.execute("SELECT count(*) FROM Stops;")
    row = dbCursor.fetchone()
    print("  # of stops:", f"{row[0]:,}")

    # Query to count the number of ride entries
    dbCursor.execute("SELECT count(*) FROM Ridership;")
    row = dbCursor.fetchone()
    print("  # of ride entries:", f"{row[0]:,}")

    # Query to get the date range of ride entries
    dbCursor.execute("SELECT Date(Ride_Date) FROM Ridership;")
    row = dbCursor.fetchall()
    print("  date range:", f"{row[0][0]} - {row[-1][0]}")

    # Query to sum the total ridership
    dbCursor.execute("SELECT SUM(Num_Riders) FROM Ridership;")
    row = dbCursor.fetchone()
    print("  Total ridership:", f"{row[0]:,}")

# Function for command1: find stations by user input pattern
def command1(user_input):
    dbCursor = dbConn.cursor()
    dbCursor.execute("""SELECT Station_ID, Station_Name 
                        FROM Stations 
                        WHERE Station_Name LIKE ? 
                        ORDER BY Station_Name ASC;""", (user_input,))
    result = dbCursor.fetchall()

    if not result: # if the result is empty, print out a message
        print("**No stations found...")
        return
    
    for row in result: # prints out the station along with the station ID
        print(f"{row[0]} : {row[1]}")

# Function for command2: find ridership by station name
def command2(user_input):
    # Initialize the database cursor
    dbCursor = dbConn.cursor()

    # Query to get the ridership data grouped by type of day
    dbCursor.execute("""SELECT Type_of_Day, SUM(Num_Riders) as Total_Daily_Ridership 
                        FROM Ridership 
                        JOIN Stations ON Ridership.Station_ID = Stations.Station_ID 
                        WHERE Station_Name = ? 
                        GROUP BY Type_of_Day""", (user_input,))
    result = dbCursor.fetchall()

    # Handle case with no data found
    if not result:
        print("**No data found...\n")
        return

    # Calculate total ridership and ridership by day type
    Total_Ridership = sum(day_ridership for _, day_ridership in result)
    Ridership_Daytype = {day_type: day_ridership for day_type, day_ridership in result}

    # Output the percentage of ridership for each day type
    print(f"Percentage of ridership for the {user_input} station: ")
    for day_type, description in [('W', 'Weekday'), ('A', 'Saturday'), ('U', 'Sunday/holiday')]:
        day_ridership = Ridership_Daytype.get(day_type, 0)
        percentage = (100 * day_ridership / Total_Ridership) if Total_Ridership > 0 else 0
        print(f"  {description} ridership: {day_ridership:,} ({percentage:.2f}%)")
    
    # Output total ridership
    print(f"  Total ridership: {Total_Ridership:,}\n")

def command3(dbConn):
    # Create a cursor object using the connection object passed to the function
    dbCursor = dbConn.cursor()

    # Execute SQL query to select total ridership on weekdays by station
    # and order the results by total ridership in descending order
    dbCursor.execute("""
    SELECT Station_Name, SUM(Num_Riders) AS Total_Ridership 
    FROM Ridership 
    JOIN Stations ON Ridership.Station_ID = Stations.Station_ID 
    WHERE Type_of_Day = 'W' 
    GROUP BY Station_Name 
    ORDER BY Total_Ridership DESC;
    """)
    results = dbCursor.fetchall()

    # Initialize variable to sum total ridership across all stations
    Weekday_Ridership = 0

    # Sum the total ridership from the query results
    for row in results:
        Weekday_Ridership += row[1]
    
    # Loop through each station's results to calculate and print ridership percentage
    for row in results:
        station_name, ridership = row

        # Calculate percentage if total weekday ridership is greater than zero
        if (Weekday_Ridership > 0):
            percentage = (ridership / Weekday_Ridership) * 100
        else:
            percentage = 0

        # Print the station name, its ridership, and the calculated percentage
        print(f"{station_name} : {ridership:,} ({percentage:.2f}%)")

def command4(user_input):
    # Create a cursor object using the database connection
    dbCursor = dbConn.cursor()

    # Check if the entered line color exists in the Lines table
    dbCursor.execute("SELECT 1 FROM Lines WHERE Color LIKE ? ;", (user_input,))
    result = dbCursor.fetchone()

    # If no result is found, print error message and exit function
    if not result:
        print("**No such line...")
        return
    
    # Prompt the user to enter the direction of the line
    direction = input("Enter a direction (N/S/W/E): ").strip()

    # Retrieve the stops in the specified direction for the entered line color
    dbCursor.execute("""
        SELECT Stops.Direction, Stop_Name, Stops.ADA 
        FROM Stops 
        JOIN StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID 
        JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID 
        WHERE Lines.Color LIKE ? AND Stops.Direction LIKE ? 
        ORDER BY Stops.Stop_Name ASC;
    """, (user_input, direction))
    result = dbCursor.fetchall()

    # If results are found, iterate over the rows and print stop details
    if result:
        for row in result:
            # Determine the handicap status based on the ADA column value
            handicapStatus = "handicap accessible" if row[2] == 1 else "not handicap accessible"
            # Print the stop name, direction, and handicap status
            print(f"{row[1]} : direction = {row[0]} ({handicapStatus})")
    else:
        # If no results are found, print error message indicating the line does not run in the chosen direction
        print("**That line does not run in the direction chosen...")

def command5(dbConn):
    # Create a cursor to interact with the database
    dbCursor = dbConn.cursor()
    
    # Print the function's purpose for user clarity
    print("Number of Stops For Each Color By Direction")

    # Execute SQL query to count the total number of stops
    dbCursor.execute("SELECT COUNT(*) AS sum_stops FROM Stops;")
    result = dbCursor.fetchone()
    
    # If no result is found, print a message and exit function
    if (not result or not result[0]):
        print("No data found.")
        return
    
    # Store the total number of stops for percentage calculation
    sum_stops = result[0]

    # Execute SQL query to get count of stops by color and direction
    dbCursor.execute("""SELECT Lines.Color, Stops.Direction, COUNT(Stops.Stop_ID) AS count_stop 
                        FROM Stops 
                        JOIN StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID 
                        JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID 
                        GROUP BY Lines.Color, Stops.Direction 
                        ORDER BY Lines.Color ASC, Stops.Direction ASC;""")
    result_Stops = dbCursor.fetchall()

    # Iterate over the result set and print stop information with percentages
    for row in result_Stops:
        color, direction, count_stop = row[0], row[1], row[2]
        # Calculate the percentage of the total stops
        percentage = (count_stop / sum_stops) * 100
        # Print each line color with its direction and the corresponding stop count and percentage
        print(f"{color.capitalize()} going {direction} : {count_stop} ({percentage:.2f}%)")
        
def command6(dbConn):
    # Create a database cursor for executing SQL commands
    dbCursor = dbConn.cursor()
    
    # Prompt user for station name with wildcard support and strip leading/trailing spaces
    user_input = input("\nEnter a station name (wildcards _ and %): ").strip()

    # Retrieve station name and total yearly ridership from the Ridership table
    dbCursor.execute("""
        SELECT Stations.Station_Name, strftime('%Y', Ride_Date) AS Year, SUM(Num_Riders) AS Total_Riders 
        FROM Ridership 
        JOIN Stations ON Ridership.Station_ID = Stations.Station_ID 
        WHERE Stations.Station_Name LIKE ? 
        GROUP BY Station_Name, Year 
        ORDER BY Station_Name ASC, Year ASC;
    """, (user_input,))
    station_data = dbCursor.fetchall()

    # Handle no station found case
    if not station_data:
        print("**No station found...\n")
        return
    # Handle multiple stations found case
    elif len(set(row[0] for row in station_data)) > 1:
        print("**Multiple stations found...\n")
        return
    else:
        # If a single station is found, proceed to display yearly ridership data
        station_name = station_data[0][0]
        print(f"Yearly Ridership at {station_name}")
        for row in station_data:
            year, total_riders = row[1], row[2]
            print(f"{year} : {total_riders:,}")

    # Ask user if they want to see a plot of the data
    plotOpt = input("\nPlot? (y/n) ").strip().lower()

    # Plot if user opts in
    if plotOpt == 'y':
        # Prepare data for plotting
        years = [row[1] for row in station_data]
        ridership = [row[2] for row in station_data]

        # Plotting code remains unchanged
        plt.plot(years, ridership, marker='o')
        plt.title(f"Yearly Ridership at {station_name}")
        plt.xlabel("Year")
        plt.ylabel("Number of Riders")
        plt.grid(True)
        plt.show()
    else:
        print()

def command7(dbConn):
    # Establish a database cursor for executing SQL commands
    dbCursor = dbConn.cursor()
    
    # Prompt the user to input a station name with support for wildcards
    user_input = input("\nEnter a station name (wildcards _ and %): ").strip()

    # Retrieve station names that match the user input pattern
    dbCursor.execute("SELECT Station_Name FROM Stations WHERE Station_Name LIKE ?;", (user_input,))
    station_rows = dbCursor.fetchall()

    # Handle cases with no matching stations or multiple matches
    if not station_rows:
        print("**No station found...\n")
        return
    elif len(station_rows) > 1:
        print("**Multiple stations found...\n")
        return

    # Store the single matching station name
    station_name = station_rows[0][0]
    
    # Request the user to input a year
    year = input("Enter a year: ").strip()

    # Execute a query to fetch total ridership by month for the given station and year
    dbCursor.execute("""
        SELECT strftime('%m', Ride_Date) AS Month, SUM(Num_Riders) AS TotalRiders
        FROM Ridership
        JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
        WHERE Station_Name = ? AND strftime('%Y', Ride_Date) = ?
        GROUP BY Month
        ORDER BY Month ASC;""", (station_name, year))

    # Fetch all rows from the executed query
    ridership_rows = dbCursor.fetchall()

    # Print the fetched monthly ridership data
    print(f"Monthly Ridership at {station_name} for {year}")
    for row in ridership_rows:
        month, total_riders = row
        print(f"{month}/{year} : {total_riders:,}")

    # Ask the user if they want to plot the data
    plot_opt = input("\nPlot? (y/n) ").strip().lower()

    # If user opts to plot, generate a plot of the monthly ridership data
    if plot_opt == 'y':
        # Create lists of months and ridership data for plotting
        months = [int(month) for month, _ in ridership_rows]
        ridership = [total for _, total in ridership_rows]

        # Generate and display the plot
        plt.plot(months, ridership, marker='o')
        plt.title(f"Monthly Ridership at {station_name} Station ({year})")
        plt.xlabel("Month")
        plt.ylabel("Number of Riders")
        plt.xticks(range(1, 13))  # Ensure all months are represented on the x-axis
        plt.grid(True)  # Enable grid for better readability
        plt.show()
    else:
        print();  # Print a new line for clean output

# Function to output the total ridership for two stations for each day in a given year.
def command8(dbConn):
    # Initialize the database cursor
    dbCursor = dbConn.cursor()

    # Prompt the user for the year to compare ridership against
    user_input = input("\nYear to compare against? ").strip()

    # Nested function to fetch data for a station based on a name pattern
    def fetch_station_data(station_name_pattern):
        # Execute SQL query to retrieve station name and ID
        dbCursor.execute("""SELECT Station_Name, Station_ID 
                             FROM Stations 
                             WHERE Station_Name LIKE ?;""", (station_name_pattern,))
        rows = dbCursor.fetchall()

        # Check if the station data exists or if multiple entries are found
        if len(rows) != 1:
            if not rows:
                print("**No station found...")
            else:
                print("**Multiple stations found...")
            return None, None
        return rows[0]

    # Retrieve and validate data for the first station
    station1, station_id_1 = fetch_station_data(input("\nEnter station 1 (wildcards _ and %): ").strip())
    if not station1:
        return
    
    # Retrieve and validate data for the second station
    station2, station_id_2 = fetch_station_data(input("\nEnter station 2 (wildcards _ and %): ").strip())
    if not station2:
        return

    # Function to print ridership data for a given station
    def print_ridership_data(station, station_id, station_number):
        # Execute SQL query to fetch ridership data
        dbCursor.execute("""SELECT Ride_Date, Num_Riders 
                             FROM Ridership 
                             WHERE Station_ID = ? AND strftime('%Y', Ride_Date) = ? 
                             ORDER BY Ride_Date ASC;""", (station_id, user_input))
        ridership = dbCursor.fetchall()
        
        # Print the retrieved ridership data
        print(f"Station {station_number}: {station_id} {station}")
        for row in ridership[:5] + ridership[-5:]:
            date, num_riders = row
            print(f"{date.split()[0]} {num_riders}")

    # Call the print function for both stations
    print_ridership_data(station1, station_id_1, "1")
    print_ridership_data(station2, station_id_2, "2")

    # Prompt user to choose whether to plot the data
    if input("\nPlot? (y/n) \n").lower() == 'y':
        # Prepare data for plotting
        dates = [row[0].split()[0] for row in dbCursor.execute("""SELECT DISTINCT Ride_Date 
                                                                   FROM Ridership 
                                                                   WHERE strftime('%Y', Ride_Date) = ? 
                                                                   ORDER BY Ride_Date ASC""", (user_input,)).fetchall()]
        ridership_1 = [row[0] for row in dbCursor.execute("""SELECT Num_Riders 
                                                              FROM Ridership 
                                                              WHERE Station_ID = ? AND strftime('%Y', Ride_Date) = ? 
                                                              ORDER BY Ride_Date ASC;""", (station_id_1, user_input)).fetchall()]
        ridership_2 = [row[0] for row in dbCursor.execute("""SELECT Num_Riders 
                                                              FROM Ridership 
                                                              WHERE Station_ID = ? AND strftime('%Y', Ride_Date) = ? 
                                                              ORDER BY Ride_Date ASC;""", (station_id_2, user_input)).fetchall()]

        # Plot the data
        plt.plot(dates, ridership_1, label=station1)
        plt.plot(dates, ridership_2, label=station2)
        plt.title(f"Ridership Each Day of {user_input}")
        plt.xlabel("Day")
        plt.ylabel("Number of Riders")
        plt.legend()
        plt.xticks(rotation=45)
        plt.show()

    else:
        print()  # If user opts out of plotting, end the function

# Function to find and plot stations within a one-mile radius based on user-provided latitude and longitude.
def command9(dbConn):
    dbCursor = dbConn.cursor()
    
    # Attempt to convert user input into a float, ensuring it represents a valid latitude.
    try:
        lat = float(input("\nEnter a latitude: "))
    except ValueError:
        print("**Latitude entered is out of bounds...")
        return
    
    # Check if latitude is within the valid range for Chicago.
    if not (40 <= lat <= 43):
        print("**Latitude entered is out of bounds...\n")
        return

    # Attempt to convert user input into a float, ensuring it represents a valid longitude.
    try:
        lon = float(input("Enter a longitude: "))
    except ValueError:
        print("**Longitude entered is out of bounds...")
        return

    # Check if longitude is within the valid range for Chicago.
    if not (-88 <= lon <= -87):
        print("**Longitude entered is out of bounds...\n")
        return

    # Calculate the conversion factors for latitude and longitude.
    lat_conversion = 1 / 69  # Approximation of miles per degree of latitude.
    lon_conversion = 1 / 51  # Approximation of miles per degree of longitude.

    # Define the latitude and longitude boundaries of the one-mile radius.
    one_mile_lat_bounds = {
        "min_latitude": round(lat - lat_conversion, 3),
        "max_latitude": round(lat + lat_conversion, 3)
    }
    one_mile_lon_bounds = {
        "min_longitude": round(lon - lon_conversion, 3),
        "max_longitude": round(lon + lon_conversion, 3)
    }

    # Execute SQL query to find stations within the one-mile radius.
    dbCursor.execute("""
        SELECT DISTINCT Stations.Station_Name, Stops.Latitude, Stops.Longitude
        FROM Stations
        JOIN Stops ON Stations.Station_ID = Stops.Station_ID
        WHERE Stops.Latitude BETWEEN ? AND ?
        AND Stops.Longitude BETWEEN ? AND ?
        ORDER BY Stations.Station_Name;
    """, (one_mile_lat_bounds['min_latitude'], one_mile_lat_bounds['max_latitude'],
          one_mile_lon_bounds['min_longitude'], one_mile_lon_bounds['max_longitude']))
    
    result = dbCursor.fetchall()

    # Check if any stations were found and print results.
    if not result:
        print("**No stations found...")
        return
    
    print("\nList of Stations Within a Mile")
    for station in result:
        print(f"{station[0]} : ({station[1]}, {station[2]})")

    # Function to plot stations on a map.
    def plot_stations(coordinates, image_path, map_size):
        x, y = zip(*coordinates)  # Unpack the station coordinates.
        image = plt.imread(image_path)  # Load the map image.

        # Plot the image with stations as red dots and label them.
        plt.imshow(image, extent=map_size)
        plt.title("Stations Near You")
        plt.scatter(x, y, s=50, marker='o', color='red', zorder=2)
        for row, (xcoord, ycoord) in zip(result, coordinates):
            plt.annotate(row[0], (xcoord, ycoord), textcoords="offset points", xytext=(0, 5), ha='center')

        # Set the limits of the map based on the extent.
        plt.xlim(map_size[:2])
        plt.ylim(map_size[2:])
        plt.show()

    # Prompt user for plot option and call plot function if 'y'.
    if input("\nPlot? (y/n) \n").lower() == 'y':
        coordinates = [(float(row[1]), float(row[2])) for row in result]
        image_path = "chicago.png"
        map_size = [-87.9277, -87.5569, 41.7012, 42.0868]  # Define the map size based on Chicago coordinates.
        plot_stations(coordinates, image_path, map_size)
    else:
        print()  # Exit if the user does not want to plot.
        return

    
##################################################################  
#
# main
#
##################################################################
    

# Welcome message for the CTA L analysis application.
print('** Welcome to CTA L analysis app **')
print()

# Establish a connection to the CTA database.
dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

# Call the function to print general statistics from the database.
print_stats(dbConn)
print()

# Main loop for user command input.
while True:
    # Prompt user for a command.
    menu_input = input("Please enter a command (1-9, x to exit): ")
    # Exit condition if the user chooses 'x'.
    if (menu_input == 'x'):
        break

    # Call the corresponding function based on user input.
    if (menu_input == '1'): # command option 1
        user_input = input("\nEnter partial station name (wildcards _ and %): ")
        command1(user_input);
        continue
    
    if (menu_input == '2'): # command option 2
        user_input = input("\nEnter the name of the station you would like to analyze: ")
        command2(user_input);
        continue

    if (menu_input == '3'): # command option 3
        print("Ridership on Weekdays for Each Station")
        command3(dbConn);
        continue

    if (menu_input == '4'): # command option 4
        user_input = input("\nEnter a line color (e.g. Red or Yellow): ")
        command4(user_input);
        continue

    if (menu_input == '5'): # command option 5
        command5(dbConn);
        continue

    if (menu_input == '6'): # command option 6
        command6(dbConn);
        continue

    if (menu_input == '7'): # command option 7
        command7(dbConn);
        continue

    if (menu_input == '8'): # command option 8
        command8(dbConn);
        continue

    if (menu_input == '9'): # command option 9
        command9(dbConn);
        continue

    # Error message for an unknown command.
    else:
        print("**Error, unknown command, try again...")
        print()



##################################################################  
#
# done
#
##################################################################
