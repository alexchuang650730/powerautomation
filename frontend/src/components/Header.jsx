import React from 'react';
import '../styles/Header.css';

const Header = () => {
  return (
    <div className="header">
      <div className="header-left">
        <h1 className="header-title">首页</h1>
      </div>
      <div className="header-right">
        <div className="header-item">
          <span className="icon">🎁</span>
          <span className="text">邀请好友赚积分</span>
        </div>
        <div className="header-item points">
          <span className="icon">🪙</span>
          <span className="text">2715</span>
        </div>
        <div className="header-item">
          <span className="text">积分充值</span>
        </div>
        <div className="header-item">
          <span className="icon">🔔</span>
        </div>
        <div className="header-item user">
          <img src="/avatar.png" alt="用户头像" className="avatar" />
          <span className="text">Alex Chuang</span>
        </div>
      </div>
    </div>
  );
};

export default Header;
