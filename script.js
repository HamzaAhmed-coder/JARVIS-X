// =========================================
// JARVIS X — FRONTEND CONTROLLER
// =========================================

const API_URL = "http://127.0.0.1:8000";


// =========================================
// ELEMENTS
// =========================================

const commandInput = document.getElementById("command-input");
const micButton = document.getElementById("mic-button");

const conversation = document.getElementById("conversation");

const statusText = document.getElementById("status-text");
const statusDot = document.getElementById("status-dot");

let stopButton = document.getElementById("stop-button");


// Agar button HTML mein nahi hai to automatically create karo
if (!stopButton) {

    stopButton = document.createElement("button");

    stopButton.id = "stop-button";

    stopButton.className = "stop-button";

    stopButton.textContent = "■  STOP JARVIS";

    document.body.appendChild(stopButton);

}


// =========================================
// CLOCK
// =========================================

function updateClock() {

    const clock =
        document.getElementById("current-time");

    if (!clock) return;

    const now = new Date();

    clock.textContent =
        now.toLocaleTimeString([], {

            hour: "2-digit",

            minute: "2-digit",

            second: "2-digit"

        });

}

updateClock();

setInterval(
    updateClock,
    1000
);


// =========================================
// CURRENT TIME FOR CHAT
// =========================================

function getMessageTime() {

    return new Date().toLocaleTimeString([], {

        hour: "2-digit",

        minute: "2-digit"

    });

}


// =========================================
// ADD USER MESSAGE
// =========================================

function addUserMessage(message) {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message user-message";

    messageElement.innerHTML = `

        <div class="message-top">

            <span>
                YOU
            </span>

            <time>
                ${getMessageTime()}
            </time>

        </div>

        <p>
            ${escapeHTML(message)}
        </p>

    `;

    conversation.appendChild(
        messageElement
    );

    scrollConversationToBottom();

}


// =========================================
// ADD JARVIS MESSAGE
// =========================================

function addJarvisMessage(message) {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message jarvis-message";

    messageElement.innerHTML = `

        <div class="message-top">

            <span>
                JARVIS
            </span>

            <time>
                ${getMessageTime()}
            </time>

        </div>

        <p>
            ${escapeHTML(message)}
        </p>

    `;

    conversation.appendChild(
        messageElement
    );

    scrollConversationToBottom();


    // Speak JARVIS response

    speakJarvis(message);

}


// =========================================
// ESCAPE HTML
// =========================================

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}


// =========================================
// SCROLL CHAT TO BOTTOM
// =========================================

function scrollConversationToBottom() {

    conversation.scrollTop =
        conversation.scrollHeight;

}


// =========================================
// JARVIS STATUS
// =========================================

function setStatus(
    text,
    active = false
) {

    statusText.textContent =
        text;


    // Remove previous voice states

    document.body.classList.remove(
        "jarvis-listening",
        "jarvis-speaking"
    );


    // LISTENING

    if (
        text === "LISTENING..."
    ) {

        document.body.classList.add(
            "jarvis-listening"
        );

    }


    // SPEAKING

    if (
        text === "SPEAKING..."
    ) {

        document.body.classList.add(
            "jarvis-speaking"
        );

    }


    // Status glow

    if (active) {

        statusDot.style.boxShadow =
            "0 0 18px #00E676";

        statusDot.style.transform =
            "scale(1.2)";

    } else {

        statusDot.style.boxShadow =
            "0 0 10px #00E676";

        statusDot.style.transform =
            "scale(1)";

    }

}


// =========================================
// SEND COMMAND TO BACKEND
// =========================================

async function sendCommand(command) {

    command =
        command.trim();

    if (!command) return;


    // Show user's message

    addUserMessage(
        command
    );


    // Clear input

    commandInput.value =
        "";


    // Change status

    setStatus(
        "THINKING...",
        true
    );


    // Show stop button

    stopButton.classList.add(
        "visible"
    );


    try {

        const response =
            await fetch(

                `${API_URL}/chat`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            message:
                                command

                        })

                }

            );


        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "JARVIS BACKEND RESPONSE:",
            data
        );


        // Get response text

        const reply =
            data.reply ||
            data.response ||
            data.message ||
            "I received your command, sir.";


        // Add response to conversation

        addJarvisMessage(
            reply
        );


        // Update status

        setStatus(
            "READY TO LISTEN",
            false
        );


    } catch (error) {

        console.error(
            "JARVIS CONNECTION ERROR:",
            error
        );


        addJarvisMessage(
            "I'm unable to connect to my backend right now, sir."
        );


        setStatus(
            "BACKEND OFFLINE",
            false
        );


    } finally {

        stopButton.classList.remove(
            "visible"
        );

    }

}


// =========================================
// ENTER KEY
// =========================================

commandInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter"
        ) {

            event.preventDefault();

            sendCommand(
                commandInput.value
            );

        }

    }
);
// =========================================
// STOP BUTTON
// =========================================

