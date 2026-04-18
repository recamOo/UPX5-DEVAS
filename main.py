import cv2
from ultralytics import YOLO

# 1. Carrega o modelo YOLO (o 'n' é de 'nano', mais rápido para tempo real)
model = YOLO('yolov8n.pt') 

# 2. Inicializa a captura da webcam (0 costuma ser a câmera integrada)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

print("Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Realiza a detecção no frame atual
    # stream=True é mais eficiente para processamento de vídeo
    results = model(frame, stream=True)

    person_count = 0

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # O ID da classe 'pessoa' no dataset COCO (padrão do YOLO) é 0
            cls = int(box.cls[0])
            if cls == 0:
                person_count += 1
                
                # Desenhar a caixa e o rótulo no frame
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "Pessoa", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 4. Exibe a contagem na tela
    cv2.putText(frame, f'Pessoas detectadas: {person_count}', (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # 5. Mostra o resultado final
    cv2.imshow('Detector YOLO - Contagem de Pessoas', frame)

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpeza
cap.release()
cv2.destroyAllWindows()