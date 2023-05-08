const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture-button');

      // Get webcam stream and start playing video
navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
.then(stream => 
    {
        video.srcObject = stream;
        video.play();
    }
).catch(err => 
    {
    console.error('Error accessing camera:', err);
    }
);

// Capture image when button is clicked
captureButton.addEventListener('click', () => 
    {
        // Draw video frame on canvas
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert canvas to image data and display in new window
        const dataURL = canvas.toDataURL();
        const imageWindow = window.open();
        imageWindow.document.write(`<img src="${dataURL}" />`);
    }
);

      // Enable capture button when video starts playing
video.addEventListener('playing', () => {
        captureButton.classList.add('enabled');
});