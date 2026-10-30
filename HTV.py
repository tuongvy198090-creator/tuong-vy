
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
.panel h1 {
    position: relative;
    display: inline-block;
    margin: 8px 0 16px;
    padding: 10px 14px 14px;
    font-family: "Arial Rounded MT Bold", "Trebuchet MS", sans-serif;
    font-size: clamp(29px, 5vw, 46px);
    font-weight: 1000;
    line-height: 1.2;
    letter-spacing: 1px;
    color: #0877a9;
    -webkit-text-stroke: 1px #ffffff;
    text-shadow:
        0 3px 0 #d8f5ff,
        0 5px 0 #69b9df,
        0 8px 12px #226b9166;
}
.panel h1::before {
    content: "❄ ❄ ❄ ❄ ❄";
    position: absolute;
    top: -13px;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    color: #ffffff;
    font-size: clamp(10px, 1.8vw, 16px);
    letter-spacing: 5px;
    -webkit-text-stroke: 0;
    text-shadow: 0 1px 3px #75c9ed;
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
<div class="pill" id="progress">Câu 1/7</div>
</div>

<div id="quiz">
<div id="qtext">Sẵn sàng chưa?</div>
<div id="answers"></div>
<div id="timer">⏱ 15 giây</div>
</div>

<div id="message"></div>

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

// ===== ÂM THANH: chỉ bổ sung, không thay đổi cơ chế trò chơi =====
const audioBase = "/app/static/audio/";
const bgTracks = {
  day: new Audio(audioBase + "nhac-nen-ban-ngay.mp3"),
  night: new Audio(audioBase + "nhac-nen-ban-dem.mp3")
};
const soundFiles = {
  warning: audioBase + "nhac-canh-bao.mp3",
  correct: audioBase + "am-thanh-dung.mp3",
  wrong: audioBase + "am-thanh-sai.mp3",
  win: audioBase + "nhac-chuc-mung-chien-thang.mp3"
};
let activeBg = null;
let activeEffect = null;
let soundEnabled = true;
Object.values(bgTracks).forEach(a => { a.loop = true; a.volume = 0.32; });
function startBackground(name){
  if(!soundEnabled) return;
  const next = bgTracks[name];
  if(!next) return;
  Object.values(bgTracks).forEach(a => { if(a !== next){ a.pause(); a.currentTime = 0; } });
  if(activeBg === next && !next.paused) return;
  activeBg = next; next.volume = 0.32;
  next.play().catch(()=>{});
}
function stopBackground(){
  Object.values(bgTracks).forEach(a => { a.pause(); a.currentTime = 0; });
  activeBg = null;
}
function playEffect(name){
  if(!soundEnabled || !soundFiles[name]) return;
  if(activeEffect){ activeEffect.pause(); activeEffect.currentTime = 0; }
  const effect = new Audio(soundFiles[name]);
  activeEffect = effect; effect.volume = 0.95;
  if(activeBg && !activeBg.paused) activeBg.volume = 0.07;
  effect.onended = () => {
    if(activeEffect === effect) activeEffect = null;
    if(activeBg && !activeBg.paused && soundEnabled) activeBg.volume = 0.32;
  };
  effect.onerror = () => { if(activeBg && !activeBg.paused) activeBg.volume = 0.32; };
  effect.play().catch(()=>{ if(activeBg && !activeBg.paused) activeBg.volume = 0.32; });
}

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
{q:"LỊCH SỬ: Chiến thắng Bạch Đằng năm 938 gắn với ai?",a:["Trần Hưng Đạo","Ngô Quyền","Lê Lợi","Quang Trung"],c:1}
];
