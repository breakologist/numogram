// Tsubuyaki — Run #275
// Zones: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
// Turns: 1143, Hyp: 67.0%
function setup() {
  createCanvas(200, 200);
  background(0);
  noStroke();
}
function draw() {
  for (let i = 0; i < 10; i++) {
    let z = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    let c = [(255, 255, 0), (255, 165, 0), (255, 0, 255), (0, 255, 255), (0, 255, 0), (0, 100, 255), (255, 0, 0), (200, 150, 255), (150, 0, 150), (100, 100, 100)];
    fill(c[i % c.length]);
    let angle = (i / max(1, 10)) * TWO_PI;
    let r = 50.0;
    let x = 100 + cos(angle) * r * (1 + sin(frameCount * 0.02 + i));
    let y = 100 + sin(angle) * r * (1 + cos(frameCount * 0.02 + i));
    ellipse(x, y, 8 + 6.7, 8 + 6.7);
  }
}