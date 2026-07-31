function getIcon(device) {

  switch (device.type) {

    case "lightOnOff": //set value on official host/device -> type
      return "💡"

    case "fan":
      return "🌀"

    case "socket":
      return "🔌"

    default:
      return "❓"
  }
}


function DeviceButton({ device, state, onToggle }) {

  const isOn = state === true


  return (
    <button
      onClick={() => onToggle(device)}
      style={{
        width: "150px",
        height: "150px",
        margin: "10px",
        fontSize: "20px",
        color: "#222",
        backgroundColor: isOn ? "#ffd966" : "#555",
        border: "none",
        borderRadius: "12px",
        cursor: "pointer",
      }}
    >

      <div style={{fontSize:"40px"}}>
        {getIcon(device)}
      </div>

      <div>
        {device.name}
      </div>

      <div>
        {isOn ? "ON" : "OFF"}
      </div>

    </button>
  )
}

export default DeviceButton