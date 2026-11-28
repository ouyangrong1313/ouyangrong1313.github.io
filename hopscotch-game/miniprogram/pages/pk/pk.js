/**
 * 童年跳房子大挑战 - 好友PK页
 * pages/pk/pk.js
 */

const app = getApp();

Page({
  data: {
    // PK记录列表
    pkRecords: [],
    // 当前最高分
    myHighestScore: 0,
    // 空状态
    isEmpty: true
  },

  onLoad() {
    this.loadPKRecords();
  },

  onShow() {
    this.loadPKRecords();
  },

  // 加载PK记录
  loadPKRecords() {
    // 从本地存储加载PK记录
    const records = wx.getStorageSync('pkRecords') || [];
    const myHighestScore = app.getHighestScore();

    // 按分数排序
    records.sort((a, b) => b.score - a.score);

    this.setData({
      pkRecords: records,
      myHighestScore: myHighestScore,
      isEmpty: records.length === 0
    });
  },

  // 添加PK记录（由分享进入时调用）
  addPKRecord(fromScore, myScore) {
    const records = wx.getStorageSync('pkRecords') || [];

    records.push({
      id: Date.now(),
      fromScore: fromScore,
      myScore: myScore,
      result: myScore > fromScore ? 'win' : (myScore < fromScore ? 'lose' : 'draw'),
      date: new Date().toLocaleDateString()
    });

    // 只保留最近20条记录
    if (records.length > 20) {
      records.splice(0, records.length - 20);
    }

    wx.setStorageSync('pkRecords', records);
  },

  // 清空记录
  clearRecords() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有PK记录吗？',
      success: (res) => {
        if (res.confirm) {
          wx.removeStorageSync('pkRecords');
          this.loadPKRecords();
        }
      }
    });
  },

  // 返回首页
  goHome() {
    wx.navigateBack();
  },

  // 发起新PK
  startPK() {
    wx.redirectTo({
      url: '/pages/game/game?mode=pk'
    });
  },

  // 分享
  onShareAppMessage() {
    return {
      title: '我在童年跳房子玩了' + this.data.myHighestScore + '分，敢来挑战我吗？90后快来集合！',
      path: '/pages/index/index?pkScore=' + this.data.myHighestScore
    };
  },

  onShareTimeline() {
    return {
      title: '童年跳房子大挑战 - 我拿了' + this.data.myHighestScore + '分！',
      query: 'pkScore=' + this.data.myHighestScore
    };
  }
})
