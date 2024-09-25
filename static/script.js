document.getElementById("uploadForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const pdfFile = document.getElementById("pdfFile").files[0];
    if (!pdfFile) {
        alert("Por favor, selecione um arquivo PDF.");
        return;
    }

    const formData = new FormData();
    formData.append("pdf", pdfFile);

    fetch("/process_pdf", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        const resultadoDiv = document.getElementById("resultado");
        if (data.error) {
            resultadoDiv.textContent = data.error;
        } else {
            resultadoDiv.innerHTML = `
                <p>${data.full_response}</p>
            `;
        }
    })
    .catch(error => {
        console.error("Erro:", error);
    });
});
