const API_URL = "http://127.0.0.1:8000/explain";

const submitButton = document.getElementById("submitbtn");
const inputBox = document.getElementById("query");
const result = document.getElementById("result");
const status = document.getElementById("status");

function setStatus(message, isError = false) {
  status.textContent = message;
  status.classList.toggle("error", isError);
}

async function activeTabUrl() {
  const [tab] = await chrome.tabs.query({ currentWindow: true, active: true });
  if (!tab?.url || !/^https?:\/\//i.test(tab.url)) {
    throw new Error("Open a normal http(s) web page before asking a question.");
  }
  return tab.url;
}

submitButton.addEventListener("click", async () => {
  const query = inputBox.value.trim();
  result.textContent = "";
  if (!query) {
    setStatus("Enter a question first.", true);
    return;
  }

  submitButton.disabled = true;
  setStatus("Reading the page…");
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: await activeTabUrl(), query }),
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(payload.detail || "The server could not answer this question.");
    result.textContent = payload.output;
    setStatus(`Answered from ${payload.source_characters.toLocaleString()} characters of page text.`);
  } catch (error) {
    setStatus(error instanceof Error ? error.message : "Something went wrong.", true);
  } finally {
    submitButton.disabled = false;
  }
});
