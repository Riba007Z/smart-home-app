import { useEffect, useState } from "react"
import DeviceButton from "./components/DeviceButton"
import VoiceButton from "./components/VoiceButton"
import { API, WS } from "./config"


function App() {

  const [devices, setDevices] = useState([])
  const [states, setStates] = useState({})


  useEffect(() => {

    const ws = new WebSocket(
      WS //later chand to host/device ip
    )

    ws.onmessage = (event)=>{

      const data = JSON.parse(
        event.data
      )

      setStates(prev => ({
        ...prev,
        [data.address]: data.value
      }))

    }

    return ()=>{
      ws.close()
    }


  }, [])


  useEffect(() => {
    fetch(`${API}/states`)
      .then(response => response.json())
      .then(data => {
        console.log("STATES:", data)
        setStates(data)
      })
      .catch(error => console.error(error))
  }, [])


  useEffect(() => {

    fetch(`${API}/devices`)
      .then(response => response.json())
      .then(data => {
        console.log("DEVICES:", data)
        setDevices(data)
      })
      .catch(error => console.error(error))

      /*fetch(`${API}/devices`)
      .then(async (response) => {
        const text = await response.text()

        alert(text)          // Shows exactly what the iPhone received

        return JSON.parse(text)
      })
      .then(data => {
        alert("Length: " + data.length)
        setDevices(data)
      })
      .catch(error => {
        alert(error.toString())
        console.error(error)
      })*/

  }, [])


  function toggleDevice(device) {

    const current =
      states[device.statusAddress] ?? false

    const next = !current


    fetch(`${API}/device`, {
      method: "POST",
      headers:{
        "Content-Type":"application/json"
      },
      body: JSON.stringify({
        address: device.groupAddress,
        value: next
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log("KNX response:", data)
    })
    .catch(error => console.error(error))


    // optimistic update
    setStates(prev => ({
      ...prev,
      [device.statusAddress]: next
    }))
  }

  function groupByRoom(devices) {
    return devices.reduce((groups, device) => {

      const room = device.room || "unknown"

      if (!groups[room]) {
        groups[room] = []
      }

      groups[room].push(device)

      return groups

    }, {})
  }

  const rooms = groupByRoom(devices)


  return (
    <div
      style={{
        padding: "20px"
      }}
    >

      <h1>Smart Home</h1> <VoiceButton />

      {/*
      <div style={{ color: "red" }}>
        Devices loaded: {devices.length}
      </div>
      */}

      {
        Object.entries(rooms).map(([room, roomDevices]) => (

          <div
            key={room}
            style={{
              marginBottom: "40px"
            }}
          >

            <h2
              style={{
                marginBottom: "15px"
              }}
            >
              {room}
            </h2>

            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "15px",
                justifyContent: "flex-start"
              }}
            >

              {
                roomDevices.map(device => (

                  <DeviceButton
                      key={device.id}
                      device={device}
                      state={states[device.statusAddress]}
                      onToggle={toggleDevice}
                  />

                ))
              }

            </div>

          </div>

        ))
      }

    </div>
  )
}


export default App