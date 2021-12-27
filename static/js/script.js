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
        console.log(await ajax('POST', '/login', { imageUrl }, json=true));
    } catch (error) {
        if (error.status == 401) { // unauthorized
            username = prompt('NEW USER\nYou have not registered yet.\nPlease enter username to register now')
            await ajax('POST', '/register', { username, imageUrl }, json=true)
        }
    }
};

function ajax(method, url, data, json=False) {
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject({status: this.status, statusText: xhr.statusText});
            }
        };
        xhr.onerror = function () {
            reject({status: this.status, statusText: xhr.statusText});
        };
        if (json) {
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(data));
        } else {
            xhr.send(data)
        }
    });
}