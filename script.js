const SAVE_KEY = 'pathsOfScripture_save';

const gameState = {
  faith: 50,
  wisdom: 50,
  humility: 50,
  currentScene: 'menu',
  inCombat: false,
  combat: {
    playerHealth: 100,
    enemyHealth: 100,
    enemy: null,
    log: []
  }
};

const scenes = {
  intro: {
    text: 'In the beginning, after Eden, two brothers worked the land. The earth was new, but sin was already crouching at the door...',
    character: { name: 'Narrator', emoji: '📜' },
    background: 'linear-gradient(to bottom, #1a1a2e 0%, #2d1b4e 100%)',
    next: 'cain_offering'
  },

  cain_offering: {
    text: "You are Cain. Your offering is rejected while Abel's is accepted. Anger burns in your chest like fire.",
    character: { name: 'Cain', emoji: '🌾' },
    background: 'linear-gradient(to bottom, #2d1b4e 0%, #3d1b1b 100%)',
    choices: [
      { text: 'Let anger consume you', next: 'cain_combat', effect: { humility: -10 } },
      { text: 'Ask God why', next: 'cain_wisdom', effect: { faith: +10, wisdom: +5 } },
      { text: 'Suppress the feeling', next: 'cain_suppress', effect: { humility: -5 } }
    ]
  },

  cain_combat: {
    type: 'combat',
    enemy: { name: 'Anger', emoji: '👿', health: 100, damage: 20 },
    win: 'cain_victory',
    lose: 'cain_defeat'
  },

  cain_victory: {
    text: 'Through prayer and faith, you mastered your anger. The spirit of rage dissipates like morning fog.',
    character: { name: 'Cain', emoji: '🙏' },
    background: 'linear-gradient(to bottom, #2d3b1b 0%, #1a2d1b 100%)',
    next: 'cain_redemption'
  },

  cain_redemption: {
    text: '🎓 REDEMPTION: You chose a better path. Abel lives. The cycle is broken. You learned that sin can be mastered before it masters you.',
    character: { name: 'Cain', emoji: '✨' },
    background: 'linear-gradient(to bottom, #d4af37 0%, #c9a227 100%)',
    choices: [{ text: 'Play Again', next: 'intro' }]
  },

  cain_defeat: {
    text: 'The anger consumed you. You raise your hand against your brother... and the first murder stains the earth.',
    character: { name: 'God', emoji: '⚡' },
    background: 'linear-gradient(to bottom, #1a0000 0%, #000 100%)',
    next: 'cain_lesson'
  },

  cain_lesson: {
    text: '🎓 LESSON: Unmastered sin leads to destruction. But even in judgment, God showed mercy-marking Cain for protection.',
    character: { name: 'God', emoji: '🛡️' },
    background: 'linear-gradient(to bottom, #4a3b5c 0%, #2d1b4e 100%)',
    choices: [{ text: 'Try Again', next: 'intro' }]
  },

  cain_wisdom: {
    text: "God speaks: 'If you do what is right, will you not be accepted? Sin crouches at your door - you must master it.'",
    character: { name: 'God', emoji: '☁️' },
    background: 'linear-gradient(to bottom, #1a2d3b 0%, #2d3b1b 100%)',
    next: 'cain_redemption'
  },

  cain_suppress: {
    text: 'You bury your anger deep. It festers. Grows. Until one day in the field...',
    character: { name: 'Cain', emoji: '😠' },
    background: 'linear-gradient(to bottom, #3d1b1b 0%, #1a0000 100%)',
    next: 'cain_combat'
  },

  joseph_intro: {
    text: 'Years later, Joseph is sold into slavery. He stands in a foreign land without comfort, with only God in his heart.',
    character: { name: 'Joseph', emoji: '🧵' },
    background: 'linear-gradient(to bottom, #1d243d 0%, #2d3b56 100%)',
    choices: [
      { text: 'Trust God in the dark', next: 'joseph_justice', effect: { faith: +12, wisdom: +6 } },
      { text: 'Become bitter', next: 'joseph_bitter', effect: { humility: -8, faith: -5 } },
      { text: 'Hide your hurt', next: 'joseph_endurance', effect: { humility: +4, wisdom: +3 } }
    ]
  },

  joseph_justice: {
    text: 'Joseph keeps integrity when Potiphar’s wife tempts him. His faith remains steady, even when false accusation follows.',
    character: { name: 'Joseph', emoji: '🛡️' },
    background: 'linear-gradient(to bottom, #1f3b2b 0%, #163328 100%)',
    next: 'david_intro'
  },

  joseph_bitter: {
    text: 'Bitterness grows in the prison cell. You carry resentment instead of trust, and the wound deepens.',
    character: { name: 'Joseph', emoji: '😔' },
    background: 'linear-gradient(to bottom, #2f1a23 0%, #190b12 100%)',
    next: 'david_intro'
  },

  joseph_endurance: {
    text: 'You learn to wait quietly. Joseph does not boast; he serves, and in time God lifts him.',
    character: { name: 'Joseph', emoji: '🌱' },
    background: 'linear-gradient(to bottom, #1f2e38 0%, #233c46 100%)',
    next: 'david_intro'
  },

  david_intro: {
    text: 'David stands before Goliath. The giant dares the armies of Israel, but the shepherd has a different kind of courage.',
    character: { name: 'David', emoji: '🏹' },
    background: 'linear-gradient(to bottom, #2d1b4e 0%, #1a2536 100%)',
    choices: [
      { text: 'Trust in God’s power', next: 'david_trust', effect: { faith: +10, wisdom: +8 } },
      { text: 'Measure by fear', next: 'david_fear', effect: { faith: -8, humility: -6 } },
      { text: 'Fight in your own strength', next: 'david_combat', effect: { wisdom: -4 } }
    ]
  },

  david_combat: {
    type: 'combat',
    enemy: { name: 'Goliath', emoji: '🪖', health: 110, damage: 24 },
    win: 'david_trust',
    lose: 'david_fear'
  },

  david_trust: {
    text: 'David picks up five stones, but the real strength was not in the sling — it was in holy trust.',
    character: { name: 'David', emoji: '✨' },
    background: 'linear-gradient(to bottom, #173d2a 0%, #1b5e43 100%)',
    next: 'daniel_intro'
  },

  david_fear: {
    text: 'Fear grows larger than faith. The giant seems unstoppable when your eyes are fixed on him rather than God.',
    character: { name: 'David', emoji: '😟' },
    background: 'linear-gradient(to bottom, #2d1a1a 0%, #1e0d0d 100%)',
    next: 'daniel_intro'
  },

  daniel_intro: {
    text: 'Daniel is cast into a kingdom of power and pressure. The lion’s den waits for those who do not bow away from God.',
    character: { name: 'Daniel', emoji: '🦁' },
    background: 'linear-gradient(to bottom, #20314f 0%, #10273e 100%)',
    choices: [
      { text: 'Pray without turning away', next: 'daniel_prayer', effect: { faith: +14, humility: +6 } },
      { text: 'Compromise for safety', next: 'daniel_compromise', effect: { faith: -10, wisdom: -8 } },
      { text: 'Quietly serve', next: 'daniel_service', effect: { humility: +8, wisdom: +4 } }
    ]
  },

  daniel_prayer: {
    text: 'Daniel kneels and prays. The lions are not more powerful than the God who protects the faithful.',
    character: { name: 'Daniel', emoji: '🙏' },
    background: 'linear-gradient(to bottom, #1d2d3d 0%, #204862 100%)',
    next: 'final_reflection'
  },

  daniel_compromise: {
    text: 'You choose comfort over obedience. The path feels safe at first, but it twists the heart away from truth.',
    character: { name: 'Daniel', emoji: '⚠️' },
    background: 'linear-gradient(to bottom, #2a1e1a 0%, #17110f 100%)',
    next: 'final_reflection'
  },

  daniel_service: {
    text: 'Daniel keeps humility and service at the center. That posture leads to wisdom and favor.',
    character: { name: 'Daniel', emoji: '🌟' },
    background: 'linear-gradient(to bottom, #2f3557 0%, #1b2948 100%)',
    next: 'final_reflection'
  },

  final_reflection: {
    text: 'The path of Scripture is not a single moment, but a lifetime of choosing faith over fear, wisdom over pride, and humility over self.',
    character: { name: 'Narrator', emoji: '📖' },
    background: 'linear-gradient(to bottom, #1f1d27 0%, #41355d 100%)',
    choices: [{ text: 'Begin a new journey', next: 'intro' }]
  }
};

