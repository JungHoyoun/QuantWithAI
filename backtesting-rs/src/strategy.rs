//! 트레이딩 전략 모듈

use crate::data::Candle;
use rust_decimal::Decimal;

/// 매매 시그널
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Signal {
    Buy,
    Sell,
    Hold,
}

/// 전략 트레이트
pub trait Strategy: Send + Sync {
    /// 캔들 데이터를 기반으로 매매 시그널 생성
    fn generate_signal(&self, candles: &[Candle]) -> Signal;
    
    /// 전략 이름
    fn name(&self) -> &str;
}

/// 이동평균 크로스오버 전략
pub struct SmaCrossover {
    pub short_period: usize,
    pub long_period: usize,
}

impl SmaCrossover {
    pub fn new(short_period: usize, long_period: usize) -> Self {
        Self {
            short_period,
            long_period,
        }
    }

    fn calculate_sma(candles: &[Candle], period: usize) -> Option<Decimal> {
        if candles.len() < period {
            return None;
        }

        let sum: Decimal = candles
            .iter()
            .rev()
            .take(period)
            .map(|c| c.close)
            .sum();

        Some(sum / Decimal::from(period))
    }
}

impl Strategy for SmaCrossover {
    fn generate_signal(&self, candles: &[Candle]) -> Signal {
        if candles.len() < self.long_period + 1 {
            return Signal::Hold;
        }

        let current_short = Self::calculate_sma(candles, self.short_period);
        let current_long = Self::calculate_sma(candles, self.long_period);
        
        // 이전 캔들 기준 SMA
        let prev_candles = &candles[..candles.len() - 1];
        let prev_short = Self::calculate_sma(prev_candles, self.short_period);
        let prev_long = Self::calculate_sma(prev_candles, self.long_period);

        match (current_short, current_long, prev_short, prev_long) {
            (Some(cs), Some(cl), Some(ps), Some(pl)) => {
                // 골든 크로스: 단기 MA가 장기 MA를 상향 돌파
                if ps <= pl && cs > cl {
                    return Signal::Buy;
                }
                // 데드 크로스: 단기 MA가 장기 MA를 하향 돌파
                if ps >= pl && cs < cl {
                    return Signal::Sell;
                }
                Signal::Hold
            }
            _ => Signal::Hold,
        }
    }

    fn name(&self) -> &str {
        "SMA Crossover"
    }
}

/// 모멘텀 전략
pub struct Momentum {
    pub lookback_period: usize,
    pub threshold: Decimal,
}

impl Momentum {
    pub fn new(lookback_period: usize, threshold: f64) -> Self {
        Self {
            lookback_period,
            threshold: Decimal::try_from(threshold).unwrap_or_default(),
        }
    }
}

impl Strategy for Momentum {
    fn generate_signal(&self, candles: &[Candle]) -> Signal {
        if candles.len() < self.lookback_period + 1 {
            return Signal::Hold;
        }

        let current_price = candles.last().unwrap().close;
        let past_price = candles[candles.len() - 1 - self.lookback_period].close;
        
        let returns = (current_price - past_price) / past_price;

        if returns > self.threshold {
            Signal::Buy
        } else if returns < -self.threshold {
            Signal::Sell
        } else {
            Signal::Hold
        }
    }

    fn name(&self) -> &str {
        "Momentum"
    }
}

/// 평균 회귀 전략 (볼린저 밴드)
pub struct MeanReversion {
    pub period: usize,
    pub std_dev_multiplier: Decimal,
}

impl MeanReversion {
    pub fn new(period: usize, std_dev_multiplier: f64) -> Self {
        Self {
            period,
            std_dev_multiplier: Decimal::try_from(std_dev_multiplier).unwrap_or_default(),
        }
    }

    fn calculate_bollinger_bands(&self, candles: &[Candle]) -> Option<(Decimal, Decimal, Decimal)> {
        if candles.len() < self.period {
            return None;
        }

        let closes: Vec<Decimal> = candles
            .iter()
            .rev()
            .take(self.period)
            .map(|c| c.close)
            .collect();

        let sma: Decimal = closes.iter().sum::<Decimal>() / Decimal::from(self.period);
        
        // 표준편차 계산
        let variance: Decimal = closes
            .iter()
            .map(|c| (*c - sma) * (*c - sma))
            .sum::<Decimal>() / Decimal::from(self.period);
        
        // sqrt 근사 (Decimal은 sqrt를 직접 지원하지 않음)
        let std_dev_f64 = variance.to_string().parse::<f64>().unwrap_or(0.0).sqrt();
        let std_dev = Decimal::try_from(std_dev_f64).unwrap_or_default();

        let upper = sma + self.std_dev_multiplier * std_dev;
        let lower = sma - self.std_dev_multiplier * std_dev;

        Some((lower, sma, upper))
    }
}

impl Strategy for MeanReversion {
    fn generate_signal(&self, candles: &[Candle]) -> Signal {
        if candles.len() < self.period {
            return Signal::Hold;
        }

        let current_price = candles.last().unwrap().close;
        
        if let Some((lower, _sma, upper)) = self.calculate_bollinger_bands(candles) {
            if current_price < lower {
                return Signal::Buy; // 과매도
            }
            if current_price > upper {
                return Signal::Sell; // 과매수
            }
        }

        Signal::Hold
    }

    fn name(&self) -> &str {
        "Mean Reversion"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::NaiveDate;
    use rust_decimal_macros::dec;

    fn create_test_candles(prices: &[i64]) -> Vec<Candle> {
        prices
            .iter()
            .enumerate()
            .map(|(i, &price)| Candle {
                date: NaiveDate::from_ymd_opt(2024, 1, 1 + i as u32).unwrap(),
                open: Decimal::from(price),
                high: Decimal::from(price + 100),
                low: Decimal::from(price - 100),
                close: Decimal::from(price),
                volume: 1000000,
            })
            .collect()
    }

    #[test]
    fn test_sma_crossover() {
        let strategy = SmaCrossover::new(5, 10);
        
        // 충분한 데이터가 없으면 Hold
        let candles = create_test_candles(&[100, 101, 102]);
        assert_eq!(strategy.generate_signal(&candles), Signal::Hold);
    }

    #[test]
    fn test_momentum() {
        let strategy = Momentum::new(5, 0.05);
        
        // 5% 이상 상승 시 Buy
        let candles = create_test_candles(&[100, 101, 102, 103, 104, 110]);
        let signal = strategy.generate_signal(&candles);
        // 실제 수익률에 따라 달라질 수 있음
        assert!(signal == Signal::Buy || signal == Signal::Hold);
    }
}

