
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hành Trình Vượt Biển Băng",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, footer, header,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

game = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport"
 content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<style>
*{box-sizing:border-box}
body{
 margin:0;overflow:hidden;font-family:Arial,sans-serif;
 background:#8dddf4;color:white
}
#game{position:fixed;inset:0}
canvas{display:block}
#hud{
 position:fixed;top:8px;left:8px;right:8px;
 display:flex;justify-content:space-between;gap:6px;
 pointer-events:none;z-index:5
}
.pill{
 background:#073b63e8;padding:9px 12px;
 border-radius:14px;font-size:14px;font-weight:bold;
 box-shadow:0 3px 8px #1235
}
#questionBox{
 position:fixed;top:58px;left:50%;transform:translateX(-50%);
 width:min(720px,94vw);z-index:5;text-align:center;
 pointer-events:none
}
#question{
 background:#073b63ed;border:3px solid #bceeff;
 border-radius:16px;padding:12px;font-size:clamp(15px,2.5vw,23px);
 font-weight:bold;box-shadow:0 4px 12px #1237
}
#answers{
 display:grid;grid-template-columns:repeat(4,minmax(0,1fr));
 gap:5px;margin-top:6px
}
.answer{
 background:#fff;color:#123c5c;border:3px solid #b6edff;
 border-radius:12px;padding:8px 3px;
 font-weight:bold;font-size:clamp(11px,1.8vw,16px);
 min-height:54px;display:flex;align-items:center;
 justify-content:center;overflow-wrap:anywhere
}
.answer.selected{background:#ffe46b;border-color:#ff9e28}
#message{
 position:fixed;top:34%;left:50%;transform:translateX(-50%);
 width:min(90vw,520px);background:#073b63ed;
 padding:13px;border-radius:16px;text-align:center;
 font-weight:bold;font-size:20px;z-index:8;display:none
}
#start{
 position:fixed;inset:0;z-index:10;background:#06385bdc;
 display:flex;align-items:center;justify-content:center;padding:16px
}
.panel{
 background:linear-gradient(#1683ad,#06416c);
 border:4px solid #d3f5ff;border-radius:24px;
 padding:24px;max-width:530px;width:100%;
 text-align:center;box-shadow:0 8px 35px #002b
}
.panel h1{font-size:clamp(27px,6vw,43px);margin:5px}
.panel p{line-height:1.6}
button{
 border:0;border-radius:14px;padding:12px 17px;
 font-size:16px;font-weight:bold;cursor:pointer;
 color:#123b5a;background:#ffe36a
}
#startBtn{font-size:21px;background:#aaffc8;padding:15px 26px}
#controls{
 position:fixed;bottom:14px;left:0;right:0;
 display:flex;justify-content:space-between;align-items:end;
 padding:0 15px;z-index:6;pointer-events:none
}
.pad{display:grid;grid-template-columns:repeat(3,48px);
 grid-template-rows:repeat(2,48px);gap:4px;pointer-events:auto}
.ctrl{
 border:2px solid #ffffffbb;background:#064b78cc;
 color:white;border-radius:14px;font-size:23px;
 padding:0;touch-action:none;user-select:none
}
.ctrl:active{background:#e4fbff;color:#123}
#jump{
 width:75px;height:75px;border-radius:50%;
 background:#ffdc5c;color:#123;font-size:15px;
 border:4px solid #fff;pointer-events:auto;touch-action:none
}
#help{
 position:fixed;bottom:112px;right:12px;
 background:#073b63c9;padding:7px 10px;border-radius:10px;
 font-size:12px;z-index:5
}
@media(min-width:800px){
 #controls{padding:0 35px}
 .ctrl{opacity:.82}
}
</style>
</head>
<body>
<div id="game"></div>

<div id="hud">
 <div class="pill" id="stage">🐧 BỜ XUẤT PHÁT</div>
 <div class="pill" id="lives">❤️❤️❤️</div>
 <div class="pill" id="progress">Câu 0/5</div>
</div>

