

document.addEventListener('DOMContentLoaded', function () {

    var sessionname = sessionStorage.getItem('username');
    //if session has no username- do nothing and let the form get submitted
    if (sessionname === null || sessionname === undefined || sessionname === "")
        return;
    else {
        //if session already has username- remove the form elements from the document    
        manageElements();
    };

});

function formSubmitListener() {
    const name = document.querySelector('#name').value;
    //get the input value and set it as session's username
    sessionStorage.setItem('username', name);
    const sessionname = sessionStorage.getItem('username');
    manageElements();

}

function manageElements() {
    var elem = document.getElementById('name');
    elem.parentNode.remove();
    const sessionname = sessionStorage.getItem('username');
    var ele = document.createElement('p');
    ele.innerText = "Hello " + sessionname;
    document.getElementById("subhead-section").appendChild(ele);
    document.getElementById('chat_section').style.visibility = "visible";

}


////chat code

var socket = io.connect('http://127.0.0.1:5000');
const sessionname = sessionStorage.getItem('username');

      // When connected, configure buttons
      socket.on( 'connect', function() {
        socket.emit( 'my event', {
          data: 'User Connected'
        })

         console.log('inside socket.on')
         document.querySelector('#send-button').addEventListener("click", () => {
            
            // Save time in format HH:MM:SS
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();

            let user_input=document.getElementById("message").value
            socket.emit('my event',{user_name: sessionname, message: user_input});
              });

      
      socket.on('my response', function (msg) {
        console.log(msg)
        if (typeof msg.user_name !== 'undefined') {
            let elem = document.getElementById('placeholder');
            elem.parentNode.remove();
            let div_ele=document.createElement(div);
            div_ele.innerText=msg.user_name + '</b> ' + msg.message;
            document.getElementById('placeholder').appendChild(div_ele)
        }
    })
    
});