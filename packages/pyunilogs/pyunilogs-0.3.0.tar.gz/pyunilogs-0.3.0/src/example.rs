// Copyright 2022 Mandiant, Inc. All Rights Reserved
// Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0
// Unless required by applicable law or agreed to in writing, software distributed under the License
// is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and limitations under the License.

// Modified from https://github.com/mandiant/macos-UnifiedLogs/blob/d062321f8b4f2897d5ff6b29a7fcbff3277fc414/examples/unifiedlog_parser_json/src/main.rs

use macos_unifiedlogs::dsc::SharedCacheStrings;
use macos_unifiedlogs::parser::{
    build_log, collect_shared_strings, collect_strings, collect_timesync, parse_log,
};
use macos_unifiedlogs::timesync::TimesyncBoot;
use macos_unifiedlogs::unified_log::{LogData, UnifiedLogData};
use macos_unifiedlogs::uuidtext::UUIDText;
use std::collections::VecDeque;
use std::fs;
use std::path::PathBuf;

pub struct LogExtraction {
    string_results: Vec<UUIDText>,
    shared_strings_results: Vec<SharedCacheStrings>,
    timesync_data: Vec<TimesyncBoot>,

    missing_data: Vec<UnifiedLogData>,
    oversize_strings: UnifiedLogData,

    persistent_log_paths: VecDeque<String>,
    special_log_paths: VecDeque<String>,
    signpost_log_paths: VecDeque<String>,
    highvolume_log_paths: VecDeque<String>,
    livedata_log_paths: VecDeque<String>,
}

impl LogExtraction {
    pub fn from_path(path: &str) -> Self {
        let mut archive_path = PathBuf::from(path);

        // Parse all UUID files which contain strings and other metadata
        let string_results = collect_strings(&archive_path.display().to_string()).unwrap();

        archive_path.push("dsc");
        // Parse UUID cache files which also contain strings and other metadata
        let shared_strings_results =
            collect_shared_strings(&archive_path.display().to_string()).unwrap();
        archive_path.pop();

        archive_path.push("timesync");
        // Parse all timesync files
        let timesync_data = collect_timesync(&archive_path.display().to_string()).unwrap();
        archive_path.pop();

        let mut persistent_log_paths = VecDeque::new();

        archive_path.push("Persist");
        // Find all the persistent directory paths
        if archive_path.exists() {
            let paths = fs::read_dir(&archive_path).unwrap();

            for log_path in paths {
                let data = log_path.unwrap();
                let full_path = data.path().display().to_string();
                persistent_log_paths.push_back(full_path);
            }
        }

        let mut special_log_paths = VecDeque::new();

        archive_path.pop();
        archive_path.push("Special");

        if archive_path.exists() {
            let paths = fs::read_dir(&archive_path).unwrap();

            // Loop through all tracev3 files in Special directory
            for log_path in paths {
                let data = log_path.unwrap();
                let full_path = data.path().display().to_string();
                special_log_paths.push_back(full_path);
            }
        }

        let mut signpost_log_paths = VecDeque::new();

        archive_path.pop();
        archive_path.push("Signpost");

        if archive_path.exists() {
            let paths = fs::read_dir(&archive_path).unwrap();

            // Loop through all tracev3 files in Signpost directory
            for log_path in paths {
                let data = log_path.unwrap();
                let full_path = data.path().display().to_string();
                signpost_log_paths.push_back(full_path);
            }
        }

        let mut highvolume_log_paths = VecDeque::new();

        archive_path.pop();
        archive_path.push("HighVolume");

        if archive_path.exists() {
            let paths = fs::read_dir(&archive_path).unwrap();

            // Loop through all tracev3 files in Signpost directory
            for log_path in paths {
                let data = log_path.unwrap();
                let full_path = data.path().display().to_string();
                highvolume_log_paths.push_back(full_path);
            }
        }

        archive_path.pop();
        archive_path.push("logdata.LiveData.tracev3");

        let mut livedata_log_paths = VecDeque::new();
        if archive_path.exists() {
            livedata_log_paths.push_back(archive_path.display().to_string());
        }

        return Self {
            string_results,
            shared_strings_results,
            timesync_data,

            missing_data: Vec::new(),
            oversize_strings: UnifiedLogData {
                header: Vec::new(),
                catalog_data: Vec::new(),
                oversize: Vec::new(),
            },

            persistent_log_paths,
            signpost_log_paths,
            special_log_paths,
            highvolume_log_paths,
            livedata_log_paths,
        };
    }

