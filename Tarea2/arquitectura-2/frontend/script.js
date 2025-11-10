document.getElementById("shorten").addEventListener("click", async () => {
  const longUrl = document.getElementById("url").value;
  if (!longUrl) return alert("Por favor ingresa una URL");

  const response = await fetch("http://localhost:8000/shorten", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ long_url: longUrl }),
  });

  const data = await response.json();
  const result = document.getElementById("result");

  if (data.short) {
    result.innerHTML = `URL corta: <a href="${data.short}" target="_blank">${data.short}</a>`;
  } else {
    result.textContent =
      "Error: " + (data.error || "No se pudo acortar la URL");
  }
});
