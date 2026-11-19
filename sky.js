/* Sky: a very light, slow cloud field drawn behind a few sections, in the section's own colours (ivory clouds on
   ivory, pale red on MEA red). One small WebGL shader per canvas, rendered at a fraction of the size (clouds are soft),
   paused when off screen, a single still frame for reduced motion, and nothing at all without WebGL (the section keeps
   its solid colour). The canvas sits inside its section (position: absolute), never fixed to the window.
   <canvas class="sky" data-base="#f2eee7" data-tint="#e9c9bd" data-amt=".55" data-scale="1.6" data-speed="1"> */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var VS = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
  var FS = [
    "#ifdef GL_FRAGMENT_PRECISION_HIGH", "precision highp float;", "#else", "precision mediump float;", "#endif",
    "uniform vec2 uR;uniform float uT;uniform vec3 uB;uniform vec3 uC;uniform float uA;uniform float uS;uniform vec2 uP;uniform float uW;",
    "float h(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}",
    "float n(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);",
    "return mix(mix(h(i),h(i+vec2(1.,0.)),u.x),mix(h(i+vec2(0.,1.)),h(i+vec2(1.,1.)),u.x),u.y);}",
    "float fb(vec2 p){float v=0.,a=.5;mat2 m=mat2(1.6,1.2,-1.2,1.6);for(int i=0;i<5;i++){v+=a*n(p);p=m*p;a*=.5;}return v;}",
    "void main(){vec2 uv=gl_FragCoord.xy/uR;vec2 asp=vec2(uR.x/uR.y,1.);vec2 p=uv*asp*uS;",
    "vec2 q=vec2(fb(p+vec2(0.,uT*.5)),fb(p+vec2(5.2,1.3)-uT*.35));",
    "float c=fb(p+1.8*q+vec2(uT*.7,uT*.12));",
    "c=smoothstep(.38,.9,c);",
    "float s=fb(p*2.3+q+uT*.9);c*=.78+.22*s;",                       /* a little inner texture */
    "vec2 d=(uv-uP)*asp;c*=1.-exp(-dot(d,d)*14.)*uW*.9;",            /* the pointer parts the clouds */
    "vec3 col=mix(uB,uC,clamp(c*uA,0.,1.));",
    "col+=(h(gl_FragCoord.xy+uT)-.5)/255.;",                         /* dither against banding */
    "gl_FragColor=vec4(col,1.);}"
  ].join("\n");

  function rgb(hex) { hex = (hex || "#f2eee7").replace("#", ""); return [0, 2, 4].map(function (i) { return parseInt(hex.substr(i, 2), 16) / 255; }); }

  function make(cv) {
    var gl = cv.getContext("webgl", { antialias: false, alpha: false, depth: false, stencil: false, premultipliedAlpha: false, preserveDrawingBuffer: false, powerPreference: "low-power" });
    if (!gl) return;
    function sh(t, s) { var x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); return gl.getShaderParameter(x, gl.COMPILE_STATUS) ? x : null; }
    var vs = sh(gl.VERTEX_SHADER, VS), fs = sh(gl.FRAGMENT_SHADER, FS); if (!vs || !fs) return;
    var pr = gl.createProgram(); gl.attachShader(pr, vs); gl.attachShader(pr, fs); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return;
    gl.useProgram(pr);
    var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(pr, "p"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var U = {}; ["uR", "uT", "uB", "uC", "uA", "uS", "uP", "uW"].forEach(function (k) { U[k] = gl.getUniformLocation(pr, k); });
    var ds = cv.dataset, base = rgb(ds.base), tint = rgb(ds.tint);
    gl.uniform3fv(U.uB, base); gl.uniform3fv(U.uC, tint);
    gl.uniform1f(U.uA, +(ds.amt || .6)); gl.uniform1f(U.uS, +(ds.scale || 1.6));
    var speed = +(ds.speed || 1), t = Math.random() * 40, last = 0, on = false, raf = 0;
    var px = .5, py = .5, tx = .5, ty = .5, w = 0, tw = 0, host = cv.parentNode;

    function size() {
      var r = cv.getBoundingClientRect(), q = r.width > 1200 ? .3 : r.width > 700 ? .38 : .5;
      var W = Math.max(32, Math.round(r.width * q)), H = Math.max(32, Math.round(r.height * q));
      if (cv.width !== W || cv.height !== H) { cv.width = W; cv.height = H; gl.viewport(0, 0, W, H); }
      gl.uniform2f(U.uR, W, H);
    }
    function draw() {
      px += (tx - px) * .06; py += (ty - py) * .06; w += (tw - w) * .05;
      gl.uniform1f(U.uT, t); gl.uniform2f(U.uP, px, py); gl.uniform1f(U.uW, w);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      cv.classList.add("on");
    }
    function frame(now) {
      if (!on) return;
      var dt = Math.min((now - (last || now)) / 1000, .05); last = now;
      t += dt * .045 * speed;
      draw();
      raf = requestAnimationFrame(frame);
    }
    function start() { if (on || reduce) return; on = true; last = 0; raf = requestAnimationFrame(frame); }
    function stop() { on = false; cancelAnimationFrame(raf); }
    size(); draw();
    if ("ResizeObserver" in window) new ResizeObserver(function () { size(); draw(); }).observe(cv);
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { es[es.length - 1].isIntersecting ? start() : stop(); }).observe(cv);
    else start();
    document.addEventListener("visibilitychange", function () { if (document.hidden) stop(); });
    if (!reduce && window.matchMedia("(hover: hover)").matches) {
      host.addEventListener("pointermove", function (e) { var r = cv.getBoundingClientRect(); tx = (e.clientX - r.left) / r.width; ty = 1 - (e.clientY - r.top) / r.height; tw = 1; }, { passive: true });
      host.addEventListener("pointerleave", function () { tw = 0; }, { passive: true });
    }
  }
  function boot() { Array.prototype.forEach.call(document.querySelectorAll("canvas.sky"), make); }
  if ("requestIdleCallback" in window) requestIdleCallback(boot, { timeout: 600 }); else setTimeout(boot, 120);
})();