<div id="questionBox" style="display:none">
 <div id="question"></div>
 <div id="answers"></div>
</div>

<div id="message"></div>

<div id="help">← → di chuyển · ↑ tiến · ↓ lùi · SPACE nhảy</div>

<div id="controls">
 <div class="pad">
  <button class="ctrl" data-key="ArrowLeft" style="grid-column:1;grid-row:1">←</button>
  <button class="ctrl" data-key="ArrowUp" style="grid-column:2;grid-row:1">↑</button>
  <button class="ctrl" data-key="ArrowRight" style="grid-column:3;grid-row:1">→</button>
  <button class="ctrl" data-key="ArrowDown" style="grid-column:2;grid-row:2">↓</button>
 </div>
 <button id="jump">NHẢY<br>⬆</button>
</div>

<div id="start">
 <div class="panel">
  <div style="font-size:66px">🐧 🐧</div>
  <h1>HÀNH TRÌNH<br>VƯỢT BIỂN BĂNG</h1>
  <p>
   Hãy giúp chim cánh cụt mẹ và chim con vượt biển,
   trả lời câu hỏi lớp 8 để lấy xô cá rồi nhảy qua
   những tảng băng yếu để trở về!
  </p>
  <p>❤️ Có 3 mạng. Trả lời sai sẽ mất 1 mạng.</p>
  <p>💻 Laptop: dùng phím mũi tên và SPACE.<br>
  📱 Điện thoại: dùng các nút điều khiển.</p>
  <button id="startBtn">BẮT ĐẦU CHƠI!</button>
 </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(function(){
const $=id=>document.getElementById(id);
if(!window.THREE){
 $('message').style.display='block';
 $('message').innerText='Không tải được thư viện 3D. Hãy kiểm tra Internet rồi tải lại trang.';
 return;
}

// ---------- CÂU HỎI LỚP 8 ----------
const bank=[
 {q:"TOÁN: Giá trị của 2³ là bao nhiêu?",
  a:["6","8","9","12"],c:1},
 {q:"TOÁN: Phân tích x² - 9 thành nhân tử.",
  a:["(x-9)(x+1)","(x-3)²","(x-3)(x+3)","x(x-9)"],c:2},
 {q:"VẬT LÍ: Đơn vị của áp suất là gì?",
  a:["Niutơn","Jun","Oát","Pascal"],c:3},
 {q:"VẬT LÍ: Khối lượng riêng được tính bằng công thức nào?",
  a:["D=m/V","D=V/m","D=m×V","D=F/S"],c:0},
 {q:"HÓA HỌC: Chất nào sau đây là đơn chất?",
  a:["Nước","Khí oxi","Muối ăn","Khí cacbonic"],c:1},
 {q:"HÓA HỌC: Công thức hóa học của nước là gì?",
  a:["CO₂","O₂","H₂O","NaCl"],c:2},
 {q:"SINH HỌC: Cơ quan nào thực hiện trao đổi khí ở phổi người?",
  a:["Phế nang","Thực quản","Dạ dày","Thận"],c:0},
 {q:"SINH HỌC: Đòn bẩy là loại máy cơ đơn giản nào?",
  a:["Mặt phẳng nghiêng","Ròng rọc","Bánh xe","Đòn bẩy"],c:3},
 {q:"ĐỊA LÍ: Đường xích đạo chia Trái Đất thành hai bán cầu nào?",
  a:["Đông và Tây","Bắc và Nam","Trên và dưới","Lục địa và đại dương"],c:1},
 {q:"LỊCH SỬ: Ai lãnh đạo cuộc khởi nghĩa Lam Sơn?",
  a:["Trần Hưng Đạo","Quang Trung","Lê Lợi","Ngô Quyền"],c:2},
 {q:"NGỮ VĂN: Từ nào là từ láy?",
  a:["Lấp lánh","Nhà cửa","Sách vở","Cây cối"],c:0},
 {q:"TIẾNG ANH: Choose the correct form: She ___ to school every day.",
  a:["go","going","gone","goes"],c:3},
 {q:"TOÁN: Tổng các góc trong một tứ giác bằng bao nhiêu?",
  a:["180°","360°","90°","270°"],c:1},
 {q:"VẬT LÍ: Lực có thể làm vật thay đổi điều gì?",
  a:["Chỉ màu sắc","Chỉ nhiệt độ","Chuyển động hoặc biến dạng","Khối lượng riêng luôn tăng"],c:2},
 {q:"ĐỊA LÍ: Trái Đất có hình dạng gần giống hình gì?",
  a:["Cầu dẹt ở hai cực","Lập phương","Hình trụ","Hình nón"],c:0}
];

// ---------- CẢNH 3D ----------
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x91e2f8);
scene.fog=new THREE.Fog(0x91e2f8,28,85);

const camera=new THREE.PerspectiveCamera(
 65,window.innerWidth/window.innerHeight,0.1,200
);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
$('game').appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xe7faff,0x477a91,2));
const sun=new THREE.DirectionalLight(0xffffff,2.4);
sun.position.set(-8,15,8);
sun.castShadow=true;
scene.add(sun);

