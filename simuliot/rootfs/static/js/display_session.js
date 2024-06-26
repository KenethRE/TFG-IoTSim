function convertTypeToIcon(type) {
    switch (type) {
        case 'Thermometer':
            return 'thermometer'
        case 'Water_Flow':
            return 'water'
        case 'Air_Flow':
            return 'air'
        case 'US_Sensor':
            return 'sensors'
        case 'Switch':
            return 'switch'
        case 'Hub':
            return 'router'
        case 'Switch_Config':
            return 'tune'
        case 'Thermo_Config':
            return 'nest_thermostat'
        case 'Thermo_Switch':
            return 'switch'
        case 'Volume_Sensor':
            return 'brand_awareness'
    }
}

function loadDeviceSession() {
    fetch("/api/session", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => {
        if (response.ok) {
            response.json().then(data => {
                for (var i = 0; i < data.length; i++){
                    console.log(data[i]);
                    addDevice(data[i]);
                }
            });
        }
    });
}

function addDevice(device) {
    var newDevice = document.createElement("div");
    newDevice.className = "card";
    newDevice.id = device.id;

    var deviceHeader = document.createElement("div");
    deviceHeader.className = "card-header";

    var deviceTitle = document.createElement("h5");
    deviceTitle.className = "card-header-text";
    deviceTitle.textContent = device.Name;

    var deviceLocation = document.createElement("p");
    deviceLocation.className = "card-header-text";
    deviceLocation.textContent = "Location: " + device.Location;

    var deviceValue = document.createElement("input");
    deviceValue.className = "card-header-text";
    deviceValue.id = device.id + "_val";
    deviceValue.type = "text";
    deviceValue.placeholder = "Enter value";
    deviceValue.style.width = "50%";
    deviceValue.style.margin = "10px";

    var deviceUpdate = document.createElement("button");
    deviceUpdate.className = "btn btn-primary";
    deviceUpdate.textContent = "Update";
    deviceUpdate.onclick = function () { UpdateDeviceValue(device.DeviceID); };

    var deviceBody = document.createElement("div");
    deviceBody.className = "material-symbols-outlined";
    deviceBody.textContent = convertTypeToIcon(device.Type);

    deviceHeader.appendChild(deviceTitle);
    deviceHeader.appendChild(deviceLocation);
    deviceHeader.appendChild(deviceValue);
    deviceHeader.appendChild(deviceUpdate);
    newDevice.appendChild(deviceHeader);
    newDevice.appendChild(deviceBody);

    //add them to the session div
    document.getElementById("session").appendChild(newDevice);
}

function terminateSession() {
    if (confirm("Are you sure you want to terminate the session? You will be redirected to the main menu.")) {
        $.ajax({
            type: "GET",
            url: "/api/kill-session",
            success: function(response) {
                window.location.reload();
            }
        });
    }
}
function startSession() {
    if (confirm("All devices will start publishing. Are you sure you want to continue?")) {
        fetch('/start_session', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            }
        }).then(response => {
            if (response.ok) {
                window.location.href = "{% url 'display_session' %}";
            } else {
                alert("Error starting session.");
            }
        });
    }
}
function UpdateDeviceValue(id) {
    id_val = id + "_val";
    var value = document.getElementById(id_val).value;
    var deviceID = id;
    console.log(value + " " + deviceID);
    fetch('/update_device_value', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            'value': value,
            'deviceID': deviceID
        })
    }).then(response => {
        if (response.ok) {
            alert("Device value updated.");
        } else {
            alert("Error updating device value.");
        }
    });
}

function UpdateDeviceValue(deviceID) {
    var value = document.getElementById(deviceID + "_val").value;
    $.ajax({
        type: "POST",
        url: "/api/update_device_value",
        data: {
            'deviceID': deviceID,
            'value': value
        },
        success: function(response) {
            location.reload();
        }
    });
}

function startSession() {
    $.ajax({
        type: "POST",
        url: "/api/start_session",
        success: function(response) {
            location.reload();
        }
    });
}