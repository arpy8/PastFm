chrome.runtime.onMessage.addListener((message) => {
    document.getElementById("song").textContent = message.song || "No song playing";
    document.getElementById("artist").textContent = message.artist || "Unknown artist";
});

// Get stored song data when popup opens
chrome.storage.local.get(['currentSong'], function(result) {
    if (result.currentSong) {
        document.getElementById("song").textContent = result.currentSong.song || "No song playing";
        document.getElementById("artist").textContent = result.currentSong.artist || "Unknown artist";
    }
});

// Query current tab on popup open
chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    const currentTab = tabs[0];
    if (currentTab.url.includes("music.youtube.com")) {
        chrome.scripting.executeScript({
            target: { tabId: currentTab.id },
            func: () => {
                const songName = document.querySelector('.title.style-scope.ytmusic-player-bar').textContent;
                let formatted_string = document.querySelector('.byline.style-scope.ytmusic-player-bar').textContent;
                formatted_string = formatted_string.split("•"); 
                
                return { song: songName, artist: formatted_string[0], views: formatted_string[1], likes: formatted_string[2] };
            }
        }, (results) => {
            if (results && results[0]) {
                const songInfo = results[0].result;
                document.getElementById("song").textContent = songInfo.song;
                document.getElementById("artist").textContent = songInfo.artist;
                document.getElementById("views").textContent = songInfo.views;
                document.getElementById("likes").textContent = songInfo.likes;
            }
        });
    }
});