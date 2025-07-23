import { useState } from 'react';
import axios from 'axios';

import { CONVERSATION_URL } from '../../utils';

import styles from './Chat.module.css';

type TChatMessage = {
  type: 'user' | 'reply';
  text: string;
};

type TKeyDownEvent = {
  key: string; 
  shiftKey: any; preventDefault: () => void; 
}

type TChatProps = {
    docId: string;
    setDocId: (id: string) => void;
}

const Chat = ({ docId, setDocId }: TChatProps) => {

  const [message, setMessage] = useState<string>('');
  const [chatHistory, setChatHistory] = useState<TChatMessage[]>([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    // Add user message to history
    setChatHistory((prev) => [...prev, { type: 'user', text: message }]);
    setMessage('');

    try {
      const res = await axios.post(CONVERSATION_URL, { docId, message });
      setChatHistory((prev) => [...prev, { type: 'reply', text: res.data.reply }]);
    } catch (err) {
      setChatHistory((prev) => [
        ...prev,
        { type: 'reply', text: 'Sorry, I could not process your request.' },
      ]);
      console.error(err);
    }
  };

  const handleKeyDown = (e: TKeyDownEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleGoBack = () => {
    setDocId("");
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(e.target.value);
  }

  return (
    <div className={styles['chatContainer']}>
      <div className={styles['chatHeader']}>
        <span>Chat with Document</span>
        <button className={styles['backButton']} onClick={handleGoBack}>
          ← Back to Upload
        </button>
      </div>

      <div className={styles.chatBody}>
        {!chatHistory.length ? (
          <p className={styles['chatStart']}>
            Start the conversation by asking a question about your document...
          </p>
        ) : (
          chatHistory.map((msg, idx) => (
            <div key={idx} className={msg.type === 'user' ? styles['userMessage'] : styles['reply']}>
              {msg.text}
            </div>
          ))
        )}
      </div>

      <div className={styles['chatFooter']}>
        <input
          value={message}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          aria-label="Chat input"
        />
        <button onClick={sendMessage} className={styles['sendButton']}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;