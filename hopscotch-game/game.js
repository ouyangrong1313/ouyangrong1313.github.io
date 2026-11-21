/**
 * 童年跳房子大挑战 - game.js
 * 游戏入口文件
 */

// 游戏主逻辑（如果使用 Canvas 渲染）
// const canvas = wx.createCanvas()
// const context = canvas.getContext('2d')

// 触发游戏加载
wx.loadSubpackage({
  name: 'main',
  success: () => {
    console.log('游戏资源加载完成')
  },
  fail: () => {
    console.log('游戏资源加载失败')
  }
})

// 显示加载提示
wx.showLoading({
  title: '游戏加载中...',
  mask: true
})

// 游戏初始化完成后隐藏加载提示
setTimeout(() => {
  wx.hideLoading()
}, 1000)

console.log('跳房子游戏启动')
