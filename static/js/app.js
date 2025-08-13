(function () {
  const el = document.getElementById("trade-uuid");
  if (el) {
    const key = el.dataset.key;
    // Required behavior: JS reads and logs data attribute on page load
    console.log("trade-uuid data-key:", key);
  }
})();
