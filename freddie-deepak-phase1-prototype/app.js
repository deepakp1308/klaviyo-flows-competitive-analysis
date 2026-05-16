/* =========================================================================
   Freddie Deepak's Phase 1 Prototype — Router + Scene Manager
   v1.0 · May 2026

   Responsibilities:
   - hash-routing (#s05-3 etc.) with deep-link support
   - Prev / Next / Esc keyboard nav
   - advance-hotspot click → next scene
   - top-chrome counter sync (feature N · scene X of Y)
   - scene-graph validator (logs missing successors on load)
   - channel-tab switch where data-channel-variants exists
   ========================================================================= */

(function () {
  'use strict';

  // ----- Constants ---------------------------------------------------------
  const DEFAULT_SCENE = 's-menu';
  const TRANSITION_MS = 240;

  // ----- DOM hooks ---------------------------------------------------------
  const stage      = document.querySelector('.stage');
  const prevBtn    = document.querySelector('[data-nav="prev"]');
  const nextBtn    = document.querySelector('[data-nav="next"]');
  const exitBtn    = document.querySelector('[data-nav="exit"]');
  const counterEl  = document.querySelector('.counter-label');
  const channelTabs = document.querySelectorAll('.channel-tabs button');

  if (!stage) { console.error('[fdpx] missing .stage'); return; }

  // ----- Scene index -------------------------------------------------------
  // Build a list of every scene id in DOM order; expose for debugging.
  const allScenes = Array.from(stage.querySelectorAll('.scene[data-scene]'));
  const sceneIds = allScenes.map(s => s.dataset.scene);
  window.__fdpx_sceneIds = sceneIds;

  // ----- Scene-graph validator (G2) ----------------------------------------
  // Each scene has a data-advance-to (success path) and inherits prev by order.
  function validateGraph() {
    const idSet = new Set(sceneIds);
    const hotspots = stage.querySelectorAll('[data-advance-to]');
    let missing = 0;
    hotspots.forEach(h => {
      const target = h.dataset.advanceTo;
      if (target && target !== 's-exit' && !idSet.has(target)) {
        console.warn('[fdpx] missing target scene:', target, 'from', h.closest('.scene')?.dataset.scene);
        missing++;
      }
    });
    if (missing === 0) console.info('[fdpx] scene graph OK ·', sceneIds.length, 'scenes');
    else console.warn('[fdpx] scene graph has', missing, 'broken edges');
  }

  // ----- C-XX inventory audit (G4) -----------------------------------------
  function validateCids() {
    const allowedBaseline = new Set(); // C-01..C-96
    for (let i = 1; i <= 96; i++) allowedBaseline.add('C-' + String(i).padStart(2, '0'));
    allowedBaseline.add('C-97'); // the one approved new C-ID
    const cidsInDom = new Set();
    stage.querySelectorAll('[data-cid]').forEach(el => {
      const raw = el.dataset.cid;
      raw.split(/[, ]+/).forEach(c => c && cidsInDom.add(c));
    });
    let bad = 0;
    cidsInDom.forEach(cid => {
      // Variant form: C-XX/v.label
      const base = cid.split('/')[0];
      if (!allowedBaseline.has(base)) {
        console.warn('[fdpx] unknown C-ID in DOM:', cid);
        bad++;
      }
    });
    if (bad === 0) console.info('[fdpx] C-ID inventory OK ·', cidsInDom.size, 'unique refs');
  }

  // ----- Scene visibility --------------------------------------------------
  let currentSceneId = null;

  function getScene(id) {
    return stage.querySelector('.scene[data-scene="' + id + '"]');
  }

  function showScene(id, opts = {}) {
    const target = getScene(id);
    if (!target) {
      console.warn('[fdpx] no scene with id', id, '— falling back to', DEFAULT_SCENE);
      id = DEFAULT_SCENE;
      return showScene(DEFAULT_SCENE);
    }

    const previous = currentSceneId ? getScene(currentSceneId) : null;
    if (previous === target) return;

    // Fade-out previous
    if (previous) {
      previous.style.opacity = '0';
      setTimeout(() => { previous.hidden = true; previous.style.opacity = ''; }, TRANSITION_MS);
    }

    // Fade-in target after the fade-out window
    setTimeout(() => {
      target.hidden = false;
      // force reflow so the opacity transition runs
      void target.offsetHeight;
      target.style.opacity = '1';

      // Focus the advance hotspot for keyboard users
      const hotspot = target.querySelector('[data-advance-to]');
      if (hotspot && !opts.noFocus) hotspot.focus({ preventScroll: false });

      // Scroll to top of stage
      window.scrollTo({ top: 0, behavior: opts.smooth === false ? 'auto' : 'smooth' });
    }, previous ? TRANSITION_MS : 0);

    currentSceneId = id;
    updateChrome(target);
    updateChannelTabs(target);
  }

  // ----- Chrome counter ----------------------------------------------------
  function updateChrome(scene) {
    if (!counterEl) return;
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

    // Prev/Next disabled at boundaries
    const idx = sceneIds.indexOf(currentSceneId);
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
      // Disable tabs without a registered variant
      const available = ch === channel || variants.includes(ch);
      btn.disabled = !available;
      btn.dataset.targetVariant = available && ch !== channel ? variantSceneFor(scene.dataset.scene, ch) : '';
    });
  }

  function variantSceneFor(baseId, channel) {
    // Convention: variants are sibling scenes named like "s05-3-sms" or "s01-3-w"
    if (channel === 'email') {
      // strip any -sms or -w suffix to get back to base
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

  // ----- Hash routing ------------------------------------------------------
  function readHash() {
    const h = (location.hash || '').replace(/^#/, '').trim();
    return h || DEFAULT_SCENE;
  }
  function setHash(id) {
    if (readHash() === id) {
      // Same hash — fire showScene directly
      showScene(id);
    } else {
      location.hash = '#' + id;
    }
  }
  window.addEventListener('hashchange', () => showScene(readHash()));

  // ----- Click delegation --------------------------------------------------
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
        location.href = '../freddie-deepak-phase1.html';
        return;
      }
      setHash(dest);
      return;
    }
  });

  // ----- Nav buttons -------------------------------------------------------
  if (prevBtn) prevBtn.addEventListener('click', () => {
    const idx = sceneIds.indexOf(currentSceneId);
    if (idx > 0) setHash(sceneIds[idx - 1]);
  });
  if (nextBtn) nextBtn.addEventListener('click', () => {
    const idx = sceneIds.indexOf(currentSceneId);
    if (idx >= 0 && idx < sceneIds.length - 1) setHash(sceneIds[idx + 1]);
  });
  if (exitBtn) exitBtn.addEventListener('click', () => {
    location.href = '../freddie-deepak-phase1.html';
  });

  // ----- Channel tab switch ------------------------------------------------
  channelTabs.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.targetVariant;
      if (target) setHash(target);
    });
  });

  // ----- Keyboard nav (G7 a11y) --------------------------------------------
  document.addEventListener('keydown', e => {
    // Skip when typing in an input
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

  // ----- Initial render ----------------------------------------------------
  function init() {
    // Hide all scenes, then show the routed one
    allScenes.forEach(s => { s.hidden = true; });
    showScene(readHash(), { smooth: false });
    validateGraph();
    validateCids();
    console.info('[fdpx] Freddie Deepak Phase 1 Prototype ready ·', sceneIds.length, 'scenes loaded');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
