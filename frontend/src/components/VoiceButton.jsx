import { useState } from "react"
import { API } from "../config"


function VoiceButton() {

    const [listening, setListening] = useState(false)


    function startListening() {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition


        if (!SpeechRecognition) {

            alert("Speech recognition not supported")
            return
        }


        const recognition = new SpeechRecognition()


        recognition.lang = "sl-SI"
        recognition.continuous = false
        recognition.interimResults = false



        recognition.onstart = () => {

            console.log("Listening...")
            setListening(true)

        }


        recognition.onresult = async (event) => {


            const text =
                event.results[0][0].transcript


            console.log("Heard:", text)



            try {

                const response = await fetch(
                    `${API}/voice`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            text: text
                        })
                    }
                )


                const data = await response.json()


                console.log("Assistant:", data)


            }

            catch(error) {

                console.error(error)

            }


        }



        recognition.onerror = (event)=>{

            console.error(
                "Speech error:",
                event.error
            )

        }



        recognition.onend = ()=>{

            setListening(false)

        }


        recognition.start()
        
    }



    return (

        <button
            onClick={startListening}
            style={{
                padding:"15px",
                fontSize:"20px"
            }}
        >

            {
                listening
                ? "🎤 Listening..."
                : "🎤 Voice"
            }

        </button>

    )

}


export default VoiceButton