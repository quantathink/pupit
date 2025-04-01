const fs = require('fs');
const path = require('path');

// Function One, Open ai chat bot
async function OpenAI(s){
    try{
        const response = await fetch
        (
            'http://127.0.0.1:5000/router',
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
// Function Two, garbage Cleaner
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

// Function Three, simple answer bot
async function simple_answer(s){
    try{
        const response = await fetch
        (
            'http://127.0.0.1:5000/simple_answer',
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

// Secretary Mindsimple answer bot
async function secretary_mind(s, Document){
    try{
        const response = await fetch
        (
            'http://127.0.0.1:5000/secretary_mind',
            {
                method:'POST',
                headers:
                {
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({s:s,Document:Document})
            }
        )
        const data = await response.json();
        return(data.bot)
    } catch (error){
        console.log('Error',error)
    }
}

// Secretary Mindsimple answer bot
async function accountant_mind(s){
    try{
        const response = await fetch
        (
            'http://127.0.0.1:5000/accountant_mind',
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

                                                                        //ON Message

client.on('message', async (message) => 
    {
    garbage_clean('clean')
    //console.log(`Message received from ${message.from}: ${message.body}`);
    chatId = message.from
    answer = await OpenAI(message.body)
    let routing_dict = {'route':'jarvis','status':'','answer':answer}
    console.log(`Routing to:  ${answer}`)
    console.log(`Message from:  ${chatId}`)
    console.log(`Context of message from:  ${message.body}`)
    
    
    switch (answer) {
        case '.mp3':
            const files = fs.readdirSync('./vids');
            let mpxFile = files.find(file => file.endsWith(answer));
            const media = await MessageMedia.fromFilePath('./vids/'+ mpxFile);
            client.sendMessage(chatId, media, { caption: 'Here is you file!'});
            break;
        case 'secretary':
            let Document = await message.downloadMedia();
            let Document_file = await secretary_mind(message.body, Document)
            if (Document_file == 'File is Saved'){
                client.sendMessage(chatId, Document_file);
            }else{
                let doc_media = await MessageMedia.fromFilePath('./docs/'+ Document_file);

                client.sendMessage(chatId, doc_media);
                client.sendMessage(chatId, 'Here is the document Master Bruce');
            }
        case 'accountant':
            let ans = await accountant_mind(message.body)
            //let message_body = message.body + ' what is needed to be done, Just say "save" or "load"'
            //answer = await simple_answer(message_body)
            //console.log(answer)
            //console.log(typeof(Document))


            // Define a directory to save images
            /*
            const saveDir = './docs';
            if (!fs.existsSync(saveDir)) {
                fs.mkdirSync(saveDir, { recursive: true });
            }
                    // Generate a filename with timestamp
            const fileExtension = Document.mimetype.split('/')[1]; // Extract file type (e.g., png, jpg)
            const filename = `image_${Date.now()}.${fileExtension}`;
            const filepath = path.join(saveDir, filename);
            // Save the image
            fs.writeFileSync(filepath, Document.data, { encoding: 'base64' });
            console.log(`Image saved: ${filepath}`);
            client.sendMessage(chatId, 'Image received and saved!');
            */
            break;
        default:
            client.sendMessage(chatId,answer);
            break;     

      }
    }
)




client.initialize();