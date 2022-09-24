from website.templates2 import base_example_template
from hypergen.imports import *

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def chat(request):

    textarea(id_="chat-log", cols="100", rows="20")
    br()
    input_(id_="chat-message-input", type_="text", size="100")
    br()
    input_(id_="chat-message-submit", type_="button", value="Send")

    script("""
                
        const roomName = "hypergen_it"

        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            document.querySelector('#chat-log').value += (data.message + '\\n');
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
    """)
