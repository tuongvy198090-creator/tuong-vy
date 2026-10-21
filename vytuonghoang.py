
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Penguin Ice Quest", layout="wide")

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"]{display:none}
.block-container{padding:0!important;max-width:100%!important}
iframe{border:0}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
body{margin:0;overflow:hidden;font-family:Arial;background:#8ddff5}
canvas{display:block}
#hud{position:fixed;top:8px;left:8px;right:8px;display:flex;justify-content:space-between;gap:5px;z-index:3;pointer-events:none}
.tag{background:#063b62ed;color:white;border-radius:12px;padding:9px;font-weight:bold;font-size:13px}
#quiz{position:fixed;top:55px;left:50%;transform:translateX(-50%);width:96%;max-width:750px;z-index:4;text-align:center;pointer-events:none}
#q{background:#073c63ee;color:white;border:3px solid white;border-radius:13px;padding:10px;font-size:clamp(14px,2.5vw,22px);font-weight:bold}
#answers{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:5px;margin-top:5px}
.ans{min-height:48px;padding:6px 2px;background:#fff;color:#073c63;border:3px solid #91e2ff;border-radius:10px;font-weight:bold;font-size:clamp(10px,1.8vw,15px);display:flex;align-items:center;justify-content:center;overflow-wrap:anywhere}
.ans.sel{background:#ffe56c;border-color:#ff9b2f}
#msg{display:none;position:fixed;top:43%;left:50%;transform:translate(-50%,-50%);width:90%;max-width:480px;background:#063b62ee;color:white;border:3px solid white;border-radius:16px;padding:16px;text-align:center;font-size:20px;font-weight:bold;z-index:7}
#start{position:fixed;inset:0;z-index:10;background:#063b62df;display:flex;align-items:center;justify-content:center;padding:15px}
.panel{background:#117ca8;border:4px solid white;border-radius:22px;padding:24px;max-width:500px;text-align:center;color:white}
.panel h1{font-size:clamp(26px,6vw,42px)}
button{border:0;border-radius:14px;padding:12px;font-size:17px;font-weight:bold;touch-action:none}
#go{background:#b4ffcb;padding:15px 22px}
#controls{position:fixed;bottom:12px;left:12px;right:12px;display:flex;justify-content:space-between;align-items:end;z-index:5;pointer-events:none}
.pad{display:grid;grid-template-columns:repeat(3,45px);grid-template-rows:repeat(2,45px);gap:4px;pointer-events:auto}
.ctrl{background:#063b62dd;color:white;border:2px solid white;padding:0;font-size:22px}
#jump{pointer-events:auto;width:72px;height:72px;border-radius:50%;background:#ffdf58;border:3px solid white;font-size:14px}
#hint{position:fixed;right:8px;bottom:112px;background:#073b62d9;color:white;padding:7px;border-radius:8px;font-size:12px;z-index:3}
</style>
</head>
<body>
<div id="hud">
 <div class="tag" id="stage">🐧 VƯỢT CẦU BĂNG</div>
 <div class="tag" id="life">❤️❤️❤️</div>
 <div class="tag" id="count">Hàng 1/5</div>
</div>
<div id="quiz">
 <div id="q">Hãy chuẩn bị!</div>
 <div id="answers"></div>
</div>
<div id="msg"></div>
<div id="hint">← → chọn hướng · ↑ tiến · SPACE nhảy</div>
<div id="controls">
 <div class="pad">
  <button class="ctrl" data-k="ArrowLeft" style="grid-column:1;grid-row:1">←</button>
  <button class="ctrl" data-k="ArrowUp" style="grid-column:2;grid-row:1">↑</button>
  <button class="ctrl" data-k="ArrowRight" style="grid-column:3;grid-row:1">→</button>
  <button class="ctrl" data-k="ArrowDown" style="grid-column:2;grid-row:2">↓</button>
 </div>
 <button id="jump">NHẢY ⬆</button>
</div>
<div id="start">
 <div class="panel">
  <div style="font-size:60px">🐧 🐧</div>
  <h1>HÀNH TRÌNH VƯỢT BIỂN BĂNG</h1>
  <p>Vượt qua 5 hàng băng, chọn đúng đáp án để hạ vách chắn, lấy xô cá rồi nhảy về nhà!</p>
  <p>Em có 3 mạng. Hãy nhảy đáp xuống đúng tảng băng.</p>
  <button id="go">BẮT ĐẦU!</button>
 </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(()=>{
const $=id=>document.getElementById(id);
if(!window.THREE){$('q').textContent='Không tải được thư viện 3D. Kiểm tra Internet rồi tải lại.';return;}

const questions=[
 {q:"TOÁN: Giá trị của 2³ là?",a:["6","8","9","12"],c:1},
 {q:"TOÁN: x² − 9 bằng biểu thức nào?",a:["(x−3)(x+3)","(x−9)²","x(x−9)","(x+9)²"],c:0},
 {q:"VẬT LÍ: Đơn vị áp suất là?",a:["Niutơn","Jun","Pascal","Oát"],c:2},
 {q:"HÓA HỌC: Công thức nước là?",a:["CO₂","H₂O","O₂","NaCl"],c:1},
 {q:"SINH HỌC: Nơi trao đổi khí ở phổi?",a:["Dạ dày","Thận","Thực quản","Phế nang"],c:3},
 {q:"ĐỊA LÍ: Xích đạo chia Trái Đất thành?",a:["Bắc và Nam","Đông và Tây","Đất và nước","Hai lục địa"],c:0},
 {q:"LỊCH SỬ: Ai lãnh đạo khởi nghĩa Lam Sơn?",a:["Ngô Quyền","Lê Lợi","Quang Trung","Trần Hưng Đạo"],c:1},
 {q:"TIẾNG ANH: She ___ to school every day.",a:["go","going","goes","gone"],c:2},
 {q:"TOÁN: Tổng góc trong tứ giác là?",a:["90°","180°","270°","360°"],c:3},
 {q:"VẬT LÍ: Khối lượng riêng D được tính bằng?",a:["m/V","V/m","m×V","F/S"],c:0},
 {q:"HÓA HỌC: Chất nào là đơn chất?",a:["Nước","Muối ăn","Khí oxi","CO₂"],c:2},
 {q:"NGỮ VĂN: Từ nào là từ láy?",a:["Nhà cửa","Lấp lánh","Sách vở","Cây cối"],c:1}
];

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x9be5f8);
scene.fog=new THREE.Fog(0x9be5f8,35,100);
const camera=new THREE.PerspectiveCamera(65,innerWidth/innerHeight,.1,200);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.outputColorSpace=THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);
renderer.domElement.style.position='fixed';
renderer.domElement.style.inset='0';
renderer.domElement.style.zIndex='0';

scene.add(new THREE.HemisphereLight(0xe8faff,0x49788b,2));
const sun=new THREE.DirectionalLight(0xffffff,2.2);
sun.position.set(-8,16,10);sun.castShadow=true;scene.add(sun);

const material=c=>new THREE.MeshStandardMaterial({color:c,roughness:.65});
const snow=material(0xf3fcff),ice=material(0x71d4f3);
const wallMat=material(0x4e9ec4),dark=material(0x17212d);
const white=material(0xffffff),orange=material(0xff9e35);
const sea=new THREE.Mesh(new THREE.PlaneGeometry(180,180),material(0x168cc1));
sea.rotation.x=-Math.PI/2;sea.position.y=-.8;scene.add(sea);

function cube(w,h,d,m,x,y,z){
 const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);
 o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;scene.add(o);return o;
}
function island(z){
 cube(15,1.5,8,snow,0,-.15,z);
 for(let i=0;i<7;i++){
  let x=(Math.random()-.5)*12;
  const mound=new THREE.Mesh(new THREE.DodecahedronGeometry(.65+Math.random()*.5),snow);
  mound.position.set(x,.5,z+(Math.random()-.5)*5);
  mound.scale.y=.55;scene.add(mound);
 }
}
island(7);island(-39);

function tree(x,z){
 cube(.5,1.5,.5,material(0x765039),x,.6,z);
 for(let i=0;i<3;i++){
  const crown=new THREE.Mesh(new THREE.ConeGeometry(1.3-i*.2,2.1,7),material(0x258e79));
  crown.position.set(x,1.6+i*.7,z);scene.add(crown);
 }
}
for(const z of [3,8,-36,-41])for(const x of [-6,-4.5,4.5,6])tree(x,z);

function makePenguin(scale){
 const g=new THREE.Group();
 const body=new THREE.Mesh(new THREE.SphereGeometry(.55,18,14),dark);
 body.scale.set(.85,1.2,.7);body.position.y=.85;g.add(body);
 const belly=new THREE.Mesh(new THREE.SphereGeometry(.42,18,14),white);
 belly.scale.set(.85,1.1,.4);belly.position.set(0,.82,.29);g.add(belly);
 const head=new THREE.Mesh(new THREE.SphereGeometry(.38,18,14),dark);
 head.position.set(0,1.7,.02);g.add(head);
 for(const s of [-1,1]){
  const eye=new THREE.Mesh(new THREE.SphereGeometry(.07,10,8),white);
  eye.position.set(s*.14,1.75,.35);g.add(eye);
  const pupil=new THREE.Mesh(new THREE.SphereGeometry(.035,8,8),dark);
  pupil.position.set(s*.14,1.75,.41);g.add(pupil);
  const wing=new THREE.Mesh(new THREE.SphereGeometry(.17,10,8),dark);
  wing.scale.set(.6,1.3,.5);wing.position.set(s*.45,.9,0);g.add(wing);
  const foot=new THREE.Mesh(new THREE.BoxGeometry(.22,.12,.34),orange);
  foot.position.set(s*.19,.1,.18);g.add(foot);
 }
 const beak=new THREE.Mesh(new THREE.ConeGeometry(.12,.26,8),orange);
 beak.rotation.x=Math.PI/2;beak.position.set(0,1.62,.43);g.add(beak);
 g.scale.setScalar(scale);scene.add(g);return g;
}
const player=makePenguin(1),baby=makePenguin(.52);
player.position.set(0,0,5);baby.position.set(1.1,0,6);

const lanes=[-4.5,-1.5,1.5,4.5];
let platforms=[],walls=[],labels=[];
let keys={},stage='intro',lives=3,row=0,selected=1;
let jumpV=0,jumping=false,question=null,lock=false;
let returnTiles=[],returnStep=0,hasBucket=false;
let lastTime=performance.now(),messageTimer;

function spriteText(text,x,y,z){
 const c=document.createElement('canvas');c.width=512;c.height=128;
 const ctx=c.getContext('2d');
 ctx.fillStyle='#063c63';ctx.fillRect(0,0,512,128);
 ctx.fillStyle='white';ctx.font='bold 36px Arial';
 ctx.textAlign='center';ctx.textBaseline='middle';
 ctx.fillText(text.length>23?text.slice(0,21)+'…':text,256,64);
 const tex=new THREE.CanvasTexture(c);
 const s=new THREE.Sprite(new THREE.SpriteMaterial({map:tex}));
 s.scale.set(2.65,.66,1);s.position.set(x,y,z);scene.add(s);labels.push(s);
 return s;
}
function clearList(arr){arr.forEach(o=>scene.remove(o));arr.length=0}
function updateHUD(){
 $('life').textContent='❤️'.repeat(lives)+'🖤'.repeat(3-lives);
 $('count').textContent=stage==='return'?'Về nhà '+(returnStep+1)+'/5':'Hàng '+Math.min(row+1,5)+'/5';
 $('stage').textContent=stage==='return'?'🐟 MANG CÁ VỀ':'🐧 VƯỢT CẦU BĂNG';
}
function say(text,ms=1300){
 $('msg').textContent=text;$('msg').style.display='block';
 clearTimeout(messageTimer);
 messageTimer=setTimeout(()=>$('msg').style.display='none',ms);
}
function makePlatform(x,z,weak=false){
 const g=new THREE.Group();
 const b=new THREE.Mesh(new THREE.BoxGeometry(2.55,.45,2.35),weak?material(0x99d9e9):ice);
 b.position.y=-.12;g.add(b);
 const top=new THREE.Mesh(new THREE.BoxGeometry(2.4,.12,2.2),snow);
 top.position.y=.17;g.add(top);
 if(weak){
  for(let i=0;i<3;i++){
   const crack=cube(.04,.02,.55,material(0x3287a8),x+(i-1)*.3,.25,z+(i%2)*.1);
   crack.position.y=.25;g.add(crack);scene.remove(crack); // được giữ trong nhóm
  }
 }
 g.position.set(x,0,z);scene.add(g);
 return {g,x,z,weak,sunk:false};
}
function buildRow(r){
 // 4 tảng băng ở mỗi hàng, cùng hàng ngang.
 const z=1-r*5;
 const rowTiles=[];
 for(let i=0;i<4;i++){
  const p=makePlatform(lanes[i],z,false);
  p.answerIndex=i;p.row=r;rowTiles.push(p);platforms.push(p);
  spriteText(String.fromCharCode(65+i)+'. '+question.a[i],lanes[i],1.12,z);
 }
 // Vách chắn dựng ngang phía trước hàng.
 const wall=cube(12,.95,.3,wallMat,0,.55,z-2.35);
 wall.userData.row=r;walls.push(wall);
 // Cột hai bên vách.
 for(const x of [-6,6]){
  const post=cube(.3,1.6,.45,snow,x,.75,z-2.35);
  walls.push(post);
 }
 return rowTiles;
}
let rowTiles=[];
function newQuestion(){
 question=questions[Math.floor(Math.random()*questions.length)];
 selected=1;
 $('q').textContent=question.q;
 $('answers').innerHTML='';
 question.a.forEach((a,i)=>{
  const d=document.createElement('div');
  d.className='ans'+(i===selected?' sel':'');
  d.textContent=String.fromCharCode(65+i)+'. '+a;
  $('answers').appendChild(d);
 });
 clearList(labels);
 updateHUD();
}
function drawBridge(){
 clearList(platforms.map(p=>p.g));platforms=[];
 clearList(walls);clearList(labels);
 // Mỗi hàng được đặt cách nhau, hàng đầu tiên ở gần người chơi.
 for(let r=0;r<5;r++){
  question=questions[(row+r)%questions.length];
  const z=1-r*5;
  for(let i=0;i<4;i++){
   const p=makePlatform(lanes[i],z,false);
   p.answerIndex=i;p.row=r;platforms.push(p);
   spriteText(String.fromCharCode(65+i)+'. '+question.a[i],lanes[i],1.12,z);
  }
  const wall=cube(12,.95,.3,wallMat,0,.55,z-2.35);
  wall.userData.row=r;walls.push(wall);
  for(const x of [-6,6])walls.push(cube(.3,1.6,.45,snow,x,.75,z-2.35));
 }
}
function showRowQuestion(){
 question=questions[Math.floor(Math.random()*questions.length)];
 $('q').textContent=question.q;
 $('answers').innerHTML='';
 question.a.forEach((a,i)=>{
  const d=document.createElement('div');
  d.className='ans'+(i===selected?' sel':'');
  d.textContent=String.fromCharCode(65+i)+'. '+a;
  $('answers').appendChild(d);
 });
 clearList(labels);
 const z=1-row*5;
 for(let i=0;i<4;i++)spriteText(String.fromCharCode(65+i)+'. '+question.a[i],lanes[i],1.12,z);
 updateHUD();
}
function removeWall(r){
 walls.forEach(w=>{
  if(w.userData.row===r){
   const from=w.position.y,begin=performance.now();
   function sink(t){
    const f=Math.min(1,(t-begin)/600);
    w.position.y=from-2*f;
    if(f<1)requestAnimationFrame(sink);
   }
   requestAnimationFrame(sink);
  }
 });
}
function loseLife(){
 lives--;updateHUD();
 if(lives<=0){
  stage='gameover';say('HẾT MẠNG! Hãy bắt đầu lại nhé.',4000);
  setTimeout(()=>$('start').style.display='flex',1800);
 }
}
function answerLanding(p){
 if(lock||stage!=='outbound'||p.row!==row)return;
 lock=true;
 if(p.answerIndex===question.c){
  removeWall(row);
  say('ĐÚNG RỒI! VÁCH CHẮN ĐANG HẠ XUỐNG!',900);
  row++;
  if(row>=5){
   stage='return';hasBucket=true;returnStep=0;
   $('q').textContent='🐟 ĐÃ LẤY XÔ CÁ! NHẢY TRỞ VỀ!';
   $('answers').innerHTML='';
   clearList(labels);
   // Đường về trên chính cầu băng; một số tảng yếu.
   returnTiles=[];
   for(let i=0;i<5;i++){
    const lane=[1,2,1,0,2][i];
    const p=makePlatform(lanes[lane],-24+i*5,[1,3].includes(i));
    returnTiles.push(p);
    spriteText(p.weak?'BĂNG YẾU':'BĂNG CHẮC',p.x,1.15,p.z);
   }
   const bucket=cube(.8,.7,.8,material(0xe7f5ff),0,.4,-34);
   spriteText('XÔ CÁ 🐟',0,1.5,-34);
   say('ĐÃ LẤY ĐƯỢC XÔ CÁ! ĐI THEO CẦU VỀ NHÀ!',2200);
   $('count').textContent='ĐƯỜNG VỀ';
  }else{
   setTimeout(()=>{
    player.position.set(0,0,5-row*5);
    baby.position.set(1.2,0,6-row*5);
    selected=1;
    drawBridge();
    showRowQuestion();
    lock=false;
   },700);
   return;
  }
 }else{
  loseLife();
  if(stage==='gameover'){lock=false;return}
  say('SAI RỒI! MẤT 1 MẠNG. THỬ LẠI HÀNG NÀY NHÉ!',1500);
  // Đáp sai thì quay về đầu hàng đó, hàng và vách vẫn còn.
  player.position.set(0,0,5-row*5);
  baby.position.set(1.2,0,6-row*5);
 }
 setTimeout(()=>lock=false,800);
}
function landReturn(p){
 if(stage!=='return'||p.sunk)return;
 p.sunk=true;
 if(p.weak){
  const start=performance.now(),y=p.g.position.y;
  function sink(t){
   const f=Math.min(1,(t-start)/700);
   p.g.position.y=y-.65*f;
   if(f<1)requestAnimationFrame(sink);
  }
  requestAnimationFrame(sink);
  say('CẨN THẬN! TẢNG BĂNG YẾU ĐANG LÚN!',900);
 }
 returnStep++;updateHUD();
 if(returnStep>=returnTiles.length){
  stage='won';$('q').textContent='🎉 CHIẾN THẮNG!';$('answers').innerHTML='';
  say('CHÚC MỪNG! MẸ CON CHIM CÁNH CỤT ĐÃ MANG CÁ VỀ!',5000);
  setTimeout(()=>{
   $('start').style.display='flex';
   $('start').querySelector('h1').textContent='CHIẾN THẮNG! 🐧';
   $('start').querySelector('p').textContent='Em đã hoàn thành hành trình vượt biển băng!';
   $('go').textContent='CHƠI LẠI';
  },1000);
 }
}
function jump(){
 if(jumping||!['outbound','return'].includes(stage))return;
 jumping=true;jumpV=8.5;
}
function start(){
 stage='outbound';row=0;lives=3;selected=1;lock=false;
 player.position.set(0,0,5);baby.position.set(1,0,6);
 $('start').style.display='none';
 $('q').textContent='Hãy nhảy lên tảng băng có đáp án đúng!';
 drawBridge();showRowQuestion();updateHUD();
}
function tick(now){
 requestAnimationFrame(tick);
 const dt=Math.min(.035,(now-lastTime)/1000||.016);lastTime=now;
 if(['outbound','return'].includes(stage)){
  const speed=5.8;
  if(keys.ArrowLeft)player.position.x-=speed*dt;
  if(keys.ArrowRight)player.position.x+=speed*dt;
  if(keys.ArrowUp)player.position.z-=speed*dt;
  if(keys.ArrowDown)player.position.z+=speed*dt;
  player.position.x=Math.max(-6,Math.min(6,player.position.x));
  if(jumping){
   player.position.y+=jumpV*dt;jumpV-=20*dt;
   if(player.position.y<=0){
    player.position.y=0;jumping=false;
    // Kiểm tra đúng tảng băng khi chân chạm đất.
    if(stage==='outbound'){
     const target=platforms.find(p=>
      p.row===row&&Math.abs(player.position.x-p.x)<1.15&&
      Math.abs(player.position.z-p.z)<1.15);
     if(target)answerLanding(target);
    }else if(stage==='return'){
     const target=returnTiles.find(p=>
      Math.abs(player.position.x-p.x)<1.2&&Math.abs(player.position.z-p.z)<1.25);
     if(target&&!target.sunk)landReturn(target);
    }
   }
  }
  baby.position.x+=(player.position.x+1.2-baby.position.x)*dt*2.5;
  baby.position.z+=(player.position.z+.8-baby.position.z)*dt*2.5;
 }
 camera.position.lerp(new THREE.Vector3(player.position.x*.4,5.8,player.position.z+10),.09);
 camera.lookAt(player.position.x,1,player.position.z-5);
 renderer.render(scene,camera);
}
requestAnimationFrame(tick);

addEventListener('keydown',e=>{
 if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' '].includes(e.key))e.preventDefault();
 if(e.key===' '){if(!e.repeat)jump();return}
 keys[e.key]=true;
});
addEventListener('keyup',e=>keys[e.key]=false);
document.querySelectorAll('[data-k]').forEach(b=>{
 const k=b.dataset.k;
 b.addEventListener('pointerdown',e=>{e.preventDefault();keys[k]=true});
 ['pointerup','pointercancel','pointerleave'].forEach(ev=>
  b.addEventListener(ev,e=>{e.preventDefault();keys[k]=false}));
});
$('jump').addEventListener('pointerdown',e=>{e.preventDefault();jump()});
$('go').addEventListener('click',()=>{
 $('start').querySelector('h1').textContent='HÀNH TRÌNH VƯỢT BIỂN BĂNG';
 $('start').querySelector('p').textContent='Vượt 5 hàng băng, trả lời đúng để hạ vách chắn, lấy cá rồi trở về!';
 $('go').textContent='BẮT ĐẦU!';
 start();
});
addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
})();
</script>
</body>
</html>
"""

components.html(html, height=850, scrolling=False)
