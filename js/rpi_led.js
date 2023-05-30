let state = document.getElementById("led_state").innerHTML;
let endpoint = "/led/".concat(state === "ON" ? "off" : "on");

function toggleLED() {
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && (this.status == 200 || this.status == 0)) {
      endpoint = "/led/" + state.toLowerCase();
      state = state === "ON" ? "OFF" : "ON";
      document.getElementById("led_state").innerHTML = state;
    }
  };
  xhttp.open("POST", endpoint);
  xhttp.send();
}