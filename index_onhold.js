//const qrcode = require("qrcode-terminal");
//const { Client } = require("whatsapp-web.js");
//const puppeteer = require("puppeteer");

const { Client, LocalAuth,  MessageMedia} = require('whatsapp-web.js');
const puppeteer = require('puppeteer-core');
const qrcode = require('qrcode-terminal');
const { BrowserLauncher } = require('puppeteer');

// Initialize WhatsApp Web Client
const client = new Client({
    puppeteer: {
        executablePath: '/usr/bin/google-chrome', // Path to installed Google Chrome binary
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    },
    authStrategy: new LocalAuth() // This helps persist sessions
});


client.on("qr", (qr) => {
// Generate and display the QR code in the terminal
    console.log("Scan the QR code below with WhatsApp:");
    qrcode.generate(qr, { small: true });
    });

client.on("ready", async () => {
    console.log("Client is ready!");
    
    try {
        const contactName = "Reminders"; // Change this to the desired contact name
        const message = "Are you mad at me? :( ";
    
        // Fetch the chat
        const chats = await client.getChats();
        const chat = chats.find((chat) => chat.name === contactName);
    
        if (!chat) {
        console.error(`Chat with contact '${contactName}' not found.`);
        return;
        }
    
        // Send the message
        await chat.sendMessage(message);
        console.log("Message sent!");
    } catch (error) {
        console.error("Error sending message:", error);
    }
    });
    
// Handle client errors
client.on("auth_failure", (msg) => console.error("Authentication failure:", msg));
client.on("disconnected", (reason) => console.log("Client disconnected:", reason));

// Start the client
client.initialize();