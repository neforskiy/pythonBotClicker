const TelegramBot = require('node-telegram-bot-api');

// replace the value below with the Telegram token you receive from @BotFather
const token = '6880969982:AAEkVx7LagpVGF60zAbBEd033kpROjs8WC0';

const webAppUrl = 'https://bhkab1xfjn.eu.loclx.io'
// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, {polling: true});


bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const text = msg.text;

    if(text === '/start'){
        await bot.sendMessage(chatId, 'Ниже появится кнопка, пожалуйста заполните форму.', {
            reply_markup: {
                inline_keyboard: [
                    [{text: 'Заполнить форму', web_app: {url: webAppUrl}}]
                ]
            }
        })
    }
});