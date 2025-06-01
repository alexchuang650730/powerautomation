import React, { useState, useEffect } from 'react';
import { getAgentFeatures, updateAgentFeatures } from '../utils/multi-agent-enhancer';

/**
 * 六大特性编辑器组件
 * 允许用户查看和修改智能体的六大特性
 */
const SixFeaturesEditor = ({ agentType, onUpdate }) => {
  const [features, setFeatures] = useState({
    platform_feature: '',
    ui_layout: '',
    prompt: '',
    thinking: '',
    content: '',
    memory: ''
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [saving, setSaving] = useState(false);

  // 特性名称映射
  const featureNames = {
    platform_feature: '特性1: PowerAutomation自动化平台功能',
    ui_layout: '特性2: UI布局',
    prompt: '特性3: 提示词',
    thinking: '特性4: 思维',
    content: '特性5: 内容',
    memory: '特性6: 记忆长度'
  };

  // 加载特性
  useEffect(() => {
    const loadFeatures = async () => {
      setLoading(true);
      setError(null);
      try {
        const agentFeatures = await getAgentFeatures(agentType);
        setFeatures(agentFeatures);
      } catch (err) {
        console.error('加载特性失败:', err);
        setError('加载特性失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    if (agentType) {
      loadFeatures();
    }
  }, [agentType]);

  // 处理特性更新
  const handleFeatureChange = (featureKey, value) => {
    setFeatures(prev => ({
      ...prev,
      [featureKey]: value
    }));
  };

  // 保存特性
  const handleSave = async () => {
    setSaving(true);
    setError(null);
    try {
      const result = await updateAgentFeatures(agentType, features);
      if (result.error) {
        throw new Error(result.error);
      }
      setEditMode(false);
      if (onUpdate) {
        onUpdate(features);
      }
    } catch (err) {
      console.error('保存特性失败:', err);
      setError('保存特性失败，请稍后重试');
    } finally {
      setSaving(false);
    }
  };

  // 取消编辑
  const handleCancel = async () => {
    setEditMode(false);
    // 重新加载特性
    try {
      const agentFeatures = await getAgentFeatures(agentType);
      setFeatures(agentFeatures);
    } catch (err) {
      console.error('重新加载特性失败:', err);
    }
  };

  if (loading) {
    return <div className="features-loading">加载中...</div>;
  }

  if (error) {
    return <div className="features-error">{error}</div>;
  }

  return (
    <div className="six-features-editor">
      <div className="features-header">
        <h3>六大特性定义 - {agentType}</h3>
        {!editMode ? (
          <button 
            className="edit-button" 
            onClick={() => setEditMode(true)}
          >
            编辑
          </button>
        ) : (
          <div className="edit-actions">
            <button 
              className="save-button" 
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? '保存中...' : '保存'}
            </button>
            <button 
              className="cancel-button" 
              onClick={handleCancel}
              disabled={saving}
            >
              取消
            </button>
          </div>
        )}
      </div>

      <div className="features-list">
        {Object.entries(features).map(([key, value]) => (
          <div key={key} className="feature-item">
            <div className="feature-name">{featureNames[key] || key}</div>
            {editMode ? (
              <textarea
                className="feature-editor"
                value={value}
                onChange={(e) => handleFeatureChange(key, e.target.value)}
                rows={3}
              />
            ) : (
              <div className="feature-value">{value}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SixFeaturesEditor;
