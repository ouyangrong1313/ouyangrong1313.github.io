/**
 * 童年跳房子大挑战 - 规则页
 * pages/rules/rules.js
 */

Page({
  data: {},

  onLoad() {},

  // 返回首页
  goBack() {
    wx.navigateBack();
  },

  // 开始游戏
  startGame() {
    wx.redirectTo({
      url: '/pages/game/game?mode=challenge'
    });
  }
})
