// Tsubuyaki -- Run #301 | dodecagon | 9
// Zones: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | Hyp: 89.9% | Kills: 24 | Turns: 393
let t=0;
function setup(){createCanvas(200,200);background(15,0,25);}
function draw(){
  t+=0.01;
  background(15,0,25,6);
  noFill();
  stroke(153,0,255,229);
  strokeWeight(1);
  let n=max(3,10);
  beginShape();
  for(let i=0;i<=n;i++){
    let a=t*1.97+i*TWO_PI/n;
    let r=60+10*sin(t*2+i);
    vertex(100+cos(a)*r,100+sin(a)*r);
  }
  endShape();
  fill(153,0,255,76);
  noStroke();
  ellipse(100,100,8,8);
}