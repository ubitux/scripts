"use strict";

function compileShader(gl, source, type) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    throw new Error(gl.getShaderInfoLog(shader));
  }
  return shader;
}

async function initCanvas(canvas, ob) {
  let aId = null;

  const gl = canvas.getContext("webgl2");
  if (!gl) {
    throw new Error("No WebGL2 context available");
  }

  const vsSrc = `#version 300 es
    const vec2 pos[] = vec2[](vec2(-1.0, -1.0), vec2(-1.0, 3.0), vec2(3.0, -1.0));
    void main() {
        gl_Position = vec4(pos[gl_VertexID], 0.0, 1.0);
    }`;

  const fsUser = await fetch(canvas.dataset.fragment).then(r => r.text());
  const fsSrc = `#version 300 es
    #if GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
    precision highp int;
    #else
    precision mediump float;
    precision mediump int;
    #endif
    out vec4 out_color;
    uniform float time;
    uniform vec2 resolution;

    #define P gl_FragCoord.xy
    #define O out_color
    #define T time
    #define R resolution
  ` + fsUser;

  const vs = compileShader(gl, vsSrc, gl.VERTEX_SHADER);
  const fs = compileShader(gl, fsSrc, gl.FRAGMENT_SHADER);

  const prog = gl.createProgram();
  gl.attachShader(prog, vs);
  gl.attachShader(prog, fs);
  gl.deleteShader(vs);
  gl.deleteShader(fs);
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
    throw new Error(gl.getProgramInfoLog(prog));
  }

  const resolutionLoc = gl.getUniformLocation(prog, "resolution");
  const timeLoc = gl.getUniformLocation(prog, "time");

  function render(time) {
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(prog);
    gl.uniform2f(resolutionLoc, canvas.width, canvas.height);
    gl.uniform1f(timeLoc, time * 0.001);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    aId = requestAnimationFrame(render);
  }

  canvas._start = function start() {
    aId = requestAnimationFrame(render);
  }

  canvas._stop = function stop() {
    if (aId === null) return;
    cancelAnimationFrame(aId);
    aId = null;
  }

  ob.observe(canvas);
}

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting)
      entry.target._start();
    else
      entry.target._stop();
  });
});

document.querySelectorAll(".shader-canvas").forEach(c => initCanvas(c, observer));
