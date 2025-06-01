import React, { useState, useRef } from 'react';
import '../styles/InputSection.css';

interface InputSectionProps {
  selectedAgent: string;
  onSendMessage: (text: string, file: File | null, agentType: string) => void;
}

const InputSection: React.FC<InputSectionProps> = ({ selectedAgent, onSendMessage }) => {
  const [inputText, setInputText] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isOnline, setIsOnline] = useState(true);
  const [selectedScene, setSelectedScene] = useState('通用场景');
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const scenes = ['通用场景', '工作汇报', '学术研究', '创意设计'];
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputText.trim() || selectedFile) {
      onSendMessage(inputText, selectedFile, selectedAgent);
      setInputText('');
      setSelectedFile(null);
    }
  };
  
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };
  
  const triggerFileInput = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };
  
  const getPlaceholder = () => {
    switch (selectedAgent) {
      case 'ppt':
        return '输入您的PPT需求，或上传参考文件...';
      case 'code':
        return '描述您需要的代码功能，或上传需求文档...';
      case 'web':
        return '描述您想要的网页设计，或上传参考图...';
      case 'general':
        return '有什么可以帮您的？';
      default:
        return '请选择一个智能体开始对话...';
    }
  };
  
  return (
    <div className="input-section">
      <div className="input-container">
        <div className="input-options">
          <div className="scene-selector">
            <select 
              value={selectedScene}
              onChange={(e) => setSelectedScene(e.target.value)}
              className="scene-select"
            >
              {scenes.map(scene => (
                <option key={scene} value={scene}>{scene}</option>
              ))}
            </select>
          </div>
          
          <div className="online-toggle">
            <span className={`toggle-label ${isOnline ? 'online' : 'offline'}`}>
              {isOnline ? '联网' : '离线'}
            </span>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={isOnline}
                onChange={() => setIsOnline(!isOnline)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>
        
        <div className="input-main">
          <textarea
            className="input-textarea"
            placeholder={getPlaceholder()}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={3}
          />
          
          <div className="input-actions">
            <button 
              type="button" 
              className="upload-button"
              onClick={triggerFileInput}
              title="上传文件"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              {selectedFile && <span className="file-name">{selectedFile.name}</span>}
            </button>
            
            <input 
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
            
            <button 
              type="button" 
              className="send-button"
              onClick={handleSubmit}
              disabled={!selectedAgent || (!inputText.trim() && !selectedFile)}
            >
              发送
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </div>
        
        {selectedFile && (
          <div className="selected-file">
            <span className="file-info">
              已选择: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
            </span>
            <button 
              className="remove-file" 
              onClick={() => setSelectedFile(null)}
            >
              ×
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default InputSection;
