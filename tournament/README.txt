How to Run the application
	
	In order to sucessfully run the application a postgressql instance is needed to support data storage.
	Application contains 3 files
		tournament.sql - This file contains the DDL for creating the database objects.
		tournament.py - This Module implements various functions that is used to Manage the swiss style Tournamnets.
		tournament_test.py - This module contains few functions that implement few test case scenarios.
	From the command line navigate to the tournament directory.
	Run the Module tournament_test.py by issuing ">python tournament_test.py" command.
	If at the end you get the message "Success!  All tests pass!" then all the functions in tournament.py are working as expected.
