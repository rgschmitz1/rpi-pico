const sendHttpRequest = (method, url, data) => {
  const promise = new Promise((resolve, reject) => {
    const xhttp = new XMLHttpRequest();
    xhttp.open(method, url);
    if (data) {
      xhttp.setRequestHeader('Content-Type', 'application/json');
    }
    xhttp.onload = () => {
      if (xhttp.status <= 400) {
        resolve(xhttp.response);
      } else {
        reject(xhttp.response);
      }
    };
    xhttp.onerror = () => {
      reject('Something went wrong!');
    };
    xhttp.send(JSON.stringify(data));
  });
  return promise;
};

const toggleRpiLED = () => {
  let rpi_led_state = document.getElementById('rpi_led').innerHTML;
  rpi_led_state = rpi_led_state === 'ON' ? 'OFF' : 'ON'
  sendHttpRequest('POST', '/led', {state: rpi_led_state})
    .then(() => {
      document.getElementById('rpi_led').innerHTML = rpi_led_state;
    })
    .catch(err => {
      console.log('ERR: ' + err);
    });
};

const getRpiTemp = () => {
  sendHttpRequest('GET', '/temp')
    .then(responseData => {
      document.getElementById('rpi_temp').innerHTML = responseData;
    })
    .catch(err => {
      console.log('ERR: ' + err);
    });
};

// Get Raspberry Pi Pico temperature every 10 seconds
setInterval(getRpiTemp, 10000);
