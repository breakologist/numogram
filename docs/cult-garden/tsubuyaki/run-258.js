// Tsubuyaki — Run #238
// Zones: [0, 1, 2, 3, 4, 5, 7, 8, 9]
// Turns: 269, Hyp: 3.0%
function setup() {
  createCanvas(200, 200);
  background(0);
  noStroke();
}
function draw() {
  for (let i = 0; i < 9; i++) {
    let z = [0, 1, 2, 3, 4, 5, 7, 8, 9];
    let c = [(255, 255, 0), (255, 165, 0), (255, 0, 255), (0, 255, 255), (0, 255, 0), (0, 100, 255), (200, 150, 255), (150, 0, 150), (100, 100, 100)];
    fill(c[i % c.length]);
    let angle = (i / max(1, 9)) * TWO_PI;
    let r = 50.0;
    let x = 100 + cos(angle) * r * (1 + sin(frameCount * 0.02 + i));
    let y = 100 + sin(angle) * r * (1 + cos(frameCount * 0.02 + i));
    ellipse(x, y, 8 + 0.3, 8 + 0.3);
  }
}