'''
Ingest data from a GitHub repository containing match data into a Delta Lake bronze layer.
'''

import json
import polars as pl
from deltalake import write_deltalake
from schemas import apply_schema
from pathlib import Path
from github_utils import get_github_contents, process_github_contents

def main():
    print("Bronze ingestion started...")

    # GitHub repository files download
    repo_url = 'https://github.com/SkillCorner/opendata/tree/master/data/matches'
    base_path = Path(__file__).resolve().parent.parent

    data_path = Path(base_path / "data/raw/")
    
    print(f"Start downloading from: {repo_url}")
    print(f"Saving files at: {data_path.absolute()}")
    
    data_path.mkdir(parents=True, exist_ok=True)
    
    contents = get_github_contents(repo_url)
    
    if not contents:
        print("Cannot access the GitHub repository or no contents found.")
        return
    
    downloaded_files = []

    process_github_contents(contents, repo_url, data_path, downloaded_files)

    print("Download finished!")

    # Ingestion to Delta Lake bronze layerrows_match, rows_tracking = [], []
    rows_match, rows_tracking = [], []
    df_dynamic = pl.DataFrame()

    for match_file in Path(base_path / "data/raw/").glob("*_match.json"):
        match = json.loads(match_file.read_text(encoding="utf-8"))
        match_id = match["id"]
        rows_match.append({"match_id": match_id, "json": json.dumps(match, ensure_ascii=False)})

        trk_file = match_file.with_name(match_file.stem.replace("_match", "_tracking_extrapolated.jsonl"))
        if trk_file.exists():
            for line in trk_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    rows_tracking.append({"match_id": match_id, "json": line})

        dynamic_file = match_file.with_name(match_file.stem.replace("_match", "_dynamic_events.csv"))
        if dynamic_file.exists():
            df_dynamic = (
                pl.concat([
                    df_dynamic,
                    pl.read_csv(dynamic_file, infer_schema_length=None)
                ])
            )
    
    # Load match video info file
    match_video_info_file = pl.read_csv(base_path / "data/raw/match_video_info.csv", infer_schema_length=None)

    df_match = apply_schema(pl.DataFrame(rows_match), "bronze_match_raw")
    df_tracking = apply_schema(pl.DataFrame(rows_tracking), "bronze_tracking_raw")
    df_match_video_info = apply_schema(match_video_info_file, "bronze_match_video_info")

    if df_match.height: 
        write_deltalake(str(base_path / "data/delta/bronze/match"), df_match.to_arrow(), mode="overwrite", overwrite_schema=True)
    if df_tracking.height:   
        write_deltalake(str(base_path / "data/delta/bronze/tracking"), df_tracking.to_arrow(), mode="overwrite", overwrite_schema=True)
    if df_dynamic.height:
        write_deltalake(str(base_path / "data/delta/bronze/dynamic_events"), df_dynamic.to_arrow(), mode="overwrite", overwrite_schema=True)
    if df_match_video_info.height:
        write_deltalake(str(base_path / "data/delta/bronze/match_video_info"), df_match_video_info.to_arrow(), mode="overwrite", overwrite_schema=True)

    print("Bronze layer ingestion completed!")

if __name__ == "__main__":
    main()
