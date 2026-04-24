import os

import cv2
import numpy as np
from ultralytics import YOLO

try:
    import face_recognition
except ImportError:
    print("Erro: biblioteca 'face_recognition' nao encontrada.")
    print("Instale com: pip install face-recognition")
    raise SystemExit(1)


KNOWN_FACES_DIR = "faces_db"
TOLERANCE = 0.5
RESIZE_SCALE = 0.5


def load_known_faces(base_dir):
    known_face_encodings = []
    known_face_names = []

    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
        print(f"Aviso: pasta '{base_dir}' criada. Adicione imagens para reconhecimento.")
        return known_face_encodings, known_face_names

    valid_ext = {".jpg", ".jpeg", ".png", ".bmp"}

    for person_name in os.listdir(base_dir):
        person_dir = os.path.join(base_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        for image_name in os.listdir(person_dir):
            _, ext = os.path.splitext(image_name.lower())
            if ext not in valid_ext:
                continue

            image_path = os.path.join(person_dir, image_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if not encodings:
                print(f"Aviso: nenhum rosto encontrado em '{image_path}'.")
                continue

            known_face_encodings.append(encodings[0])
            known_face_names.append(person_name)

    return known_face_encodings, known_face_names

# 1. Carrega o modelo YOLO (o 'n' e de 'nano', mais rapido para tempo real)
model = YOLO('yolov8n.pt')

# 2. Carrega base de rostos conhecidos
known_face_encodings, known_face_names = load_known_faces(KNOWN_FACES_DIR)
print(f"Rostos cadastrados: {len(known_face_names)}")

# 3. Inicializa a captura da webcam (0 costuma ser a camera integrada)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

print("Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 4. Realiza a deteccao de pessoas no frame atual
    # stream=True é mais eficiente para processamento de vídeo
    results = model(frame, stream=True)

    person_count = 0

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # O ID da classe 'pessoa' no dataset COCO (padrao do YOLO) e 0
            cls = int(box.cls[0])
            if cls == 0:
                person_count += 1
                
                # Desenhar a caixa e o rótulo no frame
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "Pessoa", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 5. Reconhecimento facial com base local (faces_db)
    small_frame = cv2.resize(frame, (0, 0), fx=RESIZE_SCALE, fy=RESIZE_SCALE)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    recognized_count = 0
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Desconhecido"

        if known_face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings,
                face_encoding,
                tolerance=TOLERANCE,
            )
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = int(np.argmin(face_distances))

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                recognized_count += 1

        inv_scale = 1 / RESIZE_SCALE
        top = int(top * inv_scale)
        right = int(right * inv_scale)
        bottom = int(bottom * inv_scale)
        left = int(left * inv_scale)

        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (255, 0, 0), cv2.FILLED)
        cv2.putText(
            frame,
            name,
            (left + 6, bottom - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
        )

    # 6. Exibe contagens na tela
    cv2.putText(frame, f'Pessoas detectadas: {person_count}', (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.putText(frame, f'Rostos detectados: {len(face_locations)}', (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(frame, f'Rostos reconhecidos: {recognized_count}', (20, 115),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # 7. Mostra o resultado final
    cv2.imshow('YOLO + Reconhecimento Facial', frame)

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpeza
cap.release()
cv2.destroyAllWindows()