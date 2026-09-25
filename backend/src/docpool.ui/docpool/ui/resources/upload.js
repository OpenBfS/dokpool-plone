// Delegated events also handle wizard steps loaded by pat-inject.
// Files stay in the native input and are submitted with the wizard form.
const selector = ".docpool-upload--input";

document.addEventListener("change", (event) => {
  const input = event.target;
  if (!input.matches?.(`${selector} input[type='file']`)) return;

  const list = input.closest(selector).querySelector(".docpool-upload__files");
  list.replaceChildren(
    ...Array.from(input.files, (file) => {
      const item = document.createElement("li");
      item.className = "text-break";
      item.textContent = file.name;
      return item;
    }),
  );
  list.classList.toggle("d-none", input.files.length === 0);
});

for (const type of ["dragenter", "dragover", "dragleave", "drop"]) {
  document.addEventListener(type, (event) => {
    const upload = event.target.closest?.(selector);
    if (!upload || !event.dataTransfer?.types.includes("Files")) return;

    event.preventDefault();
    if (type === "dragleave") {
      if (!upload.contains(event.relatedTarget)) {
        upload.classList.remove("is-dragover");
      }
      return;
    }
    if (type === "drop") {
      upload.classList.remove("is-dragover");
      if (!event.dataTransfer.files.length) return;

      const input = upload.querySelector("input[type='file']");
      input.files = event.dataTransfer.files;
      input.dispatchEvent(new Event("change", { bubbles: true }));
      return;
    }

    event.dataTransfer.dropEffect = "copy";
    upload.classList.add("is-dragover");
  });
}