const mat=(color,roughness=0.8)=>new THREE.MeshStandardMaterial({
 color,roughness
});
const snow=mat(0xf1fcff),ice=mat(0x78d8f6,0.3);
const deepIce=mat(0x3a9fce,0.35);
const black=mat(0x171e2b),white=mat(0xffffff);
const orange=mat(0xff9d35),yellow=mat(0xffd65b);
const ocean=mat(0x168ec4,0.35);

const sea=new THREE.Mesh(
 new THREE.PlaneGeometry(180,180),
 ocean
);
sea.rotation.x=-Math.PI/2;
sea.position.y=-0.7;
sea.receiveShadow=true;
scene.add(sea);

const box=(w,h,d,material,x,y,z)=>{
 const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
 m.position.set(x,y,z);
 m.castShadow=true;m.receiveShadow=true;scene.add(m);
 return m;
};

function makeIsland(z,far=false){
 const group=new THREE.Group();
 const width=far?13:15;
 const land=box(width,1.3,8,snow,0,-0.15,z);
 group.add(land);
 for(let i=0;i<9;i++){
  const x=(Math.random()-.5)*width;
  const zz=z+(Math.random()-.5)*6;
  const mound=new THREE.Mesh(
   new THREE.DodecahedronGeometry(.5+Math.random()*.8,0),snow
  );
  mound.position.set(x,.6,zz);
  mound.scale.y=.5;
  mound.castShadow=true;group.add(mound);
 }
 scene.add(group);
 return group;
}
makeIsland(6);
makeIsland(-36,true);

// ---------- CÂY THÔNG TRÊN BỜ ----------
function tree(x,z){
 const trunk=new THREE.Mesh(
  new THREE.CylinderGeometry(.18,.35,1.7,8),mat(0x765238)
 );
 trunk.position.set(x,.65,z);scene.add(trunk);
 for(let i=0;i<3;i++){
  const crown=new THREE.Mesh(
   new THREE.ConeGeometry(1.2-i*.19,2.2,7),
   mat(i===1?0x287f72:0x399b80)
  );
  crown.position.set(x,1.9+i*.8,z);
  crown.castShadow=true;scene.add(crown);
 }
}
for(let z of [3,7,-33,-38]){
 for(let x of [-6,-4.5,4.5,6])tree(x,z);
}

