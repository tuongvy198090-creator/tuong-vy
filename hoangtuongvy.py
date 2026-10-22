
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Chim Cánh Cụt Vượt Băng",
    layout="wide"
)

st.title("🐧 CHIM CÁNH CỤT VƯỢT BĂNG")
st.write("Trả lời đúng để vượt sông, lấy thùng cá rồi mang về!")

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { margin:0; background:#bdeeff; font-family:Arial; }
#game { width:100%; height:650px; position:relative;
overflow:hidden; background:linear-gradient(#9ce5ff,#e7fbff); }
#world { position:absolute; inset:0; }
.bank { position:absolute; top:0; height:100%; width:18%;
background:linear-gradient(90deg,#f5ffff,#b8e9f5);
border:3px solid white; box-sizing:border-box; }
#leftBank { left:0; }
#rightBank { right:0; }
.water { position:absolute; left:18%; width:64%; top:0;
height:100%; background:linear-gradient(#44bce8,#138ac8); }
.water:after { content:""; position:absolute; inset:0;
background:repeating-linear-gradient(170deg,
transparent 0 35px,rgba(255,255,255,.20) 36px 39px); }
.bankLabel { position:absolute; top:25px; width:100%;
text-align:center; font-weight:bold; font-size:17px; color:#14516b; }
#fishBucket { position:absolute; right:5%; top:48%;
font-size:53px; z-index:8; }
#penguin { position:absolute; left:8%; top:47%;
font-size:52px; z-index:10; transition:left .25s,top .25s; }
#baby { position:absolute; left:12%; top:58%;
font-size:30px; z-index:10; }
#iceArea { position:absolute; left:19%; width:62%; top:18%;
height:66%; display:grid; grid-template-columns:repeat(5,1fr);
grid-template-rows:repeat(5,1fr); gap:8px; z-index:3; }
.ice { position:relative; background:#dffaff;
border:3px solid #fff; border-radius:13px;
box-shadow:0 5px 0 #72cce7; display:flex;
align-items:center; justify-content:center; font-size:24px; }
.ice.weak { background:#a6e4f5; border-color:#e8ffff; }
.wall { position:absolute; top:0; right:-4px; height:100%;
width:9px; background:#75818c; border-radius:5px; }
.wall.down { display:none; }
#questionBox { background:#fff; border-radius:14px;
padding:12px; margin-top:10px; }
#question { font-size:18px; font-weight:bold; margin-bottom:10px; }
#answers { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
button { border:0; padding:12px; border-radius:10px;
background:#167db2; color:white; font-size:16px; cursor:pointer; }
button:disabled { opacity:.45; }
#status { font-weight:bold; padding:8px; }
#controls { display:flex; gap:8px; justify-content:center; margin-top:10px; }
#controls button { min-width:85px; }
</style>
</head>
<body>
<div id="game">
  <div id="world">
    <div class="water"></div>
    <div class="bank" id="leftBank">
      <div class="bankLabel">🏁 BỜ XUẤT PHÁT</div>
    </div>
    <div class="bank" id="rightBank">
      <div class="bankLabel">🏆 BỜ THÙNG CÁ</div>
    </div>
    <div id="fishBucket">🪣🐟</div>
    <div id="penguin">🐧</div>
    <div id="baby">🐧</div>
    <div id="iceArea"></div>
  </div>
</div>

<div id="questionBox">
  <div id="status">Hãy trả lời câu hỏi để bắt đầu vượt sông!</div>
  <div id="question"></div>
  <div id="answers"></div>
  <div id="controls">
    <button onclick="move(-1)">⬅ Lùi</button>
    <button onclick="move(1)">Tiến ➡</button>
  </div>
</div>

<script>
const questions = [
 {q:"Toán: Giá trị của 2³ là?", a:["6","8","9","4"], c:1},
 {q:"Toán: 25% của 200 bằng?", a:["25","40","50","75"], c:2},
 {q:"KHTN: Đơn vị đo lực là?", a:["Jun","Niutơn","Oát","Mét"], c:1},
 {q:"Sinh học: Cơ quan hô hấp của cá là?", a:["Phổi","Da","Mang","Tim"], c:2},
 {q:"Địa lí: Trái Đất có dạng gần giống?", a:["Hình cầu","Hình vuông","Hình nón","Hình trụ"], c:0}
];

let row = 0;
let hasFish = false;
let returning = false;
let answered = false;
let finished = false;
let pos = 0;

const area = document.getElementById("iceArea");
for(let r=0;r<5;r++){
 for(let c=0;c<5;c++){
  const ice=document.createElement("div");
  ice.className="ice";
  ice.id=`ice-${r}-${c}`;
  ice.innerHTML="🧊<div class='wall' id='wall-"+r+"-"+c+"'></div>";
  if((r+c)%3===0) ice.classList.add("weak");
  area.appendChild(ice);
 }
}

function showQuestion(){
 if(finished) return;
 answered=false;
 let qIndex = returning ? 4-row : row;
 if(qIndex<0) qIndex=0;
 if(qIndex>=questions.length) qIndex=questions.length-1;
 const q=questions[qIndex];
 document.getElementById("question").textContent =
 (returning ? "CHẶNG VỀ - " : "CHẶNG ĐI - ") + q.q;
 const answers=document.getElementById("answers");
 answers.innerHTML="";
 q.a.forEach((ans,i)=>{
  const b=document.createElement("button");
  b.textContent=String.fromCharCode(65+i)+". "+ans;
  b.onclick=()=>answer(i,q.c,b);
  answers.appendChild(b);
 });
 document.getElementById("status").textContent =
 returning ? "Đưa cá trở về bờ xuất phát!" : "Chọn đáp án đúng để mở vách ngăn!";
}

function answer(choice, correct, button){
 if(answered || finished) return;
 answered=true;
 if(choice===correct){
  document.getElementById("status").textContent="🎉 Chính xác! Vách ngăn đã hạ xuống!";
  const wall=document.getElementById("wall-"+row+"-"+(returning?0:4));
  if(wall) wall.classList.add("down");
  document.querySelectorAll("#answers button").forEach(b=>b.disabled=true);
  if(!returning){
   pos=Math.min(5,pos+1);
   document.getElementById("penguin").style.left=(8+pos*13)+"%";
   row++;
   if(row>=5){
    hasFish=true;
    returning=true;
    row=0;
    document.getElementById("fishBucket").textContent="🪣";
    document.getElementById("penguin").textContent="🐧🐟";
    document.getElementById("status").textContent="🐟 Đã lấy cá! Bắt đầu chặng quay về!";
    document.getElementById("question").textContent="Nhấn Tiến để tiếp tục!";
    document.getElementById("answers").innerHTML="";
    return;
   }
  }else{
   pos=Math.max(0,pos-1);
   document.getElementById("penguin").style.left=(8+pos*13)+"%";
   row++;
   if(row>=5){
    finished=true;
    document.getElementById("penguin").style.left="8%";
    document.getElementById("status").textContent="🏆 CHIẾN THẮNG! Cả nhà chim cánh cụt đã mang cá về!";
    document.getElementById("question").textContent="🎊 Chúc mừng em hoàn thành thử thách!";
    document.getElementById("answers").innerHTML="";
    document.getElementById("fishBucket").textContent="🎉🐟";
    return;
   }
  }
  setTimeout(showQuestion,900);
 }else{
  document.getElementById("status").textContent="❄️ Chưa đúng! Em mất một mạng, thử lại nhé.";
  document.querySelectorAll("#answers button").forEach(b=>b.disabled=true);
  setTimeout(()=>{
   answered=false;
   document.querySelectorAll("#answers button").forEach(b=>b.disabled=false);
  },900);
 }
}

function move(direction){
 if(finished) return;
 if(!answered){
  document.getElementById("status").textContent="Hãy trả lời câu hỏi trước khi di chuyển nhé!";
  return;
 }
 if(returning){
  document.getElementById("penguin").style.left =
  Math.max(8,Math.min(78,parseFloat(document.getElementById("penguin").style.left||"8") + direction*5))+"%";
 }
}
document.addEventListener("keydown",e=>{
 if(e.key==="ArrowRight") move(1);
 if(e.key==="ArrowLeft") move(-1);
});
showQuestion();
</script>
</body>
</html>
"""

components.html(html, height=850, scrolling=True)
