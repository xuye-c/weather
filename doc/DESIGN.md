# Weather APP backend

## Use Cases
**Search weather for a specific location**
* User input the name of the city
* The system validates whether the city is in database
    * if not, throw exception
    * if days not selected
        * System search for the weather for the last 7 days
    * if day/range selected
        * The system validates whether weather of the days is recorded, give not found message for those missing days
* The mimic-frontend display the result returned
* Google map API display map

**Edit an existing record by searching**
* User input the name of the city and the day range
* The system return the current result stored if the record exists
* User click the "Edit" button to the record to be edited.
* System pop-up the "input window" with "city name", "day" and "temperature" bars. "City name" should not be allowed to change.
* User input the new data
* System update the database, close the input window, and refresh the mimic-frontend display based on the new data.

**User input a new record**
* User click "new record" button
* System pop-up the "input window" with "city name", "day" and "temperature" bars blank.
* User input data.
* System search by city name and day to check if there is record in data base.
    * if there is, display old data and "ask" message: whether you are to cover the old data.
        * if user cancels, close the input window
        * if user confirms, delete this piece of data
    * write new data into the database
    *show succeed message

**User delete a piece of record**
* User input the name of the city and the day range
* The system return the current result stored if the record exists
* User click the "Delete" button to the record to be deleted.
* System display "ask" message: whether you are to delete this piece of data
    * if user confirms, system delete this piece of data
    * if user cancels, system close ask message and do nothing

**User Export Data**
* User input the name of the city and the day range
* The system return the current result stored if the record exists
* User Click Export
* Save the pieces of records displayed into a .csv file



## Design Plan
### SQLite Database management
* DatabaseManager
    * Writer
        * Delete Existing Data
        * Write new data
    * Reader
        * validate if there is existing record -- (days&city names)
        * read content from database
    * csvFactory(?)
* Exceptions
* GoogleMapAPI
### Micmic Frontend view(not planned)
* Views
    * Search bar
        * textbase city name
        * selectable dates
        * "confirm" button to start search
    * Result Window:
        * display result found in database and returned from the backend
    * TinyTerminal:
        * display error messages translated
    * Legend:
        * Google mapview
        * Cityname and info
    * input Winodw (display only when it needs to be popped up)
        * cityname, days, temperature, info(if needed)
    * Localization preparation(?)
### Controller for user input and M-V communication
* ExceptionTranslator
    * Show Exceptions from backend in User-friendly way
* InputManager
    * First Validates if user input misses necessary info or changes unchangeable info
    * Call backend to validate whether there is record in database if needed
    * Pass user input to backend
* Dataparser
    * pass result from backend to Result Window