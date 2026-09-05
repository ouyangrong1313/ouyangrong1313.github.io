/**
 * 童年跳房子大挑战 - 首页
 * pages/index/index.js
 */
const app = getApp();

Page({
  data: {
    highestScore: 0,
    isPKMode: false,
    pkScore: 0,
    showPKNotice: false
  },

  onLoad() {
    // 获取最高分
    const highestScore = app.getHighestScore();
    this.setData({
      highestScore: highestScore,
      isPKMode: app.globalData.isPKMode,
      pkScore: app.globalData.pkScore
    });

    // 如果是PK模式，显示提示
    if (app.globalData.isPKMode && app.globalData.pkScore > 0) {
      this.setData({ showPKNotice: true });
    }
  },

  onShow() {
    // 每次显示页面时刷新最高分
    const highestScore = app.getHighestScore();
    this.setData({ highestScore: highestScore });
  },

  // 开始闯关
  startGame() {
    app.globalData.isPKMode = false;
    wx.navigateTo({
      url: '/pages/game/game?mode=challenge'
    });
  },

  // 查看规则
  showRules() {
    wx.navigateTo({
      url: '/pages/rules/rules'
    });
  },

  // 好友PK
  startPK() {
    app.globalData.isPKMode = true;
    wx.navigateTo({
      url: '/pages/game/game?mode=pk'
    });
  },

  // 查看PK排行榜
  viewPK() {
    wx.navigateTo({
      url: '/pages/pk/pk'
    });
  },

  // 分享设置
  onShareAppMessage() {
    const score = this.data.highestScore;
    return {
      title: '我在童年跳房子玩了' + score + '分，敢来挑战我吗？90后快来集合！',
      path: '/pages/index/index?pkScore=' + score,
      imageUrl: '/images/share-bg.png'
    };
  },

  onShareTimeline() {
    const score = this.data.highestScore;
    return {
      title: '童年跳房子大挑战 - 我拿了' + score + '分！',
      query: 'pkScore=' + score
    };
  }
})