// ---------- NHÂN VẬT CHIM CÁNH CỤT ----------
function penguin(scale=1){
 const root=new THREE.Group();
 const body=new THREE.Mesh(
  new THREE.SphereGeometry(.55,20,16),black
 );
 body.scale.set(.85,1.18,.72);
 body.position.y=.9;
 body.castShadow=true;root.add(body);

 const belly=new THREE.Mesh(
  new THREE.SphereGeometry(.44,20,16),white
 );
 belly.scale.set(.82,1.12,.38);
 belly.position.set(0,.87,.29);root.add(belly);

 const head=new THREE.Mesh(
  new THREE.SphereGeometry(.39,20,16),black
 );
 head.position.set(0,1.77,.02);head.castShadow=true;root.add(head);

 const eyeMat=mat(0xffffff);
 const pupil=mat(0x111111);
 for(const side of [-1,1]){
  const eye=new THREE.Mesh(new THREE.SphereGeometry(.075,12,10),eyeMat);
  eye.position.set(side*.14,1.82,.35);root.add(eye);
  const dot=new THREE.Mesh(new THREE.SphereGeometry(.035,10,8),pupil);
  dot.position.set(side*.14,1.81,.414);root.add(dot);

  const wing=new THREE.Mesh(
   new THREE.SphereGeometry(.19,12,10),black
  );
  wing.scale.set(.55,1.2,.45);
  wing.position.set(side*.47,.95,.02);
  wing.rotation.z=side*-.15;root.add(wing);

  const foot=new THREE.Mesh(
   new THREE.BoxGeometry(.24,.12,.38),orange
  );
  foot.position.set(side*.2,.12,.2);root.add(foot);
 }
 const beak=new THREE.Mesh(
  new THREE.ConeGeometry(.12,.3,8),orange
 );
 beak.rotation.x=Math.PI/2;
 beak.position.set(0,1.68,.43);root.add(beak);
 root.scale.setScalar(scale);
 return root;
}

const player=penguin(1);
player.position.set(0,0,5);
scene.add(player);
const baby=penguin(.55);
baby.position.set(1.4,0,5.7);
scene.add(baby);

// Xô cá
const bucket=new THREE.Group();
const bucketBody=new THREE.Mesh(
 new THREE.CylinderGeometry(.55,.42,.75,16,1,true),
 mat(0x8bd5ee)
);
bucketBody.position.y=.4;bucket.add(bucketBody);
const rim=new THREE.Mesh(
 new THREE.TorusGeometry(.52,.07,8,20),mat(0xeafaff)
);
rim.rotation.x=Math.PI/2;rim.position.y=.78;bucket.add(rim);
for(let i=0;i<4;i++){
 const fish=new THREE.Mesh(
  new THREE.SphereGeometry(.12,10,8),orange
 );
 fish.scale.set(1,.45,2);
 fish.position.set((i-1.5)*.19,.82,.05);
 bucket.add(fish);
}
bucket.position.set(0,0,-37);
scene.add(bucket);

// ---------- BỐN TẢNG BĂNG ----------
const lanes=[-4.5,-1.5,1.5,4.5];
let platforms=[];
let stage='intro';
let lives=3,questionIndex=0,selected=1;
let currentQ=null,returnIndex=0,returnCount=9;
let jumping=false,jumpV=0,groundY=0;
let invulnerable=0,answerLock=false;
let msgTimer=null;
let pressed={};
let lastTime=performance.now();
let returningPlatforms=[];
let answerMeshes=[];

function clearObjects(arr){
 arr.forEach(o=>scene.remove(o));
 arr.length=0;
}
function clearPlatforms(){
 clearObjects(platforms);
}
function makePlatform(x,z,weak=false){
 const group=new THREE.Group();
 const base=new THREE.Mesh(
  new THREE.BoxGeometry(2.35,.48,2.4),
  weak?mat(0x9adbe9):ice
 );
 base.position.y=-.12;
 base.castShadow=true;base.receiveShadow=true;
 group.add(base);

 const top=new THREE.Mesh(
  new THREE.BoxGeometry(2.2,.12,2.24),
  snow
 );
 top.position.y=.17;group.add(top);

 if(weak){
  const crackMat=mat(0x3988ad);
  for(let i=0;i<3;i++){
   const crack=new THREE.Mesh(
    new THREE.BoxGeometry(.04,.015,.55),crackMat
   );
   crack.position.set((i-1)*.28,.24,(i%2-.5)*.2);
   crack.rotation.y=(i-1)*.5;group.add(crack);
  }
 }
 group.position.set(x,0,z);
 scene.add(group);
 return {group,x,z,weak,sunk:false};
}

