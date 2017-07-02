
resume = function() {
    song = 'spotify:track:4iV5W9uYEdYUVa79Axb7Rh';
    $.ajax('/add_song?song=' + song)
};
pause = function() {
    $.ajax('/pause')
};

socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('client_connected', {data: 'I\'m connected!'});
});

socket.on('queue_changed', function(data) {
    console.log('the queue is updating')
    app.queue = data;
});

socket.on('suggestions_changed', function(data) {
    console.log('new suggestions inbound');
    app.suggestions = data;
});

app = new Vue({
    el: '#app',
    data: {
        queue: [],
        search: '',
        suggestions: []
    },
    watch: {
        search: function () {
            socket.emit('searchbar_changed', {query: this.search})
        }
    }
})

