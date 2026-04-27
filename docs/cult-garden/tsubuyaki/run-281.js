// Tsubuyaki — Run #261
// Zones: [0]
// Turns: 510, Hyp: 3.0%
function setup() {
  createCanvas(200, 200);
  background(0);
  noStroke();
}
function draw() {
  for (let i = 0; i < 1; i++) {
    let z = [0];
    let c = [(255, 255, 0)];
    fill(c[i % c.length]);
    let angle = (i / max(1, 1)) * TWO_PI;
    let r = 50.0;
    let x = 100 + cos(angle) * r * (1 + sin(frameCount * 0.02 + i));
    let y = 100 + sin(angle) * r * (1 + cos(frameCount * 0.02 + i));
    ellipse(x, y, 8 + 0.3, 8 + 0.3);
  }
}