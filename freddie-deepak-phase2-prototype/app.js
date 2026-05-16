/* Freddie Deepak Phase 2 Prototype — Router (fork of Phase 1; email-first) */

(function () {
  'use strict';

  const DEFAULT_SCENE = 's2-menu';
  const TRANSITION_MS = 240;
  const DONE_KEY = 'fdp2_done_features';

  const stage = document.querySelector('.stage');
  const prevBtn = document.querySelector('[data-nav="prev"]');
  const nextBtn = document.querySelector('[data-nav="next"]');
  const exitBtn = document.querySelector('[data-nav="exit"]');
  const counterEl = document.querySelector('.counter-label');
  const channelTabs = document.querySelectorAll('.channel-tabs button');
  const payoffEl = document.getElementById('chrome-payoff');
  const progressFill = document.getElementById('chrome-progress-fill');
  const progressLabel = document.getElementById('chrome-progress-label');
  const progressBar = document.querySelector('.chrome-progress');

  let autoAdvanceTimer = null;

  if (!stage) { console.error('[fdp2] missing .stage'); return; }

  function clearAutoAdvance() {
    if (autoAdvanceTimer) {
      clearTimeout(autoAdvanceTimer);
      autoAdvanceTimer = null;
    }
  }

  function prefersReducedMotion() {
    try {
      return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch (e) {
      return false;
    }
  }

  function scheduleAutoAdvance(sceneEl) {
    clearAutoAdvance();
    if (!sceneEl || prefersReducedMotion()) return;
    const rawMs = sceneEl.dataset.autoAdvanceMs;
    const dest = sceneEl.dataset.autoAdvanceTo;
    if (!rawMs || !dest) return;
    const ms = parseInt(rawMs, 10);
    if (!ms || ms < 800) return;
    const sceneId = sceneEl.dataset.scene;
    autoAdvanceTimer = setTimeout(function () {
      autoAdvanceTimer = null;
      if (currentSceneId !== sceneId) return;
      if (readHash() !== sceneId) return;
      setHash(dest);
    }, ms);
  }

  function payoffText(sceneId, scene) {
    const overrides = window.FDPX_DATA && window.FDPX_DATA.scenePayoffs;
    if (overrides && overrides[sceneId]) return overrides[sceneId];
    const f = scene.dataset.feature;
    const title = scene.dataset.title || '';
    if (f && window.FDPX_DATA && window.FDPX_DATA.features) {
      const feat = window.FDPX_DATA.features.find(function (x) { return x.num === f; });
      if (feat && title) return feat.name + ' — ' + title + '.';
      if (feat) return feat.tagline;
    }
    if (title) return title + ' — follow the highlighted control.';
    return '';
  }

  function markFeatureProgressFromScene(sceneId) {
    var m = sceneId.match(/^s2(\d{2})-outro$/);
    if (!m) return;
    var raw = sessionStorage.getItem(DONE_KEY) || '';
    var set = new Set(raw.split(',').filter(Boolean));
    set.add(m[1]);
    sessionStorage.setItem(DONE_KEY, Array.from(set).sort().join(','));
  }

  function syncMenuDoneStates() {
    var grid = document.getElementById('feature-menu');
    if (!grid) return;
    var done = (sessionStorage.getItem(DONE_KEY) || '').split(',').filter(Boolean);
    grid.querySelectorAll('.menu-tile[data-feature-num]').forEach(function (tile) {
      var n = tile.getAttribute('data-feature-num');
      tile.classList.toggle('menu-tile--done', done.indexOf(n) !== -1);
    });
  }

  const allScenes = Array.from(stage.querySelectorAll('.scene[data-scene]'));
  const sceneIds = allScenes.map(s => s.dataset.scene);
  window.__fdp2_sceneIds = sceneIds;

  function validateGraph() {
    const idSet = new Set(sceneIds);
    const hotspots = stage.querySelectorAll('[data-advance-to]');
    let missing = 0;
    hotspots.forEach(h => {
      const target = h.dataset.advanceTo;
      if (target && target !== 's-exit' && !idSet.has(target)) {
        console.warn('[fdp2] missing target scene:', target, 'from', h.closest('.scene')?.dataset.scene);
        missing++;
      }
    });
    if (missing === 0) console.info('[fdp2] scene graph OK ·', sceneIds.length, 'scenes');
    else console.warn('[fdp2] scene graph has', missing, 'broken edges');
  }

  function validateCids() {
    const allowedBaseline = new Set();
    for (let i = 1; i <= 96; i++) allowedBaseline.add('C-' + String(i).padStart(2, '0'));
    for (let i = 97; i <= 105; i++) allowedBaseline.add('C-' + String(i).padStart(2, '0'));
    const cidsInDom = new Set();
    stage.querySelectorAll('[data-cid]').forEach(el => {
      const raw = el.dataset.cid;
      raw.split(/[, ]+/).forEach(c => c && cidsInDom.add(c));
    });
    let bad = 0;
    cidsInDom.forEach(cid => {
      const base = cid.split('/')[0];
      if (!allowedBaseline.has(base)) {
        console.warn('[fdp2] unknown C-ID in DOM:', cid);
        bad++;
      }
    });
    if (bad === 0) console.info('[fdp2] C-ID inventory OK ·', cidsInDom.size, 'unique refs');
  }

  let currentSceneId = null;

  function getScene(id) {
    return stage.querySelector('.scene[data-scene="' + id + '"]');
  }

  function showScene(id, opts = {}) {
    const target = getScene(id);
    if (!target) {
      console.warn('[fdp2] no scene with id', id, '— falling back to', DEFAULT_SCENE);
      id = DEFAULT_SCENE;
      return showScene(DEFAULT_SCENE);
    }

    clearAutoAdvance();
    const previous = currentSceneId ? getScene(currentSceneId) : null;
    if (previous === target) return;

    if (previous) {
      previous.style.opacity = '0';
      previous.style.transform = 'translateY(8px)';
      setTimeout(() => {
        previous.hidden = true;
        previous.style.opacity = '';
        previous.style.transform = '';
      }, TRANSITION_MS);
    }

    setTimeout(() => {
      target.hidden = false;
      void target.offsetHeight;
      target.style.opacity = '0';
      target.style.transform = 'translateY(10px)';
      requestAnimationFrame(() => {
        target.style.opacity = '1';
        target.style.transform = 'translateY(0)';
      });

      const hotspot = target.querySelector('[data-advance-to]');
      if (hotspot && !opts.noFocus) hotspot.focus({ preventScroll: false });

      window.scrollTo({
        top: 0,
        behavior: (opts.smooth === false || prefersReducedMotion()) ? 'auto' : 'smooth'
      });

      scheduleAutoAdvance(target);
    }, previous ? TRANSITION_MS : 0);

    currentSceneId = id;
    markFeatureProgressFromScene(id);
    updateChrome(target);
    updateChannelTabs(target);
  }

  function updateChrome(scene) {
    if (counterEl) {
      const f = scene.dataset.feature;
      const step = scene.dataset.step;
      const of = scene.dataset.of;
      const title = scene.dataset.title || '';
      if (f && step && of) {
        counterEl.innerHTML =
          '<strong>Feature ' + f + '</strong> &middot; ' +
          'Scene <strong>' + step + ' of ' + of + '</strong>' +
          (title ? ' &middot; ' + title : '');
      } else if (title) {
        counterEl.innerHTML = '<strong>' + title + '</strong>';
      } else {
        counterEl.textContent = '';
      }
    }

    if (payoffEl) {
      payoffEl.textContent = payoffText(currentSceneId, scene);
    }

    const idx = sceneIds.indexOf(currentSceneId);
    const pct = sceneIds.length > 1 ? Math.round((idx / (sceneIds.length - 1)) * 100) : 100;
    if (progressFill) progressFill.style.width = pct + '%';
    if (progressBar) progressBar.setAttribute('aria-valuenow', String(pct));
    if (progressLabel) progressLabel.textContent = 'Scene ' + (idx >= 0 ? idx + 1 : 0) + ' / ' + sceneIds.length;

    if (currentSceneId === 's2-menu') syncMenuDoneStates();

    if (prevBtn) prevBtn.disabled = idx <= 0;
    if (nextBtn) nextBtn.disabled = idx === -1 || idx >= sceneIds.length - 1;
  }

  function updateChannelTabs(scene) {
    if (!channelTabs.length) return;
    const channel = scene.dataset.channel || 'email';
    const variants = (scene.dataset.channelVariants || '').split(',').filter(Boolean);
    channelTabs.forEach(btn => {
      const ch = btn.dataset.channel;
      btn.classList.toggle('active', ch === channel);
      const available = ch === channel || variants.includes(ch);
      btn.disabled = !available;
      btn.dataset.targetVariant = available && ch !== channel ? variantSceneFor(scene.dataset.scene, ch) : '';
    });
  }

  function variantSceneFor(baseId, channel) {
    if (channel === 'email') {
      return baseId.replace(/-(sms|w)$/, '');
    }
    if (channel === 'sms') {
      const candidate = baseId.replace(/-(sms|w)$/, '') + '-sms';
      return getScene(candidate) ? candidate : '';
    }
    if (channel === 'whatsapp') {
      const candidate = baseId.replace(/-(sms|w)$/, '') + '-w';
      return getScene(candidate) ? candidate : '';
    }
    return '';
  }

  function readHash() {
    const h = (location.hash || '').replace(/^#/, '').trim();
    return h || DEFAULT_SCENE;
  }
  function setHash(id) {
    if (readHash() === id) {
      showScene(id);
    } else {
      location.hash = '#' + id;
    }
  }
  window.addEventListener('hashchange', () => showScene(readHash()));

  document.addEventListener('click', e => {
    const tile = e.target.closest('[data-jump-to]');
    if (tile) {
      e.preventDefault();
      setHash(tile.dataset.jumpTo);
      return;
    }
    const hotspot = e.target.closest('[data-advance-to]');
    if (hotspot) {
      e.preventDefault();
      const dest = hotspot.dataset.advanceTo;
      if (dest === 's-exit') {
        location.href = '../freddie-deepak-phase2.html';
        return;
      }
      setHash(dest);
      return;
    }
  });

  if (prevBtn) prevBtn.addEventListener('click', () => {
    const idx = sceneIds.indexOf(currentSceneId);
    if (idx > 0) setHash(sceneIds[idx - 1]);
  });
  if (nextBtn) nextBtn.addEventListener('click', () => {
    const idx = sceneIds.indexOf(currentSceneId);
    if (idx >= 0 && idx < sceneIds.length - 1) setHash(sceneIds[idx + 1]);
  });
  if (exitBtn) exitBtn.addEventListener('click', () => {
    location.href = '../freddie-deepak-phase2.html';
  });

  channelTabs.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.targetVariant;
      if (target) setHash(target);
    });
  });

  document.addEventListener('keydown', e => {
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) return;

    if (e.key === 'ArrowRight' || e.key === 'PageDown') {
      e.preventDefault();
      const idx = sceneIds.indexOf(currentSceneId);
      if (idx >= 0 && idx < sceneIds.length - 1) setHash(sceneIds[idx + 1]);
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      const idx = sceneIds.indexOf(currentSceneId);
      if (idx > 0) setHash(sceneIds[idx - 1]);
    } else if (e.key === 'Escape') {
      e.preventDefault();
      if (currentSceneId !== DEFAULT_SCENE) setHash(DEFAULT_SCENE);
    } else if (e.key === 'Home') {
      e.preventDefault();
      setHash(DEFAULT_SCENE);
    } else if (e.key === 'End') {
      e.preventDefault();
      setHash(sceneIds[sceneIds.length - 1]);
    }
  });

  function init() {
    allScenes.forEach(s => { s.hidden = true; });
    showScene(readHash(), { smooth: false });
    validateGraph();
    validateCids();
    console.info('[fdp2] Freddie Deepak Phase 2 Prototype ready ·', sceneIds.length, 'scenes');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