function addAnswerText(){
 clearObjects(answerMeshes);
 const canvas=document.createElement('canvas');
 canvas.width=512;canvas.height=160;
 const ctx=canvas.getContext('2d');
 const texture=new THREE.CanvasTexture(canvas);
 // Nhãn 3D đơn giản đặt trên từng tảng băng.
 currentQ.a.forEach((a,i)=>{
  const c=document.createElement('canvas');
  c.width=512;c.height=128;
  const g=c.getContext('2d');
  g.fillStyle='#073b63';g.fillRect(0,0,512,128);
  g.fillStyle='#ffffff';g.font='bold 38px Arial';
  g.textAlign='center';g.textBaseline='middle';
  const text=a.length>21?a.slice(0,20)+'…':a;
  g.fillText(String.fromCharCode(65+i)+'. '+text,256,64);
  const tex=new THREE.CanvasTexture(c);
  const sprite=new THREE.Sprite(new THREE.SpriteMaterial({
   map:tex,transparent:false
  }));
  sprite.scale.set(2.5,.62,1);
  sprite.position.set(lanes[i],.9,-1);
  scene.add(sprite);answerMeshes.push(sprite);
 });
}

function drawPlatforms(){
 clearPlatforms();
 for(let i=0;i<4;i++){
  platforms.push(makePlatform(lanes[i],-1,false));
 }
}

function chooseQuestion(){
 currentQ=bank[Math.floor(Math.random()*bank.length)];
 // Hạn chế lặp câu hỏi ngay trong lượt chơi.
 if(bank.length>1 && currentQ===lastQuestion) {
  currentQ=bank[(bank.indexOf(currentQ)+1)%bank.length];
 }
 lastQuestion=currentQ;
 selected=1;
 $('question').innerText=currentQ.q;
 $('answers').innerHTML='';
 currentQ.a.forEach((a,i)=>{
  const el=document.createElement('div');
  el.className='answer'+(i===selected?' selected':'');
  el.innerText=String.fromCharCode(65+i)+'. '+a;
  $('answers').appendChild(el);
 });
 $('questionBox').style.display='block';
 updateHUD();
 addAnswerText();
}
let lastQuestion=null;

function updateSelected(){
 [...$('answers').children].forEach((el,i)=>{
  el.classList.toggle('selected',i===selected);
 });
}

function updateHUD(){
 $('lives').innerText='❤️'.repeat(Math.max(0,lives))+
 '🖤'.repeat(Math.max(0,3-lives));
 if(stage==='outbound'){
  $('stage').innerText='🧠 VƯỢT CẦU BĂNG';
  $('progress').innerText='Câu '+(questionIndex+1)+'/5';
 }else if(stage==='return'){
  $('stage').innerText='🐟 MANG CÁ TRỞ VỀ';
  $('progress').innerText='Tảng '+Math.min(returnIndex+1,returnCount)+'/'+returnCount;
 }else if(stage==='won'){
  $('stage').innerText='🏆 CHIẾN THẮNG';
  $('progress').innerText='Đã về đích!';
 }
}

function message(text,duration=1600){
 $('message').innerText=text;
 $('message').style.display='block';
 clearTimeout(msgTimer);
 msgTimer=setTimeout(()=>$('message').style.display='none',duration);
}

function loseLife(){
 lives--;
 updateHUD();
 if(lives<=0){
  stage='gameover';
  $('questionBox').style.display='none';
  message('HẾT MẠNG! Hãy bắt đầu lại hành trình nhé.',5000);
  setTimeout(()=>{
   $('start').style.display='flex';
   $('startBtn').innerText='CHƠI LẠI';
  },2200);
 }
}

function startOutbound(){
 stage='outbound';lives=3;questionIndex=0;
 $('start').style.display='none';
 $('message').style.display='none';
 player.position.set(0,0,5);
 baby.position.set(1.4,0,5.7);
 drawPlatforms();
 chooseQuestion();
 updateHUD();
}

