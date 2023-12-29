/* Forked from: https://github.com/MaxHalford/procedural-art/blob/master/3_unknown_pleasures.html 

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
    var sum = 0;
    for (var i = 0; i < 6; i += 1) {
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
    var sigma2 = Math.pow(sigma, 2);
    var numerator = Math.exp(-Math.pow((x - mu), 2) / (2 * sigma2));
    var denominator = Math.sqrt(2 * Math.PI * sigma2);
    return numerator / denominator;
}

/**
 * @description Exports the SVG content to an SVG file with the filename "JoyDivision.svg".
 */
function exportSVG(button) {
    button.disabled = true;
    var svg = document.getElementById('JoyDivision');

    // Clone the SVG to avoid modifying the original
    var clonedSvg = svg.cloneNode(true);

    // Get the computed styles for the root element
    var computedStyles = getComputedStyle(document.documentElement);

    // Replace CSS variables in the SVG content
    clonedSvg.innerHTML = clonedSvg.innerHTML.replace(/var\(--HTML_BG\)/g, computedStyles.getPropertyValue('--HTML_BG'));
    clonedSvg.innerHTML = clonedSvg.innerHTML.replace(/var\(--text\)/g, computedStyles.getPropertyValue('--text'));

    var svgContent = new XMLSerializer().serializeToString(clonedSvg);
    var blob = new Blob([svgContent], { type: 'image/svg+xml;charset=utf-8' });

    // Create a direct download link for the button
    button.href = URL.createObjectURL(blob);
    button.target = '_blank';
    button.download = 'JoyDivision.svg';

    // Enable the button after a short delay
    setTimeout(function () {
        button.disabled = false;
    }, 500);
}

/**
 * @description Main function to generate and display the Joy Division-inspired SVG.
 */
function main(){
    var svg = document.getElementById('JoyDivision');
    var linesGroup = document.getElementById('lines');

    // Determine x and y range
    var xMin = 140;
    var xMax = svg.getBoundingClientRect().width - xMin;
    var yMin = 100;
    var yMax = svg.getBoundingClientRect().height - yMin;

    // Determine the number of lines and the number of points per line
    var nLines = 80;
    var nPoints = 80;

    var mx = (xMin + xMax) / 2;
    var dx = (xMax - xMin) / nPoints;
    var dy = (yMax - yMin) / nLines;

    var x = xMin;
    var y = yMin;

    for (var i = 0; i < nLines; i++) {
    var linePath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    var pathData = '';

    var nModes = randInt(1, 4);
    var mus = [];
    var sigmas = [];

    for (var j = 0; j < nModes; j++) {
        mus[j] = rand(mx - 50, mx + 50);
        sigmas[j] = randNormal(24, 30);
    }

    var w = y;

    for (var k = 0; k < nPoints; k++) {
        x = x + dx;
        var noise = 0;

        for (var l = 0; l < nModes; l++) {
        noise += normalPDF(x, mus[l], sigmas[l]);
        }

        var yy = 0.3 * w + 0.7 * (y - 600 * noise + noise * Math.random() * 200 + Math.random());
        pathData += (k === 0 ? 'M' : 'L') + x + ' ' + yy;
        w = yy;
    }

    linePath.setAttribute('d', pathData);
    linesGroup.appendChild(linePath);

    x = xMin;
    y = y + dy;
    }

}main();
