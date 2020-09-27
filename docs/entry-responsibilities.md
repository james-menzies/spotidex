## Entry-VM

An Entry-VM manages the entire main display of the app.

When it is loaded, it:

Looks at the settings to determine which views are being displayed. It has a record of all the dependencies for each view. It instantiates an instance of each view.

The view will query the viewmodel for the views.

The viewmodel will then provide a method for the view to return the data dictionary for the current track. If the information has not changed since the last request, it returns None instead.

