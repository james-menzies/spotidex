sequenceDiagram
participant PlayInfoVM
participant SpotifyAuth
participant Session
participant SpotifyTrack
participant Contexts
participant TerminalWrapper

PlayInfoVM ->> PlayInfoVM: Reset song variables
PlayInfoVM ->> TerminalWrapper: Update "Refreshing..."
PlayInfoVM ->>+ SpotifyAuth: Call song retrieval
SpotifyAuth -->>- PlayInfoVM: Return Spotify Track
opt if song present
    PlayInfoVM ->>+ Session: Query if song already processed.
    Session -->>- PlayInfoVM: return SpotifyTrack
    PlayInfoVM ->>+ SpotifyTrack: generate missing contexts
    SpotifyTrack ->>+ Contexts: Generate data
    Contexts ->> Contexts: Check against cache / make API request
    Contexts -->>- SpotifyTrack: return
    SpotifyTrack -->>- PlayInfoVM: return
    PlayInfoVM ->> PlayInfoVM: expose new variable
end
opt if song not present
    PlayInfoVM ->>+ Session: Query if song already processed.
    Session -->>- PlayInfoVM: return False
    PlayInfoVM ->>+ SpotifyTrack: create (injecting req. contexts)
    SpotifyTrack -->>- PlayInfoVM: return (simalar to above)
    PlayInfoVM ->> PlayInfoVM: expose new variable
end
opt if song same as previous refresh
    PlayInfoVM ->> PlayInfoVM: expose variable as 'None'
end
    PlayInfoVM ->> TerminalWrapper: Update "Updated."
