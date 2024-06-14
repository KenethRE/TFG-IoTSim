let previousSession = [];
function getStarted() {
    if (previousSession.length > 0) {
        // alert user that previous session will be deleted
        if (confirm("Starting a new session will delete the previous session. Do you want to continue?")) {
            fetch("/api/session", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => {
                if (response.ok) {
                    console.log("Previous session deleted");
                    window.location.href = "/create_session";
                }
            });
        }
    } else {
        window.location.href = "/create_session";
    }
}
function checkPreviousSession() {
    // check if there is a previous session
    fetch("/api/session", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => {
        if (response.ok) {
            response.json().then(data => {
                previousSession = data;
                if (data.length > 0) {
                    document.getElementById("continueBtn").style.display = "block";
                    document.getElementById("continueBtn").style.visibility = "visible";
                }
                console.log(previousSession);
            });
        }
    });

}

function previousSessionPage() {
    if (previousSession.length > 0) {
        window.location.href = "/session";
    }
}
