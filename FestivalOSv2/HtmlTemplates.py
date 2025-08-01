clearMapButtonHTML = """
            <button
                onclick="fetch('/api/clear_map').then(() => console.log('Map cleared'))"
                style="position:absolute; top:50px; right:80px; z-index:999;
                background-color:#1E1E1E; color:white; border:2px solid #444;
                border-radius:20px; padding:0px 20px; font-size: 26px;
                font-weight: bold; font-family: Arial, sans-serif;">
                <h1> Clear Map </h1>
            </button>
            """

addQRcodeImageHTML = """
            <button
                onclick="fetch('/api/add_qr_code')
                    .then(() => {
                        smoothReloadMap();
                        console.log('QR Code added and map updated');
                    })"
                style="position:absolute; top:175px; right:80px; z-index:999;
                background-color:#1E1E1E; color:white; border:2px solid #444;
                border-radius:20px; padding:0px 20px; font-size: 26px;
                font-weight: bold; font-family: Arial, sans-serif;">
                <h1> View QR Code </h1>
            </button>
            """

booth0HTML = """
            <button
                onclick="fetch('/api/navigate_to/0')
                    .then(() => {
                        smoothReloadMap();
                        console.log('Navigating to Booth #0');
                    })"
                style="position:absolute; top:300px; right:80px; z-index:999;
                background-color:#1E1E1E; color:white; border:2px solid #444;
                border-radius:20px; padding:0px 20px; font-size: 26px;
                font-weight: bold; font-family: Arial, sans-serif;">
                <h1> Navigate to X Booth </h1>
            </button>
            """

booth1HTML = """
            <button
                onclick="fetch('/api/navigate_to/1').then(() => console.log('Navigating to Y Booth'))"
                style="position:absolute; top:425px; right:80px; z-index:999;
                background-color:#1E1E1E; color:white; border:2px solid #444;
                border-radius:20px; padding:0px 20px; font-size: 26px;
                font-weight: bold; font-family: Arial, sans-serif;">
                <h1> Navigate to Y Booth </h1>
            </button>
            """

booth2HTML = """
            <button
                onclick="fetch('/api/navigate_to/2').then(() => console.log('Navigating to Z Booth'))"
                style="position:absolute; top:550px; right:80px; z-index:999;
                background-color:#1E1E1E; color:white; border:2px solid #444;
                border-radius:20px; padding:0px 20px; font-size: 26px;
                font-weight: bold; font-family: Arial, sans-serif;">
                <h1 >Navigate to Z Booth </h1>
            </button>
            """

styleHTML = """
            <style>
            body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: #121212;
                }
                /* Hide scrollbars */
                ::-webkit-scrollbar {
                    display: none;
                }
                html, body {
                    scrollbar-width: none;
                    -ms-overflow-style: none;
                }
                iframe {
                    background-color: #121212;
                    transform: rotate(0deg);
                    transform-origin: center center;
                }
            </style>
            """

# Create a script for smooth iframe reloading
smooth_reload_script = """
<script>
function smoothReloadMap() {
    const iframe = document.getElementById('map-frame');
    if (!iframe) return;

    // Create a new iframe
    const newIframe = document.createElement('iframe');
    newIframe.id = 'map-frame-new';
    newIframe.style.cssText = 'width: 100%; height: 100%; border: none; opacity: 0; transition: opacity 0.5s ease;';
    newIframe.src = '/index.html?' + new Date().getTime();

    // Wait for the new iframe to load
    newIframe.onload = function() {
        // Fade in the new iframe
        setTimeout(() => {
            newIframe.style.opacity = '1';

            // After transition completes, remove old iframe
            setTimeout(() => {
                iframe.remove();
                newIframe.id = 'map-frame';
            }, 500);
        }, 100);
    };

    // Insert the new iframe before the old one
    iframe.parentNode.insertBefore(newIframe, iframe);
}
</script>
"""
