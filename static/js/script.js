const webcam = document.getElementById('webcam');
const canvas = document.getElementById('still_photo');
const ctx = canvas.getContext('2d');

(async function() {
    console.log('Capturing webcam...');
    webcam.srcObject = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    webcam.play();
})();

async function login() { 
    console.debug('Drawing webcam photo on canvas...');
    ctx.drawImage(webcam, 0, 0, canvas.width, canvas.height);
    const imageUrl = canvas.toDataURL('image/jpeg');
    try {
        await postJSON('/login', { imageUrl });
        alert('User Logged in!')
    } catch (error) {
        if (error.status == 401) {  // unauthorized
            username = prompt('NEW USER\nYou have not registered yet.\nPlease enter username to register now')
            await postJSON('/register', { username, imageUrl });
        }
    }
};

async function postJSON(url, data) {
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
}