function resolveAnswer(){
 if(stage!=='outbound'||answerLock||jumping)return;
 answerLock=true;
 const correct=selected===currentQ.c;
 if(correct){
  message('✨ CHÍNH XÁC! VÁCH NGĂN ĐANG HẠ XUỐNG!',1100);
  // Hạ tảng băng đã chọn rồi mở lượt tiếp theo.
  const p=platforms[selected];
  if(p){
   const from=p.group.position.y;
   const start=performance.now();
   function sink(t){
    const f=Math.min(1,(t-start)/500);
    p.group.position.y=from-1.5*f;
    if(f<1)requestAnimationFrame(sink);
   }
   requestAnimationFrame(sink);
  }
  questionIndex++;
  player.position.z=-1;
  setTimeout(()=>{
   if(stage!=='outbound')return;
   if(questionIndex>=5){
    beginReturn();
   }else{
    player.position.set(0,0,5);
    baby.position.set(1.4,0,5.7);
    drawPlatforms();
    chooseQuestion();
    answerLock=false;
   }
  },1000);
 }else{
  loseLife();
  if(stage==='gameover'){answerLock=false;return}
  message('❄️ Sai rồi! Em mất 1 mạng. Hãy thử lại nhé!');
  player.position.set(0,0,5);
  setTimeout(()=>{answerLock=false},500);
 }
}

function beginReturn(){
 stage='return';returnIndex=0;
 $('questionBox').style.display='none';
 clearObjects(answerMeshes);
 clearPlatforms();
 clearObjects(returningPlatforms);
 player.position.set(0,0,-31);
 baby.position.set(1.2,0,-30.5);
 bucket.position.set(0,0,-37);
 bucket.visible=true;

 // Tạo đường băng về trên cùng cây cầu, có băng yếu.
 for(let i=0;i<returnCount;i++){
  const laneIndex=[1,2,1,0,1,2,3,2,1][i%9];
  const x=lanes[laneIndex];
  const z=-29-i*2.6;
  const weak=[2,5,7].includes(i);
  const p=makePlatform(x,z,weak);
  p.laneIndex=laneIndex;
  returningPlatforms.push(p);
 }
 updateHUD();
 message('🐟 Đã lấy được xô cá! Nhảy qua cầu băng để trở về!',2600);
}

function checkReturnLanding(){
 if(stage!=='return')return;
 const target=returningPlatforms[returnIndex];
 if(!target)return;

 const dx=player.position.x-target.x;
 const dz=player.position.z-target.z;
 if(Math.abs(dx)<1.1 && Math.abs(dz)<1.25){
  if(target.weak){
   target.sunk=true;
   target.group.position.y=-.65;
   message('⚠️ BĂNG YẾU! Nhảy tiếp thật nhanh!',900);
   setTimeout(()=>{
    if(stage==='return'&&returnIndex<returnCount){
     // Nếu đứng quá lâu trên băng yếu, mất mạng và quay lại.
     if(Math.abs(player.position.z-target.z)<1.6){
      loseLife();
      if(stage==='return'){
       player.position.set(target.x,0,target.z+2.5);
      }
     }
    }
   },1200);
  }else{
   target.group.children[0].material=mat(0x7de6b1);
  }
  returnIndex++;
  updateHUD();
  if(returnIndex>=returnCount){
   stage='won';
   $('questionBox').style.display='none';
   message('🎉 CHÚC MỪNG! MẸ CON CHIM CÁNH CỤT ĐÃ MANG CÁ VỀ AN TOÀN!',6000);
   $('start').style.display='flex';
   $('startBtn').innerText='CHƠI LẠI';
   $('start').querySelector('h1').innerHTML='CHIẾN THẮNG!<br>🐧🐟';
   $('start').querySelector('p').innerText='Em đã vượt biển băng thành công và mang xô cá về nhà!';
  }
 }
}

function jump(){
 if(jumping||stage==='intro'||stage==='won'||stage==='gameover')return;
 jumping=true;jumpV=7.5;
 if(stage==='outbound'){
  setTimeout(resolveAnswer,400);
 }
}

