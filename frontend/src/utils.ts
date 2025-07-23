// Change backend url api link given your custom settings. 
const API_URL = 'http://localhost:5000'; 
const UPLOAD_URL = [API_URL, '/upload'].join('');
const CONVERSATION_URL = [API_URL, '/conversation'].join('');

export {
    UPLOAD_URL,
    CONVERSATION_URL,
}