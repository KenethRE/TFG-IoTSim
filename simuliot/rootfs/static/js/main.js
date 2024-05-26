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
                }
            });
        }
    } else {
        window.location.href = "/create_session";
        console.log("No previous session");
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
                console.log(previousSession);
            });
        }
    });

    if (previousSession.length > 0) {
        document.getElementById("continueBtn").style.display = "block";
        document.getElementById("continueBtn").style.visibility = "visible";
    }
}
