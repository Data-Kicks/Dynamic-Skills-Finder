'''
This module defines the schemas for the Bronze, Silver, and Gold layers
of a data pipeline using Polars and PyArrow. It includes functions to convert
Polars data types to PyArrow data types and to retrieve the schemas in
PyArrow format.
'''

import polars as pl
import pyarrow as pa


# -------------------- SCHEMAS --------------------

## -------------------- BRONZE --------------------
bronze_schemas = {
    "bronze_match_raw": {
        "match_id": pl.Int64,
        "json": pl.Utf8,
    },
    "bronze_tracking_raw": {
        "match_id": pl.Int64,
        "json": pl.Utf8,
    },
    "bronze_match_video_info": {
        "match_id": pl.Int64,
        "youtube_video_id": pl.Utf8,
        "first_period_start": pl.Int32,
        "second_period_start": pl.Int32,
    }
}

## -------------------- SILVER --------------------
silver_schemas = {
    ### -------------------- DIMENSIONS --------------------
    "dim_match": {
        "match_id": pl.Int64,            
        "home_team_score": pl.Int32,
        "away_team_score": pl.Int32,
        "home_team_side_first": pl.Utf8,
        "home_team_side_second": pl.Utf8,
        "away_team_side_first": pl.Utf8,
        "away_team_side_second": pl.Utf8,
        "date_time": pl.Datetime("us"),
        "stadium_id": pl.Int32,          
        "home_team_id": pl.Int32,        
        "away_team_id": pl.Int32,        
        "team_homekit_id": pl.Int32,  
        "team_awaykit_id": pl.Int32,  
        "home_team_coach_id": pl.Int32,
        "away_team_coach_id": pl.Int32,
        "home_team_playing_minutes_tip": pl.Float32,
        "away_team_playing_minutes_tip": pl.Float32,
        "home_team_playing_minutes_otip": pl.Float32,
        "away_team_playing_minutes_otip": pl.Float32,
        "first_period_duration_minutes": pl.Float32,
        "second_period_duration_minutes": pl.Float32,
        "competition_edition_id": pl.Int32,           
        "competition_id": pl.Int32,
        "season_id": pl.Int32,
        "round_number": pl.Int32,
        "youtube_video_id": pl.Utf8,
        "first_period_start": pl.Int32,
        "second_period_start": pl.Int32,
    },

    "dim_player": {
        "player_id": pl.Int32,            
        "team_id": pl.Int32,              
        "first_name": pl.Utf8,
        "last_name": pl.Utf8,
        "short_name": pl.Utf8,
        "birthday": pl.Date,
        "gender": pl.Utf8,
    },

    "dim_team": {
        "team_id": pl.Int32,      
        "name": pl.Utf8,
        "short_name": pl.Utf8,
        "acronym": pl.Utf8,
    },

    "dim_competition": {
        "competition_edition_id": pl.Int32,  
        "competition_id": pl.Int32,
        "competition_name": pl.Utf8,
        "area": pl.Utf8,
        "name": pl.Utf8,
        "gender": pl.Utf8,
        "age_group": pl.Utf8,
        "season_id": pl.Int32,
        "season_start_year": pl.Utf8,
        "season_end_year": pl.Utf8,
        "season_name": pl.Utf8,
    },

    "dim_team_kit": {
        "team_kit_id": pl.Int32,  
        "jersey_color": pl.Utf8,
        "number_color": pl.Utf8,
    },

    ### -------------------- FACTS --------------------
    "fact_player_match": {
        "match_id": pl.Int64,     
        "player_id": pl.Int32,    
        "team_id": pl.Int32,      
        "competition_edition_id": pl.Int32,  
        "competition_id": pl.Int32,
        "season_id": pl.Int32,
        "number": pl.Int16,
        "minutes_played": pl.Float32,
        "start_time": pl.Utf8,
        "end_time": pl.Utf8,
        "player_role_id": pl.Int32,      
        "position_group": pl.Utf8,
        "position_acronym": pl.Utf8,
        "yellow_card": pl.Int32,
        "red_card": pl.Int32,
        "goal": pl.Int32,
        "own_goal": pl.Int32,
        "injured": pl.Boolean,
    },

    "fact_tracking": {
        "match_id": pl.Int64,     
        "frame": pl.Int32,        
        "timestamp": pl.Utf8,
        "period": pl.Int32,
        "object_id": pl.Int32,    
        "x": pl.Float32,
        "y": pl.Float32,
        "z": pl.Float32,
        "group": pl.Utf8,
        "has_possession": pl.Boolean,
        "is_detected": pl.Boolean,
    },

    "fact_dynamic_events": {
        "match_id": pl.Int64,     
        "event_id": pl.Utf8,      
        "frame_start": pl.Int32, 
        "frame_end": pl.Int32, 
        "time_start": pl.Utf8, 
        "time_end": pl.Utf8, 
        "period": pl.Int32, 
        "team_id": pl.Int32,      
        "team_shortname": pl.Utf8,
        "event_type": pl.Utf8, 
        "event_subtype": pl.Utf8,
        "player_id": pl.Int32, 
        "player_name": pl.Utf8, 
        "player_position": pl.Utf8, 
        "player_in_possession_id": pl.Int32, 
        "player_in_possession_name": pl.Utf8, 
        "player_in_possession_position": pl.Utf8,
        "x_start": pl.Float32,
        "y_start": pl.Float32,
        "x_end": pl.Float32,
        "y_end": pl.Float32,
        "player_in_possession_x_start": pl.Float32,
        "player_in_possession_y_start": pl.Float32,
        "player_in_possession_x_end": pl.Float32,
        "player_in_possession_y_end": pl.Float32,
        "channel_start": pl.Utf8, 
        "third_start": pl.Utf8, 
        "channel_end": pl.Utf8, 
        "third_end": pl.Utf8,
        "team_in_possession_phase_type": pl.Utf8, 
        "team_out_of_possession_phase_type": pl.Utf8,
        "start_type": pl.Utf8, 
        "end_type": pl.Utf8,
        "game_state_id": pl.Int32, 
        "game_state": pl.Utf8,
        "associated_player_possession_event_id": pl.Utf8,
        "targeted": pl.Boolean, 
        "received": pl.Boolean,
        "xthreat": pl.Float32, 
        "xpass_completion": pl.Float32, 
        "passing_option_score": pl.Float32,
        "speed_avg_band": pl.Utf8,
        "pressing_chain_index": pl.Int32,
        "pressing_chain_end_type": pl.Utf8,
        "first_line_break": pl.Boolean,
        "second_last_line_break": pl.Boolean,
        "last_line_break": pl.Boolean,
        "pass_ahead": pl.Boolean,
        "minute_start": pl.Int16, 
        "minute_end": pl.Int16,
        "seconds_start": pl.Int32, 
        "seconds_end": pl.Int32, 
        "zone_start": pl.Utf8,
        "zone_end": pl.Utf8,
        "player_in_possession_zone_start": pl.Utf8,
        "player_in_possession_zone_end": pl.Utf8,
    },
}

