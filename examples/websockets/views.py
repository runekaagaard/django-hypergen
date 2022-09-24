from website.templates2 import base_example_template
from hypergen.imports import *

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def chat(request):
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
            hypergen.applyCommands(JSON.parse(e.data))
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        hypergen.append = function(id, html) {
          const el = document.getElementById(id)
          el.innerHTML = el.innerHTML + html
        }

        myapp = {}
        myapp.sendChatMessage = function(e, id) {
            if (e.keyCode !== 13)  return
    
            chatSocket.send(JSON.stringify({
                'message': e.target.value
            }));
            e.target.value = '';
        }
    """)

    style(""" input, textarea {width: 100%} """)
    input_(id_="message", type_="text", placeholder="Write your message here and press enter.", autofocus=True,
        onkeyup="myapp.sendChatMessage(event, 'message')")
    ul(id_="messages")

def websocket(group_name=None, channel_name=None, target_id=None):
    return lambda f: None

N = 0

@websocket(group_name="chat", channel_name="message", target_id="num-messages")
def chat_message(msg):
    global N

    N += 1
    p("You have", N, "messages in total.", sep=" ")
    command("hypergen.append", "messages", hypergen(lambda: li(msg)))
