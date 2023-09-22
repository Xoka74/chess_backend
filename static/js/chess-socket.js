class ChessWebSocket extends WebSocket {




}

const url = 'ws://'
    + window.location.host
    + '/ws/sessions/'
    + sessionId
    + '/'

const ws = new WebSocket(url);

ws.onopen = function (e) {
    console.log('Chat socket connection opened!');
}

ws.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
}

ws.onmessage = function (e) {
    let data = JSON.parse(e.data)
    let event_type = data.type;
    let result = data.result_data;
    console.log(data)
    if (event_type === 'make_move') {

    } else if (event_type === 'surrender') {

    } else if (event_type === 'join_session') {

    } else if (event_type === 'message_error') {

    }
}