## -------------------- GOLD --------------------
gold_schemas = {
    "gold_tracking": {
        "match_id": pl.Int64,
        "date_time": pl.Datetime("us"),
        "frame": pl.Int32,
        "timestamp": pl.Utf8,
        "competition_name": pl.Utf8,
        "season_name": pl.Utf8,
        "round_number": pl.Int32,
        "period": pl.Int32,
        "object_id": pl.Int32,
        "player_id": pl.Int32,
        "player_name": pl.Utf8,
        "player_number": pl.Int16,
        "team_id": pl.Int32,
        "team_shortname": pl.Utf8,
        "group": pl.Utf8,
        "position_acronym": pl.Utf8,
        "x": pl.Float32,
        "y": pl.Float32,
        "z": pl.Float32,
        "has_possession": pl.Boolean,
        "team_jersey_color": pl.Utf8,
        "team_number_color": pl.Utf8,
    },

    "gold_dynamic_events": {
        "match_id": pl.Int64,
        "match_name": pl.Utf8,
        "match_longname": pl.Utf8,
        "date_time": pl.Datetime("us"),
        "competition_name": pl.Utf8,
        "season_name": pl.Utf8,
        "round_number": pl.Int32,
        "event_id": pl.Utf8,
        "frame_start": pl.Int32, 
        "frame_end": pl.Int32, 
        "time_start": pl.Utf8, 
        "time_end": pl.Utf8,
        "minute_start": pl.Int16, 
        "minute_end": pl.Int16,
        "seconds_start": pl.Int32, 
        "seconds_end": pl.Int32, 
        "period": pl.Int32, 
        "period_name": pl.Utf8,
        "team_id": pl.Int32, 
        "team_shortname": pl.Utf8,
        "group": pl.Utf8,
        "team_jersey_color": pl.Utf8,
        "team_number_color": pl.Utf8,
        "event_type": pl.Utf8, 
        "event_subtype": pl.Utf8,
        "player_id": pl.Int32, 
        "player_name": pl.Utf8, 
        "player_number": pl.Int16,
        "position_group": pl.Utf8, 
        "player_position": pl.Utf8, 
        "player_in_possession_id": pl.Int32, 
        "player_in_possession_name": pl.Utf8, 
        "player_in_possession_position": pl.Utf8,
        "x_start": pl.Float32,
        "y_start": pl.Float32,
        "x_end": pl.Float32,
        "y_end": pl.Float32,
        "channel_start": pl.Utf8, 
        "channel_end": pl.Utf8,
        "third_start": pl.Utf8,  
        "third_end": pl.Utf8,
        "zone_start": pl.Utf8,
        "zone_end": pl.Utf8,
        "player_in_possession_zone_start": pl.Utf8,
        "player_in_possession_zone_end": pl.Utf8,
        "team_in_possession_phase_type": pl.Utf8, 
        "team_out_of_possession_phase_type": pl.Utf8,
        "start_type": pl.Utf8, 
        "end_type": pl.Utf8,
        "game_state_id": pl.Int32, 
        "game_state": pl.Utf8,
        "associated_player_possession_event_id": pl.Utf8,
        "targeted": pl.Boolean, 
        "received": pl.Boolean,
        "xthreat": pl.Float32, 
        "xpass_completion": pl.Float32, 
        "passing_option_score": pl.Float32,
        "speed_avg_band": pl.Utf8,
        "pressing_chain_index": pl.Int32,
        "pressing_chain_end_type": pl.Utf8,
        "youtube_video_id": pl.Utf8,
        "event_start_seconds": pl.Int32,
        "event_end_seconds": pl.Int32,
        "home_team_side_first": pl.Utf8,
        "home_team_side_second": pl.Utf8,
        "away_team_side_first": pl.Utf8,
        "away_team_side_second": pl.Utf8,
        "x_start_tracking": pl.Float32,
        "y_start_tracking": pl.Float32,
        "x_end_tracking": pl.Float32,
        "y_end_tracking": pl.Float32,
    },

    "gold_player_aggregates": {
        "player_id": pl.Int32, 
        "player_name": pl.Utf8, 
        "birthday": pl.Date, 
        "age": pl.Int16, 
        "team_id": pl.Int32, 
        "team_shortname": pl.Utf8, 
        "competition_id": pl.Int32, 
        "competition_name": pl.Utf8, 
        "season_id": pl.Int32, 
        "season_name": pl.Utf8, 
        "positions": pl.Utf8, 
        "minutes_played": pl.Int32, 
        "matches_played": pl.Int16, 
        "starts": pl.Int16,
        "off_ball_runs": pl.Int32, 
        "off_ball_runs_targeted": pl.Int32, 
        "dropping_off_runs": pl.Int32, 
        "dropping_off_runs_targeted": pl.Int32, 
        "coming_short_runs": pl.Int32, 
        "coming_short_runs_targeted": pl.Int32, 
        "pulling_wide_runs": pl.Int32, 
        "pulling_wide_runs_targeted": pl.Int32, 
        "pulling_half_space_runs": pl.Int32, 
        "pulling_half_space_runs_targeted": pl.Int32, 
        "support_runs": pl.Int32, 
        "support_runs_targeted": pl.Int32, 
        "run_ahead_of_the_ball_runs": pl.Int32, 
        "run_ahead_of_the_ball_runs_targeted": pl.Int32, 
        "overlap_runs": pl.Int32, 
        "overlap_runs_targeted": pl.Int32, 
        "underlap_runs": pl.Int32, 
        "underlap_runs_targeted": pl.Int32, 
        "behind_runs": pl.Int32, 
        "behind_runs_targeted": pl.Int32, 
        "cross_receiver_runs": pl.Int32, 
        "cross_receiver_runs_targeted": pl.Int32, 
        "on_ball_engagements": pl.Int32, 
        "pressures": pl.Int32, 
        "recovery_pressures": pl.Int32, 
        "counter_pressures": pl.Int32, 
        "on_ball_engagement_recoveries": pl.Int32, 
        "pressure_recoveries": pl.Int32, 
        "recovery_pressure_recoveries": pl.Int32, 
        "counter_pressure_recoveries": pl.Int32, 
        "on_ball_engagements_high": pl.Int32, 
        "on_ball_engagement_high_recoveries": pl.Int32, 
        "pressures_high": pl.Int32, 
        "pressure_high_recoveries": pl.Int32, 
        "recovery_pressures_high": pl.Int32, 
        "recovery_pressure_high_recoveries": pl.Int32, 
        "counter_pressures_high": pl.Int32, 
        "counter_pressure_high_recoveries": pl.Int32,
        "passing_option_score_avg": pl.Float32,
        "off_ball_runs_90": pl.Float32, 
        "off_ball_runs_targeted_90": pl.Float32,  
        "dropping_off_runs_90": pl.Float32,  
        "dropping_off_runs_targeted_90": pl.Float32,  
        "coming_short_runs_90": pl.Float32,  
        "coming_short_runs_targeted_90": pl.Float32,  
        "pulling_wide_runs_90": pl.Float32, 
        "pulling_wide_runs_targeted_90": pl.Float32, 
        "pulling_half_space_runs_90": pl.Float32,  
        "pulling_half_space_runs_targeted_90": pl.Float32, 
        "support_runs_90": pl.Float32,  
        "support_runs_targeted_90": pl.Float32, 
        "run_ahead_of_the_ball_runs_90": pl.Float32, 
        "run_ahead_of_the_ball_runs_targeted_90": pl.Float32, 
        "overlap_runs_90": pl.Float32, 
        "overlap_runs_targeted_90": pl.Float32, 
        "underlap_runs_90": pl.Float32, 
        "underlap_runs_targeted_90": pl.Float32, 
        "behind_runs_90": pl.Float32, 
        "behind_runs_targeted_90": pl.Float32, 
        "cross_receiver_runs_90": pl.Float32, 
        "cross_receiver_runs_targeted_90": pl.Float32, 
        "on_ball_engagements_90": pl.Float32, 
        "pressures_90": pl.Float32,  
        "recovery_pressures_90": pl.Float32, 
        "counter_pressures_90": pl.Float32,  
        "on_ball_engagement_recoveries_90": pl.Float32, 
        "pressure_recoveries_90": pl.Float32,  
        "recovery_pressure_recoveries_90": pl.Float32, 
        "counter_pressure_recoveries_90": pl.Float32, 
        "on_ball_engagements_high_90": pl.Float32, 
        "on_ball_engagement_high_recoveries_90": pl.Float32,
        "pressures_high_90": pl.Float32, 
        "pressure_high_recoveries_90": pl.Float32,
        "recovery_pressures_high_90": pl.Float32, 
        "recovery_pressure_high_recoveries_90": pl.Float32,
        "counter_pressures_high_90": pl.Float32, 
        "counter_pressure_high_recoveries_90": pl.Float32,
        "off_ball_runs_targeted_pct": pl.Float32, 
        "dropping_off_runs_targeted_pct": pl.Float32, 
        "coming_short_runs_targeted_pct": pl.Float32, 
        "pulling_wide_runs_targeted_pct": pl.Float32, 
        "pulling_half_space_runs_targeted_pct": pl.Float32, 
        "support_runs_targeted_pct": pl.Float32, 
        "run_ahead_of_the_ball_runs_targeted_pct": pl.Float32, 
        "overlap_runs_targeted_pct": pl.Float32, 
        "underlap_runs_targeted_pct": pl.Float32, 
        "behind_runs_targeted_pct": pl.Float32, 
        "cross_receiver_runs_targeted_pct": pl.Float32, 
        "on_ball_engagement_recoveries_pct": pl.Float32, 
        "pressure_recoveries_pct": pl.Float32, 
        "recovery_pressure_recoveries_pct": pl.Float32, 
        "counter_pressure_recoveries_pct": pl.Float32, 
        "on_ball_engagement_high_recoveries_pct": pl.Float32,
        "pressure_high_recoveries_pct": pl.Float32,
        "recovery_pressure_high_recoveries_pct": pl.Float32,
        "counter_pressure_high_recoveries_pct": pl.Float32,
        "passes": pl.Int32, 
        "passes_completed": pl.Int32, 
        "pass_completion_pct": pl.Float32, 
        "xpass_completion_avg": pl.Float32, 
        "xpass_completion_completed_avg": pl.Float32, 
        "xthreat": pl.Float32, 
        "xthreat_avg": pl.Float32,
        "line_breaking_passes": pl.Int32,
        "line_breaking_passes_completed": pl.Int32,
        "first_line_breaking_passes": pl.Int32,
        "second_last_line_breaking_passes": pl.Int32,
        "last_line_breaking_passes": pl.Int32,
        "first_line_breaking_passes_completed": pl.Int32,
        "second_last_line_breaking_passes_completed": pl.Int32,
        "last_line_breaking_passes_completed": pl.Int32,
        "ahead_passes": pl.Int32,
        "ahead_passes_completed": pl.Int32,
        "line_breaking_passes_90": pl.Float32,
        "line_breaking_passes_completed_90": pl.Float32,
        "first_line_breaking_passes_90": pl.Float32,
        "second_last_line_breaking_passes_90": pl.Float32,
        "last_line_breaking_passes_90": pl.Float32,
        "first_line_breaking_passes_completed_90": pl.Float32,
        "second_last_line_breaking_passes_completed_90": pl.Float32,
        "last_line_breaking_passes_completed_90": pl.Float32,
        "passes_90": pl.Float32,
        "passes_completed_90": pl.Float32,
        "ahead_passes_90": pl.Float32,
        "ahead_passes_completed_90": pl.Float32,
    },

    "gold_team_aggregates": {
        "team_id": pl.Int32, 
        "team_shortname": pl.Utf8, 
        "competition_id": pl.Int32, 
        "competition_name": pl.Utf8, 
        "season_id": pl.Int32, 
        "season_name": pl.Utf8,
        "minutes_played": pl.Int32, 
        "matches_played": pl.Int16, 
        "off_ball_runs": pl.Int32, 
        "off_ball_runs_targeted": pl.Int32, 
        "dropping_off_runs": pl.Int32, 
        "dropping_off_runs_targeted": pl.Int32, 
        "coming_short_runs": pl.Int32, 
        "coming_short_runs_targeted": pl.Int32, 
        "pulling_wide_runs": pl.Int32, 
        "pulling_wide_runs_targeted": pl.Int32, 
        "pulling_half_space_runs": pl.Int32, 
        "pulling_half_space_runs_targeted": pl.Int32, 
        "support_runs": pl.Int32, 
        "support_runs_targeted": pl.Int32, 
        "run_ahead_of_the_ball_runs": pl.Int32, 
        "run_ahead_of_the_ball_runs_targeted": pl.Int32, 
        "overlap_runs": pl.Int32, 
        "overlap_runs_targeted": pl.Int32, 
        "underlap_runs": pl.Int32, 
        "underlap_runs_targeted": pl.Int32, 
        "behind_runs": pl.Int32, 
        "behind_runs_targeted": pl.Int32, 
        "cross_receiver_runs": pl.Int32, 
        "cross_receiver_runs_targeted": pl.Int32, 
        "on_ball_engagements": pl.Int32, 
        "pressures": pl.Int32, 
        "recovery_pressures": pl.Int32, 
        "counter_pressures": pl.Int32, 
        "on_ball_engagement_recoveries": pl.Int32, 
        "pressure_recoveries": pl.Int32, 
        "recovery_pressure_recoveries": pl.Int32, 
        "counter_pressure_recoveries": pl.Int32,  
        "on_ball_engagements_high": pl.Int32, 
        "on_ball_engagement_high_recoveries": pl.Int32, 
        "pressures_high": pl.Int32, 
        "pressure_high_recoveries": pl.Int32, 
        "recovery_pressures_high": pl.Int32, 
        "recovery_pressure_high_recoveries": pl.Int32, 
        "counter_pressures_high": pl.Int32, 
        "counter_pressure_high_recoveries": pl.Int32, 
        "recovery_height_avg": pl.Float32,
        "off_ball_runs_90": pl.Float32, 
        "off_ball_runs_targeted_90": pl.Float32,  
        "dropping_off_runs_90": pl.Float32,  
        "dropping_off_runs_targeted_90": pl.Float32,  
        "coming_short_runs_90": pl.Float32,  
        "coming_short_runs_targeted_90": pl.Float32,  
        "pulling_wide_runs_90": pl.Float32, 
        "pulling_wide_runs_targeted_90": pl.Float32, 
        "pulling_half_space_runs_90": pl.Float32,  
        "pulling_half_space_runs_targeted_90": pl.Float32, 
        "support_runs_90": pl.Float32,  
        "support_runs_targeted_90": pl.Float32, 
        "run_ahead_of_the_ball_runs_90": pl.Float32, 
        "run_ahead_of_the_ball_runs_targeted_90": pl.Float32, 
        "overlap_runs_90": pl.Float32, 
        "overlap_runs_targeted_90": pl.Float32, 
        "underlap_runs_90": pl.Float32, 
        "underlap_runs_targeted_90": pl.Float32, 
        "behind_runs_90": pl.Float32, 
        "behind_runs_targeted_90": pl.Float32, 
        "cross_receiver_runs_90": pl.Float32, 
        "cross_receiver_runs_targeted_90": pl.Float32, 
        "on_ball_engagements_90": pl.Float32, 
        "pressures_90": pl.Float32,  
        "recovery_pressures_90": pl.Float32, 
        "counter_pressures_90": pl.Float32,  
        "on_ball_engagement_recoveries_90": pl.Float32, 
        "pressure_recoveries_90": pl.Float32,  
        "recovery_pressure_recoveries_90": pl.Float32, 
        "counter_pressure_recoveries_90": pl.Float32, 
        "on_ball_engagements_high_90": pl.Float32, 
        "on_ball_engagement_high_recoveries_90": pl.Float32,
        "pressures_high_90": pl.Float32, 
        "pressure_high_recoveries_90": pl.Float32,
        "recovery_pressures_high_90": pl.Float32, 
        "recovery_pressure_high_recoveries_90": pl.Float32,
        "counter_pressures_high_90": pl.Float32, 
        "counter_pressure_high_recoveries_90": pl.Float32, 
        "off_ball_runs_targeted_pct": pl.Float32, 
        "dropping_off_runs_targeted_pct": pl.Float32, 
        "coming_short_runs_targeted_pct": pl.Float32, 
        "pulling_wide_runs_targeted_pct": pl.Float32, 
        "pulling_half_space_runs_targeted_pct": pl.Float32, 
        "support_runs_targeted_pct": pl.Float32, 
        "run_ahead_of_the_ball_runs_targeted_pct": pl.Float32, 
        "overlap_runs_targeted_pct": pl.Float32, 
        "underlap_runs_targeted_pct": pl.Float32, 
        "behind_runs_targeted_pct": pl.Float32, 
        "cross_receiver_runs_targeted_pct": pl.Float32, 
        "on_ball_engagement_recoveries_pct": pl.Float32, 
        "pressure_recoveries_pct": pl.Float32, 
        "recovery_pressure_recoveries_pct": pl.Float32, 
        "counter_pressure_recoveries_pct": pl.Float32, 
        "on_ball_engagement_high_recoveries_pct": pl.Float32, 
        "pressure_high_recoveries_pct": pl.Float32, 
        "recovery_pressure_high_recoveries_pct": pl.Float32, 
        "counter_pressure_high_recoveries_pct": pl.Float32, 
        "defense_recovery_height_avg": pl.Float32, 
        "midfield_recovery_height_avg": pl.Float32,
        "attack_recovery_height_avg": pl.Float32, 
        "defense_recoveries": pl.Int32, 
        "midfield_recoveries": pl.Int32,
        "attack_recoveries": pl.Int32,
    }
}


