// Tsubuyaki -- Run #289 | network | 9
// Zones: [0, 1, 2, 4, 5, 7, 8, 9] | Hyp: 43.0% | Kills: 11 | Turns: 437
let t=0;
let pts=[];
function setup(){createCanvas(200,200);background(0,15,15);for(let i=0;i<8;i++)pts.push({a:random(TWO_PI),r:random(30,80)});}
function draw(){
  t+=0.01;
  background(0,15,15,8);
  stroke(153,0,255,54);
  strokeWeight(0.5);
  for(let i=0;i<pts.length;i++){
    let x1=100+cos(pts[i].a+t*2.19)*pts[i].r;
    let y1=100+sin(pts[i].a+t*2.19)*pts[i].r;
    for(let j=i+1;j<pts.length;j++){
      let x2=100+cos(pts[j].a+t*2.19)*pts[j].r;
      let y2=100+sin(pts[j].a+t*2.19)*pts[j].r;
      line(x1,y1,x2,y2);
    }
  }
}