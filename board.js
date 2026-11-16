const notes = document.querySelectorAll(".pin-note");
let touchPreview = null;
let previewLayer = 10;

// Raise the whole pin slot so sibling papers cannot cover its preview.
function raiseNote(note) {
  note.parentElement.style.zIndex = String(++previewLayer);
}


function closeTouchPreview() {
  touchPreview?.classList.remove("preview");
  touchPreview = null;
}

document.addEventListener("pointerdown", event => {
  if (touchPreview && !touchPreview.contains(event.target)) closeTouchPreview();
});

let leavingBoard = false;
window.addEventListener("pageshow", () => {
  leavingBoard = false;
  document.body.classList.remove("leaving-board");
  document.querySelector(".lifting-note")?.classList.remove("lifting-note", "preview");
});

for (const note of notes) {
  let touch = false;
  note.addEventListener("focus", () => raiseNote(note));
  note.addEventListener("pointerenter", event => {
    if (event.pointerType === "mouse") {
      raiseNote(note);
      note.classList.add("preview");
    }
  });
  note.addEventListener("pointerleave", event => {
    if (!leavingBoard && event.pointerType === "mouse") note.classList.remove("preview");
  });
  note.addEventListener("pointerdown", event => {
    touch = event.pointerType === "touch" || event.pointerType === "pen";
  });
  note.addEventListener("click", async event => {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    if (touch && event.detail && touchPreview !== note) {
      event.preventDefault();
      closeTouchPreview();
      touchPreview = note;
      raiseNote(note);
      note.classList.add("preview");
      touch = false;
      return;
    }
    touch = false;
    if (matchMedia("(prefers-reduced-motion: reduce)").matches || !note.animate) return;
    event.preventDefault();
    if (leavingBoard) return;
    leavingBoard = true;
    note.classList.add("preview", "lifting-note");
    document.body.classList.add("leaving-board");
    const lift = note.animate([
      { translate: "0 0", rotate: "0deg", scale: 1 },
      { translate: "0 -14px", rotate: "-3deg", scale: 1.05, offset: .45 },
      { translate: "0 -36px", rotate: "1deg", scale: 1.12, opacity: 0 }
    ], { duration: 460, easing: "ease-in-out" });
    try {
      await lift.finished;
    } finally {
      window.location.assign(note.href);
    }
  });
}

const clock = document.querySelector(".guild-clock");
const hourHand = clock.querySelector("#hour-hand");
const minuteHand = clock.querySelector("#minute-hand");
const taiwanTime = new Intl.DateTimeFormat("en-GB", {
  timeZone: "Asia/Taipei", hourCycle: "h23",
  hour: "2-digit", minute: "2-digit", second: "2-digit"
});

function updateClock(now = new Date()) {
  const [hour, minute, second] = taiwanTime.format(now).split(":").map(Number);
  const minutes = minute + second / 60;
  hourHand.setAttribute("transform", "rotate(" + ((hour % 12) * 30 + minutes / 2) + ")");
  minuteHand.setAttribute("transform", "rotate(" + minutes * 6 + ")");
  clock.setAttribute("aria-label", "台灣時間 " + hour + " 時 " + minute + " 分");
  clock.removeAttribute("hidden");
}
updateClock();
setInterval(updateClock, 1000);
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) updateClock();
});
