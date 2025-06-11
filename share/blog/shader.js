async function loadText(url) {
  const res = await fetch(url);
  return res.text();
}

function compileShader(gl, source, type) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    throw new Error(gl.getShaderInfoLog(shader));
  }
  return shader;
}

async function initCanvas(canvas) {
  const gl = canvas.getContext("webgl2");
  if (!gl) {
    throw new Error("No WebGL2 context available");
  }
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;

  const vsSrc = `#version 300 es
    const vec2 pos[] = vec2[](vec2(-1.0, -1.0), vec2(-1.0, 3.0), vec2(3.0, -1.0));
    void main() {
        gl_Position = vec4(pos[gl_VertexID], 0.0, 1.0);
    }`;

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
    uniform vec2 resolution;` + await loadText(canvas.dataset.fragment);

  const vs = compileShader(gl, vsSrc, gl.VERTEX_SHADER);
  const fs = compileShader(gl, fsSrc, gl.FRAGMENT_SHADER);

  const prog = gl.createProgram();
  gl.attachShader(prog, vs);
  gl.attachShader(prog, fs);
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
    throw new Error(gl.getProgramInfoLog(prog));
  }
  gl.deleteShader(vs);
  gl.deleteShader(fs);

  const resolutionLoc = gl.getUniformLocation(prog, "resolution");
  const timeLoc = gl.getUniformLocation(prog, "time");

  function render(time) {
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(prog);
    gl.uniform2f(resolutionLoc, canvas.width, canvas.height);
    gl.uniform1f(timeLoc, time * 0.001);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    requestAnimationFrame(render);
  }
  requestAnimationFrame(render);
}

document.querySelectorAll(".shader-canvas").forEach(initCanvas);
