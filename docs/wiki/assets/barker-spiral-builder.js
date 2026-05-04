function setup() {
  createCanvas(900, 600);
  background(15, 23, 42);
  // Draw Barker Spiral with interactive features
}

function draw() {
  translate(450, 320);
  // Draw spiral arms
  for (let k = 0; k < 45; k++) {
    let angle = -HALF_PI + k * TWO_PI / 45;
    let r_inner = 40 * pow(1.08, k);
    let r_outer = r_inner * 1.08;
    // Draw arc segment
    stroke(96, 165, 250);
    strokeWeight(1);
    noFill();
    // Use quadraticBezier or curve to draw arc
  }
}

function mouseMoved() {
  // Highlight arm under mouse
}