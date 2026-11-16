const panel = document.querySelector(".flip-panel");
const flipButton = document.querySelector(".flip-button");
const faces = [document.querySelector(".flip-front"), document.querySelector(".flip-back")];
const storage = document.querySelector(".board-storage");
const leaves = [...storage.children];
const requestedFace = Number(new URLSearchParams(location.hash.slice(1)).get("face"));
let pageIndex = Number.isInteger(requestedFace) && requestedFace >= 0 && requestedFace < leaves.length ? requestedFace : 0;
let turns = 0;
let turning = false;
faces[0].append(leaves[pageIndex]);

function updateReturnLinks() {
  const board = location.pathname.split("/").pop();
  for (const note of notes) {
    const url = new URL(note.href);
    url.searchParams.set("board", board);
    url.searchParams.set("face", String(pageIndex));
    note.href = url.href;
  }
}
updateReturnLinks();

flipButton.addEventListener("click", () => {
  if (leaves.length <= 1 || turning || leavingBoard) return;
  turning = true;
  closeTouchPreview();
  document.querySelectorAll(".pin-note.preview").forEach(note => note.classList.remove("preview"));
  const outgoing = faces[turns % 2];
  const incoming = faces[(turns + 1) % 2];
  const nextIndex = (pageIndex + 1) % leaves.length;
  incoming.append(leaves[nextIndex]);
  faces.forEach(face => { face.inert = true; });
  document.querySelector(".flip-demo").classList.add("is-turning");
  turns += 1;
  panel.style.transform = "rotateY(" + (-180 * turns) + "deg)";

  function finish() {
    if (!turning) return;
    panel.removeEventListener("transitionend", onEnd);
    clearTimeout(fallback);
    storage.append(leaves[pageIndex]);
    outgoing.replaceChildren();
    outgoing.setAttribute("aria-hidden", "true");
    incoming.inert = false;
    incoming.setAttribute("aria-hidden", "false");
    pageIndex = nextIndex;
    updateReturnLinks();
    document.querySelector(".flip-demo").classList.remove("is-turning");
    turning = false;
  }
  function onEnd(event) {
    if (event.target === panel && event.propertyName === "transform") finish();
  }
  panel.addEventListener("transitionend", onEnd);
  const fallback = setTimeout(finish,
    matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 1350);
});
