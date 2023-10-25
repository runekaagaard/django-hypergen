from hypergen.imports import *

@liveview(perm=NO_PERM_REQUIRED)
def index(request):
    from anteams.consumers import chatroom_group
    # command("hypergen.websocket.open", "ws://127.0.0.1:8002/ws/anteams")
    script("""
        // Create a WebSocket connection to a specified URL
        let ws = new WebSocket('ws://127.0.0.1:8002/ws/anteams');

        // Define a function to send data via the WebSocket
        function sendData(data) {
            // Ensure the WebSocket is open before sending data
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify(data));  // Assume data is an object
            } else {
                console.error('WebSocket is not open: cannot send data');
            }
        }

        // Set up event handlers to capture WebSocket events
        ws.onopen = function(event) {
            console.log('WebSocket is open now.');
        };

        ws.onclose = function(event) {
            console.log('WebSocket is closed now.');
        };

        ws.onerror = function(event) {
            console.error('WebSocket error observed:', event);
        };

        ws.onmessage = function(event) {
            // Output replies from the server
            console.log('Received:', JSON.parse(event.data));
        };

        // Example usage:
        // sendData({ message: 'Hello, server!' });
    """)
    button("anteams_message", onclick=call_js("sendData", {"message": "YO!", "type": "anteams_message"}), id_="send")
    button("anteams_group", onclick=call_js("sendData", {"message": "YO!", "type": "anteams_group"}), id_="send2")
    button("group_add", onclick=call_js("sendData",
        {"group_name": chatroom_group("love_group")["name"], "type": "group_add"}), id_="send3")
    button(
        "group_send", onclick=call_js("sendData",
        {"group_name": chatroom_group("love_group")["name"], "type": "group_send", "message": "I'm the love group!"}),
        id_="send4")
