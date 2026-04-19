Este projeto usa visão computacional em tempo real para detectar e contar pessoas pela webcam, utilizando o modelo YOLOv8 (Ultralytics) com OpenCV.

O que este código faz
O script em main.py:

Carrega o modelo YOLOv8 nano (arquivo yolov8n.pt).
Abre a webcam padrão do computador.
Processa cada frame do vídeo.
Detecta objetos no frame com YOLO.
Filtra apenas a classe pessoa (ID 0 no COCO).
Desenha caixas nas pessoas detectadas.
Mostra na tela a quantidade de pessoas detectadas.
Encerra ao pressionar a tecla q.
Tecnologias usadas
Python
OpenCV
Ultralytics YOLOv8
Pré-requisitos
Python 3.8 ou superior
Webcam funcionando
Dependências instaladas:
ultralytics
opencv-python
Instalação
Instale as bibliotecas necessárias:

pip install ultralytics opencv-python

Como executar
No terminal, na pasta do projeto, execute:

python main.py

Ao abrir a janela do vídeo:

O retângulo verde marca cada pessoa detectada.
O texto em vermelho mostra o total detectado no frame atual.
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
Observações importantes
A contagem é por frame, não por pessoas únicas ao longo do tempo.
Se a câmera não for a padrão, troque o índice em VideoCapture(0) para 1, 2, etc.
O desempenho depende do hardware (CPU/GPU).
Melhorias futuras (opcional)
Adicionar rastreamento para contar pessoas únicas.
Definir confiança mínima para reduzir falsos positivos.
Salvar vídeo com as detecções.
Exibir FPS na tela.
