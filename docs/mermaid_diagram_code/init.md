sequenceDiagram
    
    User->>+ MainMenu: Begin Session
    MainMenu ->>+  PlaybackInfo: create
    PlaybackInfo ->>+ PlaybackInfoVM: create
    PlaybackInfoVM -->>- PlaybackInfo: return
    PlaybackInfo ->>+ PlaybackInfoVM: get Subviews
    PlaybackInfoVM -->>- PlaybackInfo: return
    Note left of PlaybackInfo: Widgets and callbacks created
    PlaybackInfo -->>- MainMenu: return
    MainMenu ->> TerminalWrapper: Change Scene