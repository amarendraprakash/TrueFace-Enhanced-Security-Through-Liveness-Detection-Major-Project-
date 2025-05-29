const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const result = document.getElementById("result");
const context = canvas.getContext("2d");

// Access the user's camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error("Error accessing camera:", err);
    });

// Capture the frame and send to backend
function capture() {
    result.innerText = "Processing...";
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const image = canvas.toDataURL("image/png");

    fetch("/verify_liveness", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: image }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            result.innerText = "✅ " + data.message;
            result.style.color = "green";

            // If liveness is confirmed, store the image and redirect
            localStorage.setItem("capturedImage", image);  // Save image to localStorage
            window.location.href = "/welcome";  // Redirect to welcome page
        } else {
            result.innerText = "❌ " + data.message;
            result.style.color = "red";
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        result.innerText = "❌ Error during verification!";
        result.style.color = "red";
    });
}