stopButton.addEventListener(
    "click",
    function() {

        window.speechSynthesis.cancel();


        setStatus(
            "READY TO LISTEN",
            false
        );


        stopButton.classList.remove(
            "visible"
        );

    }
);


// =========================================
// INITIAL STATUS
// =========================================

setStatus(
    "READY TO LISTEN",
    false
);


// =========================================
// JARVIS TEXT TO SPEECH
// =========================================

let currentSpeech = null;


function speakJarvis(text) {

    // Stop any previous speech

    window.speechSynthesis.cancel();


    if (
        !text ||
        !text.trim()
    ) {

        return;

    }


    currentSpeech =
        new SpeechSynthesisUtterance(
            text
        );


    // JARVIS voice settings

    currentSpeech.lang =
        "en-US";

    currentSpeech.rate =
        0.92;

    currentSpeech.pitch =
        0.82;

    currentSpeech.volume =
        1;


    // When JARVIS starts speaking

    currentSpeech.onstart =
        function() {

            console.log(
                "JARVIS STARTED SPEAKING"
            );


            setStatus(
                "SPEAKING...",
                true
            );


            stopButton.classList.add(
                "visible"
            );

        };


    // When JARVIS finishes speaking

    currentSpeech.onend =
        function() {

            console.log(
                "JARVIS FINISHED SPEAKING"
            );


            setStatus(
                "READY TO LISTEN",
                false
            );


            stopButton.classList.remove(
                "visible"
            );

        };


    // If speech gets cancelled

    currentSpeech.onerror =
        function(event) {

            console.log(
                "Speech error:",
                event.error
            );


            setStatus(
                "READY TO LISTEN",
                false
            );


            stopButton.classList.remove(
                "visible"
            );

        };


    window.speechSynthesis.speak(
        currentSpeech
    );

}


// =========================================
// LIVE SYSTEM STATUS
// =========================================

async function updateSystemStatus() {

    try {

        const response =
            await fetch(
                `${API_URL}/system-status`
            );


        if (!response.ok) {

            throw new Error(
                `System status error: ${response.status}`
            );

        }


        const data =
            await response.json();


        // -----------------------------
        // STATUS TEXT
        // -----------------------------

        const backendStatus =
            document.getElementById(
                "backend-status"
            );

        const voiceStatus =
            document.getElementById(
                "voice-status"
            );

        const aiStatus =
            document.getElementById(
                "ai-status"
            );

        const networkStatus =
            document.getElementById(
                "network-status"
            );

        const powerStatus =
            document.getElementById(
                "power-status"
            );


        if (backendStatus) {

            backendStatus.textContent =
                data.backend;

        }


        if (voiceStatus) {

            voiceStatus.textContent =
                data.voice_system;

        }


        if (aiStatus) {

            aiStatus.textContent =
                data.ai_model;

        }


        if (networkStatus) {

            networkStatus.textContent =
                data.network;

        }


        if (powerStatus) {

            powerStatus.textContent =
                data.power;

        }


        // -----------------------------
        // CPU
        // -----------------------------

        const cpuValue =
            document.getElementById(
                "cpu-value"
            );

        const cpuBar =
            document.getElementById(
                "cpu-bar"
            );


        if (cpuValue) {

            cpuValue.textContent =
                data.cpu + "%";

        }


        if (cpuBar) {

            cpuBar.style.width =
                data.cpu + "%";

        }


        // -----------------------------
        // MEMORY
        // -----------------------------

        const memoryValue =
            document.getElementById(
                "memory-value"
            );

        const memoryBar =
            document.getElementById(
                "memory-bar"
            );


        if (memoryValue) {

            memoryValue.textContent =
                data.memory + "%";

        }


        if (memoryBar) {

            memoryBar.style.width =
                data.memory + "%";

        }


        // -----------------------------
        // DISK
        // -----------------------------

        const diskValue =
            document.getElementById(
                "disk-value"
            );

        const diskBar =
            document.getElementById(
                "disk-bar"
            );


        if (diskValue) {

            diskValue.textContent =
                data.disk + "%";

        }


        if (diskBar) {

            diskBar.style.width =
                data.disk + "%";

        }


        console.log(
            "SYSTEM STATUS UPDATED:",
            data
        );


    } catch (error) {

        console.error(
            "SYSTEM STATUS ERROR:",
            error
        );

    }

}


// First update

updateSystemStatus();


// Update every 5 seconds

setInterval(
    updateSystemStatus,
    5000
);
// =========================================
// JARVIS VOICE RECOGNITION
// =========================================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


let recognition = null;

let isListening = false;

let waitingForCommand = false;

let voiceSessionActive = false;