    pub fn next(&mut self) -> Option<Vec<LogData>> {
        if let Some(path) = self.persistent_log_paths.pop_front() {
            return Some(self.parse_tracev3_file(&path, true));
        } else if let Some(path) = self.signpost_log_paths.pop_front() {
            return Some(self.parse_tracev3_file(&path, true));
        } else if let Some(path) = self.special_log_paths.pop_front() {
            return Some(self.parse_tracev3_file(&path, true));
        } else if let Some(path) = self.highvolume_log_paths.pop_front() {
            return Some(self.parse_tracev3_file(&path, true));
        } else if let Some(path) = self.livedata_log_paths.pop_front() {
            return Some(self.parse_tracev3_file(&path, true));
        }

        if !self.missing_data.is_empty() {
            return Some(self.parse_missing_data());
        }

        return None;
    }

    fn parse_tracev3_file(&mut self, path: &str, exclude_missing: bool) -> Vec<LogData> {
        let mut log_data = parse_log(&path).unwrap();

        // Append all previously parsed Oversize entries from tracker to current parsed tracev3 file
        log_data
            .oversize
            .append(&mut self.oversize_strings.oversize);

        // Get all constructed logs and any log data that failed to get constrcuted (if exclude_missing = true)
        let (results, missing_logs) = build_log(
            &log_data,
            &self.string_results,
            &self.shared_strings_results,
            &self.timesync_data,
            exclude_missing,
        );

        // Take all Oversize entries and add to tracker
        self.oversize_strings
            .oversize
            .append(&mut log_data.oversize.clone());

        // Add log entries that failed to find strings to missing tracker
        // We will try parsing them again at the end once we have all Oversize entries
        self.missing_data.push(missing_logs);

        return results;
    }

    fn parse_missing_data(&mut self) -> Vec<LogData> {
        // Include all log entries now, if any logs are missing data its because the data has rolled
        let exclude_missing = false;
        let mut missing_logs_parsed = Vec::new();
        for leftover_data in self.missing_data.iter_mut() {
            // Add all of our previous oversize data to logs for lookups
            leftover_data
                .oversize
                .append(&mut self.oversize_strings.oversize);

            // Exclude_missing = false
            // If we fail to find any missing data its probably due to the logs rolling
            // Ex: tracev3A rolls, tracev3B references Oversize entry in tracev3A will trigger missing data since tracev3A is gone
            let (results, _) = build_log(
                &leftover_data,
                &self.string_results,
                &self.shared_strings_results,
                &self.timesync_data,
                exclude_missing,
            );

            missing_logs_parsed.extend(results);

            // output(&results, output_path, "dataFoundInMultipleLogFiles").unwrap();
        }
        self.missing_data.clear();
        return missing_logs_parsed;
    }
}

// Parse a provided directory path. Currently expect the path to follow macOS log collect structure
pub fn parse_log_archive(path: &str) -> Vec<LogData> {
    let mut archive_path = PathBuf::from(path);

    // Parse all UUID files which contain strings and other metadata
    let string_results = collect_strings(&archive_path.display().to_string()).unwrap();

    archive_path.push("dsc");
    // Parse UUID cache files which also contain strings and other metadata
    let shared_strings_results =
        collect_shared_strings(&archive_path.display().to_string()).unwrap();
    archive_path.pop();

    archive_path.push("timesync");
    // Parse all timesync files
    let timesync_data = collect_timesync(&archive_path.display().to_string()).unwrap();
    archive_path.pop();

    // Keep UUID, UUID cache, timesync files in memory while we parse all tracev3 files
    // Allows for faster lookups
    parse_trace_file(
        &string_results,
        &shared_strings_results,
        &timesync_data,
        path,
    )

    // println!("\nFinished parsing Unified Log data. Saved results to json files");
}

