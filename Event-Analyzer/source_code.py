
### Here we first import what we will need to run our code

from ast import If

import ipywidgets as widgets # I included this to provide a widget for the user to click in order to upload a file
from pathlib import Path
import pandas as pd  
from IPython.display import display
import io
import os

"""All of the above imports are necessary for the code to run. 
The ipywidgets library is used to create interactive widgets in Jupyter notebooks, 
which allows users to upload files. The display function from IPython.display is used to display the widgets 
and other outputs in the notebook. The pandas library is used for data manipulation and analysis, while the io 
module is used to handle input/output operations, such as reading files from memory."""

# This section answers 2A. I always consider parameters inside functions as place holders
# This function calculate the number of events , where len() is used and events is a place holder
def count_events(events : int )-> int :
    """
        counts the total number of events.
        variable
        ----------
        total_events : 
        Parameters
        ----------
        events : pandas.DataFrame
                The DataFrame containing event records. 
    
        Returns
        -------
        int
            The total number of events in the DataFrame.
        ------
        TypeError
            If the event is not a pandas DataFrame.
        """

    total_events = len(events)
    print(f"Total Number of Events: {total_events}")
    pass

#This answers 2B . This function calculate how many events were successful and how many failed
def count_by_status(events : int) -> int:
    """
        counts the total number of events by status.
        Variables
        ----------
        status_counts : pandas.Series
                A Series containing the counts of events grouped by their status.   
        Parameters
        ----------
        events : pandas.DataFrame
                The DataFrame containing event records. 
    
        Returns
        -------
        int
            The total number of events group by status in the DataFrame.
        ------
        TypeError
            If the event is not a pandas DataFrame.
        """
    status_counts = events['status'].value_counts()

    print(" Status Occurrences:")
    for status, count in status_counts.items():
        print(f"• {status}: {count} times")
    pass


# This answers 2C
def count_by_user(events : int) -> int:
    """
        counts the total number of events by user.
        variables
        ----------
        user_counts : pandas.Series
                A Series containing the counts of events grouped by their user.
        count : which is a variable that is used to store the count of events for each user.
        Parameters
        ----------
        events : pandas.DataFrame
                The DataFrame containing event records. 
    
        Returns
        -------
        int
            The total number of events in the DataFrame.
        ------
        TypeError
            If the event is not a pandas DataFrame.
        """
    user_counts = events['user'].value_counts()

    print("Events per User:")
    for user, count in user_counts.items():
        print(f"• {user}: {count} events")

    pass

# This answers 2D
def calculate_average_duration(events : float) -> float:
    """
        calculates the average duration of events.
        variables
        ----------
        average_duration : float
                The average duration of events calculated from the 'duration' column in the DataFrame.
        Parameters
        ----------
        events : pandas.DataFrame
                The DataFrame containing event records. 
    
        Returns
        -------
        float
            The average duration of events in the DataFrame.
        ------
        TypeError
            If the event is not a pandas DataFrame.
        """
    average_duration = events['duration'].mean()

    print(f"Average Event Duration: {average_duration:.2f} seconds")

    pass

# This answers 2E
def find_slowest_event(events :pd.DataFrame) -> pd.series:
    """
        finds the slowest event in the DataFrame.
        variables
        ----------
        longest_event_idx : int
                The index of the event with the maximum duration in the DataFrame.  
        longest_event : pandas.Series
                The row corresponding to the slowest event in the DataFrame.
        Parameters
        ----------
        events : pandas.DataFrame
                The DataFrame containing event records. 
    
        Returns
        -------
        pandas.Series
            The row corresponding to the slowest event.
        ------
        TypeError
            If the event is not a pandas DataFrame.
        """
    longest_event_idx = events['duration'].idxmax()
    longest_event = events.loc[longest_event_idx]

    print("Longest Event:")
    print(f"• User: {longest_event['user']}")
    print(f"• Action: {longest_event['action']}")
    print(f"• Duration: {longest_event['duration']} seconds")

    pass

# This answers 2F
def get_failed_events(events : pd.DataFrame) -> pd.Series:
    """
        gets the failed events from the DataFrame.
        variables
        ----------
        failed_events : pandas.DataFrame
                The DataFrame containing only the failed events.
        Parameters
        ----------
        events : pandas.DataFrame
                The DataFrame containing event records.

        Returns
        -------
        pandas.DataFrame
            The DataFrame containing only the failed events.
        ------
        TypeError
            If the event is not a pandas DataFrame.
        """
    failed_events = events[events['status'] == 'failed']

    print("Failed Events:")
    if not failed_events.empty:
        display(failed_events)
    else:
        print("No failed events found.")

    pass
 
#The is no question for this function but I included it to display a banner for the user. Just for fun
def display_banner()-> str:  # No parameters for this code
    """ Displays a banner with the text "Event Analyzer" using ASCII art.
         
    
        Parameters
        ----------
         There are no parameters for this function.
    
        Returns
        -------
        String
            A string containing the ASCII art representation of "Event Analyzer".
        ------
        TypeError
            if the function is called with any arguments.
            if you did not import Figlet from pyfiglet library.
        """
    from pyfiglet import Figlet

    fig = Figlet(font="banner")
    print(fig.renderText("Event"))
    print(fig.renderText("Analyzer"))
     

def main() -> None:
    """    calls all the functions above to display the results of the analysis on the events data.
             
            variables
            ----------
             script_dir : Path
                    The directory path of the current script file.
             file_path : Path
                    The path to the "events.json" file located in the same directory as the script.
             df : pandas.DataFrame
                    The DataFrame containing the loaded events data from the JSON file.
            Parameters
            ----------
             There are no parameters for this function.
        
            Returns
            -------
            A report for the user containing the results of the analysis on the events data.
            ------
            TypeError
                if the function is called with any arguments.
                if you did not import Path from pathlib library.
                if you did not import pandas as pd library.
            """
    script_dir = Path(__file__).parent
    file_path = script_dir / "events.json"

    print(f"Looking for: {file_path}")

    try:
        df = pd.read_json(file_path)

        print(f"Successfully loaded: {file_path.name}")

        print("\n" + "=" * 40 + "\n")
        display_banner()
        print("\n" + "=" * 40 + "\n")
        print("\n","Preview of your data:")
        display(df.head())
        count_events(df)
        print("\n")
        count_by_status(df)
        print("\n")
        count_by_user(df)
        print("\n")
        calculate_average_duration(df)
        print("\n")
        find_slowest_event(df)
        print("\n")
        get_failed_events(df)
        print("\n" + "=" * 40 + "\n")

    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    """
    The main entry point of the script. It calls the main() function to execute the analysis on the events data.
    This block ensures that the main() function is only executed when the script is run directly,
    """
    main()




 