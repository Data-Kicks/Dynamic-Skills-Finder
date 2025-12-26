"""
Build gold views and aggregated tables from silver data.
"""

import polars as pl
from pathlib import Path
from schemas import apply_schema
from delta_utils import read_delta
from datetime import datetime

def main():
    print("Gold views and aggregated tables creation started...")

    base_path = Path(__file__).resolve().parent.parent

    # Final gold views
    silver_match = read_delta(base_path / "data/delta/silver/match")
    silver_team = read_delta(base_path / "data/delta/silver/team")
    silver_player = read_delta(base_path / "data/delta/silver/player")
    silver_competition = read_delta(base_path / "data/delta/silver/competition")
    silver_team_kit = read_delta(base_path / "data/delta/silver/team_kit")
    silver_tracking = read_delta(base_path / "data/delta/silver/tracking")
    silver_player_match = read_delta(base_path / "data/delta/silver/player_match")
    silver_dynamic_events = read_delta(base_path / "data/delta/silver/dynamic_events")

    tracking_view_df = (
        silver_tracking
        .join(
            silver_player_match
            .with_columns(object_id = pl.col("player_id"))
            .select(["match_id", "object_id", "player_id","number","team_id","position_acronym"]).rename({"number":"player_number"}),
            on=["match_id","object_id"], how="left"
        )
        .join(silver_match.select([
                "match_id","date_time","home_team_id","away_team_id","competition_edition_id","round_number",
                "team_homekit_id","team_awaykit_id"
        ]), on="match_id", how="left")

        # Player/team info
        .join(silver_player.select(["player_id","short_name"]).rename({"short_name":"player_name"}),
              on="player_id", how="left")
        .join(silver_team.select(["team_id","short_name"])
                    .rename({"short_name":"team_shortname"}),
              on="team_id", how="left")
    
        # Kit & competition info
        .with_columns(
            pl.when(pl.col("team_id").is_null())
              .then(pl.lit(None))
              .when(pl.col("team_id") == pl.col("home_team_id"))
              .then(pl.col("team_homekit_id"))
              .otherwise(pl.col("team_awaykit_id"))
              .alias("team_kit_id")
        )
        .join(silver_team_kit.select(["team_kit_id","jersey_color","number_color"])
                    .rename({"jersey_color":"team_jersey_color","number_color":"team_number_color"}),
              on="team_kit_id", how="left")
        .join(silver_competition.select(["competition_edition_id","competition_name","season_name"]),
              on="competition_edition_id", how="left")
        .select([
            "match_id","date_time",
            "competition_name","season_name","round_number",
            "player_id","player_name", "player_number", "team_id","team_shortname","group","position_acronym",
            "frame","timestamp","period","object_id",
            "x","y","z",
            "has_possession",
            "team_jersey_color","team_number_color",
        ])
        .filter(pl.col("timestamp").is_not_null())
    ).collect()

    dynamic_events_view_df = (
        silver_dynamic_events
        .join(silver_match.select([
                "match_id","date_time","home_team_id","away_team_id","team_homekit_id","team_awaykit_id","competition_edition_id","round_number",
                "youtube_video_id", "first_period_start", "second_period_start", "home_team_side_first", "home_team_side_second",
                "away_team_side_first", "away_team_side_second"
        ]), on="match_id", how="left")
        .with_columns(
            pl.when(pl.col("period") == 1)
              .then(pl.col("first_period_start") + pl.col("seconds_start"))
              .otherwise(pl.col("second_period_start") + pl.col("seconds_start") - (45*60) )
              .alias("event_start_seconds"),
            pl.when(pl.col("period") == 1)
              .then(pl.col("first_period_start") + pl.col("seconds_end"))
              .otherwise(pl.col("second_period_start") + pl.col("seconds_end") - (45*60) )
              .alias("event_end_seconds")
        )
        .drop(["first_period_start", "second_period_start"])
        .with_columns(
            period_name = pl.when(pl.col("period") == 1)
                            .then(pl.lit("First Half"))
                            .when(pl.col("period") == 2)
                            .then(pl.lit("Second Half"))
                            .when(pl.col("period") == 3)
                            .then(pl.lit("First Extra Time"))
                            .when(pl.col("period") == 4)
                            .then(pl.lit("Second Extra Time"))
                            .otherwise(pl.lit("Penalty Shootout"))
        )
        .with_columns(
            pl.when(pl.col("team_id").is_null())
              .then(pl.lit(None))
              .when(pl.col("team_id") == pl.col("home_team_id"))
              .then(pl.lit("home"))
              .otherwise(pl.lit("away"))
              .alias("group")
        )
        .join(silver_team.select(["team_id","short_name"])
                          .rename({"team_id":"home_team_id", 
                                   "short_name":"home_team_shortname"}),
              on="home_team_id", how="left"
        )
        .join(silver_team.select(["team_id","short_name"])
                          .rename({"team_id":"away_team_id", 
                                   "short_name":"away_team_shortname"}),
              on="away_team_id", how="left"
        )
        .with_columns(
            match_name = pl.concat_str([
                  pl.col("home_team_shortname"), 
                  pl.lit(" - "), 
                  pl.col("away_team_shortname")
            ]),
            match_longname = pl.concat_str([
                  pl.lit("R"),
                  pl.col("round_number"),
                  pl.lit(": "),
                  pl.col("home_team_shortname"),
                  pl.lit(" - "), 
                  pl.col("away_team_shortname")
            ])
        )
        .drop(["home_team_shortname", "away_team_shortname"])
    
        # Kit & competition info
        .with_columns(
            pl.when(pl.col("team_id").is_null())
              .then(pl.lit(None))
              .when(pl.col("team_id") == pl.col("home_team_id"))
              .then(pl.col("team_homekit_id"))
              .otherwise(pl.col("team_awaykit_id"))
              .alias("team_kit_id")
        )
        .join(silver_player_match.select(["match_id","player_id","number","position_group"]).rename({"number":"player_number"}),
              on=["match_id","player_id"], how="left")
        .join(silver_team_kit.select(["team_kit_id","jersey_color","number_color"])
                    .rename({"jersey_color":"team_jersey_color","number_color":"team_number_color"}),
              on="team_kit_id", how="left")
        .join(silver_competition.select(["competition_edition_id","competition_name","season_name"]),
              on="competition_edition_id", how="left")

        # Tracking plot coords
        .with_columns(
            pl.when((pl.col("group") == "home") & (pl.col("home_team_side_first") == "right") & (pl.col("period") == 1))
              .then(pl.col("x_start") * (-1))
              .otherwise(
                  pl.when((pl.col("group") == "home") & (pl.col("home_team_side_first") == "left") & (pl.col("period") == 1))
                  .then(pl.col("x_start"))
                  .otherwise(
                        pl.when((pl.col("group") == "home") & (pl.col("home_team_side_second") == "right") & (pl.col("period") == 2))
                        .then(pl.col("x_start") * (-1))
                        .otherwise(
                            pl.when((pl.col("group") == "home") & (pl.col("home_team_side_second") == "left") & (pl.col("period") == 2))
                            .then(pl.col("x_start"))
                            .otherwise(
                                pl.when((pl.col("group") == "away") & (pl.col("away_team_side_first") == "right") & (pl.col("period") == 1))
                                .then(pl.col("x_start") * (-1))
                                .otherwise(
                                    pl.when((pl.col("group") == "away") & (pl.col("away_team_side_first") == "left") & (pl.col("period") == 1))
                                    .then(pl.col("x_start"))
                                    .otherwise(
                                        pl.when((pl.col("group") == "away") & (pl.col("away_team_side_second") == "right") & (pl.col("period") == 2))
                                        .then(pl.col("x_start") * (-1))
                                        .otherwise(
                                            pl.when((pl.col("group") == "away") & (pl.col("away_team_side_second") == "left") & (pl.col("period") == 2))
                                            .then(pl.col("x_start"))
                                            .otherwise(pl.lit(None))
                                        )
                                    )
                                )
                            )
                        )
                  )
            ).alias("x_start_tracking"),
            pl.when((pl.col("group") == "home") & (pl.col("home_team_side_first") == "right") & (pl.col("period") == 1))
              .then(pl.col("x_end") * (-1))
              .otherwise(
                  pl.when((pl.col("group") == "home") & (pl.col("home_team_side_first") == "left") & (pl.col("period") == 1))
                  .then(pl.col("x_end"))
                  .otherwise(
                        pl.when((pl.col("group") == "home") & (pl.col("home_team_side_second") == "right") & (pl.col("period") == 2))
                        .then(pl.col("x_end") * (-1))
                        .otherwise(
                            pl.when((pl.col("group") == "home") & (pl.col("home_team_side_second") == "left") & (pl.col("period") == 2))
                            .then(pl.col("x_end"))
                            .otherwise(
                                pl.when((pl.col("group") == "away") & (pl.col("away_team_side_first") == "right") & (pl.col("period") == 1))
                                .then(pl.col("x_end") * (-1))
                                .otherwise(
                                    pl.when((pl.col("group") == "away") & (pl.col("away_team_side_first") == "left") & (pl.col("period") == 1))
                                    .then(pl.col("x_end"))
                                    .otherwise(
                                        pl.when((pl.col("group") == "away") & (pl.col("away_team_side_second") == "right") & (pl.col("period") == 2))
                                        .then(pl.col("x_end") * (-1))
                                        .otherwise(
                                            pl.when((pl.col("group") == "away") & (pl.col("away_team_side_second") == "left") & (pl.col("period") == 2))
                                            .then(pl.col("x_end"))
                                            .otherwise(pl.lit(None))
                                        )
                                    )
                                )
                            )
                        )
                  )
            ).alias("x_end_tracking"),
            pl.when((pl.col("group") == "home") & (pl.col("home_team_side_first") == "right") & (pl.col("period") == 1))
              .then(pl.col("y_start") * (-1))
              .otherwise(
                  pl.when((pl.col("group") == "home") & (pl.col("home_team_side_first") == "left") & (pl.col("period") == 1))
                  .then(pl.col("y_start"))
                  .otherwise(
                        pl.when((pl.col("group") == "home") & (pl.col("home_team_side_second") == "right") & (pl.col("period") == 2))
                        .then(pl.col("y_start") * (-1))
                        .otherwise(
                            pl.when((pl.col("group") == "home") & (pl.col("home_team_side_second") == "left") & (pl.col("period") == 2))
                            .then(pl.col("y_start"))
                            .otherwise(
                                pl.when((pl.col("group") == "away") & (pl.col("away_team_side_first") == "right") & (pl.col("period") == 1))
                                .then(pl.col("y_start") * (-1))
                                .otherwise(
                                    pl.when((pl.col("group") == "away") & (pl.col("away_team_side_first") == "left") & (pl.col("period") == 1))
                                    .then(pl.col("y_start"))
                                    .otherwise(
                                        pl.when((pl.col("group") == "away") & (pl.col("away_team_side_second") == "right") & (pl.col("period") == 2))
                                        .then(pl.col("y_start") * (-1))
                                        .otherwise(
                                            pl.when((pl.col("group") == "away") & (pl.col("away_team_side_second") == "left") & (pl.col("period") == 2))
                                            .then(pl.col("y_start"))
                                            .otherwise(pl.lit(None))
                                        )
                                    )
                                )
                            )
                        )
                  )
            ).alias("y_start_tracking"),
            pl.when((pl.col("group") == "home") & (pl.col("home_team_side_first") == "right") & ((pl.col("period") == 1)) )
              .then(pl.col("y_end") * (-1))
              .otherwise(
                  pl.when((pl.col("group") == "home") & (pl.col("home_team_side_first") == "left") & (pl.col("period") == 1))
                  .then(pl.col("y_end"))
                  .otherwise(
                        pl.when((pl.col("group") == "home") & (pl.col("home_team_side_second") == "right") & (pl.col("period") == 2))
                        .then(pl.col("y_end") * (-1))
                        .otherwise(
                            pl.when((pl.col("group") == "home") & (pl.col("home_team_side_second") == "left") & (pl.col("period") == 2))
                            .then(pl.col("y_end"))
                            .otherwise(
                                pl.when((pl.col("group") == "away") & (pl.col("away_team_side_first") == "right") & (pl.col("period") == 1))
                                .then(pl.col("y_end") * (-1))
                                .otherwise(
                                    pl.when((pl.col("group") == "away") & (pl.col("away_team_side_first") == "left") & (pl.col("period") == 1))
                                    .then(pl.col("y_end"))
                                    .otherwise(
                                        pl.when((pl.col("group") == "away") & (pl.col("away_team_side_second") == "right") & (pl.col("period") == 2))
                                        .then(pl.col("y_end") * (-1))
                                        .otherwise(
                                            pl.when((pl.col("group") == "away") & (pl.col("away_team_side_second") == "left") & (pl.col("period") == 2))
                                            .then(pl.col("y_end"))
                                            .otherwise(pl.lit(None))
                                        )
                                    )
                                )
                            )
                        )
                  )
            ).alias("y_end_tracking")
        )
        .select([
            "match_id", "match_name", "match_longname",
            "date_time",
            "competition_name","season_name","round_number",
            "event_id", 
            "frame_start", "frame_end", 
            "time_start", "time_end",
            "minute_start", "minute_end",
            "seconds_start", "seconds_end", 
            "period", "period_name",
            "team_id", "team_shortname", "group",
            "team_jersey_color","team_number_color",
            "event_type", "event_subtype",
            "player_id", "player_name", "player_number", "position_group", "player_position", 
            "player_in_possession_id", "player_in_possession_name", "player_in_possession_position",
            "x_start","y_start",
            "x_end","y_end",
            "channel_start", "channel_end", 
            "third_start", "third_end",
            "zone_start", "zone_end",
            "player_in_possession_zone_start", "player_in_possession_zone_end",
            "team_in_possession_phase_type", "team_out_of_possession_phase_type",
            "start_type", 
            "end_type",
            "game_state_id", "game_state",
            "associated_player_possession_event_id",
            "targeted", "received",
            "xthreat", "xpass_completion", "passing_option_score",
            "first_line_break", "second_last_line_break", "last_line_break",
            "pass_ahead",
            "speed_avg_band",
            "pressing_chain_index",
            "pressing_chain_end_type",
            "youtube_video_id", 
            "event_start_seconds", "event_end_seconds", 
            "home_team_side_first", "home_team_side_second",
            "away_team_side_first", "away_team_side_second",
            "x_start_tracking", "y_start_tracking",
            "x_end_tracking", "y_end_tracking"
        ])
    ).collect()

    tracking_view = apply_schema(tracking_view_df, "gold_tracking")
    dynamic_events_view = apply_schema(dynamic_events_view_df, "gold_dynamic_events")

    gold_path = Path(base_path / "data/delta/gold")
    gold_path.mkdir(parents=True, exist_ok=True)
    app_ext_data_path = Path(base_path.parent / "apps/dynamicSkillsFinder/inst/extdata")
    app_ext_data_path.mkdir(parents=True, exist_ok=True)

    tracking_view.write_parquet(Path(f"{gold_path}/tracking.parquet"))
    tracking_view.to_pandas().to_parquet(f"{app_ext_data_path}/tracking.parquet")

    dynamic_events_view.write_parquet(Path(f"{gold_path}/dynamic_events.parquet"))
    dynamic_events_view.to_pandas().to_parquet(f"{app_ext_data_path}/dynamic_events.parquet")

    print("Dynamic events and tracking views created!")

    # Aggregated gold tables
    now = datetime.utcnow()

    agg_player_match_df = (
        silver_player_match.select([
            "match_id", "player_id" , "team_id", "competition_edition_id",
            "minutes_played", "start_time", "position_acronym"
        ])
        .filter(pl.col("position_acronym") != "SUB")
        .with_columns(pl.when(pl.col("start_time") == "00:00:00")
                        .then(pl.lit(1))
                        .otherwise(pl.lit(0))
                        .alias("starts"))
        .group_by([
            "player_id", "team_id", "competition_edition_id"
        ])
        .agg([
            pl.col("match_id").count().alias("matches_played"),
            pl.col("minutes_played").sum().alias("minutes_played"),
            pl.col("starts").sum().alias("starts"),
            pl.col("position_acronym").unique().alias("positions_list")
        ])
        .with_columns(
            pl.col("positions_list").list.join(", ").alias("positions")
        )
        .drop("positions_list")
        .join(silver_player.select(["player_id", "short_name", "birthday"]).rename({"short_name":"player_name"}),
                on="player_id", how="left")
        .with_columns(
            age = (
                pl.lit(now.year) - pl.col("birthday").dt.year() -
                (
                    (pl.lit(now.month) < pl.col("birthday").dt.month()) |
                    ((pl.lit(now.month) == pl.col("birthday").dt.month()) & (pl.lit(now.day) < pl.col("birthday").dt.day()))
                )
            ).cast(pl.Int16)
        )
        .join(silver_team.select(["team_id","short_name"]).rename({"short_name":"team_shortname"}),
                on="team_id", how="left")
        .join(silver_competition.select(["competition_edition_id", "competition_id", "season_id", "competition_name", "season_name"]),
                on="competition_edition_id", how="left")
        .select([
            "player_id", "player_name", "birthday", "age", "team_id", "team_shortname",
            "competition_id", "competition_name", "season_id", "season_name",
            "positions", "minutes_played", "matches_played", "starts"
        ]).collect()
    )

    agg_player_dynamic_events_df = (dynamic_events_view_df
        .select(["player_id", "team_id", "competition_name", "season_name", "event_type", "event_subtype", "team_out_of_possession_phase_type", 
                 "passing_option_score", "targeted", "end_type"])
        .group_by([
            "player_id", "team_id", "competition_name", "season_name"
        ])
        .agg([
            (pl.col("event_type") == "off_ball_run").sum().alias("off_ball_runs"),
            ((pl.col("event_type") == "off_ball_run") & (pl.col("targeted"))).sum().alias("off_ball_runs_targeted"),
            (pl.col("event_subtype") == "dropping_off").sum().alias("dropping_off_runs"),
            ((pl.col("event_subtype") == "dropping_off") & (pl.col("targeted"))).sum().alias("dropping_off_runs_targeted"),
            (pl.col("event_subtype") == "coming_short").sum().alias("coming_short_runs"),
            ((pl.col("event_subtype") == "coming_short") & (pl.col("targeted"))).sum().alias("coming_short_runs_targeted"),
            (pl.col("event_subtype") == "pulling_wide").sum().alias("pulling_wide_runs"),
            ((pl.col("event_subtype") == "pulling_wide") & (pl.col("targeted"))).sum().alias("pulling_wide_runs_targeted"),
            (pl.col("event_subtype") == "pulling_half_space").sum().alias("pulling_half_space_runs"),
            ((pl.col("event_subtype") == "pulling_half_space") & (pl.col("targeted"))).sum().alias("pulling_half_space_runs_targeted"),
            (pl.col("event_subtype") == "support").sum().alias("support_runs"),
            ((pl.col("event_subtype") == "support") & (pl.col("targeted"))).sum().alias("support_runs_targeted"),
            (pl.col("event_subtype") == "run_ahead_of_the_ball").sum().alias("run_ahead_of_the_ball_runs"),
            ((pl.col("event_subtype") == "run_ahead_of_the_ball") & (pl.col("targeted"))).sum().alias("run_ahead_of_the_ball_runs_targeted"),
            (pl.col("event_subtype") == "overlap").sum().alias("overlap_runs"),
            ((pl.col("event_subtype") == "overlap") & (pl.col("targeted"))).sum().alias("overlap_runs_targeted"),
            (pl.col("event_subtype") == "underlap").sum().alias("underlap_runs"),
            ((pl.col("event_subtype") == "underlap") & (pl.col("targeted"))).sum().alias("underlap_runs_targeted"),
            (pl.col("event_subtype") == "behind").sum().alias("behind_runs"),
            ((pl.col("event_subtype") == "behind") & (pl.col("targeted"))).sum().alias("behind_runs_targeted"),
            (pl.col("event_subtype") == "cross_receiver").sum().alias("cross_receiver_runs"),
            ((pl.col("event_subtype") == "cross_receiver") & (pl.col("targeted"))).sum().alias("cross_receiver_runs_targeted"),
            (pl.col("event_type") == "on_ball_engagement").sum().alias("on_ball_engagements"),
            (pl.col("event_subtype") == "pressure").sum().alias("pressures"),
            (pl.col("event_subtype") == "recovery_press").sum().alias("recovery_pressures"),
            (pl.col("event_subtype") == "counter_press").sum().alias("counter_pressures"),
            ((pl.col("event_type") == "on_ball_engagement")
                & (pl.col("end_type") == "direct_regain")).sum().alias("on_ball_engagement_recoveries"),
            ((pl.col("event_subtype") == "pressure") 
                & (pl.col("end_type") == "direct_regain")).sum().alias("pressure_recoveries"),
            ((pl.col("event_subtype") == "recovery_press")
                & (pl.col("end_type") == "direct_regain")).sum().alias("recovery_pressure_recoveries"),
            ((pl.col("event_subtype") == "counter_press")
                & (pl.col("end_type") == "direct_regain")).sum().alias("counter_pressure_recoveries"),
            ((pl.col("event_type") == "on_ball_engagement") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("on_ball_engagements_high"),
            ((pl.col("event_type") == "on_ball_engagement")
                & (pl.col("end_type") == "direct_regain") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("on_ball_engagement_high_recoveries"),
            ((pl.col("event_subtype") == "pressure") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("pressures_high"),
            ((pl.col("event_subtype") == "pressure")
                & (pl.col("end_type") == "direct_regain") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("pressure_high_recoveries"),
            ((pl.col("event_subtype") == "recovery_press") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("recovery_pressures_high"),
            ((pl.col("event_subtype") == "recovery_press")
                & (pl.col("end_type") == "direct_regain") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("recovery_pressure_high_recoveries"),
            ((pl.col("event_subtype") == "counter_press") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("counter_pressures_high"),
            ((pl.col("event_subtype") == "counter_press")
                & (pl.col("end_type") == "direct_regain") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("counter_pressure_high_recoveries"),
            pl.col("passing_option_score").mean().round(2).alias("passing_option_score_avg"),
        ])
    )

    agg_player_df = (agg_player_match_df
        .join(agg_player_dynamic_events_df, on=["player_id", "team_id", "competition_name", "season_name"], how="left")
        .with_columns(
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("off_ball_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("off_ball_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("off_ball_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("off_ball_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("dropping_off_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("dropping_off_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("dropping_off_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("dropping_off_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("coming_short_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("coming_short_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("coming_short_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("coming_short_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_wide_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("pulling_wide_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_wide_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("pulling_wide_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_half_space_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("pulling_half_space_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_half_space_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("pulling_half_space_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("support_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("support_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("support_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("support_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("run_ahead_of_the_ball_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("run_ahead_of_the_ball_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("run_ahead_of_the_ball_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("run_ahead_of_the_ball_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("overlap_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("overlap_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("overlap_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("overlap_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("underlap_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("underlap_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("underlap_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("underlap_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("behind_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("behind_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("behind_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("behind_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("cross_receiver_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("cross_receiver_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("cross_receiver_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("cross_receiver_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagements") / pl.col("minutes_played") * 90))
            ).round(2).alias("on_ball_engagements_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagement_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("on_ball_engagement_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressures") / pl.col("minutes_played") * 90))
            ).round(2).alias("pressures_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressure_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("pressure_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressures") / pl.col("minutes_played") * 90))
            ).round(2).alias("recovery_pressures_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressure_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("recovery_pressure_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressures") / pl.col("minutes_played") * 90))
            ).round(2).alias("counter_pressures_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressure_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("counter_pressure_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagements_high") / pl.col("minutes_played") * 90))
            ).round(2).alias("on_ball_engagements_high_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagement_high_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("on_ball_engagement_high_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressures_high") / pl.col("minutes_played") * 90))
            ).round(2).alias("pressures_high_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressure_high_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("pressure_high_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressures_high") / pl.col("minutes_played") * 90))
            ).round(2).alias("recovery_pressures_high_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressure_high_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("recovery_pressure_high_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressures_high") / pl.col("minutes_played") * 90))
            ).round(2).alias("counter_pressures_high_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressure_high_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("counter_pressure_high_recoveries_90"),
        )
        .with_columns(
            (pl.when(pl.col("off_ball_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("off_ball_runs_targeted") / pl.col("off_ball_runs")) * 100)
            ).round(2).alias("off_ball_runs_targeted_pct"),
            (pl.when(pl.col("dropping_off_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("dropping_off_runs_targeted") / pl.col("dropping_off_runs")) * 100)
            ).round(2).alias("dropping_off_runs_targeted_pct"),
            (pl.when(pl.col("coming_short_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("coming_short_runs_targeted") / pl.col("coming_short_runs")) * 100)
            ).round(2).alias("coming_short_runs_targeted_pct"),
            (pl.when(pl.col("pulling_wide_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_wide_runs_targeted") / pl.col("pulling_wide_runs")) * 100)
            ).round(2).alias("pulling_wide_runs_targeted_pct"),
            (pl.when(pl.col("pulling_half_space_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_half_space_runs_targeted") / pl.col("pulling_half_space_runs")) * 100)
            ).round(2).alias("pulling_half_space_runs_targeted_pct"),
            (pl.when(pl.col("support_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("support_runs_targeted") / pl.col("support_runs")) * 100)
            ).round(2).alias("support_runs_targeted_pct"),
            (pl.when(pl.col("run_ahead_of_the_ball_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("run_ahead_of_the_ball_runs_targeted") / pl.col("run_ahead_of_the_ball_runs")) * 100)
            ).round(2).alias("run_ahead_of_the_ball_runs_targeted_pct"),
            (pl.when(pl.col("overlap_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("overlap_runs_targeted") / pl.col("overlap_runs")) * 100)
            ).round(2).alias("overlap_runs_targeted_pct"),
            (pl.when(pl.col("underlap_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("underlap_runs_targeted") / pl.col("underlap_runs")) * 100)
            ).round(2).alias("underlap_runs_targeted_pct"),
            (pl.when(pl.col("behind_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("behind_runs_targeted") / pl.col("behind_runs")) * 100)
            ).round(2).alias("behind_runs_targeted_pct"),
            (pl.when(pl.col("cross_receiver_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("cross_receiver_runs_targeted") / pl.col("cross_receiver_runs")) * 100)
            ).round(2).alias("cross_receiver_runs_targeted_pct"),
            (pl.when(pl.col("on_ball_engagements") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagement_recoveries") / pl.col("on_ball_engagements")) * 100)
            ).round(2).alias("on_ball_engagement_recoveries_pct"),
            (pl.when(pl.col("pressures") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressure_recoveries") / pl.col("pressures")) * 100)
            ).round(2).alias("pressure_recoveries_pct"),
            (pl.when(pl.col("recovery_pressures") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressure_recoveries") / pl.col("recovery_pressures")) * 100)
            ).round(2).alias("recovery_pressure_recoveries_pct"),
            (pl.when(pl.col("counter_pressures") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressure_recoveries") / pl.col("counter_pressures")) * 100)
            ).round(2).alias("counter_pressure_recoveries_pct"),
            (pl.when(pl.col("on_ball_engagements_high") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagement_high_recoveries") / pl.col("on_ball_engagements_high")) * 100)
            ).round(2).alias("on_ball_engagement_high_recoveries_pct"),
            (pl.when(pl.col("pressures_high") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressure_high_recoveries") / pl.col("pressures_high")) * 100)
            ).round(2).alias("pressure_high_recoveries_pct"),
            (pl.when(pl.col("recovery_pressures_high") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressure_high_recoveries") / pl.col("recovery_pressures_high")) * 100)
            ).round(2).alias("recovery_pressure_high_recoveries_pct"),
            (pl.when(pl.col("counter_pressures_high") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressure_high_recoveries") / pl.col("counter_pressures_high")) * 100)
            ).round(2).alias("counter_pressure_high_recoveries_pct")
        )
    ).fill_nan(pl.lit(0.0)).fill_null(pl.lit(0.0))

    agg_player_in_possession_events_df = (dynamic_events_view_df
        .select(["player_in_possession_id", "team_id", "competition_name", "season_name", "event_type", "event_subtype", "team_out_of_possession_phase_type", 
                 "passing_option_score", "targeted", "received", "end_type", "xthreat", "xpass_completion","first_line_break", "second_last_line_break", "last_line_break",
                 "pass_ahead"
                ])
        .group_by([
             "player_in_possession_id",  "team_id", "competition_name", "season_name"
        ])
        .agg([
            ((pl.col("targeted")) & (pl.col("event_type") == "passing_option")).sum().alias("passes"),
            ((pl.col("received")) & (pl.col("event_type") == "passing_option")).sum().alias("passes_completed"),
            pl.col("xpass_completion").filter((pl.col("targeted")) & (pl.col("event_type") == "passing_option")).mean().round(2).alias("xpass_completion_avg"),
            pl.col("xpass_completion").filter((pl.col("received")) & (pl.col("event_type") == "passing_option")).mean().round(2).alias("xpass_completion_completed_avg"),
            pl.col("xthreat").filter((pl.col("received")) & (pl.col("event_type") == "passing_option")).sum().round(2).alias("xthreat"),
            pl.col("xthreat").filter((pl.col("received")) & (pl.col("event_type") == "passing_option")).mean().round(2).alias("xthreat_avg"),
            ((pl.col("targeted")) & (pl.col("event_type") == "passing_option") & ((pl.col("first_line_break")) | (pl.col("second_last_line_break")) | (pl.col("last_line_break")))).sum().alias("line_breaking_passes"),
            ((pl.col("received")) & (pl.col("event_type") == "passing_option") & ((pl.col("first_line_break")) | (pl.col("second_last_line_break")) | (pl.col("last_line_break")))).sum().alias("line_breaking_passes_completed"),
            ((pl.col("targeted")) & (pl.col("event_type") == "passing_option") & (pl.col("first_line_break"))).sum().alias("first_line_breaking_passes"),
            ((pl.col("targeted")) & (pl.col("event_type") == "passing_option") & (pl.col("second_last_line_break"))).sum().alias("second_last_line_breaking_passes"),
            ((pl.col("targeted")) & (pl.col("event_type") == "passing_option") & (pl.col("last_line_break"))).sum().alias("last_line_breaking_passes"),
            ((pl.col("received")) & (pl.col("event_type") == "passing_option") & (pl.col("first_line_break"))).sum().alias("first_line_breaking_passes_completed"),
            ((pl.col("received")) & (pl.col("event_type") == "passing_option") & (pl.col("second_last_line_break"))).sum().alias("second_last_line_breaking_passes_completed"),
            ((pl.col("received")) & (pl.col("event_type") == "passing_option") & (pl.col("last_line_break"))).sum().alias("last_line_breaking_passes_completed"),
            ((pl.col("targeted")) & (pl.col("event_type") == "passing_option") & (pl.col("pass_ahead"))).sum().alias("ahead_passes"),
            ((pl.col("received")) & (pl.col("event_type") == "passing_option") & (pl.col("pass_ahead"))).sum().alias("ahead_passes_completed"),
        ])
        .with_columns(
            (pl.when(pl.col("passes") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("passes_completed") / pl.col("passes")) * 100)
            ).round(2).alias("pass_completion_pct")
        )
        .rename({"player_in_possession_id":"player_id"})
        .select([
            "player_id", "team_id", "competition_name", "season_name", "passes", "passes_completed", "pass_completion_pct", "xpass_completion_avg", 
            "xpass_completion_completed_avg", "xthreat", "xthreat_avg", "line_breaking_passes", "line_breaking_passes_completed",
            "first_line_breaking_passes", "second_last_line_breaking_passes", "last_line_breaking_passes",
            "first_line_breaking_passes_completed", "second_last_line_breaking_passes_completed", "last_line_breaking_passes_completed",
            "ahead_passes", "ahead_passes_completed"
        ])
        .join(agg_player_match_df, on=["player_id", "team_id", "competition_name", "season_name"], how="left")
        .with_columns(
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("line_breaking_passes") / pl.col("minutes_played") * 90))
            ).round(2).alias("line_breaking_passes_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("line_breaking_passes_completed") / pl.col("minutes_played") * 90))
            ).round(2).alias("line_breaking_passes_completed_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("first_line_breaking_passes") / pl.col("minutes_played") * 90))
            ).round(2).alias("first_line_breaking_passes_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("second_last_line_breaking_passes") / pl.col("minutes_played") * 90))
            ).round(2).alias("second_last_line_breaking_passes_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("last_line_breaking_passes") / pl.col("minutes_played") * 90))
            ).round(2).alias("last_line_breaking_passes_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("first_line_breaking_passes_completed") / pl.col("minutes_played") * 90))
            ).round(2).alias("first_line_breaking_passes_completed_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("second_last_line_breaking_passes_completed") / pl.col("minutes_played") * 90))
            ).round(2).alias("second_last_line_breaking_passes_completed_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("last_line_breaking_passes_completed") / pl.col("minutes_played") * 90))
            ).round(2).alias("last_line_breaking_passes_completed_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("passes") / pl.col("minutes_played") * 90))
            ).round(2).alias("passes_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("passes_completed") / pl.col("minutes_played") * 90))
            ).round(2).alias("passes_completed_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("ahead_passes") / pl.col("minutes_played") * 90))
            ).round(2).alias("ahead_passes_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("ahead_passes_completed") / pl.col("minutes_played") * 90))
            ).round(2).alias("ahead_passes_completed_90")
        )
    ).fill_nan(pl.lit(0.0)).fill_null(pl.lit(0.0))

    agg_player_df = agg_player_df.join(
        agg_player_in_possession_events_df,
        on=["player_id", "team_id", "competition_name", "season_name"],
        how="left"
    )

    agg_player = apply_schema(agg_player_df, "gold_player_aggregates")
    agg_player.write_parquet(Path(f"{gold_path}/agg_player.parquet"))
    agg_player.to_pandas().to_parquet(f"{app_ext_data_path}/agg_player.parquet")

    print("Aggregated player table created!")

    agg_team_match_df = (
        pl.concat([
            silver_match.select(
                team_id=pl.col("home_team_id"),
                competition_edition_id=pl.col("competition_edition_id"),
                first_period_duration_minutes=pl.col("first_period_duration_minutes"),
                second_period_duration_minutes=pl.col("second_period_duration_minutes")
            ),
            silver_match.select(
                team_id = pl.col("away_team_id"),
                competition_edition_id = pl.col("competition_edition_id"),
                first_period_duration_minutes = pl.col("first_period_duration_minutes"),
                second_period_duration_minutes = pl.col("second_period_duration_minutes")
            )
        ])
        .with_columns((pl.col("first_period_duration_minutes") + pl.col("second_period_duration_minutes")).alias("total_match_minutes"))
        .group_by(["team_id", "competition_edition_id"])
        .agg(
            pl.sum("total_match_minutes").alias("minutes_played"),
            pl.len().alias("matches_played")
        )
        .join(silver_competition.select(["competition_edition_id", "competition_id", "season_id", "competition_name", "season_name"]),
            on="competition_edition_id", how="left")
        .join(silver_team.select(["team_id","short_name"]).rename({"short_name":"team_shortname"}),
            on="team_id", how="left")
        .select([
            "team_id", "team_shortname", "competition_id", "competition_name", "season_id", "season_name", "minutes_played", "matches_played"
        ]).collect()
    )

    agg_team_dynamic_events_df = (dynamic_events_view_df
        .select(["team_id", "competition_name", "season_name", "event_type", "event_subtype", "x_end", "team_out_of_possession_phase_type",
                 "targeted", "end_type"])
        .group_by([
            "team_id", "competition_name", "season_name"
        ])
        .agg([
            (pl.col("event_type") == "off_ball_run").sum().alias("off_ball_runs"),
            ((pl.col("event_type") == "off_ball_run") & (pl.col("targeted"))).sum().alias("off_ball_runs_targeted"),
            (pl.col("event_subtype") == "dropping_off").sum().alias("dropping_off_runs"),
            ((pl.col("event_subtype") == "dropping_off") & (pl.col("targeted"))).sum().alias("dropping_off_runs_targeted"),
            (pl.col("event_subtype") == "coming_short").sum().alias("coming_short_runs"),
            ((pl.col("event_subtype") == "coming_short") & (pl.col("targeted"))).sum().alias("coming_short_runs_targeted"),
            (pl.col("event_subtype") == "pulling_wide").sum().alias("pulling_wide_runs"),
            ((pl.col("event_subtype") == "pulling_wide") & (pl.col("targeted"))).sum().alias("pulling_wide_runs_targeted"),
            (pl.col("event_subtype") == "pulling_half_space").sum().alias("pulling_half_space_runs"),
            ((pl.col("event_subtype") == "pulling_half_space") & (pl.col("targeted"))).sum().alias("pulling_half_space_runs_targeted"),
            (pl.col("event_subtype") == "support").sum().alias("support_runs"),
            ((pl.col("event_subtype") == "support") & (pl.col("targeted"))).sum().alias("support_runs_targeted"),
            (pl.col("event_subtype") == "run_ahead_of_the_ball").sum().alias("run_ahead_of_the_ball_runs"),
            ((pl.col("event_subtype") == "run_ahead_of_the_ball") & (pl.col("targeted"))).sum().alias("run_ahead_of_the_ball_runs_targeted"),
            (pl.col("event_subtype") == "overlap").sum().alias("overlap_runs"),
            ((pl.col("event_subtype") == "overlap") & (pl.col("targeted"))).sum().alias("overlap_runs_targeted"),
            (pl.col("event_subtype") == "underlap").sum().alias("underlap_runs"),
            ((pl.col("event_subtype") == "underlap") & (pl.col("targeted"))).sum().alias("underlap_runs_targeted"),
            (pl.col("event_subtype") == "behind").sum().alias("behind_runs"),
            ((pl.col("event_subtype") == "behind") & (pl.col("targeted"))).sum().alias("behind_runs_targeted"),
            (pl.col("event_subtype") == "cross_receiver").sum().alias("cross_receiver_runs"),
            ((pl.col("event_subtype") == "cross_receiver") & (pl.col("targeted"))).sum().alias("cross_receiver_runs_targeted"),
            (pl.col("event_type") == "on_ball_engagement").sum().alias("on_ball_engagements"),
            (pl.col("event_subtype") == "pressure").sum().alias("pressures"),
            (pl.col("event_subtype") == "recovery_press").sum().alias("recovery_pressures"),
            (pl.col("event_subtype") == "counter_press").sum().alias("counter_pressures"),
            ((pl.col("event_type") == "on_ball_engagement")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"]))).sum().alias("on_ball_engagement_recoveries"),
            ((pl.col("event_subtype") == "pressure") 
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"]))).sum().alias("pressure_recoveries"),
            ((pl.col("event_subtype") == "recovery_press")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"]))).sum().alias("recovery_pressure_recoveries"),
            ((pl.col("event_subtype") == "counter_press")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"]))).sum().alias("counter_pressure_recoveries"),
            ((pl.col("event_type") == "on_ball_engagement") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("on_ball_engagements_high"),
            ((pl.col("event_type") == "on_ball_engagement")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"])) 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("on_ball_engagement_high_recoveries"),
            ((pl.col("event_subtype") == "pressure") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("pressures_high"),
            ((pl.col("event_subtype") == "pressure")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"])) 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("pressure_high_recoveries"),
            ((pl.col("event_subtype") == "recovery_press") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("recovery_pressures_high"),
            ((pl.col("event_subtype") == "recovery_press")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"])) 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("recovery_pressure_high_recoveries"),
            ((pl.col("event_subtype") == "counter_press") 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("counter_pressures_high"),
            ((pl.col("event_subtype") == "counter_press")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"])) 
                & (pl.col("team_out_of_possession_phase_type") == "high_block")).sum().alias("counter_pressure_high_recoveries"),
        ])
    )

    agg_team_df = (agg_team_match_df
        .join(agg_team_dynamic_events_df, on=["team_id", "competition_name", "season_name"], how="left")
        .with_columns(
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("off_ball_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("off_ball_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("off_ball_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("off_ball_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("dropping_off_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("dropping_off_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("dropping_off_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("dropping_off_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("coming_short_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("coming_short_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("coming_short_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("coming_short_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_wide_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("pulling_wide_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_wide_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("pulling_wide_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_half_space_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("pulling_half_space_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_half_space_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("pulling_half_space_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("support_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("support_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("support_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("support_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("run_ahead_of_the_ball_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("run_ahead_of_the_ball_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("run_ahead_of_the_ball_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("run_ahead_of_the_ball_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("overlap_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("overlap_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("overlap_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("overlap_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("underlap_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("underlap_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("underlap_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("underlap_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("behind_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("behind_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("behind_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("behind_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("cross_receiver_runs") / pl.col("minutes_played") * 90))
            ).round(2).alias("cross_receiver_runs_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("cross_receiver_runs_targeted") / pl.col("minutes_played") * 90))
            ).round(2).alias("cross_receiver_runs_targeted_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagements") / pl.col("minutes_played") * 90))
            ).round(2).alias("on_ball_engagements_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagement_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("on_ball_engagement_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressures") / pl.col("minutes_played") * 90))
            ).round(2).alias("pressures_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressure_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("pressure_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressures") / pl.col("minutes_played") * 90))
            ).round(2).alias("recovery_pressures_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressure_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("recovery_pressure_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressures") / pl.col("minutes_played") * 90))
            ).round(2).alias("counter_pressures_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressure_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("counter_pressure_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagements_high") / pl.col("minutes_played") * 90))
            ).round(2).alias("on_ball_engagements_high_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagement_high_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("on_ball_engagement_high_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressures_high") / pl.col("minutes_played") * 90))
            ).round(2).alias("pressures_high_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressure_high_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("pressure_high_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressures_high") / pl.col("minutes_played") * 90))
            ).round(2).alias("recovery_pressures_high_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressure_high_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("recovery_pressure_high_recoveries_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressures_high") / pl.col("minutes_played") * 90))
            ).round(2).alias("counter_pressures_high_90"),
            (pl.when(pl.col("minutes_played") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressure_high_recoveries") / pl.col("minutes_played") * 90))
            ).round(2).alias("counter_pressure_high_recoveries_90"),
        )
        .with_columns(
            (pl.when(pl.col("off_ball_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("off_ball_runs_targeted") / pl.col("off_ball_runs")) * 100)
            ).round(2).alias("off_ball_runs_targeted_pct"),
            (pl.when(pl.col("dropping_off_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("dropping_off_runs_targeted") / pl.col("dropping_off_runs")) * 100)
            ).round(2).alias("dropping_off_runs_targeted_pct"),
            (pl.when(pl.col("coming_short_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("coming_short_runs_targeted") / pl.col("coming_short_runs")) * 100)
            ).round(2).alias("coming_short_runs_targeted_pct"),
            (pl.when(pl.col("pulling_wide_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_wide_runs_targeted") / pl.col("pulling_wide_runs")) * 100)
            ).round(2).alias("pulling_wide_runs_targeted_pct"),
            (pl.when(pl.col("pulling_half_space_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pulling_half_space_runs_targeted") / pl.col("pulling_half_space_runs")) * 100)
            ).round(2).alias("pulling_half_space_runs_targeted_pct"),
            (pl.when(pl.col("support_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("support_runs_targeted") / pl.col("support_runs")) * 100)
            ).round(2).alias("support_runs_targeted_pct"),
            (pl.when(pl.col("run_ahead_of_the_ball_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("run_ahead_of_the_ball_runs_targeted") / pl.col("run_ahead_of_the_ball_runs")) * 100)
            ).round(2).alias("run_ahead_of_the_ball_runs_targeted_pct"),
            (pl.when(pl.col("overlap_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("overlap_runs_targeted") / pl.col("overlap_runs")) * 100)
            ).round(2).alias("overlap_runs_targeted_pct"),
            (pl.when(pl.col("underlap_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("underlap_runs_targeted") / pl.col("underlap_runs")) * 100)
            ).round(2).alias("underlap_runs_targeted_pct"),
            (pl.when(pl.col("behind_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("behind_runs_targeted") / pl.col("behind_runs")) * 100)
            ).round(2).alias("behind_runs_targeted_pct"),
            (pl.when(pl.col("cross_receiver_runs") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("cross_receiver_runs_targeted") / pl.col("cross_receiver_runs")) * 100)
            ).round(2).alias("cross_receiver_runs_targeted_pct"),
            (pl.when(pl.col("on_ball_engagements") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagement_recoveries") / pl.col("on_ball_engagements")) * 100)
            ).round(2).alias("on_ball_engagement_recoveries_pct"),
            (pl.when(pl.col("pressures") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressure_recoveries") / pl.col("pressures")) * 100)
            ).round(2).alias("pressure_recoveries_pct"),
            (pl.when(pl.col("recovery_pressures") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressure_recoveries") / pl.col("recovery_pressures")) * 100)
            ).round(2).alias("recovery_pressure_recoveries_pct"),
            (pl.when(pl.col("counter_pressures") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressure_recoveries") / pl.col("counter_pressures")) * 100)
            ).round(2).alias("counter_pressure_recoveries_pct"),
            (pl.when(pl.col("on_ball_engagements_high") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("on_ball_engagement_recoveries") / pl.col("on_ball_engagements_high")) * 100)
            ).round(2).alias("on_ball_engagement_high_recoveries_pct"),
            (pl.when(pl.col("pressures_high") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("pressure_high_recoveries") / pl.col("pressures_high")) * 100)
            ).round(2).alias("pressure_high_recoveries_pct"),
            (pl.when(pl.col("recovery_pressures_high") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("recovery_pressure_high_recoveries") / pl.col("recovery_pressures_high")) * 100)
            ).round(2).alias("recovery_pressure_high_recoveries_pct"),
            (pl.when(pl.col("counter_pressures_high") == 0)
                .then(pl.lit(0.0))
                .otherwise((pl.col("counter_pressure_high_recoveries") / pl.col("counter_pressures_high")) * 100)
            ).round(2).alias("counter_pressure_high_recoveries_pct")
        )
    ).fill_nan(pl.lit(0.0)).fill_null(pl.lit(0.0))

    agg_team_lines_recoveries_df = (dynamic_events_view_df
        .select(["team_id", "competition_name", "season_name", "position_group", "event_type", "x_end", "end_type"])
        .group_by([
            "team_id", "competition_name", "season_name", "position_group"
        ])
        .agg([
            (pl.col("x_end").filter((pl.col("event_type") == "on_ball_engagement")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"]))
                & (pl.col("position_group").is_in(["Full Back","Central Defender"])))).mean().round(2).alias("defense_recovery_height_avg"),
            (pl.col("x_end").filter((pl.col("event_type") == "on_ball_engagement")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"]))
                & (pl.col("position_group") == "Midfield"))).mean().round(2).alias("midfield_recovery_height_avg"),
            (pl.col("x_end").filter((pl.col("event_type") == "on_ball_engagement")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"]))
                & (pl.col("position_group").is_in(["Center Forward","Wide Attacker"])))).mean().round(2).alias("attack_recovery_height_avg"),
            ((pl.col("event_type") == "on_ball_engagement")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"]))
                & (pl.col("position_group").is_in(["Full Back","Central Defender"]))).sum().alias("defense_recoveries"),
            ((pl.col("event_type") == "on_ball_engagement")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"]))
                & (pl.col("position_group") == "Midfield")).sum().alias("midfield_recoveries"),
            ((pl.col("event_type") == "on_ball_engagement")
                & (pl.col("end_type").is_in(["direct_regain", "indirect_regain"]))
                & (pl.col("position_group").is_in(["Center Forward","Wide Attacker"]))).sum().alias("attack_recoveries"),
        ])
    )
    
    agg_team_df = agg_team_df.join(
        agg_team_lines_recoveries_df,
        on=["team_id", "competition_name", "season_name"],
        how="left"
    )

    agg_team = apply_schema(agg_team_df, "gold_team_aggregates")
    agg_team.write_parquet(Path(f"{gold_path}/agg_team.parquet"))
    agg_team.to_pandas().to_parquet(f"{app_ext_data_path}/agg_team.parquet")

    print("Aggregated team table created!")

    print("Gold layer build completed!")

if __name__ == "__main__":
    main()