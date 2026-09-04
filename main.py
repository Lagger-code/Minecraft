<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot 🤖</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            width: 100%;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 10px;
        }
        
        .chat-container {
            width: 100%;
            max-width: 600px;
            height: 90vh;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 1.5em;
            font-weight: bold;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .message {
            display: flex;
            margin-bottom: 10px;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message.bot {
            justify-content: flex-start;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 10px;
            word-wrap: break-word;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 0;
        }
        
        .message.bot .message-content {
            background: #f0f0f0;
            color: #333;
            border-bottom-left-radius: 0;
        }
        
        .chat-input-area {
            padding: 15px;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }
        
        input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 25px;
            font-size: 1em;
            outline: none;
            transition: border-color 0.3s;
        }
        
        input:focus {
            border-color: #667eea;
        }
        
        button {
            padding: 12px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: scale(1.05);
        }
        
        button:active {
            transform: scale(0.95);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .loading {
            display: flex;
            align-items: center;
            gap: 5px;
            color: #999;
        }
        
        .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            animation: bounce 1.4s infinite;
        }
        
        .dot:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .dot:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
                opacity: 0.6;
            }
            50% {
                transform: translateY(-10px);
                opacity: 1;
            }
        }
        
        .info-text {
            font-size: 0.85em;
            color: #999;
            text-align: center;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            🤖 AI Chatbot
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-content">
                    Hallo! 👋 Ich bin dein AI Chatbot. Wie kann ich dir heute helfen?
                </div>
            </div>
        </div>
        
        <div class="chat-input-area">
            <input 
                type="text" 
                id="userInput" 
                placeholder="Schreib eine Nachricht..." 
                autocomplete="off"
            >
            <button id="sendBtn" onclick="sendMessage()">Senden</button>
        </div>
        <div class="info-text">Powered by Hugging Face API (kostenlos) 🚀</div>
    </div>
    
    <script>
        const chatMessages = document.getElementById('chatMessages');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');
        
        const API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill";
        const HF_TOKEN = "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";
        
        async function sendMessage() {
            const message = userInput.value.trim();
            
            if (!message) return;
            
            addMessage(message, 'user');
            userInput.value = '';
            sendBtn.disabled = true;
            
            const loadingId = 'loading-' + Date.now();
            addMessage('<div class="loading"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', 'bot', loadingId);
            
            try {
                const response = await fetch(API_URL, {
                    headers: {
                        Authorization: `Bearer ${HF_TOKEN}`,
                    },
                    method: "POST",
                    body: JSON.stringify({ inputs: message }),
                });
                
                if (!response.ok) {
                    throw new Error('API Error: ' + response.status);
                }
                
                const result = await response.json();
                removeMessage(loadingId);
                
                let botMessage = '';
                if (result[0] && result[0].generated_text) {
                    botMessage = result[0].generated_text;
                } else {
                    botMessage = "Entschuldigung, ich konnte keine Antwort generieren. Versuche es erneut! 🤔";
                }
                
                addMessage(botMessage, 'bot');
                
            } catch (error) {
                removeMessage(loadingId);
                console.error('Error:', error);
                addMessage("Entschuldigung, es gab einen Fehler. Bitte überprüfe deine Internetverbindung und versuche es erneut! ⚠️", 'bot');
            }
            
            sendBtn.disabled = false;
            userInput.focus();
        }
        
        function addMessage(text, sender, id = null) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            if (id) messageDiv.id = id;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = text;
            
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function removeMessage(id) {
            const element = document.getElementById(id);
            if (element) element.remove();
        }
        
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        userInput.focus();
    </script>
</body>
</html>