if (SpeechRecognition) {

    recognition =
        new SpeechRecognition();


    recognition.continuous =
        true;


    recognition.interimResults =
        false;


    recognition.lang =
        "en-US";


    // =====================================
    // MIC BUTTON
    // =====================================

    micButton.addEventListener(
        "click",
        function() {

            console.log(
                "MIC BUTTON CLICKED"
            );


            // If already listening,
            // stop listening

            if (isListening) {

                recognition.stop();

                voiceSessionActive =
                    false;

                waitingForCommand =
                    false;

                return;

            }


            // User explicitly activated
            // voice session

            voiceSessionActive =
                true;

            waitingForCommand =
                false;


            try {

                recognition.start();

            } catch (error) {

                console.log(
                    "Recognition could not start:",
                    error
                );

            }

        }
    );


    // =====================================
    // START LISTENING
    // =====================================

    recognition.onstart =
        function() {

            isListening =
                true;


            micButton.classList.add(
                "active"
            );


            setStatus(
                "READY TO LISTEN",
                true
            );


            console.log(
                "JARVIS MICROPHONE ACTIVE"
            );

        };


    // =====================================
    // SPEECH RESULT
    // =====================================

    recognition.onresult =
        function(event) {


            for (

                let i =
                    event.resultIndex;

                i <
                    event.results.length;

                i++

            ) {


                if (
                    !event.results[i].isFinal
                ) {

                    continue;

                }


                const transcript =
                    event.results[i][0]
                        .transcript
                        .trim();


                const text =
                    transcript.toLowerCase();


                console.log(
                    "YOU SAID:",
                    transcript
                );


                // ---------------------------------
                // VOICE STOP
                // ---------------------------------

                if (

                    text === "stop" ||

                    text.includes(
                        "stop jarvis"
                    ) ||

                    text.includes(
                        "jarvis stop"
                    )

                ) {


                    window.speechSynthesis.cancel();


                    if (stopButton) {

                        stopButton.classList.remove(
                            "visible"
                        );

                    }


                    waitingForCommand =
                        false;


                    setStatus(
                        "READY TO LISTEN",
                        false
                    );


                    continue;

                }


                // ---------------------------------
                // WAKE WORD
                // ---------------------------------

                if (
                    !waitingForCommand
                ) {


                    // Jarvis not detected

                    if (
                        !text.includes(
                            "jarvis"
                        )
                    ) {

                        continue;

                    }


                    // Remove JARVIS
                    // from sentence

                    const command =
                        text
                            .replace(
                                /\bjarvis\b/gi,
                                ""
                            )
                            .trim();


                    console.log(
                        "JARVIS WAKE WORD DETECTED"
                    );


                    setStatus(
                        "LISTENING...",
                        true
                    );


                    // --------------------------------
                    // "Jarvis, open calculator"
                    // --------------------------------

                    if (command) {

                        waitingForCommand =
                            false;


                        commandInput.value =
                            command;


                        sendCommand(
                            command
                        );


                        continue;

                    }


                    // --------------------------------
                    // User only said "Jarvis"
                    // --------------------------------

                    waitingForCommand =
                        true;


                    commandInput.value =
                        "";


                    continue;

                }


                // ---------------------------------
                // COMMAND AFTER "JARVIS"
                // ---------------------------------

                waitingForCommand =
                    false;


                commandInput.value =
                    transcript;


                setStatus(
                    "THINKING...",
                    true
                );


                sendCommand(
                    transcript
                );

            }

        };
            // =====================================
    // END
    // =====================================

    recognition.onend =
        function() {

            isListening =
                false;


            micButton.classList.remove(
                "active"
            );


            console.log(
                "JARVIS MICROPHONE ENDED"
            );


            // Restart only while the user
            // has explicitly activated
            // the voice session.

            if (
                voiceSessionActive
            ) {

                setTimeout(
                    function() {

                        try {

                            recognition.start();

                        } catch (error) {

                            console.log(
                                "Recognition restart skipped."
                            );

                        }

                    },
                    300
                );


            } else {

                setStatus(
                    "READY TO LISTEN",
                    false
                );

            }

        };


    // =====================================
    // ERROR
    // =====================================

    recognition.onerror =
        function(event) {

            console.error(
                "MIC ERROR:",
                event.error
            );


            isListening =
                false;


            micButton.classList.remove(
                "active"
            );


            // Permission denied

            if (

                event.error ===
                    "not-allowed"

                ||

                event.error ===
                    "service-not-allowed"

            ) {

                voiceSessionActive =
                    false;


                waitingForCommand =
                    false;


                setStatus(
                    "MIC PERMISSION DENIED",
                    false
                );


                return;

            }


            // No speech

            if (
                event.error ===
                "no-speech"
            ) {

                setStatus(
                    "READY TO LISTEN",
                    false
                );


                return;

            }


            // Other errors

            setStatus(
                "MIC ERROR",
                false
            );

        };


    console.log(
        "JARVIS VOICE SYSTEM READY - CLICK MIC"
    );


} else {

    console.error(
        "Speech Recognition is not supported by this browser."
    );


    setStatus(
        "VOICE NOT SUPPORTED",
        false
    );

}