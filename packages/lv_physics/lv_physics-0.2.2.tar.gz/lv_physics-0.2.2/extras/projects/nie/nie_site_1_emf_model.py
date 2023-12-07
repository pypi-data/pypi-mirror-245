if __name__ == "__main__":
    from datetime import datetime
    from pathlib import Path

    from extra_helpers.emf_model_runner import run_emf_model

    FILE_ROOT = Path(__file__).resolve().parent
    MG_FILE = "dat/nie_site_1_mg.json"
    MG_FILE_PATH = Path.joinpath(FILE_ROOT, MG_FILE)
    MG_NAME = "NIE SITE 1"
    MG_CALL_SCHEDULE = 1
    START = datetime(2021, 11, 1)
    END = datetime(2021, 11, 13)

    run_emf_model(
        filename=str(MG_FILE_PATH),
        mg_name=MG_NAME,
        call_schedule=MG_CALL_SCHEDULE,
        start=START,
        end=END,
    )