const storyOrder = ['intro', 'cain_offering', 'cain_wisdom', 'cain_suppress', 'cain_combat', 'cain_victory', 'cain_redemption', 'joseph_intro', 'joseph_justice', 'joseph_bitter', 'joseph_endurance', 'david_intro', 'david_trust', 'david_fear', 'david_combat', 'daniel_intro', 'daniel_prayer', 'daniel_compromise', 'daniel_service', 'final_reflection'];

const titleEl = document.getElementById('title');
const menuScreen = document.getElementById('menu-screen');
const sceneEl = document.getElementById('scene');
const dialogueText = document.getElementById('dialogue-text');
const choicesEl = document.getElementById('choices');
const continueBtn = document.getElementById('continue-btn');
const characterEl = document.getElementById('character');
const characterEmoji = document.getElementById('character-emoji');
const characterNameEl = document.getElementById('character-name');
const combatScreen = document.getElementById('combat-screen');
const combatLog = document.getElementById('combat-log');

let audioContext = null;
let musicEnabled = true;

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function updateStats() {
  document.getElementById('faith-stat').textContent = gameState.faith;
  document.getElementById('wisdom-stat').textContent = gameState.wisdom;
  document.getElementById('humility-stat').textContent = gameState.humility;
}

function safeSaveGame() {
  try {
    const { combat, ...rest } = gameState;
    localStorage.setItem(SAVE_KEY, JSON.stringify({ ...rest, currentScene: gameState.currentScene }));
  } catch (error) {
    console.warn('Could not save game', error);
  }
}

