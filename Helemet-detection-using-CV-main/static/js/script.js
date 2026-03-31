const fileInput = document.getElementById("fileInput");
const detectBtn = document.getElementById("detectBtn");
const statusText = document.getElementById("status");
const spinner = document.getElementById("spinner");
const dropZone = document.getElementById("dropZone");

const originalPreview = document.getElementById("originalPreview");
const resultPreview = document.getElementById("resultPreview");

const originalPlaceholder = document.getElementById("originalPlaceholder");
const resultPlaceholder = document.getElementById("resultPlaceholder");

const totalCount = document.getElementById("totalCount");
const helmetCount = document.getElementById("helmetCount");
const noHelmetCount = document.getElementById("noHelmetCount");
const compliance = document.getElementById("compliance");
const downloadBtn = document.getElementById("downloadBtn");

function resetStats() {
  totalCount.textContent = "0";
  helmetCount.textContent = "0";
  noHelmetCount.textContent = "0";
  compliance.textContent = "0%";
}

function showOriginalPreview(file) {
  if (!file) return;
  originalPreview.src = URL.createObjectURL(file);
  originalPreview.style.display = "block";
  originalPlaceholder.style.display = "none";

  resultPreview.src = "";
  resultPreview.style.display = "none";
  resultPlaceholder.style.display = "block";
  downloadBtn.classList.add("hidden");
  statusText.textContent = "";
  resetStats();
}

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  showOriginalPreview(file);
});

["dragenter", "dragover"].forEach(eventName => {
  dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add("dragover");
  });
});

["dragleave", "drop"].forEach(eventName => {
  dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove("dragover");
  });
});

dropZone.addEventListener("drop", (e) => {
  const files = e.dataTransfer.files;
  if (files && files.length > 0) {
    fileInput.files = files;
    showOriginalPreview(files[0]);
  }
});

detectBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];

  if (!file) {
    statusText.textContent = "Please select an image first.";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  spinner.classList.remove("hidden");
  statusText.textContent = "Running detection...";

  detectBtn.disabled = true;
  detectBtn.textContent = "Processing...";

  try {
    const response = await fetch("/detect", {
      method: "POST",
      body: formData
    });

    let data;
    try {
      data = await response.json();
    } catch (e) {
      statusText.textContent = "Server returned an invalid response.";
      return;
    }

    if (!response.ok) {
      console.error("Backend error:", data);
      statusText.textContent = data.error || "Something went wrong.";
      return;
    }

    resultPreview.src = `${data.result_image}?t=${new Date().getTime()}`;
    resultPreview.style.display = "block";
    resultPlaceholder.style.display = "none";

    totalCount.textContent = data.total;
    helmetCount.textContent = data.helmet_count;
    noHelmetCount.textContent = data.no_helmet_count;
    compliance.textContent = `${data.compliance}%`;

    downloadBtn.href = data.result_image;
    downloadBtn.classList.remove("hidden");

    statusText.textContent = "Detection completed successfully.";
  } catch (error) {
    statusText.textContent = "Error while processing the image.";
    console.error(error);
  } finally {
    spinner.classList.add("hidden");
    detectBtn.disabled = false;
    detectBtn.textContent = "Run Detection";
  }
});