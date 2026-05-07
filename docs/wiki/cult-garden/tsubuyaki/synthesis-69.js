// Tsubuyaki -- Run #304 | ellipse | 9
// Zones: [0, 2, 4, 5, 7, 8, 9] | Hyp: 40.239999999999995% | Kills: 6 | Turns: 87
let t=0;
function setup(){createCanvas(200,200);background(20,0,20);}
function draw(){
  t+=0.02;
  background(20,0,20,10);
  noFill();
  stroke(153,0,255,102);
  strokeWeight(1+3.0);
  let rx=60+sin(t*0.5)*46;
  let ry=40+cos(t*0.5*0.7)*46;
  ellipse(100,100,rx*2,ry*2);
  if(frameCount%30<5){
    strokeWeight(3);
    ellipse(100,100,rx*2+4,ry*2+4);
  }
}