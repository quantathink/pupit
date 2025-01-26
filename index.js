//const fs = require('fs');
//const path = require('path');
//const folderPath = './vids';

                                                                        //GenAI
//const { GoogleGenerativeAI } = require("@google/generative-ai");
//const genAI = new GoogleGenerativeAI('AIzaSyCZ6Hp1HC4K13xXncG55w9TyaibrjuiOPc');
//const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash"});
/*
const sendQuestion = async function (prompt) {

    //Router Stage
    result =  await model.generateContent(prompt);
    response =  await result.response;
    answer = response.text();
    return (answer)
  }
*/
//get the function ready



//const { spawn } = require('child_process');

async function googleGemini(s){
    try{
        const response = await fetch
        (
            'http://127.0.0.1:5000/gemini',
            {
                method:'POST',
                headers:
                {
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({s:s})
            }
        )
        const data = await response.json();
        return(data.bot)
    } catch (error){
        console.log('Error',error)
    }
}
                                                                        //Pupit
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

client.on('qr', (qr) => {
    // Generate and display QR code in the terminal
    qrcode.generate(qr, { small: true });
});

client.on('ready',  () => {
    console.log('WhatsApp Web is ready!');
    client.sendMessage('971521357338@c.us','I am Alive!!!')
});


client.on('message', async (message) => 
    {
    console.log(`Message received from ${message.from}: ${message.body}`);
    answer = await googleGemini(message.body)
    //console.log(answer)
    client.sendMessage('971521357338@c.us',answer)

    }
)

client.initialize();