'''
Convert a Polars DataType to a PyArrow DataType.

:param dt: Polars DataType.

:return: Corresponding PyArrow DataType.
'''
def polars_to_arrow_type(dt: pl.DataType) -> pa.DataType:
    if dt == pl.Int8: 
        return pa.int8()
    elif dt == pl.Int16: 
        return pa.int16()
    elif dt == pl.Int32: 
        return pa.int32()
    elif dt == pl.Int64: 
        return pa.int64()
    elif dt == pl.Float32: 
        return pa.float32()
    elif dt == pl.Float64: 
        return pa.float64()
    elif dt == pl.Boolean: 
        return pa.bool_()
    elif dt == pl.Date: 
        return pa.date32()
    elif isinstance(dt, pl.Datetime): 
        return pa.timestamp("us")
    elif isinstance(dt, pl.Time): 
        return pa.time64("us")
    elif dt == pl.Utf8: 
        return pa.large_string()
    else:
        return pa.large_string()


'''
Get the PyArrow schema for a given schema name.

:param name: Name of the schema.

:return: PyArrow Schema object.
'''
def get_arrow_schema(name: str) -> pa.Schema:
    spec = bronze_schemas.get(name) or silver_schemas.get(name) or gold_schemas.get(name)
    if spec is None:
        raise ValueError(f"Schema '{name}' not found!")

    return pa.schema([pa.field(col_name, polars_to_arrow_type(col_type)) for col_name, col_type in spec.items()])


'''
Apply the specified schema to a Polars DataFrame.

:param df: Polars DataFrame to apply the schema to.
:param name: Name of the schema.

:return: Polars DataFrame with the applied schema.
'''
def apply_schema(df: pl.DataFrame, name: str) -> pl.DataFrame:
    if df is None or df.height == 0:
        return df

    spec = bronze_schemas.get(name) or silver_schemas.get(name) or gold_schemas.get(name)

    if spec is None:
        raise ValueError(f"Schema '{name}' not found!")

    out = df

    for col_name, col_type in spec.items():
        if col_name in out.columns:
            out = out.with_columns(pl.col(col_name).cast(col_type))
        else:
            out = out.with_columns(pl.lit(None).cast(col_type).alias(col_name))

    out = out.select(list(spec.keys()))

    return out
