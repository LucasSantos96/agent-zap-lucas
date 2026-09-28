// Botão de conexão
    const connectButton = document.getElementById("connect-btn");

    connectButton.addEventListener("click", async () => {
        const response = await fetch("/wuzapi/connect", {
            method: "POST"
        });

        const data = await response.json();

        console.log(data);
    });