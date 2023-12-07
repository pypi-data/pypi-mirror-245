if __name__ == "__main__":
    from datetime import datetime
    from pathlib import Path

    from extra_helpers.emf_model_runner import run_emf_model

    FILE_ROOT = Path(__file__).resolve().parent
    MG_FILE = "dat/dlc_site_3_mg.json"
    MG_FILE_PATH = Path.joinpath(FILE_ROOT, MG_FILE)
    MG_NAME = "DLC Site 3"
    MG_CALL_SCHEDULE = 1
    START = datetime(2022, 8, 1)
    END = datetime(2022, 8, 2)

    run_emf_model(
        filename=str(MG_FILE_PATH),
        mg_name=MG_NAME,
        call_schedule=MG_CALL_SCHEDULE,
        start=START,
        end=END,
    )
