//! 고속 백테스팅 라이브러리
//!
//! Python 바인딩을 통해 사용하거나, Rust에서 직접 사용할 수 있습니다.

pub mod data;
pub mod engine;
pub mod strategy;

// Python 바인딩 (pyo3 feature 활성화 시)
#[cfg(feature = "python")]
mod python;

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[cfg(feature = "python")]
#[pymodule]
fn backtesting_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(python::run_backtest, m)?)?;
    Ok(())
}

