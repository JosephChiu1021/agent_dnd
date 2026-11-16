const parameters = new URLSearchParams(location.search);
const originBoard = parameters.get("board");
const allowedBoards = ["index.html", "flip-preview.html", "pagination-test.html"];
const requestedFace = parameters.get("face");
if (allowedBoards.includes(originBoard)) {
  const target = new URL("../" + originBoard, location.href);
  if (/^\d+$/.test(requestedFace || "")) target.hash = "face=" + requestedFace;
  for (const link of document.querySelectorAll("a.back, a.brand")) link.href = target.href;
}