function saveGame() {
  safeSaveGame();
}

function startGame() {
  transitionTo(() => {
    menuScreen.classList.add('hidden');
    showScene('intro');
    ensureAudio();
    playMusicLoop();
  });
}

function loadGame() {
  try {
    const saved = localStorage.getItem(SAVE_KEY);
    if (!saved) {
      alert('No saved game found.');
      return;
    }

    const data = JSON.parse(saved);
    gameState.faith = clamp(Number(data.faith) || 50, 0, 100);
    gameState.wisdom = clamp(Number(data.wisdom) || 50, 0, 100);
    gameState.humility = clamp(Number(data.humility) || 50, 0, 100);
    gameState.currentScene = data.currentScene || 'intro';
    updateStats();

    transitionTo(() => {
      menuScreen.classList.add('hidden');
      showScene(gameState.currentScene || 'intro');
      ensureAudio();
      playMusicLoop();
    });
  } catch (error) {
    console.warn('Could not load saved game', error);
    alert('The saved game could not be loaded.');
  }
}

function transitionTo(callback) {
  const overlay = document.getElementById('page-transition');
  overlay.classList.add('active', 'wipe');

  setTimeout(() => {
    callback();
    setTimeout(() => {
      overlay.classList.remove('active', 'wipe');
    }, 100);
  }, 500);
}

function createParticles(x, y, count = 10, type = 'sparkle') {
  const container = document.getElementById('game-container');
  for (let i = 0; i < count; i += 1) {
    const particle = document.createElement('div');
    particle.className = `particle ${type}`;
    particle.style.left = `${x + (Math.random() - 0.5) * 80}px`;
    particle.style.top = `${y + (Math.random() - 0.5) * 80}px`;
    particle.style.animationDelay = `${(Math.random() * 0.5).toFixed(2)}s`;
    container.appendChild(particle);
    setTimeout(() => particle.remove(), 2000);
  }
}

function flashLightning() {
  const lightning = document.getElementById('lightning');
  lightning.classList.add('flash');
  setTimeout(() => lightning.classList.remove('flash'), 200);

  if (Math.random() > 0.5) {
    setTimeout(() => {
      lightning.classList.add('flash');
      setTimeout(() => lightning.classList.remove('flash'), 200);
    }, 300);
  }
}

function ensureAudio() {
  if (!audioContext) {
    const AudioCtor = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtor) return;
    audioContext = new AudioCtor();
  }

  if (audioContext.state === 'suspended') {
    audioContext.resume();
  }
}

function playTone(frequency, duration = 0.2, type = 'sine', volume = 0.025) {
  if (!audioContext || !musicEnabled) return;

  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();
  oscillator.type = type;
  oscillator.frequency.value = frequency;
  gainNode.gain.value = volume;
  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);
  oscillator.start();
  gainNode.gain.exponentialRampToValueAtTime(0.0001, audioContext.currentTime + duration);
  oscillator.stop(audioContext.currentTime + duration);
}

let musicLoopTimer = null;

function playMusicLoop() {
  if (!musicEnabled || !audioContext) return;

  const notes = [220, 277, 329.63, 392, 329.63, 277, 220];

  function step(index) {
    const note = notes[index % notes.length];
    playTone(note, 0.25, 'sine', 0.018);
    playTone(note / 2, 0.2, 'triangle', 0.012);
    musicLoopTimer = setTimeout(() => step(index + 1), 420);
  }

  clearTimeout(musicLoopTimer);
  step(0);
}

