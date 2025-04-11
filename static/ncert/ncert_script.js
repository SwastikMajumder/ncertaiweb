function showContent(url, image) {
    var iframe = document.getElementById("contentIframe");
    var img = document.getElementById("contentImage");

    if (url.startsWith('http://') || url.startsWith('https://')) {
        // External URL
        iframe.src = url;
    } else {
        // Internal URL
        iframe.src = url; // flask will handle the internal url.
    }

    if (image) {
        img.src = image;
        img.style.display = "block";
        iframe.style.display = "block";
    } else {
        img.style.display = "none";
        iframe.style.display = "block";
    }
}
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('accordion-button')) {
        event.target.classList.toggle('active');
        var panel = event.target.nextElementSibling;
        if (panel) {
            if (panel.style.display === 'block') {
                panel.style.display = 'none';
            } else {
                panel.style.display = 'block';
            }
        }
    }
});
