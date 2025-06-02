import React, { useState } from 'react';
import '../styles/InputArea.css';

interface InputAreaProps {
  onInputChange: (text: string) => void;
  onSubmit: () => void;
  onFileUpload: (files: FileList) => void;
  selectedAgentType?: string;
  selectedAgentName?: string;
  selectedAgentIcon?: string;
}

const InputArea: React.FC<InputAreaProps> = ({ 
  onInputChange, 
  onSubmit, 
  onFileUpload, 
  selectedAgentType,
  selectedAgentName,
  selectedAgentIcon
}) => {
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
      {selectedAgentName && (
        <div className="selected-agent-status">
          <span className="agent-icon">{selectedAgentIcon}</span>
          <span>{selectedAgentName}</span>
        </div>
      )}
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
            <span className="file-icon">⬆️</span>
          </label>
          <button type="submit" className="submit-button">➡️</button>
        </div>
      </form>
    </div>
  );
};

export default InputArea;
