import { useState } from 'react';
import UploadForm from './components/Form/Form';
import ChatInterface from './components/Chat/Chat';
import styles from './App.module.css';

function App() {
  const [docId, setDocId] = useState<string>("");

  return (
    <div className={styles['container']}>
      <header className={styles['header']}>
        <h1>Docufi Mini-Chat</h1>
        <p>Upload a financial document and ask questions</p>
      </header>

      {!docId ? (
        <UploadForm setDocId={setDocId} />
      ) : (
        <ChatInterface docId={docId} setDocId={setDocId} />
      )}
    </div>
  );
}

export default App;