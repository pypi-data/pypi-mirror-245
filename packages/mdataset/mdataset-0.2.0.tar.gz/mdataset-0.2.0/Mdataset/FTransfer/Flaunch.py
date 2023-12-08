from flask import Flask, send_file, request, render_template
import os
import zipfile
import hashlib
import secrets
import torch
import socket

def flaunch_app(folder_path):
    app = Flask(__name__)

    def generate_random_url():
        return secrets.token_urlsafe(10)

    # Generate a random secret key using torch
    secret_key = torch.randn(1).item()

    def generate_signature(url):
        return hashlib.sha256((url + str(secret_key)).encode('utf-8')).hexdigest()

    def zip_folder(folder_path):
        folder_name = os.path.basename(folder_path)
        zip_filename = f"{folder_name}.zip"

        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname=arcname)

        return zip_filename

    # Generate the random URL once
    random_url = generate_random_url()

    # Generate the signature once
    signature = generate_signature(random_url)

    @app.route('/share')
    def share_folder():
        print("Random URL:", random_url)
        print("Generated Signature:", signature)
        return render_template('index.html', random_url=random_url, signature=signature)

    @app.route('/download/<random_url>/<signature>')
    def download_folder(random_url, signature):
        expected_signature = generate_signature(random_url)
        print("Received Signature:", signature)
        print("Expected Signature:", expected_signature)

        if signature == expected_signature:
            zip_filename = zip_folder(folder_path)
            return send_file(zip_filename, as_attachment=True)
        else:
            return "Authentication failed."

    if __name__ == '__main__':
        # Get the local machine's IP address
        host = socket.gethostbyname(socket.gethostname())
        port = 8080
        page_url = f"http://{host}:{port}/share"

        print("Generated Shareable URL:", page_url)
        print("Generated Signature:", signature)

        app.run(host=host, port=port)

# folder_path = r"F:\Dataset\Polish BERT"
# create_app(folder_path)
