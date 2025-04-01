const fs = require('fs');

async function googleGemini(s){
    try{
        const response = await fetch
        (
            'http://localhost:5678/webhook-test/testing',
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

async function garbage_clean(s){
    try{
        const response = await fetch
        (
            'http://127.0.0.1:5000/garbage_clean',
            {
                method:'POST',
                headers:
                {
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({s:s})
            }
        )
        //return(data.bot)
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

                                                                        //ON Message

client.on('message', async (message) => 
    {
    console.log(`Message received from ${message.from}: ${message.body}`);
    chatId = message.from
    answer = await googleGemini(message.body)
    //console.log(answer)
    console.log(answer)

    switch (answer) {
        case '.mp3':
            const files = fs.readdirSync('./vids');
            let mpxFile = files.find(file => file.endsWith(answer));
            console.log(mpxFile)
            const media = MessageMedia.fromFilePath('./vids/'+ mpxFile);
            client.sendMessage(chatId, media, { caption: 'Here is you file!'});
            break;
        default:
            client.sendMessage('971521357338@c.us',answer);
            break;

      }
/*
    if (answer == '.mp3'){
        const files = fs.readdirSync('./vids');
        let mpxFile = files.find(file => file.endsWith(answer));
        console.log(mpxFile)
        const media = MessageMedia.fromFilePath('./vids/'+ mpxFile);
        client.sendMessage(chatId, media, { caption: 'Here is you file!'})


    }else{
        client.sendMessage('971521357338@c.us',answer)
    }
*/
    }
)

client.initialize();