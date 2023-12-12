import json
import os
from pathlib import Path

from streamlit.web import bootstrap as bs


def create_app(info, cv_path) -> None:
    (info, cv_path) = (info, cv_path)
    # print((info, cv_path))
    app_path = os.path.join(Path(__file__).parent.absolute(), "create.py")
    bs.run(
        app_path,
        "",
        args=["--info", json.dumps(info), "--cv_path", cv_path],
        flag_options={},
    )


if __name__ == "__main__":
    create_app()
