import { useEffect, useRef } from "react";
import { useMotionValueEvent, useReducedMotion } from "framer-motion";

/** Motion owns scroll sampling; canvas never changes React state while scrolling. */
export function ScrollScene({ progress, className = "" }) {
  const canvas = useRef(null);
  const render = useRef(() => {});
  const reduced = useReducedMotion();
  useMotionValueEvent(progress, "change", () => render.current());

  useEffect(() => {
    if (reduced) return;
    let disposed = false;
    let raf = 0;
    let lastFrame = -1;
    let width = 0, height = 0, dpr = 1;
    const node = canvas.current;
    const ctx = node?.getContext("2d", { alpha: false });
    if (!ctx) return;
    const images = new Array(60);
    const draw = () => {
      raf = 0;
      if (disposed || !width || !height || document.hidden) return;
      const desired = Math.min(59, Math.max(0, progress.get() * 59));
      const index = Math.round(desired);
      // Keep the last valid drawing while a frame decodes, then redraw on decode.
      let actual = index;
      if (!images[actual]) {
        actual = images.reduce((best, image, i) => image && (best < 0 || Math.abs(index - i) < Math.abs(index - best)) ? i : best, -1);
      }
      if (actual < 0 || actual === lastFrame) return;
      const image = images[actual];
      lastFrame = actual;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = "#d7d7ce";
      ctx.fillRect(0, 0, width, height);
      // Contain protects the building, dimensions and brand, especially on phones.
      const scale = Math.min(width / image.naturalWidth, height / image.naturalHeight);
      const w = image.naturalWidth * scale, h = image.naturalHeight * scale;
      ctx.drawImage(image, (width - w) / 2, (height - h) / 2, w, h);
      node.dataset.frame = String(actual + 1);
      node.style.opacity = "1";
    };
    const schedule = () => { if (!disposed && !raf) raf = requestAnimationFrame(draw); };
    render.current = schedule;
    const resize = () => {
      width = node.clientWidth; height = node.clientHeight;
      dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      node.width = Math.round(width * dpr); node.height = Math.round(height * dpr);
      lastFrame = -1;
      schedule();
    };
    const observer = new ResizeObserver(resize);
    observer.observe(node);
    // Four decode workers avoid a 60-image decode burst on the main thread.
    let next = 0;
    const priority = [0, 59, 30, 15, 45];
    const queue = [...priority, ...Array.from({ length: 60 }, (_, i) => i).filter(i => !priority.includes(i))];
    const assetPath = window.matchMedia("(max-width: 767px)").matches ? "/frames/mobile" : "/frames";
    const worker = async () => {
      while (!disposed && next < 60) {
        const index = queue[next++];
        const image = new Image();
        image.decoding = "async";
        image.src = `${assetPath}/${String(index + 1).padStart(2, "0")}.webp`;
        try { await image.decode(); } catch { continue; }
        if (!disposed) { images[index] = image; schedule(); }
      }
    };
    for (let i = 0; i < 4; i++) worker();
    document.addEventListener("visibilitychange", schedule);
    return () => {
      disposed = true;
      cancelAnimationFrame(raf);
      observer.disconnect();
      document.removeEventListener("visibilitychange", schedule);
      render.current = () => {};
      images.length = 0;
    };
  }, [progress, reduced]);

  return <div className={`absolute inset-0 ${className}`} data-testid="landing-scene">
    <img src="/frames/30.webp" alt="Architectural model of a residential building" fetchPriority="high"
      className="absolute inset-0 h-full w-full object-contain" data-testid="landing-scene-poster" />
    {!reduced && <canvas ref={canvas} aria-hidden="true" data-testid="landing-scene-canvas"
      className="absolute inset-0 h-full w-full opacity-0" />}
  </div>;
}