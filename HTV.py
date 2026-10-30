import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vượt Băng Lấy Cá 3D",
    page_icon="🐧",
    layout="wide"
)

GAME = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;font-family:Arial;background:#9cddf7}
#game{position:relative;width:100%;height:760px;overflow:hidden}
#view{position:absolute;inset:0}
canvas{width:100%;height:100%;display:block}
#hud{position:absolute;top:10px;left:10px;right:10px;display:flex;justify-content:space-between;pointer-events:none}
.pill{background:#092c49dd;color:white;padding:9px 13px;border-radius:15px;font-weight:bold;font-size:14px}
#quiz{position:absolute;top:62px;left:50%;transform:translateX(-50%);width:min(94%,780px);text-align:center;pointer-events:none}
#qtext{display:inline-block;background:#082b49ed;color:white;padding:11px 16px;border-radius:15px;font-size:clamp(15px,2.5vw,22px);font-weight:bold}
#answers{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:8px}
.ans{padding:8px 4px;border-radius:12px;background:#ffffffed;color:#12334b;border:2px solid #a7d9ef;font-size:clamp(10px,1.7vw,15px);font-weight:bold;overflow-wrap:anywhere}
#timer{display:inline-block;margin-top:7px;padding:7px 13px;border-radius:12px;background:#082b49ed;color:#fff1a6;font-weight:bold}
#message{position:absolute;left:50%;top:43%;transform:translate(-50%,-50%);background:#062d48ef;color:white;border:2px solid #ffffffaa;border-radius:17px;padding:13px 19px;font-weight:bold;font-size:20px;text-align:center;max-width:90%;display:none;z-index:5}
#overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(180deg,#061b36a8 0%,#0b4779aa 48%,#b9eaffcc 100%);z-index:10;padding:16px;backdrop-filter:blur(2px)}
.panel{position:relative;overflow:hidden;width:min(95%,590px);background:linear-gradient(155deg,#fffef2f5 0%,#d9f5fff5 55%,#a8e4fff5 100%);color:#12324a;border:3px solid #ffffff;border-radius:30px;padding:30px;text-align:center;box-shadow:0 20px 65px #002b4c88,inset 0 0 0 2px #8bd8f477}
.panel:before{content:"❄  ✦  ❄  ✦  ❄";display:block;color:#4badd7;font-size:19px;letter-spacing:12px;margin-bottom:10px}
.panel:after{content:"🐟  ❄  🐟";display:block;font-size:23px;letter-spacing:12px;margin-top:16px;opacity:.85}
/* Tiêu đề tròn trịa, dễ thương như sticker */
.panel h1 {
    position: relative;
    display: inline-block;
    margin: 12px 0 18px;
    padding: 8px 10px 12px;
    font-family: "Arial Rounded MT Bold", "Trebuchet MS", sans-serif;
    font-size: clamp(28px, 5vw, 45px);
    font-weight: 1000;
    line-height: 1.2;
    letter-spacing: 1px;
    color: #39a9dc;
    -webkit-text-stroke: 2px #ffffff;
    text-shadow:
        2px 2px 0 #ffffff,
        -2px 2px 0 #ffffff,
        2px -2px 0 #ffffff,
        -2px -2px 0 #ffffff,
        0 4px 0 #b7eaff,
        0 7px 0 #65b9e2,
        0 10px 14px #397ca655;
}

/* Tuyết phủ trên tiêu đề */
.panel h1::before {
    content: "❄ ❄ ❄ ❄";
    position: absolute;
    top: -16px;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    color: #ffffff;
    font-size: clamp(12px, 2vw, 18px);
    letter-spacing: 5px;
    -webkit-text-stroke: 0;
    text-shadow: 0 2px 4px #8bdcff;
    white-space: nowrap;
    pointer-events: none;
}
.panel p{line-height:1.6}
.welcome-icon{font-size:76px;line-height:1.2;margin:7px;filter:drop-shadow(0 8px 5px #357ca544);animation:penguinWelcome 1.6s ease-in-out infinite}
@keyframes penguinWelcome{0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-8px) rotate(3deg)}}
.welcome-tag{display:inline-block;border-radius:30px;padding:7px 13px;background:#c7efff;color:#07527b;font-weight:bold;font-size:13px;margin-bottom:12px}
button{border:0;border-radius:14px;padding:12px 18px;background:#087fba;color:white;font-size:16px;font-weight:bold;cursor:pointer;touch-action:manipulation;box-shadow:0 4px 0 #07577e}
button:active{transform:translateY(2px);box-shadow:0 2px 0 #07577e}
#start{margin-top:8px;padding:16px 30px;border:2px solid #fff8a6;border-radius:18px;background:linear-gradient(135deg,#ffdc55,#ff9f22);color:#173954;font-size:19px;box-shadow:0 6px 0 #bd6d16,0 10px 22px #07577e44;animation:startPulse 1.8s ease-in-out infinite}
@keyframes startPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.035)}}
#controls{position:absolute;bottom:12px;left:12px;right:12px;display:flex;justify-content:space-between;align-items:flex-end;pointer-events:none}
.pad{display:grid;grid-template-columns:repeat(3,46px);grid-template-rows:repeat(2,42px);gap:5px;pointer-events:auto}
.ctrl{border:2px solid #ffffffb8;border-radius:14px;background:#073451d9;color:white;font-size:21px;font-weight:bold;padding:5px;box-shadow:0 3px 0 #03233b}
#jump{width:88px;height:88px;border-radius:50%;font-size:15px;pointer-events:auto;background:linear-gradient(135deg,#12a9dc,#07669e)}
#hint{position:absolute;bottom:110px;left:50%;transform:translateX(-50%);padding:6px 10px;border-radius:10px;background:#092c49b9;color:white;font-size:12px;white-space:nowrap;pointer-events:none}
@media(max-width:520px){
.pill{font-size:11px;padding:7px 9px}
#quiz{top:57px}
.ans{padding:7px 2px;font-size:10px}
.pad{grid-template-columns:repeat(3,40px);grid-template-rows:repeat(2,38px)}
#jump{width:78px;height:78px}
.panel{padding:20px}
}
</style>
</head>
<body>
<div id="game">
<div id="view"></div>

<div id="hud">
<div class="pill" id="stage">🐧 MÀN 1: ĐI LẤY CÁ</div>
<div style="display:flex;align-items:center;gap:8px;pointer-events:auto">
   <div style="display:flex;gap:8px;align-items:center;pointer-events:auto">
  <div class="pill" id="progress">Câu 1/7</div>
  <button id="settingsBtn" aria-label="Cài đặt"
    style="padding:8px 12px;border-radius:14px;background:#092c49;color:white;font-size:20px">
    ⚙️
  </button>
</div>
    <button id="settingsBtn" title="Cài đặt"
        style="padding:8px 11px;border-radius:14px;background:#092c49dd;
        color:white;font-size:20px;box-shadow:none">⚙️</button>
</div>
</div>

<div id="quiz">
<div id="qtext">Sẵn sàng chưa?</div>
<div id="answers"></div>
<div id="timer">⏱ 15 giây</div>
</div>

<div id="message"></div>
<div id="settingsPanel" style="
display:none;position:absolute;inset:0;z-index:20;
align-items:center;justify-content:center;padding:16px;
background:#041a30aa;backdrop-filter:blur(5px)">

  <div style="
  width:min(92%,380px);padding:24px;border-radius:25px;
  background:linear-gradient(145deg,#f5fdff,#bceaff);
  border:3px solid white;text-align:center;
  color:#12324a;box-shadow:0 15px 40px #002b4c88">

    <button id="closeSettings" style="
    float:right;padding:5px 11px;background:#d5efff;
    color:#12324a;font-size:18px">✕</button>

    <h2 style="margin-top:20px">⚙️ CÀI ĐẶT</h2>

    <div style="margin:20px 0;padding:13px;background:#ffffffbb;border-radius:15px">
      <label style="font-weight:bold;font-size:16px">
        <input type="checkbox" id="soundToggle" checked
        style="width:18px;height:18px;vertical-align:middle">
        🔊 Bật âm thanh
      </label>
    </div>

    <button id="resumeBtn" style="width:100%;margin:6px 0">
      ▶️ TIẾP TỤC CHƠI
    </button>

    <button id="restartBtn" style="
    width:100%;margin:6px 0;background:#f4a735;color:#173954">
      🔄 CHƠI LẠI TỪ ĐẦU
    </button>

    <button id="homeBtn" style="
    width:100%;margin:6px 0;background:#477b9c">
      🏠 VỀ MÀN HÌNH CHÀO MỪNG
    </button>

  </div>
</div>

<div id="hint">← → chọn hướng · ↑ tiến · ↓ lùi · SPACE nhảy</div>

<div id="controls">
<div class="pad">
<div></div><button class="ctrl" id="up">↑</button><div></div>
<button class="ctrl" id="left">←</button>
<button class="ctrl" id="down">↓</button>
<button class="ctrl" id="right">→</button>
</div>
<button class="ctrl" id="jump">NHẢY<br>❄️</button>
</div>

<div id="overlay">
<div class="panel" id="panel">
<div class="welcome-tag">❄️ CUỘC PHIÊU LƯU MÙA ĐÔNG ❄️</div>
<div class="welcome-icon">🐧 🐟</div>
<h1>VƯỢT BĂNG LẤY CÁ</h1>
<p><b>Chào mừng nhà thám hiểm nhỏ!</b></p>
<p>Hãy đồng hành cùng chim cánh cụt mẹ vượt qua cây cầu băng, trả lời những câu hỏi thú vị và mang xô cá trở về an toàn.</p>
<p>🧠 Vượt thử thách kiến thức<br>
🧊 Cẩn thận với những tảng băng yếu<br>
🎮 Dùng phím điều hướng để di chuyển</p>
<button id="start">🐧 BẮT ĐẦU CHƠI</button>
</div>
</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(()=>{
"use strict";
const $=id=>document.getElementById(id);

const questionBank=[
{q:"TOÁN: Rút gọn (x+3)² − (x−3)².",a:["6x","12x","2x²+18","12x+18"],c:1},
{q:"TOÁN: Phân tích x² − 16 thành nhân tử.",a:["(x−4)²","(x+4)²","(x−4)(x+4)","x(x−16)"],c:2},
{q:"TOÁN: Khai triển (2x−3)².",a:["4x²−9","4x²−12x+9","4x²+12x+9","2x²−12x+9"],c:1},
{q:"TOÁN: Phân tích x²+6x+9 thành nhân tử.",a:["(x+3)²","(x−3)²","(x+9)(x−1)","x(x+6)+9x"],c:0},
{q:"TOÁN: Với x=2, x³−2x²+3 bằng bao nhiêu?",a:["3","5","7","11"],c:1},
{q:"HÌNH HỌC: Tứ giác có hai cặp cạnh đối song song là hình gì?",a:["Hình thang","Hình bình hành","Hình diều","Tam giác cân"],c:1},
{q:"HÌNH HỌC: Hình bình hành có hai đường chéo vuông góc là hình gì?",a:["Hình chữ nhật","Hình thang cân","Hình thoi","Hình thang vuông"],c:2},
{q:"HÌNH HỌC: Hình chữ nhật có hai cạnh kề bằng nhau là hình gì?",a:["Hình thoi","Hình vuông","Hình bình hành thường","Hình thang cân"],c:1},
{q:"HÌNH HỌC: Tam giác vuông có hai cạnh góc vuông 5 cm và 12 cm. Cạnh huyền?",a:["13 cm","15 cm","17 cm","10 cm"],c:0},
{q:"HÌNH HỌC: Tổng các góc trong một tứ giác bằng bao nhiêu?",a:["180°","270°","360°","540°"],c:2},
{q:"VẬT LÍ: Công thức tính khối lượng riêng là gì?",a:["D=mV","D=m/V","D=V/m","D=m+V"],c:1},
{q:"VẬT LÍ: Vật có khối lượng 600 g, thể tích 200 cm³. Khối lượng riêng?",a:["0,3 g/cm³","3 g/cm³","30 g/cm³","120 000 g/cm³"],c:1},
{q:"VẬT LÍ: Đổi 2,7 g/cm³ sang kg/m³.",a:["27 kg/m³","270 kg/m³","2 700 kg/m³","27 000 kg/m³"],c:2},
{q:"VẬT LÍ: Hai vật cùng thể tích, A có khối lượng lớn hơn B. Kết luận đúng?",a:["A có khối lượng riêng lớn hơn B","B lớn hơn A","Hai vật bằng nhau","Không thể so sánh"],c:0},
{q:"VẬT LÍ: Vật có D=800 kg/m³ và V=0,02 m³. Khối lượng?",a:["16 kg","40 kg","400 kg","1 600 kg"],c:0},
{q:"HÓA HỌC: Hòa tan 10 g muối vào 80 g nước. Nồng độ phần trăm xấp xỉ?",a:["10%","11,1%","12,5%","20%"],c:1},
{q:"HÓA HỌC: Hòa tan 20 g đường vào 180 g nước. Nồng độ phần trăm?",a:["10%","11,1%","20%","25%"],c:0},
{q:"HÓA HỌC: Pha 200 g dung dịch muối nồng độ 5% cần bao nhiêu gam muối?",a:["5 g","10 g","20 g","40 g"],c:1},
{q:"HÓA HỌC: Trong phản ứng hóa học, phát biểu nào đúng về khối lượng?",a:["Chất phản ứng nhẹ hơn sản phẩm","Chất phản ứng nặng hơn sản phẩm","Tổng khối lượng chất phản ứng bằng sản phẩm","Khối lượng bằng 0"],c:2},
{q:"HÓA HỌC: Dấu hiệu có thể cho thấy phản ứng hóa học xảy ra?",a:["Nước đá tan","Nước bay hơi","Xuất hiện chất khí hoặc kết tủa mới","Đường nghiền nhỏ"],c:2},
{q:"SINH HỌC: Cơ quan nào bơm máu đi khắp cơ thể?",a:["Phổi","Tim","Gan","Dạ dày"],c:1},
{q:"SINH HỌC: Trao đổi khí ở phổi diễn ra chủ yếu tại đâu?",a:["Khí quản","Phế quản","Phế nang","Thanh quản"],c:2},
{q:"SINH HỌC: Thành phần máu vận chuyển oxygen chủ yếu là gì?",a:["Hồng cầu","Bạch cầu","Tiểu cầu","Huyết tương"],c:0},
{q:"ĐỊA LÍ: Nguyên nhân chủ yếu tạo nên khác biệt khí hậu Bắc – Nam Việt Nam?",a:["Việt Nam nằm hoàn toàn trong ôn đới","Lãnh thổ kéo dài Bắc – Nam và chịu tác động gió mùa","Miền Nam gần cực Bắc hơn","Không chịu ảnh hưởng biển"],c:1},
{q:"ĐỊA LÍ: Đặc điểm phù hợp với khí hậu nhiệt đới gió mùa Việt Nam?",a:["Lạnh quanh năm, không mưa","Thay đổi theo mùa và chịu ảnh hưởng gió mùa","Chỉ có mùa đông","Thời tiết mọi vùng giống nhau"],c:1},
{q:"LỊCH SỬ: Chiến thắng Bạch Đằng năm 938 gắn với ai?",a:["Trần Hưng Đạo","Ngô Quyền","Lê Lợi","Quang Trung"],c:1},
{q:"LỊCH SỬ: Phong trào Tây Sơn gắn với ba anh em nào?",a:["Nguyễn Huệ, Nguyễn Nhạc, Nguyễn Lữ","Nguyễn Trãi, Nguyễn Huệ, Nguyễn Ánh","Trần Quốc Tuấn, Trần Quang Khải, Trần Nhật Duật","Lê Lợi, Lê Lai, Nguyễn Trãi"],c:0},
{q:"LỊCH SỬ: Chiến thắng Ngọc Hồi – Đống Đa năm 1789 gắn với ai?",a:["Ngô Quyền","Lê Lợi","Quang Trung – Nguyễn Huệ","Trần Hưng Đạo"],c:2},
{q:"ENGLISH: If it rains tomorrow, we _____ at home.",a:["stay","stayed","will stay","staying"],c:2},
{q:"ENGLISH: Choose the correct sentence.",a:["She enjoys read books.","She enjoys reading books.","She enjoy reading books.","She enjoying read books."],c:1},
{q:"ENGLISH: This exercise is _____ than the last one.",a:["difficult","more difficult","most difficult","the difficult"],c:1},
{q:"ENGLISH: Although he was tired, he _____ his homework.",a:["finish","finishes","finished","finishing"],c:2}
];

let questions=[],scene,camera,renderer,clock,penguin,fishBucket;
let ambientLight,skyLight,snow,stars=[],moon;
let iceRows=[],returnRows=[];
let started=false,phase="outbound",row=0,lane=1,step=0;
let busy=false,jumping=false,falling=false;
let jumpStart=0,jumpFrom=new THREE.Vector3(),jumpTo=new THREE.Vector3();
let fallStart=0,fallCallback=null,timerInterval=null,timeLeft=15;
let messageTimeout=null;
let penguinEyes=[],penguinWings=[],blinkAt=0,blinkUntil=0;
const laneX=[-4.2,-1.4,1.4,4.2];
const RETURN_ROW_COUNT=9,RETURN_SPACING=4.1;

function shuffle(a){
a=a.slice();
for(let i=a.length-1;i>0;i--){
let j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];
}
return a;
}
function chooseQuestions(){questions=shuffle(questionBank).slice(0,7)}
function mat(color,roughness=.75,metalness=0){
return new THREE.MeshStandardMaterial({color,roughness,metalness});
}

function init(){
scene=new THREE.Scene();
scene.background=new THREE.Color(0x9cddf7);
scene.fog=new THREE.Fog(0xb8eaff,35,100);
camera=new THREE.PerspectiveCamera(60,innerWidth/innerHeight,.1,250);
renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(innerWidth,innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
$("view").appendChild(renderer.domElement);
clock=new THREE.Clock();

ambientLight=new THREE.HemisphereLight(0xe4f8ff,0x59879c,2);
scene.add(ambientLight);
skyLight=new THREE.DirectionalLight(0xffffff,2.2);
skyLight.position.set(-8,18,8);
skyLight.castShadow=true;
scene.add(skyLight);

buildWater();
buildShore(-31);
buildShore(12);
buildDistantIcebergs();
buildSnowyTrees();
buildPenguin();
buildBucket();
buildIceRows();
buildSnow();
buildStars();
addEventListener("resize",resize);
animate();
}

function buildWater(){
const water=new THREE.Mesh(new THREE.PlaneGeometry(200,200),mat(0x55c8ed,.35));
water.rotation.x=-Math.PI/2;
water.position.set(0,-.6,-15);
scene.add(water);
for(let i=0;i<40;i++){
const line=new THREE.Mesh(new THREE.BoxGeometry(1.3,.025,.035),mat(0xc8f5ff));
line.position.set((Math.random()-.5)*38,-.53,-30+Math.random()*50);
scene.add(line);
}
}
function buildShore(z){
const land=new THREE.Mesh(new THREE.BoxGeometry(24,.8,12),mat(0xe8f5fa));
land.position.set(0,-.15,z);land.receiveShadow=true;scene.add(land);
for(let i=0;i<16;i++){
const rock=new THREE.Mesh(new THREE.DodecahedronGeometry(.3+Math.random()*.4),mat(0xb7dce9));
rock.position.set(-11+Math.random()*22,.28,z-5+Math.random()*10);
rock.scale.y=.45;scene.add(rock);
}
}
function buildDistantIcebergs(){
for(let i=0;i<18;i++){
const h=5+Math.random()*9,side=i%2===0?-1:1;
const m=new THREE.Mesh(new THREE.ConeGeometry(2.5+Math.random()*3,h,5),mat(i%2?0xc8eefa:0xa8d9ee));
m.position.set(side*(15+Math.random()*22),h/2-.5,-35+Math.random()*60);
scene.add(m);
}
}
function buildSnowyTrees(){
const trunkMat=mat(0x76513a),snowMat=mat(0xf5fcff);
const green=[mat(0x17664f),mat(0x247a5b),mat(0x318669)];
for(const side of [-1,1]){
for(let i=0;i<18;i++){
const z=10-i*3.5,x=side*(8.5+(i%3)*1.25),h=2.8+(i%4)*.45;
const tree=new THREE.Group();
const trunk=new THREE.Mesh(new THREE.CylinderGeometry(.13,.2,h*.35,7),trunkMat);
trunk.position.y=h*.175;tree.add(trunk);
for(let layer=0;layer<3;layer++){
const radius=1.05-layer*.18,layerHeight=h*.48,y=h*.25+layer*h*.22;
const leaves=new THREE.Mesh(new THREE.ConeGeometry(radius,layerHeight,8),green[(i+layer)%green.length]);
leaves.position.y=y;tree.add(leaves);
const snowCap=new THREE.Mesh(new THREE.ConeGeometry(radius*.86,layerHeight*.78,8),snowMat);
snowCap.position.y=y+.12;tree.add(snowCap);
}
tree.position.set(x,0,z);tree.rotation.y=(Math.random()-.5)*.2;scene.add(tree);
}
}
}
function buildPenguin(){
penguin=new THREE.Group();
const black=mat(0x202f43),white=mat(0xf5fbff),orange=mat(0xffa52e),eye=mat(0x101820);
function sphere(r,m,x,y,z,sx=1,sy=1,sz=1){
const o=new THREE.Mesh(new THREE.SphereGeometry(r,18,14),m);
o.position.set(x,y,z);o.scale.set(sx,sy,sz);o.castShadow=true;penguin.add(o);return o;
}
sphere(.58,black,0,.9,0,.85,1.1,.72);
sphere(.43,white,0,.9,-.39,.8,1,.25);
sphere(.36,black,0,1.72,-.02,.9,1,.8);
const eyeLeft=sphere(.07,eye,-.13,1.79,-.34);
const eyeRight=sphere(.07,eye,.13,1.79,-.34);
penguinEyes=[eyeLeft,eyeRight];
sphere(.12,orange,0,1.62,-.4,1,.5,1);
for(const s of [-1,1]){
const wing=sphere(.18,black,s*.52,1.02,-.02,1.2,.48,.65);
wing.rotation.z=s*.25;
penguinWings.push({mesh:wing,base:wing.rotation.z,side:s});
sphere(.2,orange,s*.23,.27,-.02,1,.4,1.4);
}
penguin.position.set(laneX[lane],.15,4.3);scene.add(penguin);
}
function buildBucket(){
fishBucket=new THREE.Group();
const body=new THREE.Mesh(new THREE.CylinderGeometry(.42,.3,.65,16,1,true),mat(0x8cbdcc));
body.position.y=.35;fishBucket.add(body);
const rim=new THREE.Mesh(new THREE.TorusGeometry(.4,.045,8,20),mat(0xe4f7ff));
rim.rotation.x=Math.PI/2;rim.position.y=.67;fishBucket.add(rim);
const handle=new THREE.Mesh(new THREE.TorusGeometry(.29,.035,8,20,Math.PI),mat(0xeffaff));
handle.position.y=.68;handle.rotation.z=Math.PI;fishBucket.add(handle);
for(let i=0;i<3;i++){
const fish=new THREE.Mesh(new THREE.SphereGeometry(.12,10,8),mat(0xffb84d));
fish.position.set((i-1)*.17,.58,.05);fish.scale.set(1,.5,.5);fishBucket.add(fish);
}
fishBucket.position.set(1.05,.15,-32);fishBucket.visible=false;scene.add(fishBucket);
}
function makeTile(x,z,w=2.45,d=2.5){
const group=new THREE.Group();
group.add(new THREE.Mesh(new THREE.BoxGeometry(w,.32,d),mat(0x8fdcf4,.25,.1)));
const top=new THREE.Mesh(new THREE.BoxGeometry(w-.12,.09,d-.14),mat(0xe8fbff,.2));
top.position.y=.2;group.add(top);
for(let i=0;i<3;i++){
const crack=new THREE.Mesh(new THREE.BoxGeometry(.04,.015,.7),mat(0x468ca9));
crack.position.set((i-1)*.45,.252,(i%2)*.3-.1);crack.rotation.y=.4;crack.visible=false;group.add(crack);
}
group.position.set(x,0,z);scene.add(group);
group.userData.cracks=group.children.slice(2);group.userData.cracked=false;
return group;
}
function buildIceRows(){
iceRows=[];
for(let r=0;r<7;r++){
const tiles=[];
for(let l=0;l<4;l++)tiles.push(makeTile(laneX[l],-r*4.1));
iceRows.push(tiles);
}
}
function buildSnow(){
const count=1300,positions=new Float32Array(count*3),velocities=new Float32Array(count);
for(let i=0;i<count;i++){
positions[i*3]=(Math.random()-.5)*65;positions[i*3+1]=Math.random()*28;
positions[i*3+2]=-40+Math.random()*65;velocities[i]=1.3+Math.random()*3.4;
}
const geo=new THREE.BufferGeometry();
geo.setAttribute("position",new THREE.BufferAttribute(positions,3));
snow=new THREE.Points(geo,new THREE.PointsMaterial({color:0xffffff,size:.12,transparent:true,opacity:.9}));
snow.userData.velocities=velocities;scene.add(snow);
}
function buildStars(){
const positions=[];
for(let i=0;i<450;i++)positions.push((Math.random()-.5)*120,8+Math.random()*45,-55+Math.random()*80);
const geo=new THREE.BufferGeometry();geo.setAttribute("position",new THREE.Float32BufferAttribute(positions,3));
const s=new THREE.Points(geo,new THREE.PointsMaterial({color:0xffffff,size:.16}));
s.visible=false;scene.add(s);stars.push(s);
moon=new THREE.Mesh(new THREE.SphereGeometry(2,24,20),new THREE.MeshBasicMaterial({color:0xfff0bc}));
moon.position.set(13,17,-38);moon.visible=false;scene.add(moon);
}
function setNight(on){
if(on){
scene.background=new THREE.Color(0x06132f);scene.fog=new THREE.Fog(0x101d42,22,85);
ambientLight.color.set(0x6078b8);ambientLight.groundColor.set(0x172342);ambientLight.intensity=.8;
skyLight.color.set(0x9ebaff);skyLight.intensity=.65;
stars.forEach(s=>s.visible=true);moon.visible=true;
}else{
scene.background=new THREE.Color(0x9cddf7);scene.fog=new THREE.Fog(0xb8eaff,35,100);
ambientLight.color.set(0xe4f8ff);ambientLight.groundColor.set(0x59879c);ambientLight.intensity=2;
skyLight.color.set(0xffffff);skyLight.intensity=2.2;
stars.forEach(s=>s.visible=false);moon.visible=false;
}
}
function resize(){
camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);
}
function msg(text,ms=1100){
$("message").textContent=text;$("message").style.display="block";clearTimeout(messageTimeout);
if(ms>0)messageTimeout=setTimeout(()=>$("message").style.display="none",ms);
}
function stopTimer(){if(timerInterval!==null){clearInterval(timerInterval);timerInterval=null}}
function startTimer(){
stopTimer();timeLeft=15;$("timer").textContent="⏱ 15 giây";$("timer").style.color="#fff1a6";
timerInterval=setInterval(()=>{
if(!started||phase!=="outbound"||busy){stopTimer();return}
timeLeft--;$("timer").textContent="⏱ "+timeLeft+" giây";
if(timeLeft<=5)$("timer").style.color="#ff7777";
if(timeLeft<=0){stopTimer();breakTile(iceRows[row][lane]);msg("Hết giờ! Tảng băng vỡ rồi!",1400);busy=true;setTimeout(()=>fall(resetStart),300)}
},1000);
}
function showQuestion(){
if(row>=questions.length){reachShore();return}
const q=questions[row];$("qtext").textContent=q.q;
$("answers").innerHTML=q.a.map((a,i)=>'<div class="ans">'+String.fromCharCode(65+i)+". "+a+"</div>").join("");
$("progress").textContent="Câu "+(row+1)+"/"+questions.length;
$("stage").textContent="🐧 MÀN 1: ĐI LẤY CÁ";$("quiz").style.display="block";startTimer();
}
function moveHorizontal(d){
    if(!started || busy || falling || jumping) return;

    // Màn 2: đảo chiều điều khiển
    const direction = phase === "return" ? -d : d;

    lane = Math.max(0, Math.min(3, lane + direction));
    penguin.position.x = laneX[lane];
}
function move(d){
    if(!started || busy || falling || jumping) return;
    if(d === 0) return;

    // Màn 2 đảo hướng vì chim quay mặt về hướng ngược lại
    const direction = phase === "return" ? -d : d;

    lane = Math.max(0, Math.min(3, lane + direction));
    penguin.position.x = laneX[lane];

    if(phase === "return" && fishBucket.visible){
        fishBucket.position.x = penguin.position.x + 1.05;
    }
}
function breakTile(tile){
if(!tile)return;
tile.userData.cracked=true;tile.userData.cracks.forEach(c=>c.visible=true);
tile.rotation.z=.08;tile.position.y=-.25;
}
function jump(){
if(!started||busy||falling||jumping)return;
if(phase==="outbound"){
if(!iceRows[row]||!iceRows[row][lane])return;
stopTimer();busy=true;jumping=true;jumpStart=performance.now();
jumpFrom.copy(penguin.position);jumpTo.set(laneX[lane],.15,iceRows[row][lane].position.z+.25);
penguin.userData.jumpCorrect=(lane===questions[row].c);
msg("Đang nhảy lên tảng băng...",0);
}else if(phase==="return"){
const tile=returnRows[step]&&returnRows[step][lane];if(!tile)return;
busy=true;jumping=true;jumpStart=performance.now();
jumpFrom.copy(penguin.position);jumpTo.set(tile.position.x,.15,tile.position.z);
penguin.userData.returnTile=tile;msg("Đang nhảy về phía trước!",0);
}
}
function fall(callback){
if(falling)return;
falling=true;jumping=false;busy=true;fallStart=performance.now();fallCallback=callback;
}
function resetStart(){
falling=false;jumping=false;busy=false;row=0;lane=1;step=0;phase="outbound";chooseQuestions();
penguin.position.set(laneX[lane],.15,4.3);penguin.rotation.set(0,0,0);
fishBucket.visible=false;
iceRows.forEach(r=>r.forEach(t=>{t.position.y=0;t.rotation.z=0;t.userData.cracked=false;t.userData.cracks.forEach(c=>c.visible=false)}));
returnRows.forEach(r=>r.forEach(t=>scene.remove(t)));returnRows=[];
setNight(false);$("quiz").style.display="block";showQuestion();msg("Chơi lại nhé!",1200);
}
function reachShore(){
stopTimer();phase="shore";busy=true;$("quiz").style.display="none";
penguin.position.set(0,.15,-29);fishBucket.visible=true;
fishBucket.position.set(1.05,.15,-29);
msg("Đã sang bờ! Chim mẹ đã lấy được xô cá!",1500);
setTimeout(()=>{if(!started)return;startReturn()},1500);
}
function createReturnRows(){
returnRows.forEach(r=>r.forEach(t=>scene.remove(t)));returnRows=[];
for(let r=0;r<RETURN_ROW_COUNT;r++){
const tiles=[],weak=shuffle([0,1,2,3]).slice(0,2);
for(let l=0;l<4;l++){
const tile=makeTile(laneX[l],-25+r*RETURN_SPACING,2.1,2.2);
tile.userData.weak=weak.includes(l);tiles.push(tile);
}
returnRows.push(tiles);
}
}
function startReturn(){
phase="return";step=0;lane=1;busy=false;jumping=false;falling=false;setNight(true);createReturnRows();
penguin.position.set(laneX[lane],.15,-29);penguin.rotation.set(0,Math.PI,0);
fishBucket.visible=true;fishBucket.position.set(penguin.position.x+1.05,.15,penguin.position.z);
$("stage").textContent="🌙 MÀN 2: TRỞ VỀ";$("progress").textContent="Hàng băng 1/"+RETURN_ROW_COUNT;
$("quiz").style.display="none";
$("hint").textContent="← → chọn tảng băng · ↑ tiến · ↓ lùi · SPACE nhảy";
msg("Mang xô cá trở về! Cẩn thận với băng yếu!",2200);
}
function resetBucket(){
falling=false;jumping=false;busy=false;phase="return";step=0;lane=1;
returnRows.forEach(r=>r.forEach(t=>{t.position.y=0;t.rotation.z=0;t.userData.cracked=false;t.userData.cracks.forEach(c=>c.visible=false)}));
penguin.position.set(laneX[lane],.15,-29);penguin.rotation.set(0,Math.PI,0);
fishBucket.visible=true;fishBucket.position.set(penguin.position.x+1.05,.15,penguin.position.z);
$("progress").textContent="Hàng băng 1/"+RETURN_ROW_COUNT;msg("Em đã quay lại bờ lấy cá. Thử đường băng lần nữa nhé!",1800);
}

function win(){
    busy = true;
    started = false;
    stopTimer();

    $("overlay").style.display = "flex";

    $("panel").innerHTML = `
      <style>
        .win-title {
          color: #287ba8;
          font-family: "Trebuchet MS", Arial, sans-serif;
          font-size: clamp(27px, 5vw, 42px);
          font-weight: 1000;
          line-height: 1.35;
          -webkit-text-stroke: 1px white;
          text-shadow:
            2px 3px 0 #ffffff,
            0 5px 0 #a9d9ee,
            0 8px 12px #315d7860;
          margin: 12px 0 20px;
        }

        .win-text {
          color: #244d68;
          font-size: 17px;
          font-weight: bold;
          line-height: 1.8;
          text-shadow: 0 2px 0 white;
        }

        .confetti-piece {
          position: fixed;
          top: -20px;
          width: 10px;
          height: 16px;
          z-index: 100;
          pointer-events: none;
          animation: confettiFall linear forwards;
        }

        @keyframes confettiFall {
          0% {
            transform: translateY(-20px) rotate(0deg);
            opacity: 1;
          }
          100% {
            transform: translateY(105vh) rotate(900deg);
            opacity: 0.85;
          }
        }

        .win-penguin {
          font-size: 70px;
          filter: drop-shadow(0 7px 4px #5285a455);
          animation: winBounce 1.2s ease-in-out infinite;
        }

        @keyframes winBounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-9px); }
        }
      </style>

      <div class="welcome-tag">❄️ CHUYẾN PHIÊU LƯU HOÀN THÀNH ❄️</div>
      <div class="win-penguin">🐧 🐟</div>
      <h1 class="win-title">🎉 CHIẾN THẮNG! 🎉</h1>
      <p class="win-text">
        Chim cánh cụt mẹ đã mang xô cá về an toàn!<br>
        Em đã vượt qua tất cả các tảng băng!
      </p>
      <button id="restart">🔄 CHƠI LẠI</button>
    `;

    // Tạo pháo giấy nhiều màu
    const colors = [
      "#77c9f2", "#ffb8c9", "#ffe08a",
      "#a8e6cf", "#c9b6ff", "#ffffff"
    ];

    const confetti = [];

    for(let i = 0; i < 100; i++){
      const piece = document.createElement("div");
      piece.className = "confetti-piece";
      piece.style.left = Math.random() * 100 + "vw";
      piece.style.backgroundColor =
        colors[Math.floor(Math.random() * colors.length)];
      piece.style.borderRadius = Math.random() > 0.5 ? "50%" : "3px";
      piece.style.animationDuration = (2.5 + Math.random() * 3) + "s";
      piece.style.animationDelay = (Math.random() * 1.8) + "s";

      document.body.appendChild(piece);
      confetti.push(piece);
    }

    setTimeout(() => {
      confetti.forEach(piece => piece.remove());
    }, 8000);

    $("restart").onclick = () => location.reload();
    $("quiz").style.display = "none";
}

function startGame(){
$("overlay").style.display="none";chooseQuestions();started=true;phase="outbound";
row=0;lane=1;step=0;busy=false;jumping=false;falling=false;setNight(false);
penguin.position.set(laneX[lane],.15,4.3);penguin.rotation.set(0,0,0);
fishBucket.visible=false;$("hint").textContent="← → chọn đáp án · ↑ tiến · ↓ lùi · SPACE nhảy";
iceRows.forEach(r=>r.forEach(t=>{t.position.y=0;t.rotation.z=0;t.userData.cracked=false;t.userData.cracks.forEach(c=>c.visible=false)}));
showQuestion();
}
function animate(){
requestAnimationFrame(animate);
const dt=Math.min(clock.getDelta(),.05);
if(penguinEyes.length){
const now=performance.now();
if(now>blinkAt){blinkUntil=now+140;blinkAt=now+2200+Math.random()*2200;}
const closed=now<blinkUntil;
penguinEyes.forEach(e=>{e.scale.y=closed ? 0.12 : 1;});
const flap=Math.sin(now*.009)*.22;
penguinWings.forEach(w=>{w.mesh.rotation.z=w.base+w.side*flap;});
}
if(snow){
const p=snow.geometry.attributes.position.array,v=snow.userData.velocities;
for(let i=0;i<v.length;i++){
p[i*3+1]-=v[i]*dt;p[i*3]+=Math.sin(performance.now()*.0005+i)*dt*.18;
if(p[i*3+1]<-.8){p[i*3+1]=20+Math.random()*10;p[i*3]=-32+Math.random()*64;p[i*3+2]=penguin.position.z-30+Math.random()*60}
}
snow.geometry.attributes.position.needsUpdate=true;
}
if(jumping){
const t=Math.min(1,(performance.now()-jumpStart)/650);
penguin.position.x=THREE.MathUtils.lerp(jumpFrom.x,jumpTo.x,t);
penguin.position.z=THREE.MathUtils.lerp(jumpFrom.z,jumpTo.z,t);
penguin.position.y=.15+Math.sin(t*Math.PI)*1.7;penguin.rotation.x=Math.sin(t*Math.PI)*.12;
if(phase==="return"&&fishBucket.visible)fishBucket.position.set(penguin.position.x+1.05,penguin.position.y+.05,penguin.position.z);
if(t>=1){
jumping=false;penguin.position.copy(jumpTo);penguin.rotation.x=0;
if(phase==="outbound"){
if(penguin.userData.jumpCorrect){
msg("Chính xác! Em đã đứng trên băng! ✔",850);row++;
setTimeout(()=>{if(!started)return;busy=false;if(row>=questions.length)reachShore();else{penguin.position.z=iceRows[row][0].position.z+2.7;showQuestion()}},600);
}else{breakTile(iceRows[row][lane]);msg("Sai đáp án! Băng vỡ!",1300);setTimeout(()=>fall(resetStart),300)}
}else if(phase==="return"){
const tile=penguin.userData.returnTile;
if(tile&&tile.userData.weak){
breakTile(tile);msg("Băng yếu vỡ rồi! Chim rơi xuống nước!",1300);setTimeout(()=>fall(resetBucket),300);
}else{
step++;
if(step>=RETURN_ROW_COUNT){msg("Về tới bờ an toàn!",1000);setTimeout(win,1000)}
else{$("progress").textContent="Hàng băng "+(step+1)+"/"+RETURN_ROW_COUNT;msg("Đã đáp xuống! Nhảy tiếp về phía trước!",900);setTimeout(()=>{busy=false},500)}
}
}
}
}
if(falling){
const t=Math.min(1,(performance.now()-fallStart)/650);
penguin.position.y=.15-t*2.8;penguin.rotation.x=t*1.2;
if(t>=1){falling=false;if(fallCallback){const cb=fallCallback;fallCallback=null;setTimeout(cb,450)}}
}
let desiredCam,lookAt;
if(phase==="return"){
desiredCam=new THREE.Vector3(penguin.position.x*.35,5.8,penguin.position.z-8.5);
lookAt=new THREE.Vector3(penguin.position.x*.35,1,penguin.position.z+4.5);
}else{
desiredCam=new THREE.Vector3(penguin.position.x*.55,4.8,penguin.position.z+8.5);
lookAt=new THREE.Vector3(penguin.position.x*.55,1.1,penguin.position.z-3.2);
}
camera.position.lerp(desiredCam,.09);camera.lookAt(lookAt);
if(fishBucket.visible&&phase==="return"){
fishBucket.position.x=THREE.MathUtils.lerp(fishBucket.position.x,penguin.position.x+1.05,.16);
fishBucket.position.z=THREE.MathUtils.lerp(fishBucket.position.z,penguin.position.z,.16);
fishBucket.rotation.y+=dt*.7;
}
renderer.render(scene,camera);
}

let gamePaused = false;
let soundEnabled = true;

function openSettings(){
    if(!started || gamePaused) return;

    gamePaused = true;
    stopTimer();
    $("settingsPanel").style.display = "flex";
}

function closeSettings(){
    $("settingsPanel").style.display = "none";
    gamePaused = false;

    if(started && phase === "outbound" && !busy){
        startTimer();
    }
}

$("settingsBtn").addEventListener("click", openSettings);
$("closeSettings").addEventListener("click", closeSettings);
$("resumeBtn").addEventListener("click", closeSettings);

$("soundToggle").addEventListener("change", function(){
    soundEnabled = this.checked;
});

$("restartBtn").addEventListener("click", function(){
    location.reload();
});

$("homeBtn").addEventListener("click", function(){
    location.reload();
});
$("start").addEventListener("click",startGame);
$("left").addEventListener("click",()=>{
    if(phase==="return"){
        if(!started||busy||jumping||falling)return;
       lane=Math.max(0,lane-1);
penguin.position.x=laneX[lane];
    }else{
        move(-1);
    }
});
$("right").addEventListener("click",()=>{
    if(phase==="return"){
        if(!started||busy||jumping||falling)return;
        lane=Math.min(3,lane+1);
        penguin.position.x=laneX[lane];
    }else{
        move(1);
    }
});
$("up").addEventListener("click",()=>{
if(phase==="return"){if(!busy&&!jumping){penguin.position.z-=.5;if(fishBucket.visible)fishBucket.position.z=penguin.position.z}}
else jump();
});
$("down").addEventListener("click",()=>{
if(phase==="return"&&!busy&&!jumping){penguin.position.z+=.5;if(fishBucket.visible)fishBucket.position.z=penguin.position.z}
});
$("jump").addEventListener("click",jump);
addEventListener("keydown",e=>{
if(["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"," "].includes(e.key))e.preventDefault();
if(e.key==="ArrowLeft"||e.key==="a"||e.key==="A")move(-1);
if(e.key==="ArrowRight"||e.key==="d"||e.key==="D")move(1);
if(e.key==="ArrowUp"||e.key==="w"||e.key==="W"){
if(phase==="return"&&!busy&&!jumping){penguin.position.z-=.5;if(fishBucket.visible)fishBucket.position.z=penguin.position.z}
else jump();
}
if(e.key==="ArrowDown"||e.key==="s"||e.key==="S"){
if(phase==="return"&&!busy&&!jumping){penguin.position.z+=.5;if(fishBucket.visible)fishBucket.position.z=penguin.position.z}
}
if(e.key===" "||e.key==="Enter")jump();
});
init();
})();
</script>
</body>
</html>
"""

components.html(GAME, height=760, scrolling=False)
