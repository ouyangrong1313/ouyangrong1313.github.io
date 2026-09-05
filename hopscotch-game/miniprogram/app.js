/**
 * 童年跳房子大挑战 - app.js
 * 入口文件
 */
App({
  globalData: {
    // 全局游戏配置
    gameConfig: {
      gameDuration: 60,        // 游戏时长60秒
      baseScore: 10,           // 踩中格子基础分
      missPenalty: 5,           // 踩空扣分
      perfectBonus: 5,         // 连续踩中奖励
      maxCombo: 10             // 最大连击数
    },
    // 历史最高分
    highestScore: 0,
    // 是否是好友PK模式
    isPKMode: false,
    // PK分数（从分享卡片进入时携带）
    pkScore: 0
  },

  onLaunch() {
    // 从本地存储读取最高分
    const highestScore = wx.getStorageSync('highestScore');
    if (highestScore) {
      this.globalData.highestScore = highestScore;
    }

    // 检查是否有PK分数（从分享链接进入）
    const launchOptions = wx.getLaunchOptionsSync();
    if (launchOptions && launchOptions.query && launchOptions.query.pkScore) {
      this.globalData.pkScore = parseInt(launchOptions.query.pkScore) || 0;
      this.globalData.isPKMode = true;
    }
  },

  // 保存最高分
  saveHighestScore(score) {
    if (score > this.globalData.highestScore) {
      this.globalData.highestScore = score;
      wx.setStorageSync('highestScore', score);
    }
  },

  // 获取最高分
  getHighestScore() {
    return this.globalData.highestScore;
  }
})
