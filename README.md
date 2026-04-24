Este projeto usa visao computacional em tempo real para detectar pessoas e reconhecer rostos pela webcam, utilizando YOLOv8 (Ultralytics), OpenCV e face_recognition.

O que este codigo faz
O script em main.py:

1) Carrega o modelo YOLOv8 nano (arquivo yolov8n.pt).
2) Abre a webcam padrão do computador.
3) rocessa cada frame do vídeo.
4) Detecta objetos no frame com YOLO.
5) Filtra apenas a classe pessoa (ID 0 no COCO).
6) Detecta rostos no frame.
7) Compara os rostos detectados com uma base local de pessoas cadastradas.
8) Desenha caixas nas pessoas e nos rostos detectados.
9) Mostra na tela a quantidade de pessoas e rostos reconhecidos.
10) Encerra ao pressionar a tecla q.

Tecnologias usadas:

1) Python
2) OpenCV
3) Ultralytics YOLOv8
4) face_recognition

Pré-requisitos:

Python 3.8 ou superior
Webcam funcionando
Dependências instaladas:
    ultralytics
    opencv-python
    face-recognition

Instalação:

Instale as bibliotecas necessárias:

pip install ultralytics opencv-python face-recognition

Base de rostos (obrigatorio para reconhecer nomes):

Crie a pasta faces_db na raiz do projeto com esta estrutura:

faces_db/
    Ana/
        foto1.jpg
        foto2.jpg
    Carlos/
        foto1.jpg

Cada subpasta representa o nome da pessoa.
As imagens devem conter um rosto visivel.

Como executar:

No terminal, na pasta do projeto, execute:

python main.py

Ao abrir a janela do vídeo:

O texto em vermelho mostra o total detectado no frame atual.
O retângulo verde marca cada pessoa detectada.
O retangulo azul marca cada rosto e mostra o nome (ou "Desconhecido").
Pressione q para sair.

Explicação do fluxo do código

1) Carregamento do modelo
O modelo YOLOv8 nano é carregado a partir de yolov8n.pt.
Esse modelo é leve e indicado para aplicações em tempo real.

2) Inicialização da câmera
O OpenCV abre a webcam com índice 0.
Se a câmera não puder ser acessada, o programa exibe erro e encerra.

3) Loop principal de processamento
Enquanto a câmera estiver ativa:

Lê um frame.
Roda inferência com YOLO usando stream=True.
Reinicia o contador de pessoas para aquele frame.
4) Filtragem de classe
Para cada detecção:

Lê a classe detectada.
Considera apenas classe 0 (pessoa no dataset COCO).
Incrementa a contagem.
Desenha bounding box e rótulo Pessoa no frame.
5) Exibição do resultado
O frame final é exibido com:

Caixas nas pessoas.
Texto Pessoas detectadas: X no topo.
6) Encerramento seguro
Ao pressionar q:

Libera a webcam.
Fecha as janelas do OpenCV.

Observações importantes:

A contagem é por frame, não por pessoas únicas ao longo do tempo.
Se a câmera não for a padrão, troque o índice em VideoCapture(0) para 1, 2, etc.
O desempenho depende do hardware (CPU/GPU).

Melhorias futuras (opcional)

Detectar rostos de pessoas diferentes
Armazenar as pessoas em um banco de dados
Conectar o código em uma aplicação web
Conectar o código em um esp32 com câmera 
