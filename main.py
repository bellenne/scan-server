from qr_service.app import QRServiceApp
from qr_service.config import SCANNER_VID, SCANNER_PID, BAUDRATE


def main():
    app = QRServiceApp(
        default_vid=SCANNER_VID,
        default_pid=SCANNER_PID,
        baudrate=BAUDRATE,
    )
    app.run()


if __name__ == "__main__":
    main()
