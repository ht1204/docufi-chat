import axios from 'axios';
import { UPLOAD_URL } from '../../utils';

import styles from './Form.module.css';

type TFormProps = {
    setDocId: (id: string) => void;
}


const Form = ({ setDocId }: TFormProps) => {

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const file = (e.target as any).elements.file.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(UPLOAD_URL, formData);
      setDocId(res.data.docId);
    } catch (err) {
      alert('Upload failed. Please try again.');
      console.error(err);
    }
  };

  return (
    <div className={styles.formContainer}>
      <h2>Upload Your Document</h2>
      <form onSubmit={handleUpload} className={styles.form}>
        <div className={styles.fileInput}>
          <input type="file" name="file" required />
        </div>
        <button type="submit" className={styles.uploadButton}>
          Upload & Start Chat
        </button>
      </form>
    </div>
  );
};

export default Form;