function toggleMusic() {
  const button = document.getElementById('music-toggle');
  musicEnabled = !musicEnabled;
  ensureAudio();

  if (musicEnabled) {
    button.textContent = '🎵';
    button.setAttribute('aria-label', 'Toggle background music');
    playTone(220, 0.2, 'sine', 0.04);
    playMusicLoop();
  } else {
    button.textContent = '🔇';
    button.setAttribute('aria-label', 'Enable background music');
    clearTimeout(musicLoopTimer);
  }
}

function applyChoiceEffects(effect) {
  if (!effect) return;

  Object.entries(effect).forEach(([stat, value]) => {
    if (!gameState[stat] && gameState[stat] !== 0) return;

    gameState[stat] = clamp(gameState[stat] + value, 0, 100);
    const statEl = document.getElementById(`${stat}-stat`);
    const stateBox = document.getElementById(`stat-${stat}`);
    if (statEl) statEl.textContent = gameState[stat];
    if (stateBox) {
      stateBox.classList.add('changed');
      setTimeout(() => stateBox.classList.remove('changed'), 500);
    }
  });
}

function showScene(sceneId) {
  gameState.currentScene = sceneId;
  const scene = scenes[sceneId];

  if (!scene) {
    console.error(`Scene not found: ${sceneId}`);
    return;
  }

  sceneEl.classList.add('transitioning');
  setTimeout(() => {
    sceneEl.style.background = scene.background || 'linear-gradient(to bottom, #1a1a2e 0%, #2d1b4e 100%)';
    dialogueText.textContent = scene.text;

    if (scene.character) {
      characterEl.classList.remove('exit');
      characterEl.classList.add('enter', 'active');
      characterNameEl.textContent = scene.character.name;
      characterNameEl.classList.remove('hidden');
      characterEmoji.textContent = scene.character.emoji;

      if (sceneId.includes('angry') || sceneId.includes('combat')) {
        characterEl.classList.add('angry');
        setTimeout(() => characterEl.classList.remove('angry'), 500);
      }
    } else {
      characterEl.classList.remove('active');
      characterEl.classList.add('exit');
      setTimeout(() => characterNameEl.classList.add('hidden'), 500);
    }

    const choiceButtons = [];
    choicesEl.innerHTML = '';

    if (scene.type === 'combat') {
      continueBtn.classList.remove('hidden');
      if (continueBtn) {
        continueBtn.textContent = 'Fight the enemy →';
        continueBtn.onclick = () => startCombat(scene.enemy);
      }
      choicesEl.classList.add('hidden');
    } else if (scene.choices) {
      continueBtn.classList.add('hidden');
      choicesEl.classList.remove('hidden');

      scene.choices.forEach((choice, index) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'choice-btn';
        btn.innerHTML = `<span>${choice.text}</span>`;
        btn.onclick = () => {
          applyChoiceEffects(choice.effect);
          if ((choice.text || '').toLowerCase().includes('anger') || (choice.text || '').toLowerCase().includes('sin')) {
            flashLightning();
          }
          createParticles(window.innerWidth / 2, window.innerHeight / 2, 5);
          transitionTo(() => showScene(choice.next));
        };
        choicesEl.appendChild(btn);
        choiceButtons.push(btn);
        setTimeout(() => btn.classList.add('visible'), index * 90);
      });
    } else if (scene.next) {
      continueBtn.classList.remove('hidden');
      choicesEl.classList.add('hidden');
      continueBtn.textContent = 'Click to continue →';
      continueBtn.onclick = () => {
        createParticles(window.innerWidth / 2, window.innerHeight / 2, 3);
        transitionTo(() => showScene(scene.next));
      };
    }

    sceneEl.classList.remove('transitioning');

    if (scene.background.includes('1a0000') || scene.background.includes('3d1b1b')) {
      if (Math.random() > 0.7) setTimeout(flashLightning, 1000);
    }

    saveGame();
  }, 400);
}

function startCombat(enemyData) {
  gameState.inCombat = true;
  gameState.combat.enemy = enemyData;
  gameState.combat.playerHealth = 100;
  gameState.combat.enemyHealth = enemyData.health || 100;
  gameState.combat.log = [];

  document.getElementById('enemy-name').textContent = enemyData.name;
  document.getElementById('enemy-avatar').textContent = enemyData.emoji;
  combatScreen.classList.remove('hidden');
  updateCombatUI();

  const player = document.getElementById('player-combatant');
  const enemy = document.getElementById('enemy-combatant');
  player.style.animation = 'slideInUp 0.6s ease';
  enemy.style.animation = 'slideInUp 0.6s ease 0.2s both';

  const log = document.getElementById('combat-log');
  log.innerHTML = '<div style="color: #d4af37;">Battle begins...</div>';
}