// struct FilterArgument {

// }

// struct FilteredLogData {
//     parsed_logs: HashMap<String, Vec<LogData>>,
//     statedumps: HashMap<String, Vec<>>,
// }

// Use the provided strings, shared strings, timesync data to parse the Unified Log data at provided path.
// Currently expect the path to follow macOS log collect structure
fn parse_trace_file(
    string_results: &[UUIDText],
    shared_strings_results: &[SharedCacheStrings],
    timesync_data: &[TimesyncBoot],
    path: &str,
) -> Vec<LogData> {
    let mut all_result_data = Vec::new();

    // We need to persist the Oversize log entries (they contain large strings that don't fit in normal log entries)
    // Some log entries have Oversize strings located in different tracev3 files.
    // This is very rare. Seen in ~20 log entries out of ~700,000. Seen in ~700 out of ~18 million
    let mut oversize_strings = UnifiedLogData {
        header: Vec::new(),
        catalog_data: Vec::new(),
        oversize: Vec::new(),
    };

    // Exclude missing data from returned output. Keep separate until we parse all oversize entries.
    // Then at end, go through all missing data and check all parsed oversize entries again
    let mut exclude_missing = true;
    let mut missing_data: Vec<UnifiedLogData> = Vec::new();

    let mut archive_path = PathBuf::from(path);
    archive_path.push("Persist");

    let mut log_count = 0;
    if archive_path.exists() {
        let paths = fs::read_dir(&archive_path).unwrap();

        // Loop through all tracev3 files in Persist directory
        for log_path in paths {
            let data = log_path.unwrap();
            let full_path = data.path().display().to_string();
            // println!("Parsing: {}", full_path);

            let log_data = if data.path().exists() {
                parse_log(&full_path).unwrap()
            } else {
                // println!("File {} no longer on disk", full_path);
                continue;
            };

            // Get all constructed logs and any log data that failed to get constrcuted (exclude_missing = true)
            let (results, missing_logs) = build_log(
                &log_data,
                string_results,
                shared_strings_results,
                timesync_data,
                exclude_missing,
            );
            // Take all Oversize entries and add to tracker
            oversize_strings.oversize = log_data.oversize;

            // Add log entries that failed to find strings to missing tracker
            // We will try parsing them again at the end once we have all Oversize entries
            missing_data.push(missing_logs);
            log_count += results.len();
            all_result_data.extend(results);
            // output(
            //     &results,
            //     output_path,
            //     &format!("persist_{}", data.file_name().to_str().unwrap()),
            // )
            // .unwrap();
        }
    }

    archive_path.pop();
    archive_path.push("Special");

    if archive_path.exists() {
        let paths = fs::read_dir(&archive_path).unwrap();

        // Loop through all tracev3 files in Special directory
        for log_path in paths {
            let data = log_path.unwrap();
            let full_path = data.path().display().to_string();
            // println!("Parsing: {}", full_path);

            let mut log_data = if data.path().exists() {
                parse_log(&full_path).unwrap()
            } else {
                // println!("File {} no longer on disk", full_path);
                continue;
            };
            // Append all previously parsed Oversize entries from tracker to current parsed tracev3 file
            log_data.oversize.append(&mut oversize_strings.oversize);

            let (results, missing_logs) = build_log(
                &log_data,
                string_results,
                shared_strings_results,
                timesync_data,
                exclude_missing,
            );
            // Take all Oversize entries and add to tracker
            oversize_strings.oversize = log_data.oversize;

            // Add log entries that failed to find strings to missing tracker
            // We will try parsing them again at the end once we have all Oversize entries
            missing_data.push(missing_logs);
            log_count += results.len();

            all_result_data.extend(results);
            // output(
            //     &results,
            //     output_path,
            //     &format!("special_{}", data.file_name().to_str().unwrap()),
            // )
            // .unwrap();
        }
    }

    archive_path.pop();
    archive_path.push("Signpost");

    if archive_path.exists() {
        let paths = fs::read_dir(&archive_path).unwrap();

        // Loop through all tracev3 files in Signpost directory
        for log_path in paths {
            let data = log_path.unwrap();
            let full_path = data.path().display().to_string();
            // println!("Parsing: {}", full_path);

            let log_data = if data.path().exists() {
                parse_log(&full_path).unwrap()
            } else {
                // println!("File {} no longer on disk", full_path);
                continue;
            };

            let (results, missing_logs) = build_log(
                &log_data,
                string_results,
                shared_strings_results,
                timesync_data,
                exclude_missing,
            );

            // Signposts have not been seen with Oversize entries
            missing_data.push(missing_logs);
            log_count += results.len();

            all_result_data.extend(results);
            // output(
            //     &results,
            //     output_path,
            //     &format!("signpost_{}", data.file_name().to_str().unwrap()),
            // )
            // .unwrap();
        }
    }
    archive_path.pop();
    archive_path.push("HighVolume");

    if archive_path.exists() {
        let paths = fs::read_dir(&archive_path).unwrap();

        // Loop through all tracev3 files in HighVolume directory
        for log_path in paths {
            let data = log_path.unwrap();
            let full_path = data.path().display().to_string();
            let log_data = if data.path().exists() {
                parse_log(&full_path).unwrap()
            } else {
                // println!("File {} no longer on disk", full_path);
                continue;
            };
            let (results, missing_logs) = build_log(
                &log_data,
                string_results,
                shared_strings_results,
                timesync_data,
                exclude_missing,
            );

            // Oversize entries have not been seen in logs in HighVolume
            missing_data.push(missing_logs);
            log_count += results.len();

            all_result_data.extend(results);
            // output(
            //     &results,
            //     output_path,
            //     &format!("highvolume_{}", data.file_name().to_str().unwrap()),
            // )
            // .unwrap();
        }
    }
    archive_path.pop();

    archive_path.push("logdata.LiveData.tracev3");

    // Check if livedata exists. We only have it if 'log collect' was used
    if archive_path.exists() {
        // println!("Parsing: logdata.LiveData.tracev3");
        let mut log_data = parse_log(&archive_path.display().to_string()).unwrap();
        log_data.oversize.append(&mut oversize_strings.oversize);
        let (results, missing_logs) = build_log(
            &log_data,
            string_results,
            shared_strings_results,
            timesync_data,
            exclude_missing,
        );
        missing_data.push(missing_logs);
        log_count += results.len();

        all_result_data.extend(results);
        // output(&results, output_path, "liveData").unwrap();
        oversize_strings.oversize = log_data.oversize;
        archive_path.pop();
    }

    // Include all log entries now, if any logs are missing data its because the data has rolled
    exclude_missing = false;
    for mut leftover_data in missing_data {
        // Add all of our previous oversize data to logs for lookups
        leftover_data
            .oversize
            .append(&mut oversize_strings.oversize.clone());

        // Exclude_missing = false
        // If we fail to find any missing data its probably due to the logs rolling
        // Ex: tracev3A rolls, tracev3B references Oversize entry in tracev3A will trigger missing data since tracev3A is gone
        let (results, _) = build_log(
            &leftover_data,
            string_results,
            shared_strings_results,
            timesync_data,
            exclude_missing,
        );
        log_count += results.len();

        all_result_data.extend(results);
        // output(&results, output_path, "dataFoundInMultipleLogFiles").unwrap();
    }
    // println!("Parsed {} log entries", log_count);

    return all_result_data;
    // return vec.new();
}

// // Create JSON files
// fn output(results: &Vec<LogData>, output_dir: &str, output_name: &str) -> Result<(), Box<dyn Error>> {
//     // let args = Args::parse();
//     let mut json_file = OpenOptions::new()
//         .append(true)
//         .create(true)
//         .open(format!("{}/{}.json", output_dir, output_name))?;

//     let serde_data = serde_json::to_string(&results)?;

//     json_file.write_all(serde_data.as_bytes())?;

//     Ok(())
// }
