import React, { useEffect, useState } from 'react';
import '../styles/TestResultsDisplay.css';

interface TestResult {
  name: string;
  status: 'passed' | 'failed' | 'error';
  message: string;
}

interface TestResultsProps {
  results?: {
    total: number;
    passed: number;
    failed: number;
    tests: TestResult[];
  };
  loading?: boolean;
  error?: string;
  lastUpdated?: string;
}

const TestResultsDisplay: React.FC<TestResultsProps> = ({ 
  results, 
  loading = false, 
  error = '', 
  lastUpdated = '' 
}) => {
  const [expandedTests, setExpandedTests] = useState<string[]>([]);

  const toggleExpand = (testName: string) => {
    if (expandedTests.includes(testName)) {
      setExpandedTests(expandedTests.filter(name => name !== testName));
    } else {
      setExpandedTests([...expandedTests, testName]);
    }
  };

  useEffect(() => {
    // 自动展开失败的测试
    if (results) {
      const failedTests = results.tests
        .filter(test => test.status === 'failed' || test.status === 'error')
        .map(test => test.name);
      
      if (failedTests.length > 0 && failedTests.length <= 3) {
        setExpandedTests(failedTests);
      }
    }
  }, [results]);

  if (loading) {
    return (
      <div className="test-results-container loading">
        <div className="loading-spinner"></div>
        <p>正在加载测试结果...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="test-results-container error">
        <h2>测试结果加载失败</h2>
        <p className="error-message">{error}</p>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="test-results-container empty">
        <h2>暂无测试结果</h2>
        <p>请运行测试以查看结果</p>
      </div>
    );
  }

  return (
    <div className="test-results-container">
      <div className="test-results-header">
        <h2>测试结果</h2>
        <div className="test-results-summary">
          <div className="summary-item total">
            <span className="summary-label">总计</span>
            <span className="summary-value">{results.total}</span>
          </div>
          <div className="summary-item passed">
            <span className="summary-label">通过</span>
            <span className="summary-value">{results.passed}</span>
          </div>
          <div className="summary-item failed">
            <span className="summary-label">失败</span>
            <span className="summary-value">{results.failed}</span>
          </div>
        </div>
      </div>

      <div className="test-results-list">
        {results.tests.map((test) => (
          <div 
            key={test.name} 
            className={`test-result-item ${test.status}`}
            onClick={() => toggleExpand(test.name)}
          >
            <div className="test-result-header">
              <span className={`status-indicator ${test.status}`}>
                {test.status === 'passed' ? '✓' : '✗'}
              </span>
              <span className="test-name">{test.name}</span>
              <span className="expand-icon">
                {expandedTests.includes(test.name) ? '▼' : '▶'}
              </span>
            </div>
            
            {expandedTests.includes(test.name) && (
              <div className="test-details">
                <pre>{test.message}</pre>
              </div>
            )}
          </div>
        ))}
      </div>

      {lastUpdated && (
        <div className="last-updated">
          最后更新: {lastUpdated}
        </div>
      )}

      <div className="github-link">
        <a href="https://github.com/alexchuang650730/powerautomation/issues?q=label%3Atest-results" 
           target="_blank" 
           rel="noopener noreferrer">
          在GitHub上查看完整测试报告
        </a>
      </div>
    </div>
  );
};

export default TestResultsDisplay;
