// Upload File
async function uploadFile() {

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/upload/", {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    document.getElementById("uploadStatus").innerText = result.message;
}


// Ask Question
async function askQuestion() {

    const input = document.getElementById("questionInput");
    const question = input.value;

    console.log("QUESTION:", question);

    if (!question) return;

    addMessage("You", question, "user");

    try {

        const response = await fetch("/query/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question })
        });

        console.log("RESPONSE:", response);

        const result = await response.json();

        console.log("RESULT:", result);

        addMessage("Bot", result.answer || "No response received", "bot");

    } catch (error) {

        console.error("ERROR:", error);

    }

    input.value = "";
}

// Chat Message Renderer
function addMessage(sender, text, type) {

    const chatBox = document.getElementById("chatBox");

    const message = document.createElement("div");
    message.className = "message " + type;

    message.innerHTML = "<strong>" + sender + ":</strong> " + text;

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}