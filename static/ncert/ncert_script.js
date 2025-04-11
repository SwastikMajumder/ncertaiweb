function showContent(url, image) {
    var iframe = document.getElementById("contentIframe");
    var img = document.getElementById("contentImage");
    iframe.src = url;
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