import React from 'react';
import '../styles/CaseShowcase.css';

const CaseShowcase = ({ cases }) => {
  return (
    <div className="case-showcase">
      {cases.map(caseItem => (
        <div key={caseItem.id} className="case-item">
          <div className="case-image-container">
            <img src={caseItem.image} alt={caseItem.title} className="case-image" />
            <div className="case-thumbnails">
              <img src={caseItem.thumbnail} alt="缩略图" className="case-thumbnail" />
            </div>
          </div>
          <h3 className="case-title">{caseItem.title}</h3>
        </div>
      ))}
    </div>
  );
};

export default CaseShowcase;
