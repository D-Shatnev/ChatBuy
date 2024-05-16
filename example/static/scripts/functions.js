async function sendMessage() {
    /***
     * handle for send-message button
    ***/
    let message = document.getElementById("message-input").value;  
    if (!message) return;  
    document.getElementById("message-input").value = "";
    document.getElementsByClassName("messages")[0].innerHTML+=create_message_div(message, "user");
    document.getElementsByClassName("messages")[0].innerHTML+=create_message_div("", "bot");
    
    let button = document.getElementById('send_button');
    button.style.backgroundColor = 'gray';
    button.disabled = true;

    const timeout = 10000;

    const handleTimeout = () => {
        update_bot_message_div("Нет ответа от сервера. Попробуйте позже.");
        button.disabled = false;
        button.style.backgroundColor = '';
    };

    let timeoutId = setTimeout(handleTimeout, timeout);

    try {
        messages = get_dialog_history();
        //Query to API
        const response = await fetch('http://192.168.169.101:15555/v1/chat/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            },
            body: JSON.stringify(messages)
        });

        clearTimeout(timeoutId);

        if (response.ok) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                update_bot_message_div(chunk);
            }
        } else {
            update_bot_message_div("Возникла ошибка. Перезагрузите страницу или попробуйте позже.");
        }
    } catch (error) {
        update_bot_message_div("Ошибка соединения. Попробуйте позже.");
    } finally {
        button.disabled = false;
        button.style.backgroundColor = '';
    }
}

function update_bot_message_div(chunk){
    /***
     * Updates last bot message.
     * 
     * Args:
     *      chunk (String): chunk to add to end of the last bot message. 
    ***/
    let elements = document.getElementsByClassName('message message-bot');
    elements[elements.length - 1].innerHTML += chunk;
    document.getElementsByClassName("messages")[0].scrollTop = document.getElementsByClassName("messages")[0].scrollHeight;
}

function get_dialog_history(){
    /***
     * Parse bot-user dialog and make list with dialog history.
     * 
     * Returns:
     *       Array(Object): list with objects of format {role: "user/assistant", content: "message_content"}.
    ***/
    let bot_messages = document.getElementsByClassName("message message-bot");
    let user_messages = document.getElementsByClassName("message message-user");
    let messages = []
    let counter = 0;
    while (counter<user_messages.length){
        if (counter==0){
            messages.push({role:"user", content: user_messages[counter++].innerHTML});
        }
        else{
            messages.push({role:"assistant", content: bot_messages[counter].innerHTML});
            messages.push({role:"user", content: user_messages[counter++].innerHTML});
        }
    }
    return messages;
}

function create_message_div(message, bot_or_user){
    /***
     * Makes HTML-code of message div for user or bot.
     * 
     * Args:
     *      message (String): message to put in div.
     *      bot_or_user (String): "bot" if you need to create bot`s message, "user" otherwise.
     * 
     * Returns:
     *      String: HTML-code of message div.
    ***/
    return `<div class="message message-${bot_or_user}">${message}</div>`;
}