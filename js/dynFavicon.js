function changeFavicon(src) {
    const head = document.head || document.getElementsByTagName('head')[0];
    var link  = document.createElement('link'),
    oldLink   = document.getElementById('dynamic-favicon');
    link.id   = 'dynamic-favicon';
    link.rel  = 'icon';
    link.href = src;
    if (oldLink) {
        head.removeChild(oldLink);
    }
    head.appendChild(link);
}

function animateIcon() {
    if (typeof animateIcon.i === 'undefined') {
        animateIcon.i = 0;
    }
    if (animateIcon.i === 0) {
        //frame 1
        changeFavicon("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAADFBMVEUAAAAAAADZ3unZ3unZXwkJAAAABHRSTlMA////sy1AiAAAAERJREFUOI1jYKAXYGJiwi9AuQJUISyylCtgwgKoqQDOR5JCUUOhAmy2o7iEGAW4fUFlBdhihjoKMAIc7gDsMU6JgqEMAB8UAuUEOK/gAAAAAElFTkSuQmCC");
    } else { //could be a switch if I had more frames
        //frame 2
        changeFavicon("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAADFBMVEUAAAAAAADZ3unZ3unZXwkJAAAABHRSTlMA////sy1AiAAAAEBJREFUOI1jYKAXYGJiwi9AiQI4C0kNihi1FDBhAdRUgMxHZ1JVAQ5AWAEOLyBkqaKAwvRAjAIMWXRhyhUMfQAA9t4DCY1klTUAAAAASUVORK5CYII=");
    }
    animateIcon.i++;
    if (animateIcon.i === 2) {
        animateIcon.i = 0;
    }
}

