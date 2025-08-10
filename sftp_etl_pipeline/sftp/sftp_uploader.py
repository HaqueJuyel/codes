# # import os
# # import paramiko
# # from dotenv import load_dotenv

# # load_dotenv()

# # def upload_to_sftp(file_path):
# #     host = os.getenv("SFTP_HOST")
# #     port = int(os.getenv("SFTP_PORT"))
# #     username = os.getenv("SFTP_USER")
# #     password = os.getenv("SFTP_PASSWORD")
# #     target_dir = os.getenv("SFTP_TARGET_DIR")

# #     try:
# #         transport = paramiko.Transport((host, port))
# #         transport.connect(username=username, password=password)
# #         print(f"Uploading file from local path: {file_path}")

# #         sftp = paramiko.SFTPClient.from_transport(transport)

# #         filename = os.path.basename(file_path)
# #         print(f"Uploading {filename} to SFTP server at {host}:{port}")
# #         remote_path = os.path.join(target_dir, filename)

# #         sftp.put(file_path, remote_path)
# #         print(f"Uploaded {file_path} to {remote_path} on SFTP server.")

# #         sftp.close()
# #         transport.close()

# #     except Exception as e:
# #         print(f"SFTP upload failed: {e}")

# import os
# import paramiko
# from dotenv import load_dotenv

# load_dotenv()

# def upload_to_sftp(file_path):
#     host = os.getenv("SFTP_HOST")
#     port = int(os.getenv("SFTP_PORT"))
#     username = os.getenv("SFTP_USER")
#     password = os.getenv("SFTP_PASSWORD")
#     target_dir = os.getenv("SFTP_TARGET_DIR")

#     try:
#         # Resolve absolute path and validate
#         abs_file_path = os.path.abspath(file_path)
#         if not os.path.exists(abs_file_path):
#             print(f"ERROR: File does not exist at path: {file_path}")
#             print(f"Resolved absolute path: {abs_file_path}")
#             return

#         print(f"Uploading file from local path: {abs_file_path}")

#         # Establish transport
#         transport = paramiko.Transport((host, port))
#         transport.connect(username=username, password=password)
#         sftp = paramiko.SFTPClient.from_transport(transport)

#         # Define remote path
#         filename = os.path.basename(abs_file_path)
#         remote_path = os.path.join(target_dir, filename)
#         print(f"Uploading {filename} to SFTP server at {host}:{port}, remote path: {remote_path}")

#         # Upload
#         sftp.put(abs_file_path, remote_path)
#         print(f"Uploaded {abs_file_path} to {remote_path} on SFTP server.")

#         # Cleanup
#         sftp.close()
#         transport.close()

#     except Exception as e:
#         print(f"SFTP upload failed: {type(e).__name__}: {e}")



#         import os
# import paramiko
# from dotenv import load_dotenv

# load_dotenv()

# def upload_to_sftp(file_path):
#     host = os.getenv("SFTP_HOST")
#     port = int(os.getenv("SFTP_PORT"))
#     username = os.getenv("SFTP_USER")
#     key_path = os.getenv("SFTP_PRIVATE_KEY_PATH")  # Path to private key (.pem or .ppk)
#     target_dir = os.getenv("SFTP_TARGET_DIR")

#     try:
#         # Resolve absolute path and validate
#         abs_file_path = os.path.abspath(file_path)
#         if not os.path.exists(abs_file_path):
#             print(f"ERROR: File does not exist at path: {file_path}")
#             print(f"Resolved absolute path: {abs_file_path}")
#             return

#         print(f"Uploading file from local path: {abs_file_path}")

#         # Load private key
#         key = paramiko.RSAKey.from_private_key_file(key_path)

#         # Establish transport
#         transport = paramiko.Transport((host, port))
#         transport.connect(username=username, pkey=key)
#         sftp = paramiko.SFTPClient.from_transport(transport)

#         # Define remote path
#         filename = os.path.basename(abs_file_path)
#         remote_path = os.path.join(target_dir, filename)
#         print(f"Uploading {filename} to SFTP server at {host}:{port}, remote path: {remote_path}")

#         # Upload
#         sftp.put(abs_file_path, remote_path)
#         print(f"Uploaded {abs_file_path} to {remote_path} on SFTP server.")

#         # Cleanup
#         sftp.close()
#         transport.close()

#     except Exception as e:
#         print(f"SFTP upload failed: {type(e).__name__}: {e}")

# sftp_uploader.py
import os
import posixpath
import paramiko
from dotenv import load_dotenv

load_dotenv()


def upload_to_sftp(local_folder):
    """Upload all files from a local folder to the SFTP target directory."""
    host = os.getenv("SFTP_HOST")
    port = int(os.getenv("SFTP_PORT", 22))
    username = os.getenv("SFTP_USER")
    password = os.getenv("SFTP_PASSWORD")
    target_dir = os.getenv("SFTP_TARGET_DIR", ".")

    # Normalize for Windows paths
    local_folder = os.path.normpath(local_folder)

    if not os.path.isdir(local_folder):
        print(f"❌ ERROR: Folder not found: {local_folder}")
        return

    try:
        # Connect to SFTP
        print(f"🔗 Connecting to SFTP: {username}@{host}:{port}")
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Ensure target directory exists on remote
        _mkdir_p(sftp, target_dir)

        # Upload each file in folder
        for filename in os.listdir(local_folder):
            local_file_path = os.path.join(local_folder, filename)

            if os.path.isfile(local_file_path):
                abs_file_path = os.path.abspath(local_file_path)
                remote_path = posixpath.join(target_dir, filename)  # Always POSIX for remote paths

                print(f"⬆️ Uploading {abs_file_path} → {remote_path}")
                try:
                    sftp.put(abs_file_path, remote_path)
                    print(f"✅ Uploaded: {filename}")
                except Exception as e:
                    print(f"❌ Failed to upload {filename}: {e}")

        # Close connection
        sftp.close()
        transport.close()
        print("🎯 All uploads complete.")

    except Exception as e:
        print(f"❌ SFTP upload failed: {type(e).__name__}: {e}")


def _mkdir_p(sftp, remote_directory):
    """Recursively create remote directories on SFTP server."""
    dirs = remote_directory.strip("/").split("/")
    current_path = ""
    for d in dirs:
        current_path = posixpath.join(current_path, d)
        try:
            sftp.stat("/" + current_path)
        except FileNotFoundError:
            print(f"📂 Creating remote dir: /{current_path}")
            sftp.mkdir("/" + current_path)
            try:
                sftp.chmod("/" + current_path, 0o755)  # Ensure write permission
            except Exception as chmod_err:
                print(f"⚠️ Could not set permissions for /{current_path}: {chmod_err}")




# Example usage:
