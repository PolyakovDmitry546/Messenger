const searchResultDiv = document.querySelector("#searchResultDiv")
const searchInput = document.querySelector("#searchInput")
const searchPanelDiv = document.querySelector("#searchPanelDiv")
const channelsPanelDiv = document.querySelector("#channelsPanelDiv")
const backFromSearchButton = document.querySelector("#backFromSearchButton")

async function getSerchResult(q) {
    var url = searchInput.dataset.url;
    url += `?q=${q}`;
    const response = await fetch(url);
    return response.json();
}

function showSearchResult(result) {
    if (result.users.length > 0) {
        searchResultDiv.append(document.createElement('h2').innerText = "Users");
        searchResultDiv.append(document.createElement('br'));
        for (var i in result.users) {
            var link = document.createElement('a');
            link.innerHTML = result.users[i].username;
            searchResultDiv.append(link);
            searchResultDiv.append(document.createElement('br'));
        }
    }
    if (result.channels.length > 0) {
        searchResultDiv.append(document.createElement('h2').innerText = "Channels");
        searchResultDiv.append(document.createElement('br'));
        for (var i in result.channels) {
            var link = document.createElement('a');
            link.href = result.channels[i].url;
            link.innerHTML = result.channels[i].name;
            searchResultDiv.append(link);
            searchResultDiv.append(document.createElement('br'));
        }
    }
}

function CleanPreviosSearchResult() {
    searchResultDiv.innerHTML = '';
}

var throttleTimer;
var timerId;
const throttle = (callback, time) => {
    if (throttleTimer) {
        clearTimeout(timerId);
        timerId = setTimeout(() => {
            callback();
            throttleTimer = false;
        }, time);
        return;
    };
    throttleTimer = true;
    timerId = setTimeout(() => {
        callback();
        throttleTimer = false;
    }, time)
}

const handleSearchOnkeyup = () => {
    throttle(async () => {
        console.log("trot");
        var value = searchInput.value;
        const responseData = await getSerchResult(value);
        CleanPreviosSearchResult();
        showSearchResult(responseData);
    }, 500)
}

searchInput.onkeyup = handleSearchOnkeyup

searchInput.onclick = function(e) {
    if (searchPanelDiv.getAttribute("hidden")) {
        channelsPanelDiv.setAttribute("hidden", "hidden");
        searchPanelDiv.removeAttribute("hidden");
        CleanPreviosSearchResult();
    }
};

backFromSearchButton.onclick = function(e) {
    searchPanelDiv.setAttribute("hidden", "hidden");
    searchInput.value = "";
    channelsPanelDiv.removeAttribute("hidden");
};