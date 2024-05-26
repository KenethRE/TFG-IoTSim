
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}
function dropClone(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data).cloneNode(true));
}
function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}
function allowDrop(ev) {
    ev.preventDefault();
}
function addCardBlock() {
            if (document.getElementById("room_name").value == "" || document.getElementById("room_name").value == null || document.getElementById("room_name").value == undefined || document.getElementById("room_name").value == " "){
                document.getElementById("room_name").style.border = "1px solid red";
                return;
            }
            // check for repeated room names
            var rooms = document.getElementById("rooms").children;
            for (var i = 0; i < rooms.length; i++){
                if (rooms[i].children[0].children[0].textContent == document.getElementById("room_name").value){
                    alert("Room name already exists");
                    return;
                }
            }
            if (document.getElementById("rooms").children.length >= 6){
                alert("You can only have 6 rooms");
                return;
            }
            var newCardBlock = document.createElement("div");
            newCardBlock.className = "col-md-6";

            var card = document.createElement("div");
            card.className = "card";

            var cardHeader = document.createElement("div");
            cardHeader.className = "card-header";

            var cardTitle = document.createElement("h4");
            cardTitle.className = "card-header-text";
            cardTitle.style.fontWeight = "bolder";
            cardTitle.textContent = document.getElementById("room_name").value;
            document.getElementById("room_name").value = "";

            var cardBlock = document.createElement("div");
            cardBlock.className = "card-block";
            cardBlock.ondragover = allowDrop;
            cardBlock.ondrop = dropClone;
            cardBlock.style.height = "200px";
            cardBlock.style.overflow = "auto";
            cardBlock.style.border = "1px solid #000";

            cardHeader.appendChild(cardTitle);
            newCardBlock.appendChild(cardHeader);
            newCardBlock.appendChild(cardBlock);

            document.getElementById("rooms").appendChild(newCardBlock);
}
document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        addCardBlock();
    }
});

function getDevices() {
    fetch("/api/devices", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => {
        if (response.ok) {
            response.json().then(data => {
                for (var i = 0; i < data.length; i++){
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
    newDevice.draggable = "true";
    newDevice.ondragstart = drag;

    var deviceHeader = document.createElement("div");
    deviceHeader.className = "card-header";

    var deviceTitle = document.createElement("h5");
    deviceTitle.className = "card-header-text";
    deviceTitle.textContent = device.name;

    var deviceBody = document.createElement("div");
    deviceBody.className = "material-symbols-outlined";
    deviceBody.textContent = convertTypeToIcon(device.type);

    var deviceType = document.createElement("p");
    deviceType.id = device.id + "_type";
    deviceType.textContent = "Type: " + device.type;
    deviceType.style.display = "none";

    deviceHeader.appendChild(deviceTitle);
    newDevice.appendChild(deviceHeader);
    newDevice.appendChild(deviceBody);
    newDevice.appendChild(deviceType);

    // divide devices into sensors and switches
    if (device.type == "Switch" || device.type == "Thermo_Switch") {
        document.getElementById("switches").appendChild(newDevice);
        return;
    } else if (device.type == "Thermometer" || device.type == "Water_Flow" || device.type == "Air_Flow" || device.type == "US_Sensor" || device.type == "Volume_Sensor") {
        document.getElementById("sensors").appendChild(newDevice);
        return;
    }
}

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
// post all data from all rooms when clicking Save
function saveData() {
    var rooms = document.getElementById("rooms").children;
    var data = [];
    for (var i = 0; i < rooms.length; i++){
        var room = rooms[i];
        var devices = room.children[1].children;
        for (var j = 0; j < devices.length; j++){
            data.push({
                Location: room.children[0].children[0].textContent,
                DeviceID: devices[j].id,
                Name: devices[j].children[0].children[0].textContent,
                Type: devices[j].children[2].textContent.split(": ")[1],
            });
        }
    }
    fetch("/api/session", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
            "Content-Type": "application/json"
        },
        credentials: "same-origin",
})
.then(response => {
    console.log(response);
    if (response.ok) {
        window.location.href = "/session";
    }
})
.catch((error) => {
    console.error("Error:", error);
});
}
function deleteCardBlock() {
    var rooms = document.getElementById("rooms").children;
    if (rooms.length == 0){
        return;
    }
    document.getElementById("rooms").removeChild(rooms[rooms.length - 1]);
}