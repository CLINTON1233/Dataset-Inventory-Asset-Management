import cv2
import os

FRAME_INTERVAL = 5  # ambil 1 frame tiap N frame

# ===============================
# PILIH KATEGORI
# ===============================
print("\nPILIH JENIS VIDEO:")
print("1. Serial Number")
print("2. Devices")
print("3. Materials")
print("4. Scan Code")

category_choice = input("\nPilih (1/2/3/4): ").strip()

if category_choice == "1":
    VIDEOS_DIR = "videos/serial_number"
    FRAMES_DIR = "frames/serial_number_frames"
    category_name = "SERIAL NUMBER"
elif category_choice == "2":
    VIDEOS_DIR = "videos/devices"
    FRAMES_DIR = "frames/devices_frames"
    category_name = "DEVICES"
elif category_choice == "3":
    VIDEOS_DIR = "videos/materials"
    FRAMES_DIR = "frames/materials_frames"
    category_name = "MATERIALS"
elif category_choice == "4":
    VIDEOS_DIR = "videos/scan_code"
    FRAMES_DIR = "frames/scan_code_frames"
    category_name = "SCAN CODE"
else:
    print("Pilihan tidak valid")
    exit()

os.makedirs(FRAMES_DIR, exist_ok=True)

# ===============================
# AMBIL SEMUA VIDEO
# ===============================
videos = [
    f for f in os.listdir(VIDEOS_DIR)
    if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
]

if not videos:
    print(f"Tidak ada video di {VIDEOS_DIR}")
    exit()

# ===============================
# MENU PILIH VIDEO
# ===============================
print(f"\nDAFTAR VIDEO ({category_name}):")
for i, v in enumerate(videos, 1):
    print(f"{i}. {v}")

print("0.Export SEMUA video")

choice = input("\nPilih nomor video: ").strip()

if choice == "0":
    selected_videos = videos
else:
    try:
        idx = int(choice) - 1
        selected_videos = [videos[idx]]
    except:
        print("Pilihan tidak valid")
        exit()

# ===============================
# PROSES VIDEO
# ===============================
for video_file in selected_videos:
    video_path = os.path.join(VIDEOS_DIR, video_file)
    video_name = os.path.splitext(video_file)[0]

    output_dir = os.path.join(FRAMES_DIR, video_name)
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nProcessing: {video_file}")

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS: {fps}")

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % FRAME_INTERVAL == 0:
            filename = os.path.join(
                output_dir, f"frame_{saved_count:05d}.jpg"
            )
            cv2.imwrite(filename, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"✅ {saved_count} frame tersimpan di {output_dir}")

print("\nSEMUA SELESAI!")
