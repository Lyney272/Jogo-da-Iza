# Jogo-da-Iza
Muito top.
🦫🎀 CapiCare

CapiCare é um jogo de pet virtual desenvolvido em Python + Pygame, onde você precisa cuidar de uma capivara fofinha usando um lacinho. 💕

Alimente, dê banho, brinque e coloque sua capivara para dormir para mantê-la feliz e saudável!

🎮 Sobre o jogo

No CapiCare, você tem uma capivara virtual que possui diferentes necessidades.

Ao longo do jogo, os níveis de fome, higiene, energia e diversão mudam com o passar do tempo. Você precisa ficar de olho nesses indicadores e cuidar da sua capivara.

A capivara também possui um sistema de sono: depois de 10 minutos, ela precisa dormir. Quando está cansada, algumas atividades ficam bloqueadas até que ela descanse.

O jogo foi desenvolvido para ser simples de executar e fácil de modificar, podendo receber novos recursos no futuro.

🦫 Sua capivara

A personagem principal possui diferentes estados e expressões.

Ela pode ficar:

😊 Feliz

😐 Normal

🍎 Com fome

🧼 Suja

😴 Cansada

💤 Dormindo

Além disso, ela possui um lacinho 🎀 como parte do visual da personagem.

❤️ Necessidades

A capivara possui quatro indicadores principais:

Necessidade	Descrição
🍎 Fome	Diminui com o tempo e aumenta quando a capivara come
🛁 Higiene	Diminui com o tempo e é recuperada durante o banho
⚡ Energia	Diminui com o tempo e é recuperada dormindo
❤️ Diversão	Diminui lentamente e aumenta quando a capivara brinca

Os valores são representados por barras de progresso na interface.

🕹️ Ações
🍎 Alimentar

Aumenta a fome da capivara e dá um pequeno aumento na diversão.

A capivara não pode comer quando está cansada.

🛁 Dar banho

Recupera a higiene da capivara e aumenta um pouco sua diversão.

Durante essa ação, o jogo muda para o ambiente do banheiro.

⚽ Brincar

Aumenta bastante a diversão, mas consome energia e um pouco de fome.

A capivara não pode brincar quando está cansada ou com pouca energia.

💤 Dormir

Coloca a capivara para dormir e recupera sua energia.

Enquanto dorme, ela fica no quarto e aparece com os olhos fechados.

⏰ Sistema de sono

Um dos principais sistemas do jogo é o relógio interno da capivara.

A cada 10 minutos, ela precisa dormir.

Quando esse período é atingido:

💤 Sua capivara precisa dormir!


A capivara fica cansada e não consegue realizar algumas ações.

Depois que ela dorme e recupera sua energia, pode voltar a brincar e comer normalmente.

✨ Efeitos visuais

O jogo possui alguns efeitos para deixar as ações mais divertidas:

✨ Partículas;

💕 Efeitos ao realizar ações;

🎀 Animação do personagem;

☁️ Cenários decorados;

🌸 Flores no jardim;

💤 Animação de sono;

🐾 Pequenos movimentos da capivara;

🖱️ Efeitos nos botões ao passar o mouse.

🌎 Ambientes

O jogo possui diferentes cenários que mudam de acordo com a atividade:

🌳 Jardim

É o ambiente principal e o local onde a capivara pode brincar.

🛁 Banheiro

Aparece quando a capivara toma banho.

🛏️ Quarto

É o local onde a capivara dorme.

💾 Sistema de salvamento

O jogo possui salvamento automático.

Os dados da capivara são armazenados em:

pet_save.json


São salvos, entre outras informações:

Nome
Fome
Higiene
Energia
Diversão
Horário do último sono


Isso permite que o progresso continue disponível quando o jogo for aberto novamente.

📁 Estrutura do projeto
CapiCare/
│
├── main.py
├── requirements.txt
├── README.md
│
└── pet_save.json


O arquivo pet_save.json é criado automaticamente pelo jogo após a execução.

🛠️ Tecnologias utilizadas

🐍 Python

🎮 Pygame

💾 JSON

⏱️ Time

🎨 Pygame Drawing API

📋 Requisitos

Para executar o jogo, você precisa ter:

Python 3.10 ou superior

Pygame

📦 Instalação

Clone este repositório:

git clone https://github.com/SEU-USUARIO/CapiCare.git


Entre na pasta:

cd CapiCare


Instale as dependências:

pip install -r requirements.txt

▶️ Executando o jogo

Depois de instalar as dependências, execute:

python main.py


O jogo será aberto em uma janela.

🕹️ Controles

O jogo utiliza o mouse.

Botão	Ação
🍎 Alimentar	Alimenta a capivara
🛁 Dar banho	Dá banho na capivara
💤 Dormir	Coloca a capivara para dormir
⚽ Brincar	Brinca com a capivara
🚧 Próximas atualizações

O projeto pode receber diversos novos recursos no futuro:

 🎀 Personalização do lacinho

 👒 Novos acessórios

 🏡 Personalização da casa

 🍉 Mais tipos de comida

 🧸 Mais brinquedos

 🎵 Música de fundo

 🔊 Efeitos sonoros

 🦫 Mais animações da capivara

 🌎 Mais ambientes

 🪙 Sistema de moedas

 🛍️ Loja de acessórios

 ⭐ Sistema de níveis

 🏆 Conquistas

 📅 Sistema de dias

 🌙 Ciclo de dia e noite

 🎨 Sprites ilustrados

 🐾 Animação de caminhada

 💬 Mais interações com a capivara

🎯 Objetivo do projeto

O objetivo do CapiCare é criar uma experiência de pet virtual divertida, visualmente agradável e fácil de expandir.

O projeto também serve como uma forma de praticar conceitos de:

Programação orientada a objetos;

Desenvolvimento de jogos;

Eventos e interação com o usuário;

Animações;

Interfaces gráficas;

Manipulação de arquivos;

Salvamento de dados;

Controle de tempo;

Organização de projetos Python.

🦫💕 Cuide bem da Capi!

Não deixe sua capivara com fome, suja ou cansada.

Dê comida.
Dê banho.
Brinque bastante.
E, principalmente...

💤 Não esqueça da hora de dormir!

Feito com Python, Pygame e muito carinho. 🐍 + 🎮 + 🦫 + 🎀 = ❤️

:::

Esse README já pode ser colocado diretamente na raiz do repositório como **`README.md`**.
