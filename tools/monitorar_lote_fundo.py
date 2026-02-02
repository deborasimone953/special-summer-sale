import time

from processar_fotos_lote import process_pending


SLEEP_SECONDS = 3


def main() -> None:
    print("Monitorando assets/lote_fundo/entrada... (Ctrl+C para sair)")
    while True:
        try:
            processed = process_pending()
            if processed:
                print(f"Novas fotos processadas: {processed}")
        except Exception as exc:
            print(f"Erro no processamento: {exc}")
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    main()
