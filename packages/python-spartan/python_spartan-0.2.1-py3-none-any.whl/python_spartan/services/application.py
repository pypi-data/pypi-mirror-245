import os
import requests
import zipfile
import io
import shutil


class ApplicationService:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.repository_name = "spartan-framework"

    def is_valid_folder_name(self):
        return self.project_name.isidentifier() and not self.project_name[0].isdigit()

    def download_zip(self):
        release_url = f"https://github.com/nerdmonkey/{self.repository_name}/archive/refs/heads/main.zip"
        try:
            response = requests.get(release_url)
            response.raise_for_status()
            return io.BytesIO(response.content)
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            return None

    def extract_zip(self, zip_data):
        temp_folder = "temp_extracted_folder"
        try:
            with zipfile.ZipFile(zip_data, "r") as zip_ref:
                zip_ref.extractall(temp_folder)
            return temp_folder
        except zipfile.BadZipFile:
            print("Error: The downloaded file is not a valid ZIP file.")
            return None

    def setup_project(self, temp_folder):
        extracted_files = os.listdir(temp_folder)
        if len(extracted_files) == 1 and os.path.isdir(
            os.path.join(temp_folder, extracted_files[0])
        ):
            extracted_folder = os.path.join(temp_folder, extracted_files[0])
            os.rename(extracted_folder, self.project_name)
            shutil.rmtree(temp_folder)
            return True
        return False

    def create_app(self):
        if os.path.exists(self.project_name):
            print(f"The {self.project_name} folder already exists. Aborting.")
            return
        if not self.is_valid_folder_name():
            print(f"{self.project_name} is not a valid project name. Aborting.")
            return

        zip_data = self.download_zip()
        if zip_data:
            temp_folder = self.extract_zip(zip_data)
            if temp_folder and self.setup_project(temp_folder):
                print("\n")
                ascii_art = [
                    ".d8888. d8888b.  .d8b.  d8888b. d888888b  .d8b.  d8b   db",
                    "88'  YP 88  `8D d8' `8b 88  `8D `~~88~~' d8' `8b 888o  88",
                    "`8bo.   88oodD' 88ooo88 88oobY'    88    88ooo88 88V8o 88",
                    "  `Y8b. 88~~~   88~~~88 88`8b      88    88~~~88 88 V8o88",
                    "db   8D 88      88   88 88 `88.    88    88   88 88  V888",
                    "`8888Y' 88      YP   YP 88   YD    YP    YP   YP VP   V8P",
                ]

                for line in ascii_art:
                    print(line)

                message = [
                    "Embark on your cloud software journey with Spartan determination and simplicity."
                    "Build your digital empire with unwavering focus and minimalism,"
                    "just like the warriors of ancient Sparta."
                ]

                for line in message:
                    print("\n")
                    print(line)

                print(
                    f"\nSuccessfully setup the project to {self.project_name} folder."
                )
                print(f"\nYour First Mission:")
                print(f"---------------")
                print(f"cd {self.project_name}")
                print(f"pip install -r requirements.txt")
                print(f"copy the .env.example and name it as .env")
                print(f"spartan migrate init -d sqlite")
                print(f"spartan migrate upgrade")
                print(f"spartan serve")
            else:
                print("Error: The ZIP file should contain a single top-level folder.")
