'''
Transforms raw data from the bronze layer into structured silver layer tables.
'''

import json
import polars as pl
from pathlib import Path
from schemas import apply_schema
from data_utils import seconds_from_time, get_channel, get_subthird
from delta_utils import read_delta, write_with_schema
from math import trunc

def main():
    print("Silver layer transformation started...")

    base_path = Path(__file__).resolve().parent.parent

    df_match_raw = read_delta(base_path / "data/delta/bronze/match").collect()
    df_tracking_raw = read_delta(base_path / "data/delta/bronze/tracking").collect()
    df_dynamic_events_raw = read_delta(base_path / "data/delta/bronze/dynamic_events")
    df_match_video_info = read_delta(base_path / "data/delta/bronze/match_video_info").collect()

    dim_match_rows, dim_player_rows, dim_team_rows = [], [], []
    dim_competition_rows, dim_kit_rows = [], []
    fact_player_match_rows, fact_tracking_rows = [], []

    for row in df_match_raw.iter_rows(named=True):
        match_data = json.loads(row["json"])
        match_id = match_data["id"]
        home_team_id = (match_data.get("home_team") or {}).get("id")
        away_team_id = (match_data.get("away_team") or {}).get("id")

        dim_match_rows.append({
            "match_id": match_id,
            "home_team_score": match_data.get("home_team_score"),
            "away_team_score": match_data.get("away_team_score"),
            "home_team_side_first": match_data.get("home_team_side")[0].split("_")[0],
            "home_team_side_second": match_data.get("home_team_side")[1].split("_")[0],
            "away_team_side_first": match_data.get("home_team_side")[1].split("_")[0],
            "away_team_side_second": match_data.get("home_team_side")[0].split("_")[0],
            "date_time": match_data.get("date_time"),
            "stadium_id": match_data.get("stadium", {}).get("id"),
            "home_team_id": home_team_id,
            "away_team_id": away_team_id,
            "team_homekit_id": match_data.get("home_team_kit", {}).get("id"),
            "team_awaykit_id": match_data.get("away_team_kit", {}).get("id"),
            "home_team_coach_id": match_data.get("home_team_coach"),
            "away_team_coach_id": match_data.get("away_team_coach"),
            "home_team_playing_minutes_tip": match_data.get("home_team_playing_minutes_tip"),
            "away_team_playing_minutes_tip": match_data.get("away_team_playing_minutes_tip"),
            "home_team_playing_minutes_otip": match_data.get("home_team_playing_minutes_otip"),
            "away_team_playing_minutes_otip": match_data.get("away_team_playing_minutes_otip"),
            "first_period_duration_minutes": match_data.get("match_periods", {})[0].get("duration_minutes"),
            "second_period_duration_minutes": match_data.get("match_periods", {})[1].get("duration_minutes"),
            "competition_edition_id": match_data.get("competition_edition", {}).get("id"),
            "competition_id": match_data.get("competition_edition", {}).get("competition", {}).get("id"),
            "season_id": match_data.get("competition_edition", {}).get("season", {}).get("id"),
            "round_number":match_data.get("competition_round", {}).get("round_number"),
        })

        competition_edition = match_data.get("competition_edition", {}) or {}
        competition = competition_edition.get("competition", {}) or {}
        season = competition_edition.get("season", {}) or {}
        dim_competition_rows.append({
            "competition_edition_id": competition_edition.get("id"),
            "competition_id": competition.get("id"),
            "competition_name": competition.get("name"),
            "area": competition.get("area"),
            "name": competition.get("name"),
            "gender": competition.get("gender"),
            "age_group": competition.get("age_group"),
            "season_id": season.get("id"),
            "season_start_year": season.get("start_year"),
            "season_end_year": season.get("end_year"),
            "season_name": season.get("name"),
        })

        home = match_data.get("home_team", {}) or {}
        away = match_data.get("away_team", {}) or {}
        dim_team_rows.extend([
            {
                "team_id": home.get("id"),
                "name": home.get("name"),
                "short_name": home.get("short_name"),
                "acronym": home.get("acronym"),
            },
            {
                "team_id": away.get("id"),
                "name": away.get("name"),
                "short_name": away.get("short_name"),
                "acronym": away.get("acronym"),
            },
        ])

        home_kit = match_data.get("home_team_kit", {}) or {}
        away_kit = match_data.get("away_team_kit", {}) or {}
        if home_kit:
            dim_kit_rows.append({
                "team_kit_id": home_kit.get("id"),
                "jersey_color": home_kit.get("jersey_color"),
                "number_color": home_kit.get("number_color"),
            })
        if away_kit:
            dim_kit_rows.append({
                "team_kit_id": away_kit.get("id"),
                "jersey_color": away_kit.get("jersey_color"),
                "number_color": away_kit.get("number_color"),
            })

        player_team_map = {}
        for player in match_data.get("players", []):
            player_id = player.get("id")
            team_id = player.get("team_id")
            player_team_map[player_id] = team_id

            dim_player_rows.append({
                "player_id": player.get("id"),
                "team_id": player.get("team_id"),
                "first_name": player.get("first_name"),
                "last_name": player.get("last_name"),
                "short_name": player.get("short_name"),
                "birthday": player.get("birthday"),
                "gender": player.get("gender"),
            })

            total_minutes = (player.get("playing_time") or {}).get("total") or {}
            fact_player_match_rows.append({
                "match_id": match_id,
                "player_id": player.get("id"),
                "team_id": player.get("team_id"),
                "competition_edition_id": competition_edition.get("id"),
                "competition_id": competition.get("id"),
                "season_id": season.get("id"),
                "number": player.get("number"),
                "minutes_played": total_minutes.get("minutes_played"),
                "start_time": player.get("start_time"),
                "end_time": player.get("end_time"),
                "player_role_id": (player.get("player_role") or {}).get("id"),
                "position_group": (player.get("player_role") or {}).get("position_group"),
                "position_acronym": (player.get("player_role") or {}).get("acronym"),
                "yellow_card": player.get("yellow_card"),
                "red_card": player.get("red_card"),
                "goal": player.get("goal"),
                "own_goal": player.get("own_goal"),
                "injured": player.get("injured"),
            })

        tracking_rows = (
            df_tracking_raw.filter(pl.col("match_id") == match_id)["json"]
            .to_list()
        )
        for row in tracking_rows:
            if not row.strip():
                continue
            try:
                tracking_row = json.loads(row)
            except json.JSONDecodeError:
                continue

            ts_time = tracking_row.get("timestamp")

            period = tracking_row.get("period")
            frame = tracking_row.get("frame")

            ball = tracking_row.get("ball_data") or {}
            fact_tracking_rows.append({
                "match_id": match_id,
                "frame": frame,
                "timestamp": ts_time,
                "period": period,
                "object_id": -1,
                "x": ball.get("x"),
                "y": ball.get("y"),
                "z": ball.get("z"),
                "group": "ball",
                "has_possession": False,
                "is_detected": ball.get("is_detected"),
            })

            possession_player = tracking_row.get("possession").get("player_id") or {}
            for player_row in tracking_row.get("player_data", []):
                player_id = player_row.get("player_id")
                team_id = player_team_map.get(player_id)
                if team_id is None:
                    group = None
                elif team_id == home_team_id:
                    group = "home team"
                elif team_id == away_team_id:
                    group = "away team"
                else:
                    group = None

                fact_tracking_rows.append({
                    "match_id": match_id,
                    "frame": frame,
                    "timestamp": ts_time,
                    "period": period,
                    "object_id": player_id,
                    "x": player_row.get("x"),
                    "y": player_row.get("y"),
                    "z": None,
                    "group": group,
                    "has_possession": player_id == possession_player,
                    "is_detected": player_row.get("is_detected"),
                })

    fact_tracking_rows = (
        pl.LazyFrame(fact_tracking_rows)
        .with_columns(
            zone_tracking = pl.col("y").map_elements(get_channel) + pl.col("x").map_elements(get_subthird)
        )
    )

    dynamic_events_rows = (
        df_dynamic_events_raw
            .select([
                "match_id",
                "event_id", 
                "frame_start", "frame_end", 
                "time_start", "time_end", 
                "period", 
                "team_id", "team_shortname",
                "event_type", "event_subtype",
                "player_id", "player_name", "player_position", 
                "player_in_possession_id", "player_in_possession_name", "player_in_possession_position",
                "x_start","y_start",
                "x_end","y_end",
                "player_in_possession_x_start","player_in_possession_y_start",
                "player_in_possession_x_end","player_in_possession_y_end",
                "channel_start", "third_start", 
                "channel_end", "third_end",
                "team_in_possession_phase_type", "team_out_of_possession_phase_type",
                "start_type", 
                "end_type",
                "game_state_id", "game_state",
                "associated_player_possession_event_id",
                "targeted", "received",
                "xthreat", "xpass_completion", "passing_option_score",
                "speed_avg_band",
                "pressing_chain_index",
                "pressing_chain_end_type",  
                "first_line_break", "second_last_line_break", "last_line_break",
                "pass_ahead", "quick_pass", "one_touch",
            ])
            .with_columns(
                seconds_start = pl.col("time_start").map_elements(seconds_from_time),
                seconds_end = pl.col("time_end").map_elements(lambda x:seconds_from_time(x, start= False))
            )
            .with_columns(
                minute_start = pl.col("seconds_start").map_elements(lambda x: trunc(x / 60) + 1),
                minute_end = pl.col("seconds_end").map_elements(lambda x: trunc(x / 60) + 1),
            )
            .with_columns(
                zone_start = pl.col("y_start").map_elements(get_channel) + pl.col("x_start").map_elements(get_subthird),
                zone_end = pl.col("y_end").map_elements(get_channel) + pl.col("x_end").map_elements(get_subthird),
            )
            .join(
                fact_tracking_rows.rename({
                    "frame": "frame_start",
                    "object_id": "player_in_possession_id",
                    "zone_tracking": "player_in_possession_zone_start_from_tracking"
                })
                .select(["match_id", "frame_start", "player_in_possession_id", "player_in_possession_zone_start_from_tracking"]),
                on=["match_id", "frame_start", "player_in_possession_id"],
                how="left"
            )
            .join(
                fact_tracking_rows.rename({
                    "frame": "frame_end",
                    "object_id": "player_in_possession_id",
                    "zone_tracking": "player_in_possession_zone_end_from_tracking"
                })
                .select(["match_id", "frame_end", "player_in_possession_id", "player_in_possession_zone_end_from_tracking"]),
                on=["match_id", "frame_end", "player_in_possession_id"],
                how="left"
            )
            .with_columns(
                player_in_possession_zone_start = pl.coalesce([
                    pl.col("player_in_possession_y_start").map_elements(get_channel) + pl.col("player_in_possession_x_start").map_elements(get_subthird),
                    pl.col("player_in_possession_zone_start_from_tracking")
                ]),
                player_in_possession_zone_end = pl.coalesce([
                    pl.col("player_in_possession_y_end").map_elements(get_channel) + pl.col("player_in_possession_x_end").map_elements(get_subthird),
                    pl.col("player_in_possession_zone_end_from_tracking")
                ])
            )
            .drop(["player_in_possession_zone_start_from_tracking","player_in_possession_zone_end_from_tracking"])
    ).collect()

    dim_match_df = (
        pl.DataFrame(dim_match_rows)
        .join(
            df_match_video_info,
            on="match_id",
            how="left"
        )
    )

    dim_match = apply_schema(dim_match_df, "dim_match").unique(subset=["match_id"])
    dim_player = apply_schema(pl.DataFrame(dim_player_rows), "dim_player").unique(subset=["player_id"])
    dim_team = apply_schema(pl.DataFrame(dim_team_rows), "dim_team").unique(subset=["team_id"])
    dim_competitionetition = apply_schema(pl.DataFrame(dim_competition_rows), "dim_competition").unique(subset=["competition_edition_id"])
    dim_team_kit = apply_schema(pl.DataFrame(dim_kit_rows), "dim_team_kit").unique(subset=["team_kit_id"])
    fact_player = apply_schema(pl.DataFrame(fact_player_match_rows), "fact_player_match").unique(subset=["match_id","player_id"])
    fact_tracking = apply_schema(fact_tracking_rows.collect(), "fact_tracking")
    fact_dynamic_events = apply_schema(pl.DataFrame(dynamic_events_rows), "fact_dynamic_events")

    write_with_schema(Path(base_path / "data/delta/silver/match"), dim_match, "dim_match")
    write_with_schema(Path(base_path / "data/delta/silver/player"), dim_player, "dim_player")
    write_with_schema(Path(base_path / "data/delta/silver/team"), dim_team, "dim_team")
    write_with_schema(Path(base_path / "data/delta/silver/competition"), dim_competitionetition, "dim_competition")
    write_with_schema(Path(base_path / "data/delta/silver/team_kit"),  dim_team_kit, "dim_team_kit")
    write_with_schema(Path(base_path / "data/delta/silver/player_match"), fact_player, "fact_player_match")
    write_with_schema(Path(base_path / "data/delta/silver/tracking"), fact_tracking, "fact_tracking")
    write_with_schema(Path(base_path / "data/delta/silver/dynamic_events"), fact_dynamic_events, "fact_dynamic_events")

    print("Silver layer transformation completed!")

if __name__ == "__main__":
    main()
