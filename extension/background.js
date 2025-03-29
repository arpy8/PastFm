console.log("Background script running...");

function sendURL(url) {
  console.log("Attempting to send URL:", url);
  
  fetch("https://arpy8-pastfm-backend.hf.space/update", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url: url }),
    mode: "cors"
  })
  .then(response => response.json())
  .then(data => {
    // localStorage.setItem("lastSong", data.result);
    console.log("Success:", data);
})
  .catch(error => {
    console.error("Error:", error);
  });
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.url && changeInfo.url.includes("music.youtube.com")) {
    sendURL(changeInfo.url);
  }
});