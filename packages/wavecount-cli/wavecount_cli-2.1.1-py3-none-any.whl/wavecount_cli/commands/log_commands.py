import os
from datetime import date, timedelta

import click
import inquirer as inq
from inquirer.themes import GreenPassion
from wavecount_cli.services.backend_services import Backend


@click.command(name="log", help="Get device log. Use options")
@click.pass_context
@click.argument("args", nargs=1, default=None, required=False)
@click.option(
    "-sn", "--serial-number", help="Device serial-number", default=None, is_eager=True
)
@click.option("-id", "--device-id", help="Device id", default=None, is_eager=True)
@click.option("-fd", "--from-date", help="From date", default=None, is_eager=True)
@click.option("-td", "--to-date", help="To date", default=None, is_eager=True)
def log(ctx, args, serial_number, device_id, from_date, to_date):
    try:
        force_get_log = False
        if args == "force":
            force_get_log = True
        questions = []
        if not serial_number and not device_id:
            questions.append(
                {
                    "type": "input",
                    "name": "serial_number",
                    "message": 'Enter device "serial-number"',
                }
            )
        if not from_date:
            questions.append(
                {
                    "type": "input",
                    "name": "from_date",
                    "message": 'Enter "start-date". format <YYYY-MM-DD>',
                    "default": str(date.today() - timedelta(days=1)),
                }
            )
        if not to_date:
            questions.append(
                {
                    "type": "input",
                    "name": "to_date",
                    "message": 'Enter "end-date". format <YYYY-MM-DD>',
                    "default": str(date.today()),
                }
            )
        questions.append(
            {
                "type": "checkbox",
                "name": "targets",
                "message": "Select targets",
                "choices": [
                    {"enabled": True, "name": "Azure", "value": "azure"},
                    {"enabled": True, "name": "Frames", "value": "frames"},
                    {"enabled": True, "name": "Panel", "value": "panel"},
                    {"enabled": True, "name": "Sensor", "value": "sensor"},
                ],
                "validate": lambda answer: "You must choose at least one traget."
                if len(answer) == 0
                else True,
            }
        )
        answers = inq.prompt(questions=questions, theme=GreenPassion())
        backend = Backend(ctx)
        if answers is not None:
            period = {
                "from": answers["from_date"] if "from_date" in answers else from_date,
                "to": answers["to_date"] if "to_date" in answers else to_date,
            }
            blob_data = backend.request_device_logs(
                is_forced=force_get_log,
                period=period,
                device_id=device_id,
                serial_number=answers["serial_number"]
                if "serial_number" in answers
                else serial_number,
                targets=answers["targets"],
            )
            blob_name = blob_data["blobName"]
            file = backend.download_device_logs(blob_name)
            local_path = os.path.expanduser("~/Desktop")
            local_file_path = blob_name.replace("/", "_")
            download_file_path = os.path.join(local_path, local_file_path)
            with open(download_file_path, "wb+") as download_file:
                download_file.write(file)
            click.secho("  Saved at {}".format(download_file_path), fg="green")
    except Exception as e:
        exit(1)
