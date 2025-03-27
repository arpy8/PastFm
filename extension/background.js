function sendURL() {

}


chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url && changeInfo.url.includes("music.youtube.com")) {
        
        
        chrome.runtime.sendMessage({
            type: 'TAB_URL_CHANGED',
            tabId: tabId,
            url: changeInfo.url
        });
    }
});