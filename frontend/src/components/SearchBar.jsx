import React, { useState } from 'react';
import '../styles/SearchBar.css';

const SearchBar = ({ placeholder, onSearch }) => {
  const [query, setQuery] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch && query.trim()) {
      onSearch(query);
    }
  };
  
  return (
    <div className="search-bar-container">
      <form onSubmit={handleSubmit}>
        <div className="search-input-wrapper">
          <input
            type="text"
            className="search-input"
            placeholder={placeholder}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <div className="search-actions">
            <button type="button" className="upload-button">
              <span className="icon">📁</span>
            </button>
            <button type="submit" className="submit-button">
              <span className="icon">🚀</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default SearchBar;
