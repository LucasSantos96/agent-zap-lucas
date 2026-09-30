// Botão de conexão
const connectButton = document.getElementById("connect-btn");
const disconnectButton = document.getElementById("disconnect-btn");
const groupSelect = document.getElementById("groups");
const statusSpan = document.getElementById("status");
const qrcode = document.getElementById("qrcode");

// Guarda se o WhatsApp já estava conectado na última verificação.
// Serve para saber quando a conexão caiu (fechar o QR Code).
let conectado = false;


// Mostra no topo a situação atual da conexão
function setStatus(connected) {
    if (connected) {
        statusSpan.textContent = "Conectado";
        statusSpan.className = "status connected"; // deixa o indicador verde
    } else {
        statusSpan.textContent = "Desconectado";
        statusSpan.className = "status disconnected"; // deixa o indicador vermelho
    }
}


// Limpa a área do QR Code (fecha o QR que estiver na tela)
function limparQrCode() {
    qrcode.replaceChildren(); // remove a imagem do QR Code
    qrcode.textContent = "QR Code aparecerá aqui"; // volta a mensagem padrão
}


// Limpa a lista de grupos e mostra a mensagem padrão
function limparGrupos() {
    groupSelect.replaceChildren();
    groupSelect.textContent = "Conecte o WhatsApp para listar os grupos";
}


// Busca o status no backend e atualiza a tela
async function checkStatus() {
    const response = await fetch("/wuzapi/status"); // Requisição GET para o endpoint de status
    const resultado = await response.json(); // Converte a resposta em JSON

    // O Wuzapi retorna a conexão dentro de data (campos em minúsculo)
    const connected = resultado.data?.connected === true || resultado.data?.loggedIn === true;

    setStatus(connected);

    // Se acabou de conectar: fecha o QR Code e carrega os grupos
    if (connected && !conectado) {
        conectado = true;
        limparQrCode();
        await loadGroups().catch(console.error);
    }

    // Se estava conectado e agora caiu: fecha o QR Code e limpa os grupos
    if (!connected && conectado) {
        conectado = false;
        limparQrCode();
        limparGrupos(); // esvazia a lista de grupos
    }
}


connectButton.addEventListener("click", async () => {
    const response = await fetch("/wuzapi/connect", { // Faz uma requisição POST para o endpoint de conexão
        method: "POST"
    });

    const data = await response.json();

    console.log(data);

    await new Promise(resolve => setTimeout(resolve, 2000)); // Aguarda 2 segundos antes de buscar o QR Code

    const res_qr = await fetch("/wuzapi/qrcode", { // Faz uma requisição GET para o endpoint de QR Code
        method: "GET"
    });
    const resultado = await res_qr.json(); // Converte a resposta em JSON

    const new_qr = resultado.data?.QRCode; // Pega o QR Code retornado pelo Wuzapi

    console.log(resultado);

    if (resultado.success && new_qr) { // Verifica se a requisição foi bem-sucedida e se o QR Code está presente
        const imagem = document.createElement("img");
        imagem.src = new_qr; // Define a fonte da imagem como o QR Code retornado pelo Wuzapi
        imagem.alt = "QR Code para conexão";
        imagem.width = 260; // Define a largura da imagem
        qrcode.replaceChildren(imagem); // Substitui o conteúdo do elemento qrcode pela nova imagem
    } else {
        qrcode.textContent = "Falha ao gerar QR Code. Tente novamente."; // Exibe uma mensagem de erro caso a requisição falhe
    }
});



disconnectButton.addEventListener("click", async () => {

    try {

        const response = await fetch("/wuzapi/disconnect", { // Faz uma requisição POST para o endpoint de desconexão
            method: "POST"
        });
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }
        const data = await response.json();

        console.log(data);

        // Ao desconectar, fecha o QR Code e limpa os grupos
        conectado = false;
        setStatus(false);
        limparQrCode();
        limparGrupos();

    } catch (error) {
        console.error("Erro ao desconectar:", error.message);
        console.error("Detalhes do erro:", error);
    }


});



async function loadGroups() {
    const response = await fetch("/wuzapi/group");
    if (!response.ok) {
        throw new Error(`Erro ao buscar grupos: ${response.status}`);
    }

    const result = await response.json();
    console.log("Resposta dos grupos:", result);

    const groups = result.data?.Groups; // O Wuzapi retorna os grupos dentro de data.Groups
    if (!Array.isArray(groups)) {
        throw new Error("A resposta não contém uma lista de grupos em data.Groups.");
    }

    groupSelect.replaceChildren();

    for (const group of groups) {
        const label = document.createElement("label"); // Cada grupo é uma linha clicável

        const checkbox = document.createElement("input"); // Caixinha de seleção
        checkbox.type = "checkbox";
        checkbox.value = group.JID; // Guarda o JID como valor
        checkbox.name = "group"; // Agrupa as caixinhas de grupos

        const texto = document.createElement("span");
        texto.textContent = group.Name; // Mostra o nome do grupo

        label.append(checkbox, texto); // Junta a caixinha com o nome
        groupSelect.appendChild(label);
    }
}


// Verifica o status ao abrir a página e depois a cada 3 segundos
checkStatus().catch(console.error);
setInterval(() => checkStatus().catch(console.error), 3000);
