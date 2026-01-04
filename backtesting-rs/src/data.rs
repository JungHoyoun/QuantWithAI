//! 데이터 로딩 및 처리 모듈

use chrono::NaiveDate;
use rust_decimal::Decimal;
use serde::{Deserialize, Serialize};
use std::path::Path;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DataError {
    #[error("파일을 읽을 수 없습니다: {0}")]
    IoError(#[from] std::io::Error),
    
    #[error("CSV 파싱 실패: {0}")]
    CsvError(#[from] csv::Error),
    
    #[error("데이터가 비어있습니다")]
    EmptyData,
}

/// OHLCV 캔들 데이터
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Candle {
    pub date: NaiveDate,
    pub open: Decimal,
    pub high: Decimal,
    pub low: Decimal,
    pub close: Decimal,
    pub volume: i64,
}

/// 종목 데이터
#[derive(Debug, Clone)]
pub struct StockData {
    pub symbol: String,
    pub candles: Vec<Candle>,
}

impl StockData {
    pub fn len(&self) -> usize {
        self.candles.len()
    }

    pub fn is_empty(&self) -> bool {
        self.candles.is_empty()
    }
}

/// 데이터 로더
pub struct DataLoader;

impl DataLoader {
    /// CSV 파일에서 데이터 로드
    pub fn load_csv<P: AsRef<Path>>(path: P) -> Result<StockData, DataError> {
        let mut reader = csv::Reader::from_path(path)?;
        let mut candles = Vec::new();

        for result in reader.deserialize() {
            let candle: Candle = result?;
            candles.push(candle);
        }

        if candles.is_empty() {
            return Err(DataError::EmptyData);
        }

        // 날짜순 정렬
        candles.sort_by(|a, b| a.date.cmp(&b.date));

        Ok(StockData {
            symbol: String::new(), // CSV에서 추출하거나 파일명에서 파싱
            candles,
        })
    }

    /// 여러 CSV 파일 병렬 로드
    pub fn load_multiple<P: AsRef<Path> + Sync>(
        paths: &[P],
    ) -> Vec<Result<StockData, DataError>> {
        use rayon::prelude::*;

        paths
            .par_iter()
            .map(|path| Self::load_csv(path))
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_candle_creation() {
        let candle = Candle {
            date: NaiveDate::from_ymd_opt(2024, 1, 1).unwrap(),
            open: Decimal::new(10000, 0),
            high: Decimal::new(10500, 0),
            low: Decimal::new(9800, 0),
            close: Decimal::new(10200, 0),
            volume: 1000000,
        };

        assert_eq!(candle.close, Decimal::new(10200, 0));
    }
}

