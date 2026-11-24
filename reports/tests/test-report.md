# Test Report

- Generated: 2026-11-24T22:54:43Z
- Command: `make report`
- Source SHA-256: `6e5f4bbbf687bfe26d6378ab65f7d603ea080bb5534f2800de0dc1bf6f4e6b4f`
- Python: 3.14.4
- Bash: GNU bash, version 5.3.9(1)-release (x86_64-pc-linux-gnu)
- Platform: Linux
- Tests run: 71
- Passed: 71, failed: 0, errors: 0, skipped: 0
- Duration: 9.74 s

| Test | Outcome | Seconds |
| --- | --- | ---: |
| `tests.integration.test_cli_play.PlayDirectoryTests.test_correct_guess_wins` | passed | 0.0076 |
| `tests.integration.test_cli_play.PlayDirectoryTests.test_crlf_input_is_accepted` | passed | 0.0081 |
| `tests.integration.test_cli_play.PlayDirectoryTests.test_empty_input_does_not_win` | passed | 0.0081 |
| `tests.integration.test_cli_play.PlayDirectoryTests.test_end_of_input_terminates` | passed | 0.0093 |
| `tests.integration.test_cli_play.PlayDirectoryTests.test_final_line_without_newline_is_read` | passed | 0.0092 |
| `tests.integration.test_cli_play.PlayDirectoryTests.test_hints_then_win` | passed | 0.0099 |
| `tests.integration.test_cli_play.PlayDirectoryTests.test_invalid_guess_is_not_counted` | passed | 0.0098 |
| `tests.integration.test_cli_play.PlayDirectoryTests.test_max_attempts_stops_game` | passed | 0.0105 |
| `tests.integration.test_cli_play.PlayRandomTests.test_seeded_target_is_reproducible` | passed | 0.0113 |
| `tests.integration.test_cli_play.PlayRandomTests.test_unseeded_random_target_is_in_range` | passed | 0.0161 |
| `tests.integration.test_cli_play.UsageTests.test_help` | passed | 0.0093 |
| `tests.integration.test_cli_play.UsageTests.test_rejected_arguments_exit_with_usage_code` | passed | 0.0883 |
| `tests.integration.test_cli_play.UsageTests.test_version_matches_file` | passed | 0.0093 |
| `tests.integration.test_cli_simulate.SimulateTests.test_different_seeds_differ` | passed | 0.0466 |
| `tests.integration.test_cli_simulate.SimulateTests.test_maximum_bound_is_supported` | passed | 0.0092 |
| `tests.integration.test_cli_simulate.SimulateTests.test_rows_match_reference_models` | passed | 0.124 |
| `tests.integration.test_cli_simulate.SimulateTests.test_same_seed_is_byte_identical` | passed | 0.0422 |
| `tests.integration.test_cli_simulate.SimulateTests.test_summary_is_on_stderr_only` | passed | 0.0108 |
| `tests.integration.test_makefile.MakefileTests.test_set_file_writes_build_output_and_preserves_readme` | passed | 0.0146 |
| `tests.integration.test_schema.LoaderTests.test_loads_real_simulation_output` | passed | 0.088 |
| `tests.integration.test_schema.LoaderTests.test_rejects_invalid_row_atomically` | passed | 0.074 |
| `tests.integration.test_schema.LoaderTests.test_rejects_malformed_rows_without_traceback` | passed | 0.9075 |
| `tests.integration.test_schema.LoaderTests.test_rejects_wrong_header` | passed | 0.0845 |
| `tests.integration.test_schema.LoaderTests.test_strategy_text_is_bound_not_executed` | passed | 0.0883 |
| `tests.integration.test_schema.SchemaTests.test_delete_cascades` | passed | 0.0011 |
| `tests.integration.test_schema.SchemaTests.test_rejects_orphan_trial` | passed | 0.0008 |
| `tests.integration.test_schema.SchemaTests.test_rejects_unknown_strategy` | passed | 0.0007 |
| `tests.integration.test_schema.SchemaTests.test_schema_is_idempotent` | passed | 0.0007 |
| `tests.properties.test_random_statistics.GeneratorStatistics.test_first_draw_across_adjacent_seeds_is_uniform` | passed | 2.1618 |
| `tests.properties.test_random_statistics.GeneratorStatistics.test_serial_pairs_chi_square` | passed | 1.1857 |
| `tests.properties.test_random_statistics.GeneratorStatistics.test_uniformity_chi_square` | passed | 2.7657 |
| `tests.properties.test_random_statistics.GeneratorStatistics.test_values_stay_in_range` | passed | 0.2286 |
| `tests.properties.test_strategy_properties.BisectionProperties.test_mean_matches_balanced_tree_for_complete_sizes` | passed | 0.0514 |
| `tests.properties.test_strategy_properties.BisectionProperties.test_no_comparison_strategy_beats_information_bound` | passed | 0.0336 |
| `tests.properties.test_strategy_properties.BisectionProperties.test_shell_matches_model_on_random_ranges` | passed | 0.3034 |
| `tests.properties.test_strategy_properties.BisectionProperties.test_worst_case_is_exactly_bit_length` | passed | 0.0434 |
| `tests.properties.test_strategy_properties.GallopingProperties.test_bound_holds_for_large_random_targets` | passed | 0.4021 |
| `tests.properties.test_strategy_properties.GallopingProperties.test_exhaustive_bound_and_model_agreement` | passed | 0.0391 |
| `tests.properties.test_strategy_properties.ParserProperties.test_round_trip_for_random_integers` | passed | 0.3844 |
| `tests.security.test_input_safety.InputSafetyTests.test_guess_is_never_evaluated` | passed | 0.0369 |
| `tests.security.test_input_safety.InputSafetyTests.test_hostile_directory_name_is_treated_as_data` | passed | 0.0069 |
| `tests.security.test_input_safety.InputSafetyTests.test_inherited_glob_settings_cannot_change_the_target` | passed | 0.0069 |
| `tests.security.test_input_safety.InputSafetyTests.test_inherited_noglob_cannot_change_the_target` | passed | 0.0078 |
| `tests.security.test_input_safety.InputSafetyTests.test_invalid_input_is_not_echoed` | passed | 0.0074 |
| `tests.security.test_input_safety.InputSafetyTests.test_option_values_are_never_evaluated` | passed | 0.1087 |
| `tests.security.test_input_safety.InputSafetyTests.test_simulate_options_are_never_evaluated` | passed | 0.1185 |
| `tests.security.test_input_safety.InputSafetyTests.test_source_has_no_dynamic_evaluation` | passed | 0.0015 |
| `tests.security.test_input_safety.InputSafetyTests.test_symlinked_launcher_ignores_modules_beside_the_link` | passed | 0.006 |
| `tests.unit.test_random.XorshiftTests.test_bounded_stream_matches_reference_model` | passed | 0.0487 |
| `tests.unit.test_random.XorshiftTests.test_matches_published_xorshift32_vector` | passed | 0.0019 |
| `tests.unit.test_random.XorshiftTests.test_seed_matches_reference_model` | passed | 0.0107 |
| `tests.unit.test_random.XorshiftTests.test_state_is_never_zero_after_seeding` | passed | 0.0021 |
| `tests.unit.test_random.XorshiftTests.test_step_matches_reference_model` | passed | 0.0091 |
| `tests.unit.test_strategies.StrategyExampleTests.test_bisection_finds_midpoint_in_one_probe` | passed | 0.0019 |
| `tests.unit.test_strategies.StrategyExampleTests.test_bisection_single_value_range` | passed | 0.0019 |
| `tests.unit.test_strategies.StrategyExampleTests.test_bit_length` | passed | 0.0021 |
| `tests.unit.test_strategies.StrategyExampleTests.test_galloping_hits_power_boundary` | passed | 0.0019 |
| `tests.unit.test_strategies.StrategyExampleTests.test_galloping_zero_takes_one_probe` | passed | 0.0019 |
| `tests.unit.test_strategies.StrategyExampleTests.test_linear_counts_every_probe` | passed | 0.002 |
| `tests.unit.test_target.CountDirectoryEntriesTests.test_counts_files_and_directories` | passed | 0.0026 |
| `tests.unit.test_target.CountDirectoryEntriesTests.test_directory_name_with_glob_characters` | passed | 0.0025 |
| `tests.unit.test_target.CountDirectoryEntriesTests.test_empty_directory_is_zero` | passed | 0.0024 |
| `tests.unit.test_target.CountDirectoryEntriesTests.test_filename_with_newline_counts_once` | passed | 0.0025 |
| `tests.unit.test_target.CountDirectoryEntriesTests.test_hidden_entries_are_excluded` | passed | 0.0025 |
| `tests.unit.test_target.CountDirectoryEntriesTests.test_missing_directory_fails` | passed | 0.002 |
| `tests.unit.test_validation.ParseBoundedIntegerTests.test_accepts_inclusive_bounds` | passed | 0.0036 |
| `tests.unit.test_validation.ParseBoundedIntegerTests.test_accepts_plain_decimal` | passed | 0.0018 |
| `tests.unit.test_validation.ParseBoundedIntegerTests.test_leading_zeros_are_decimal_not_octal` | passed | 0.0036 |
| `tests.unit.test_validation.ParseBoundedIntegerTests.test_rejects_more_than_ten_digits` | passed | 0.0019 |
| `tests.unit.test_validation.ParseBoundedIntegerTests.test_rejects_non_decimal_forms` | passed | 0.0214 |
| `tests.unit.test_validation.ParseBoundedIntegerTests.test_rejects_out_of_range` | passed | 0.0037 |
