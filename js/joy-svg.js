// joy-svg.js an Unknown Pleasures style svg generator, Forked from: https://github.com/MaxHalford/procedural-art/blob/master/3_unknown_pleasures.html
/*
The MIT License (MIT)

Copyright (c) 2016 Max Halford

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

/**
 * @description Generates a random floating-point number within the specified range.
 *
 * @param {number} min - The minimum value of the range.
 * @param {number} max - The maximum value of the range.
 * @returns {number} A random floating-point number within the specified range.
 */
function rand(min, max) {
  return Math.random() * (max - min) + min;
}

/**
 * @description Generates a random integer within the specified range.
 *
 * @param {number} min - The minimum value of the range.
 * @param {number} max - The maximum value of the range.
 * @returns {number} A random integer within the specified range.
 */
function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * @description Generates a random number from a normal distribution.
 *
 * @param {number} mu    - The mean of the normal distribution.
 * @param {number} sigma - The standard deviation of the normal distribution.
 * @returns {number} A random number from a normal distribution.
 */
function randNormal(mu, sigma) {
  let sum = 0;
  for (let i = 0; i < 6; i += 1) {
    sum += rand(-1, 1);
  }
  return mu + sigma * sum / 6;
}

/**
 * @description Calculates the probability density function (PDF) of a normal distribution.
 *
 * @param {number} x     - The value at which to calculate the PDF.
 * @param {number} mu    - The mean of the normal distribution.
 * @param {number} sigma - The standard deviation of the normal distribution.
 * @returns {number} The PDF value at the specified point.
 */
function normalPDF(x, mu, sigma) {
  const sigma2 = sigma ** 2;
  const numerator = Math.exp(-((x - mu) ** 2) / (2 * sigma2));
  const denominator = Math.sqrt(2 * Math.PI * sigma2);
  return numerator / denominator;
}

/**
 * @description Exports the SVG content to an SVG file with the filename "unknownPleasures.svg".
 */
function exportSVG(button) {
  button.disabled = true;

  const svg = document.getElementById("unknownPleasures");

  // Clone the SVG to avoid modifying the original
  const clonedSvg = svg.cloneNode(true);

  // Get the computed styles for the root element
  const computedStyles = getComputedStyle(document.documentElement);

  // Replace CSS variables in the SVG content
  clonedSvg.innerHTML = clonedSvg.innerHTML.replace(/var\(--html-bg\)/g, computedStyles.getPropertyValue("--html-bg"));
  clonedSvg.innerHTML = clonedSvg.innerHTML.replace(/var\(--text\)/g, computedStyles.getPropertyValue("--text"));

  const svgContent = new XMLSerializer().serializeToString(clonedSvg);
  const blob = new Blob([svgContent], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);

  // Create a temporary anchor element and trigger a click to download the SVG
  const a = document.createElement("a");
  a.href = url;
  a.download = "unknownPleasures.svg";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  // Enable the button after a short delay
  setTimeout(() => {
    button.disabled = false;
  }, 500);
}

/**
 * @description Main function to generate and display the Joy Division Unkown Pleasures inspired SVG.
 */
function displaySVG() {
  const svg = document.getElementById("unknownPleasures");
  const linesGroup = document.getElementById("lines");

  // Determine x and y range
  const xMin = 140;
  const xMax = svg.getBoundingClientRect().width - xMin;
  const yMin = 100;
  const yMax = svg.getBoundingClientRect().height - yMin;

  // Determine the number of lines and the number of points per line
  const nLines = 80;
  const nPoints = 80;

  const mx = (xMin + xMax) / 2;
  const dx = (xMax - xMin) / nPoints;
  const dy = (yMax - yMin) / nLines;

  let x = xMin;
  let y = yMin;

  for (let i = 0; i < nLines; i++) {
    const linePath = document.createElementNS("http://www.w3.org/2000/svg", "path");
    let pathData = "";

    const nModes = randInt(1, 4);
    const mus = [];
    const sigmas = [];

    for (let j = 0; j < nModes; j++) {
      mus[j] = rand(mx - 50, mx + 50);
      sigmas[j] = randNormal(24, 30);
    }

    let w = y;

    for (let k = 0; k < nPoints; k++) {
      x += dx;
      let noise = 0;

      for (let l = 0; l < nModes; l++) {
        noise += normalPDF(x, mus[l], sigmas[l]);
      }

      const yy = 0.3 * w + 0.7 * (y - 600 * noise + noise * Math.random() * 200 + Math.random());
      pathData += `${(k === 0 ? "M" : "L") + x} ${yy}`;
      w = yy;
    }

    linePath.setAttribute("d", pathData);
    linesGroup.appendChild(linePath);

    x = xMin;
    y += dy;
  }
}

/**
 * @description  Initializes the SVG display.
 */
document.addEventListener("DOMContentLoaded", () => {
  displaySVG();
  
  const btnSVG = document.getElementById("exportSVG");
  if (btnSVG) {
    btnSVG.addEventListener("click", function() { exportSVG(this); });
  }

  const btnPNG = document.getElementById("exportPNG");
  if (btnPNG) {
    btnPNG.addEventListener("click", function() { exportPNG(this); });
  }
});

/**
 * @description Exports the SVG content to a PNG file with the filename "unknownPleasures.png".
 */
function exportPNG(button) {
  button.disabled = true;

  const svg = document.getElementById("unknownPleasures");

  // Clone the SVG to avoid modifying the original
  const clonedSvg = svg.cloneNode(true);

  // Get the computed styles for the root element
  const computedStyles = getComputedStyle(document.documentElement);

  // Replace CSS variables in the SVG content
  clonedSvg.innerHTML = clonedSvg.innerHTML.replace(/var\(--html-bg\)/g, computedStyles.getPropertyValue("--html-bg"));
  clonedSvg.innerHTML = clonedSvg.innerHTML.replace(/var\(--text\)/g, computedStyles.getPropertyValue("--text"));

  const svgContent = new XMLSerializer().serializeToString(clonedSvg);
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  const svgBlob = new Blob([svgContent], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(svgBlob);

  const image = new Image();
  image.onload = function () {
    canvas.width = image.width;
    canvas.height = image.height;
    ctx.drawImage(image, 0, 0);

    URL.revokeObjectURL(url);

    // Create a temporary anchor element and trigger a click to download the PNG
    const a = document.createElement("a");
    a.href = canvas.toDataURL("image/png");
    a.download = "unknownPleasures.png";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    // Enable the button after a short delay
    setTimeout(() => {
      button.disabled = false;
    }, 500);
  };
  image.src = url;
}
