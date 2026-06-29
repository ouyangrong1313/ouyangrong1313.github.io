/**
 * 童年跳房子大挑战 - 结算页
 * pages/result/result.js
 */

const app = getApp();

Page({
  data: {
    score: 0,
    mode: 'challenge',
    highestScore: 0,
    isNewRecord: false,
    pkResult: '', // win, lose, pending
    shareText: ''
  },

  onLoad(options) {
    const score = parseInt(options.score) || 0;
    const mode = options.mode || 'challenge';

    const highestScore = app.getHighestScore();
    const isNewRecord = score >= highestScore && score > 0;

    // 判断PK结果
    let pkResult = '';
    if (mode === 'pk' && app.globalData.pkScore > 0) {
      if (score > app.globalData.pkScore) {
        pkResult = 'win';
      } else if (score < app.globalData.pkScore) {
        pkResult = 'lose';
      } else {
        pkResult = 'draw';
      }
    }

    // 生成分享文案
    const shareText = `我在童年跳房子玩了${score}分，敢来挑战我吗？90后快来集合！`;

    this.setData({
      score,
      mode,
      highestScore,
      isNewRecord,
      pkResult,
      shareText
    });

    // 重置PK模式
    if (mode === 'pk') {
      app.globalData.isPKMode = false;
    }
  },

  // 重新挑战
  playAgain() {
    wx.redirectTo({
      url: `/pages/game/game?mode=${this.data.mode}`
    });
  },

  // 返回首页
  goHome() {
    wx.redirectTo({
      url: '/pages/index/index'
    });
  },

  // 分享给好友
  shareToFriend() {
    // 微信会自动调起分享
  },

  // 分享到朋友圈
  shareToTimeline() {
    return {
      title: this.data.shareText,
      query: 'pkScore=' + this.data.score
    };
  },

  onShareAppMessage() {
    return {
      title: this.data.shareText,
      path: '/pages/index/index?pkScore=' + this.data.score,
      imageUrl: '/images/share-bg.png'
    };
  },

  onShareTimeline() {
    return {
      title: this.data.shareText,
      query: 'pkScore=' + this.data.score
    };
  }
})