function movePlayer(dt){
 if(stage!=='outbound'&&stage!=='return')return;
 const speed=5.2;
 if(pressed.ArrowLeft||pressed.a||pressed.A)player.position.x-=speed*dt;
 if(pressed.ArrowRight||pressed.d||pressed.D)player.position.x+=speed*dt;
 if(pressed.ArrowUp||pressed.w||pressed.W)player.position.z-=speed*dt;
 if(pressed.ArrowDown||pressed.s||pressed.S)player.position.z+=speed*dt;
 player.position.x=Math.max(-6,Math.min(6,player.position.x));
 player.position.z=Math.max(-39,Math.min(8,player.position.z));

 if(jumping){
  player.position.y+=jumpV*dt;
  jumpV-=18*dt;
  if(player.position.y<=groundY){
   player.position.y=groundY;
   jumping=false;
   if(stage==='return')checkReturnLanding();
  }
 }
 if(stage==='outbound'){
  // Chọn đáp án theo vị trí ngang của chim.
  let nearest=0;
  for(let i=1;i<4;i++){
   if(Math.abs(player.position.x-lanes[i])<
      Math.abs(player.position.x-lanes[nearest]))nearest=i;
  }
  selected=nearest;
  updateSelected();
 }
 // Chim con theo sau chim lớn.
 baby.position.x+=(player.position.x+1.2-baby.position.x)*Math.min(1,dt*3);
 baby.position.z+=(player.position.z+.7-baby.position.z)*Math.min(1,dt*3);
}

function updateCamera(){
 const desired=new THREE.Vector3(
  player.position.x*.45,
  5.3+player.position.y*.3,
  player.position.z+10
 );
 camera.position.lerp(desired,.08);
 camera.lookAt(player.position.x,1.1,player.position.z-5);
}

function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min(.04,(now-lastTime)/1000||.016);
 lastTime=now;
 movePlayer(dt);
 updateCamera();
 // Nhấp nhô mặt biển nhẹ.
 sea.position.y=-.7+Math.sin(now*.001)*.04;
 renderer.render(scene,camera);
}
requestAnimationFrame(animate);

window.addEventListener('keydown',e=>{
 if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' '].includes(e.key))
  e.preventDefault();
 if(e.key===' '){if(!e.repeat)jump();return}
 pressed[e.key]=true;
 if(stage==='outbound'){
  if(e.key==='ArrowLeft'||e.key==='a')selected=Math.max(0,selected-1);
  if(e.key==='ArrowRight'||e.key==='d')selected=Math.min(3,selected+1);
  updateSelected();
 }
});
window.addEventListener('keyup',e=>{pressed[e.key]=false});

document.querySelectorAll('[data-key]').forEach(btn=>{
 const key=btn.dataset.key;
 const down=e=>{e.preventDefault();pressed[key]=true};
 const up=e=>{e.preventDefault();pressed[key]=false};
 btn.addEventListener('pointerdown',down);
 btn.addEventListener('pointerup',up);
 btn.addEventListener('pointercancel',up);
 btn.addEventListener('pointerleave',up);
});
$('jump').addEventListener('pointerdown',e=>{
 e.preventDefault();jump();
});

$('startBtn').addEventListener('click',()=>{
 $('start').style.display='none';
 $('start').querySelector('h1').innerHTML='HÀNH TRÌNH<br>VƯỢT BIỂN BĂNG';
 $('start').querySelector('p').innerText=
 'Hãy giúp chim cánh cụt mẹ và chim con vượt biển, trả lời câu hỏi lớp 8 để lấy xô cá rồi nhảy qua những tảng băng yếu để trở về!';
 $('startBtn').innerText='BẮT ĐẦU CHƠI!';
 startOutbound();
});

window.addEventListener('resize',()=>{
 camera.aspect=window.innerWidth/window.innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(window.innerWidth,window.innerHeight);
});
})();
</script>
</body>
</html>
"""

components.html(game, height=900, scrolling=False)
