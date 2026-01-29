// Medallion: Bronze | Mutation: 0% | HIVE: V
/* Medallion: Bronze | Mutation: 0% | HIVE: V */

(function () {
  'use strict';

  const MESSAGE_TYPE = 'hfo:nematocyst';

  const clampString = (value, fallback = '') => (typeof value === 'string' ? value : fallback);

  const tryFocusInner = (frameEl) => {
    try {
      frameEl?.contentWindow?.focus?.();
    } catch (_) {
      // ignore
    }
    try {
      frameEl?.contentDocument?.body?.focus?.();
    } catch (_) {
      // ignore
    }
  };

  const dispatchKey = (frameEl, eventType, { key, code }) => {
    if (!frameEl) return false;

    tryFocusInner(frameEl);

    const doc = frameEl.contentDocument;
    const win = frameEl.contentWindow;

    if (!doc || !win) return false;

    const opts = {
      key: clampString(key, ' '),
      code: clampString(code, 'Space'),
      keyCode: 32,
      which: 32,
      bubbles: true,
      cancelable: true
    };

    const ev = new KeyboardEvent(eventType, opts);

    try {
      win.dispatchEvent(ev);
      doc.dispatchEvent(ev);
      doc.body?.dispatchEvent?.(ev);

      return true;
    } catch (_) {
      return false;
    }
  };

  const dispatchKeypress = (frameEl, { key, code }) => {
    // Legacy behavior: a "keypress" maps to down+up.
    const okDown = dispatchKey(frameEl, 'keydown', { key, code });
    const okUp = dispatchKey(frameEl, 'keyup', { key, code });
    return !!(okDown && okUp);
  };

  const inject = (payload, frameEl) => {
    if (!payload || typeof payload !== 'object') return { ok: false, reason: 'payload_missing' };

    const kind = clampString(payload.kind);
    const action = clampString(payload.action);

    if (kind !== 'keyboard') return { ok: false, reason: 'unsupported_kind' };

    const key = clampString(payload.key, ' ');
    const code = clampString(payload.code, 'Space');

    let ok = false;
    if (action === 'keypress') {
      ok = dispatchKeypress(frameEl, { key, code });
    } else if (action === 'keydown') {
      ok = dispatchKey(frameEl, 'keydown', { key, code });
    } else if (action === 'keyup') {
      ok = dispatchKey(frameEl, 'keyup', { key, code });
    } else {
      return { ok: false, reason: 'unsupported_action' };
    }

    return { ok };
  };

  const init = () => {
    const frameEl = document.getElementById('frame');
    if (!frameEl) return;

    window.addEventListener('message', (event) => {
      // Same-origin only: fail-closed unless event.origin matches.
      try {
        if (event.origin !== window.location.origin) return;
      } catch (_) {
        return;
      }

      const data = event.data;
      if (!data || typeof data !== 'object') return;
      if (data.type !== MESSAGE_TYPE) return;

      const result = inject(data.payload, frameEl);

      const traceId =
        typeof data.traceId === 'string'
          ? data.traceId
          : data && data.payload && typeof data.payload.traceId === 'string'
            ? data.payload.traceId
            : null;

      // Best-effort ack; parent may ignore.
      try {
        event.source?.postMessage?.(
          {
            type: `${MESSAGE_TYPE}:ack`,
            traceId,
            payload: Object.assign({}, result, traceId ? { traceId } : {}),
          },
          event.origin,
        );
      } catch (_) {
        // ignore
      }
    });
  };

  init();
})();
