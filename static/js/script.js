const webcam = document.getElementById('webcam');
const canvas = document.getElementById('still_photo');
const ctx = canvas.getContext('2d');

(async function() {
    console.log('Capturing webcam...');
    webcam.srcObject = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    webcam.play();
})();

async function takePic() { 
    console.debug('Drawing webcam photo on canvas...');
    ctx.drawImage(webcam, 0, 0, canvas.width, canvas.height);
    await sendJsonAjax('POST', '/login', { imageUrl: canvas.toDataURL('image/png') });
};

function sendJsonAjax(method, url, data) {
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
        xhr.setRequestHeader('Content-Type', 'application/json')
        xhr.send(JSON.stringify(data));
    });
}