function updateCombatUI() {
  const playerHealthEl = document.getElementById('player-health');
  const enemyHealthEl = document.getElementById('enemy-health');
  playerHealthEl.style.width = `${clamp(gameState.combat.playerHealth, 0, 100)}%`;
  enemyHealthEl.style.width = `${clamp(gameState.combat.enemyHealth, 0, 100)}%`;
}

function showDamageNumber(x, y, damage, type) {
  const num = document.createElement('div');
  num.className = `damage-number ${type}`;
  num.textContent = `-${damage}`;
  num.style.left = `${x}px`;
  num.style.top = `${y}px`;
  combatScreen.appendChild(num);
  setTimeout(() => num.remove(), 1500);
}

function combatAction(action) {
  if (!gameState.inCombat || !gameState.combat.enemy) return;

  const player = document.getElementById('player-combatant');
  const enemy = document.getElementById('enemy-combatant');
  const currentEnemy = gameState.combat.enemy;

  let playerDamage = 0;
  let enemyDamage = currentEnemy.damage || 18;
  let message = 'You strike with effort.';

  player.classList.add('attack');
  setTimeout(() => player.classList.remove('attack'), 500);

  switch (action) {
    case 'prayer':
      playerDamage = 24 + gameState.faith * 0.25;
      message = 'Your prayer cuts through the darkness.';
      break;
    case 'scripture':
      playerDamage = 18 + gameState.wisdom * 0.2;
      enemyDamage = Math.max(5, enemyDamage - 12);
      message = 'Scripture shields you and strikes back.';
      break;
    case 'faith':
      playerDamage = 34 + gameState.faith * 0.32;
      enemyDamage = Math.round(enemyDamage * 1.2);
      message = 'A leap of faith breaks the enemy’s armor.';
      player.classList.add('power-up');
      setTimeout(() => player.classList.remove('power-up'), 800);
      break;
    case 'heal':
      gameState.combat.playerHealth = Math.min(100, gameState.combat.playerHealth + 28 + gameState.humility * 0.1);
      playerDamage = 0;
      enemyDamage = Math.max(5, enemyDamage - 4);
      message = 'Divine healing restores your strength.';
      player.classList.add('heal-effect');
      setTimeout(() => player.classList.remove('heal-effect'), 1000);
      break;
    default:
      playerDamage = 10;
  }

  if (action !== 'heal') {
    gameState.combat.enemyHealth = clamp(gameState.combat.enemyHealth - playerDamage, 0, 100);
    showDamageNumber(window.innerWidth / 2 + 90, window.innerHeight / 2 - 40, Math.round(playerDamage), 'enemy');

    setTimeout(() => {
      enemy.classList.add('hit');
      setTimeout(() => enemy.classList.remove('hit'), 500);
    }, 250);
  }

  updateCombatUI();

  const logEl = document.getElementById('combat-log');
  logEl.innerHTML = `<div style="color: #d4af37; margin-bottom: 5px;">${message}</div>${logEl.innerHTML}`;

  if (gameState.combat.enemyHealth <= 0) {
    setTimeout(() => endCombat(true), 500);
    return;
  }

  setTimeout(() => {
    enemy.classList.add('attack');
    setTimeout(() => enemy.classList.remove('attack'), 500);

    gameState.combat.playerHealth = clamp(gameState.combat.playerHealth - enemyDamage, 0, 100);
    showDamageNumber(window.innerWidth / 2 - 90, window.innerHeight / 2 - 40, Math.round(enemyDamage), 'player');

    if (enemyDamage > 15) {
      document.getElementById('game-container').classList.add('shake');
      setTimeout(() => document.getElementById('game-container').classList.remove('shake'), 500);
    }

    updateCombatUI();

    if (gameState.combat.playerHealth <= 0) {
      setTimeout(() => endCombat(false), 500);
    }
  }, 800);
}

function endCombat(victory) {
  gameState.inCombat = false;
  combatScreen.classList.add('hidden');

  const currentScene = scenes[gameState.currentScene];
  const nextScene = victory ? currentScene.win : currentScene.lose;

  if (nextScene) {
    transitionTo(() => showScene(nextScene));
  }
}

window.addEventListener('beforeunload', saveGame);
window.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    const active = document.activeElement;
    if (active && active.tagName === 'BUTTON' && !active.classList.contains('menu-btn')) {
      active.click();
    }
  }
});

window.addEventListener('load', () => {
  updateStats();
  document.getElementById('music-toggle').addEventListener('click', toggleMusic);
  ensureAudio();
});

if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const style = document.createElement('style');
  style.textContent = `
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  `;
  document.head.appendChild(style);
}

updateStats();
