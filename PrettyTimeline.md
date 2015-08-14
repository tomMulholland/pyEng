| Date        | Goal           | Current Completion  |
| ------------- |:-------------:| -----:|
| 1 September 2015      | First data class entry form is functional | ![alt text](http://progressed.io/bar/50) |
| 1 October 2015      | Sample, Instrument, and Test data class entry forms are functional | ![alt text](http://progressed.io/bar/0) |
| 1 October 2015      | HTML-based browse of data is functional      |   ![alt text](http://progressed.io/bar/0) |
| 15 October 2015      | Have a plan for user permissions and access      |   ![alt text](http://progressed.io/bar/20) |
| 1 November 2015      | HTML-based search of DB is functional (using the most convenient syntax)      |   ![alt text](http://progressed.io/bar/0) |
| 1 December 2015      | HTML-based search of DB is functional (user-friendly, intuitive syntax)      |   ![alt text](http://progressed.io/bar/0) |
| 15 January 2016      | Implement user permissions and access      |   ![alt text](http://progressed.io/bar/5) |
| 1 February 2016      | Server is live and DB accepts new entries      |   ![alt text](http://progressed.io/bar/5) |

---
## September 1st, 2015
### First data class entry form is functional
#### Current Progress: ![alt text](http://progressed.io/bar/50)
* Develop Device data class entry form
* Link entry form to MongoDB
* Develop Device "search" results form (see Google Drive)
* Receive MongoDB Device entries and feed into results form

### Database mock-up is online
#### Current progress: ![alt text](http://progressed.io/bar/0)
* Discuss server with Josh Jankowski
* Get server online
* Test server access and performance

---
## October 1st, 2015
### Sample, Instrument, and Test data class entry forms are functional
#### Current progress: ![alt text](http://progressed.io/bar/0)
* Develop Sample and Test entry forms
* Develop JSON to HTML form generator
* Link new forms to database
* Develop "search" results views for Sample and Test
* Develop algorithm for receiving MongoDB search results and displaying (Device, Sample, Test)

### HTML-based browse of data is functional
#### Current progress: ![alt text](http://progressed.io/bar/0)
* Develop results view for individual entries
* Include hyperlinks from "results view" to individual entries

---
## October 15th, 2015
### Have a plan for user permissions and access
#### Current progress: ![alt text](http://progressed.io/bar/20)
* Make a plan for user authentication
* Make a plan for allowing new users
* Make a plan for avoiding malicious attacks (for example, sending code snippets in Username)

---
## November 1st, 2015
### HTML-based search of DB is functional (using the most convenient syntax)
#### Current progress: ![alt text](http://progressed.io/bar/0)
* Webpage can communicate search strings (in MongoDB syntax) to server
* Server can respond with accurate results
* Results are displayed according to algorithm developed previously

---
## December 1st, 2015
### HTML-based search of DB is functional (user-friendly, intuitive syntax)
#### Current progress: ![alt text](http://progressed.io/bar/0)
* Find algorithm or existing scripts to convert user-friendly syntax to MongoDB search syntax
* Include booleans (AND, OR, NOT), parentheses, and data field callouts (temperature:240 AND material:PLA)
* Include ability to search on ranges (temperature:[230 to 250])

---
## January 15th, 2016
### Implement user permissions and access
#### Current progress: ![alt text](http://progressed.io/bar/5)
*Users can only modify entries that they created

---
## February 1st, 2016
### Server is live and DB accepts new entries
#### Current progress: ![alt text](http://progressed.io/bar/5)

Additional Features:
---
* Maintainance events are attached to Instrument class
* Auto-suggest existing data fields
* HTML form for advanced search
* Auto fill entry forms from machine result files
