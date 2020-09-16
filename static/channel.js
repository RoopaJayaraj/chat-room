document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        socket.emit('joined');

        document.querySelector('#newChannel').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });

        
        document.querySelector('#leave').addEventListener('click', () => {
            socket.emit('left');

            localStorage.removeItem('last_channel');
            window.location.replace('/');
        })

        document.querySelector('#logout').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });

        // 'Enter' key on textarea also sends a message
        document.querySelector('#comment').addEventListener("keydown", event => {
            if (event.key == "Enter") {
                document.getElementById("send-button").click();
            }
        });
        
       
        document.querySelector('#send-button').addEventListener("click", () => {
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();
            
            let msg = document.getElementById("comment").value;

            socket.emit('send message', msg, timestamp);
            document.getElementById("comment").value = '';
        });

        // // Send button emits a "image sent" event
        // document.querySelector('#image-send').addEventListener("click", () => {
        //     // Save user input
        //     let img_path = document.getElementById("img-path").value;

        //     socket.emit('send image', img_path);
            
        //     // Clear input
        //     document.getElementById("comment").value = '';
        // });
    });
    
    socket.on('status', data => {

        let row =  `${data.msg}` 
        document.querySelector('#chat').value += row + '\n';

        
        localStorage.setItem('last_channel', data.channel)
    })

    
    socket.on('announce message', data => {

        let row =  `${data.timestamp}` + ' - ' + '[' + `${data.user}` + ']:  ' + `${data.msg}`
        document.querySelector('#chat').value += row + '\n'
        send_notification(data.user,data.msg)
    })
    function send_notification(username,msg){
        if(window.Notification && Notification.permission !== "denied") {
            Notification.requestPermission(function(status) {  // status is "granted", if accepted by user
                var n = new Notification('Flack', { 
                    body: username+' says..'+'\n'+msg,
                    icon: '../static/images/favicon-16x16.png' // optional
                }); 
            });
        }
    }
    
});