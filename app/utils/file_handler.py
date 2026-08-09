import csv
import json
from pathlib import Path


class FileHandler:
    """
    Handles exporting notices into different file formats.
    """

    EXPORT_DIR = Path("exports")

    def __init__(self):
        self.EXPORT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    def export_json(self, notices):
        """
        Export notices as a JSON file.
        """

        file_path = self.EXPORT_DIR / "notices.json"

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                notices,
                file,
                indent=4,
                ensure_ascii=False
            )

        return file_path

    def export_csv(self, notices):
        """
        Export notices as a CSV file.
        """

        file_path = self.EXPORT_DIR / "notices.csv"

        if not notices:
            headers = [
                "id",
                "title",
                "description",
                "category",
                "created_at",
                "expiry_date",
                "status"
            ]
        else:
            headers = list(notices[0].keys())

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=headers
            )

            writer.writeheader()
            writer.writerows(notices)

        return file_path

    def export_txt(self, notices):
        """
        Export notices as a text file.
        """

        file_path = self.EXPORT_DIR / "notices.txt"

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            for notice in notices:
                file.write("=" * 60 + "\n")
                file.write(
                    f"Notice ID: {notice['id']}\n"
                )
                file.write(
                    f"Title: {notice['title']}\n"
                )
                file.write(
                    f"Description: {notice['description']}\n"
                )
                file.write(
                    f"Category: {notice['category']}\n"
                )
                file.write(
                    f"Created At: {notice['created_at']}\n"
                )
                file.write(
                    f"Expiry Date: {notice['expiry_date']}\n"
                )
                file.write(
                    f"Status: {notice['status']}\n"
                )

            file.write("=" * 60 + "\n")


        return file_path


file_handler = FileHandler()