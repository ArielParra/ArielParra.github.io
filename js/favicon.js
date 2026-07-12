/**
 * @description Changes the website favicon dynamically by replacing the existing favicon with a new one.
 *
 * @param {string} src - The source URL of the new favicon.
 */
function changeFavicon(src) {
  const head = document.head || document.getElementsByTagName("head")[0];
  const link = document.createElement("link");
  const oldLink = document.getElementById("dynamic-favicon");
  link.id = "dynamic-favicon";
  link.rel = "icon";
  link.href = String(src).trim();
  link.type = "image/png";
  if (oldLink) {
    head.removeChild(oldLink);
  }
  head.appendChild(link);
}

/**
 * @description Animates the website favicon by toggling between two frames.
 *                The frames are two different favicon images encoded in base64.
 */
function animateFavicon() {
  if (typeof animateFavicon.i === "undefined") {
    animateFavicon.i = 0;
  }
  if (animateFavicon.i === 0) {
    // frame 1
    changeFavicon("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAD1BMVEUAAADZ3unZ3umBocEAAABzlIVGAAAABXRSTlMA/////xzQJlIAAABcSURBVDiN1ZFZCgAgCETD6f5n7qNFXIjECJqfZHwNoqW8EoC9kQek5XTzAByFAaJaR6uX+rsBOGS6RFDlEeCNJ0Y1DgctQOYsYGwsDnC4ArzL3AHUwvk1ygM/qwF3cQR0OcerjwAAAABJRU5ErkJggg==");
  } else { // could be a switch if I had more frames
    // frame 2
    changeFavicon("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAD1BMVEUAAADZ3unZ3umBocEAAABzlIVGAAAABXRSTlMA/////xzQJlIAAABXSURBVDiN1ZJbCgAgCAQlvf+ZC4rcHkZhBM3Xsg6FEdErmHldeISawGm6WwJPOBZCooxyVAHbPoIgUluIJ4JBK8DdsAvZgj7crjA73/8fdoRh2td+4X8itwsEqgbpVBgAAAAASUVORK5CYII=");
  }
  animateFavicon.i++;
  if (animateFavicon.i === 2) {
    animateFavicon.i = 0;
  }
}
document.addEventListener("DOMContentLoaded", () => {
  const ua = navigator.userAgent;
  const isFirefox = ua.toLowerCase().indexOf("firefox") !== -1;
  if (!isFirefox) {
    // For Chromium/webkit or other browsers that do not support gif as favicons
    setInterval(animateFavicon, 800);
  } else {
    // For Firefox
    const link = document.createElement("link");
    link.rel = "icon";
    link.href = "./img/favicon.gif";
    link.type = "image/gif";
    document.head.appendChild(link);
  }
});
