use std::collections::VecDeque;
use std::panic;

use example::LogExtraction;
use macos_unifiedlogs::unified_log;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;

mod example;

#[pyclass(module = "pyunilogs", get_all)]
pub struct LogData {
    pub subsystem: String,
    pub thread_id: u64,
    pub pid: u64,
    pub euid: u32,
    pub library: String,
    pub library_uuid: String,
    pub activity_id: u64,
    pub time: f64,
    pub category: String,
    pub event_type: String,
    pub log_type: String,
    pub process: String,
    pub process_uuid: String,
    pub message: String,
    pub raw_message: String,
    pub boot_uuid: String,
    pub timezone_name: String,
    // #[pyo3(get)]
    // pub message_entries: Vec<FirehoseItemInfo>,
}

impl LogData {
    fn from_logdata(logdata: &unified_log::LogData) -> Self {
        Self {
            subsystem: logdata.subsystem.to_owned(),
            thread_id: logdata.thread_id,
            pid: logdata.pid,
            euid: logdata.euid,
            library: logdata.library.to_owned(),
            library_uuid: logdata.library_uuid.to_owned(),
            activity_id: logdata.activity_id,
            time: logdata.time,
            category: logdata.category.to_owned(),
            event_type: logdata.event_type.to_owned(),
            log_type: logdata.log_type.to_owned(),
            process: logdata.process.to_owned(),
            process_uuid: logdata.process_uuid.to_owned(),
            message: logdata.message.to_owned(),
            raw_message: logdata.raw_message.to_owned(),
            boot_uuid: logdata.boot_uuid.to_owned(),
            timezone_name: logdata.timezone_name.to_owned(),
        }
    }
}

#[pyclass]
struct LogIterator {
    extraction: LogExtraction,
    chunk: Vec<macos_unifiedlogs::unified_log::LogData>,
}

impl LogIterator {
    pub fn from_extraction(extraction: LogExtraction) -> Self {
        return Self {
            extraction,
            chunk: Vec::new(),
        };
    }
}

#[pymethods]
impl LogIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&mut self) -> Option<LogData> {
        if let Some(log_data) = self.chunk.pop() {
            return Some(LogData::from_logdata(&log_data));
        }

        if let Some(chunk) = self.extraction.next() {
            self.chunk = chunk;
            return self.__next__();
        }

        return None;
    }
}

#[pyfunction]
fn extract_logarchive(input_path: String) -> PyResult<LogIterator> {
    let final_result = panic::catch_unwind(|| {
        let mut log_extraction = LogExtraction::from_path(&input_path);

        return LogIterator::from_extraction(log_extraction);
    });

    if final_result.is_err() {
        // quick and dirty catch the panics
        return Err(PyRuntimeError::new_err(
            "Error extracting logs with pyunilogs",
        ));
    } else {
        return Ok(final_result.unwrap());
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn pyunilogs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(extract_logarchive, m)?)?;
    m.add_class::<LogData>()?;
    Ok(())
}
