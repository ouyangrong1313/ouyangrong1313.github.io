/**
 * 童年跳房子大挑战 - 游戏主页面
 * pages/game/game.js
 */

const app = getApp();

Page({
  data: {
    gameStatus: 'ready',
    gameMode: 'challenge',
    score: 0,
    timeLeft: 60,
    combo: 0,
    tiles: [],
    currentTile: 0,
    playerTile: -1,
    hintText: '',
    hintVisible: false
  },

  config: {
    gameDuration: 60,
    baseScore: 10,
    missPenalty: 5,
    perfectBonus: 5,
    maxCombo: 10
  },

  timer: null,

  onLoad(options) {
    this.setData({ gameMode: options.mode || 'challenge' });
    this.initTiles();
  },

  onUnload() {
    if (this.timer) clearInterval(this.timer);
  },

  initTiles() {
    const tiles = [];
    for (let i = 0; i < 7; i++) {
      tiles.push({ id: i, status: 'normal', number: i + 1 });
    }
    tiles[0].status = 'current';
    this.setData({ tiles, currentTile: 0 });
  },

  startGame() {
    if (this.data.gameStatus === 'playing') return;
    this.setData({
      gameStatus: 'playing',
      score: 0,
      timeLeft: this.config.gameDuration,
      combo: 0,
      playerTile: -1,
      hintVisible: false
    });
    this.initTiles();
    this.timer = setInterval(() => this.tick(), 1000);
  },

  tick() {
    const timeLeft = this.data.timeLeft - 1;
    this.setData({ timeLeft });
    if (timeLeft <= 0) this.endGame();
  },

  onTileTap(e) {
    const tileId = e.currentTarget.dataset.id;
    if (this.data.gameStatus === 'ready') {
      this.startGame();
      return;
    }
    if (this.data.gameStatus !== 'playing') return;
    if (tileId === this.data.currentTile) {
      this.handleLand(tileId);
    } else if (tileId !== this.data.playerTile) {
      this.handleMiss();
    }
  },

  handleLand(tileId) {
    const { tiles, currentTile, combo, score } = this.data;
    let addScore = this.config.baseScore;
    let newCombo = combo + 1;
    let hintText = '+' + addScore;

    if (newCombo > 1) {
      const bonus = Math.min(newCombo, this.config.maxCombo) * this.config.perfectBonus;
      addScore += bonus;
      hintText = '+' + addScore + ' 连击x' + newCombo;
    }

    const newTiles = [...tiles];
    newTiles[currentTile].status = 'landed';
    newTiles[tileId].status = 'landed';

    const available = newTiles.filter((t, i) => i !== tileId);
    const nextTile = available[Math.floor(Math.random() * available.length)];
    const nextId = nextTile ? nextTile.id : (tileId === 6 ? 0 : tileId + 1);
    newTiles[nextId].status = 'current';

    this.setData({
      tiles: newTiles,
      currentTile: nextId,
      playerTile: tileId,
      score: score + addScore,
      combo: newCombo,
      hintText: hintText,
      hintVisible: true
    });

    setTimeout(() => this.setData({ hintVisible: false }), 500);
  },

  handleMiss() {
    const { combo, score, tiles, currentTile } = this.data;
    const newTiles = [...tiles];
    newTiles[currentTile].status = 'current';
    this.setData({
      tiles: newTiles,
      combo: 0,
      score: Math.max(0, score - this.config.missPenalty),
      hintText: '-' + this.config.missPenalty + ' 稳住！',
      hintVisible: true
    });
    setTimeout(() => this.setData({ hintVisible: false }), 500);
  },

  endGame() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
    this.setData({ gameStatus: 'ended' });
    app.saveHighestScore(this.data.score);
    setTimeout(() => {
      wx.redirectTo({
        url: '/pages/result/result?score=' + this.data.score + '&mode=' + this.data.gameMode
      });
    }, 500);
  },

  onShareAppMessage() {
    return {
      title: '我在童年跳房子玩了' + this.data.score + '分，敢来挑战我吗？',
      path: '/pages/index/index?pkScore=' + this.data.score
    };
  }
})