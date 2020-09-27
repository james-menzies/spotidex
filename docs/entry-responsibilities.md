## Entry-VM

An Entry-VM manages the entire main display of the app.

When it is loaded, it:

Looks at the settings to determine which views are being displayed. It has a record of all the dependencies for each view.

It then instantiates an instance of all of these views.

It then loads the current song and exposes that variable.



The view will call the get_views method, and the entry_vm will return them.

The entry will provide an update method, which will


It then queries the session to see if there was a previous match, if so, it loads it in and makes sure that all of its dependencies are loaded.

