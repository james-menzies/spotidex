sequenceDiagram

    User ->>+ PlaybackInfo: Refresh Page
    PlaybackInfo ->> TerminalWrapper: run task
    Note over PlaybackInfo, TerminalWrapper: Passes function from PlaybackInfoVM
    PlaybackInfo ->> PlaybackInfo: Receives update
    PlaybackInfo ->> TerminalWrapper: Flashes messages
    opt If update required    
        PlaybackInfo ->>+ SubView: Requests new widget
        SubView -->>- PlaybackInfo: return
        PlaybackInfo ->>- PlaybackInfo: updates Frame
    end