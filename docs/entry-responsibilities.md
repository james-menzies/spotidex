## Entry-VM

An Entry-VM manages the entire main display of the app.

When it is loaded, it:

Looks at the settings to determine which views are being displayed. It has a record of all the dependencies for each view. It instantiates an instance of each view. It will return the primary view and subviews when requested.

The viewmodel will then provide a method for the view to return the data dictionary for the current track. If the information has not changed since the last request, it returns None instead.

The viewmodel is also responsible for keeping track of the position the user is browsing and responding to previous and next requests.

## Entry

Entry is the view counterpart to Entry-VM. Entry instantiates Entry VM and retrieves the primary and sub-views.

It then initially requests the song data from Entry-VM. It then queries



No. 13: Dance of the knights (Act 1)
Romeo and Juliet Op. 64
Sergei Prokofiev
Performed by: Gergiev,
