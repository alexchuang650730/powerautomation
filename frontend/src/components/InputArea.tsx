import React, { useState } from 'react';
import './InputArea.css';

interface InputAreaProps {
  onInputChange: (text: string) => void;
  onSubmit: () => void;
  onFileUpload: (files: FileList) => void;
}

const InputArea: React.FC<InputAreaProps> = ({ onInputChange, onSubmit, onFileUpload }) => {
  const [inputText, setInputText] = useState('');
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(e.target.value);
    onInputChange(e.target.value);
  };
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit();
  };
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileUpload(e.target.files);
    }
  };
  
  return (
    <div className="input-area">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          className="input-field"
          placeholder="输入人问宏"
          value={inputText}
          onChange={handleInputChange}
        />
        <div className="input-actions">
          <label className="file-upload-label">
            <input 
              type="file" 
              className="file-input" 
              onChange={handleFileChange}
              multiple
            />
            <span className="file-icon">📎</span>
          </label>
          <button type="submit" className="submit-button">发送</button>
        </div>
      </form>
    </div>
  );
};

export default InputArea;
