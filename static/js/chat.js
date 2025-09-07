/**
 * Chat functionality for the Finance Hub chatbot
 */

class ChatManager {
    constructor() {
        this.chatbox = document.getElementById("chatbox");
        this.userInput = document.getElementById("userInput");
        this.sendButton = document.querySelector('button[onclick="sendMessage()"]');
        
        this.initializeEventListeners();
        this.loadChatHistory();
    }

    initializeEventListeners() {
        // Enter key support
        this.userInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                this.sendMessage();
            }
        });

        // Remove inline onclick and add proper event listener
        if (this.sendButton) {
            this.sendButton.removeAttribute('onclick');
            this.sendButton.addEventListener("click", () => this.sendMessage());
        }
    }

    async loadChatHistory() {
        try {
            const response = await fetch("/chat-history");
            const data = await response.json();

            data.history.forEach(chat => {
                this.addMessage(chat.user, "user");
                this.addMessage(chat.bot, "bot");
            });

            this.scrollToBottom();
        } catch (error) {
            console.error("Error loading chat history:", error);
        }
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, "user");
        this.userInput.value = "";

        try {
            // Show loading indicator
            this.showLoadingIndicator();

            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // Remove loading indicator
            this.removeLoadingIndicator();

            if (data.error) {
                this.addMessage(`Error: ${data.error}`, "bot");
            } else {
                this.addMessage(data.response, "bot");
            }

        } catch (error) {
            this.removeLoadingIndicator();
            this.addMessage("Error: Unable to get response. Please try again.", "bot");
            console.error("Chat error:", error);
        }
    }

    addMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `${sender}-message`;
        
        // Format the message for better readability
        const formattedMessage = message.replace(/\n/g, "<br>");
        messageDiv.innerHTML = formattedMessage;
        
        this.chatbox.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showLoadingIndicator() {
        const loadingDiv = document.createElement("div");
        loadingDiv.className = "bot-message loading";
        loadingDiv.innerHTML = "Typing...";
        loadingDiv.id = "loading-indicator";
        this.chatbox.appendChild(loadingDiv);
        this.scrollToBottom();
    }

    removeLoadingIndicator() {
        const loadingIndicator = document.getElementById("loading-indicator");
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    }

    scrollToBottom() {
        this.chatbox.scrollTop = this.chatbox.scrollHeight;
    }
}

// Initialize chat when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    new ChatManager();
});

// Global function for backward compatibility (remove this in future versions)
function sendMessage() {
    // This function is kept for backward compatibility
    // The ChatManager class handles this functionality now
    console.warn("sendMessage() is deprecated. Use ChatManager class instead.");
} 